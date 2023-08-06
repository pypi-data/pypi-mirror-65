# -*- coding: utf-8 -*-
import os
import time
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from py_common_util.common.annotations import print_exec_time
from skydl.datasets.super_tf_dataset_builder import SuperDatasetBuilder
from skydl.datasets.translate_dataset_builder import TranslateDatasetBuilder
from skydl.models_zoo.attention.attention import BahdanauAttention
from skydl.models_zoo.attention.decoder import Decoder
from skydl.models_zoo.attention.encoder import Encoder

###############################
# global parameters
EPOCHS = 10
BATCH_SIZE = 64
embedding_dim = 256
units = 1024
###############################
dataset_name = TranslateDatasetBuilder.camelcase_to_snakecase("TranslateDatasetBuilder")
# num_examples = 21621
num_examples = TranslateDatasetBuilder.get_num_examples(dataset_name, tfds.Split.TRAIN)
batched_datasets = TranslateDatasetBuilder.load_batched_datasets(dataset_name,
                                                                 config_name="plain_text",
                                                                 split=[tfds.Split.TRAIN],
                                                                 batch_size=num_examples,
                                                                 shuffle=-1)
batched_dataset_features = TranslateDatasetBuilder.read_batched_datasets(batched_datasets)
all_cn_sentences = []
all_en_sentences = []
for features, labels in batched_dataset_features:
    all_en_sentences += [feature.decode('utf-8') for feature in features]
    all_cn_sentences += [label.decode('utf-8') for label in labels]
input_tensor, target_tensor, inp_lang, targ_lang = TranslateDatasetBuilder.load_dataset_from_sentences(all_en_sentences,
                                                                                                       all_cn_sentences)
# TranslateDatasetBuilder.convert(inp_lang, input_tensor[0])
dataset = tf.data.Dataset.from_tensor_slices((input_tensor, target_tensor)).batch(BATCH_SIZE, drop_remainder=True)
train_data, _, test_data = SuperDatasetBuilder.split_full_datasets(dataset, num_examples, train_size=0.9,
                                                                   validation_size=0, test_size=0.1)
###############################
vocab_inp_size = len(inp_lang.word_index) + 1
vocab_tar_size = len(targ_lang.word_index) + 1
###############################
# encoder layer
encoder = Encoder(vocab_inp_size, embedding_dim, units, BATCH_SIZE)
# decoder layer
decoder = Decoder(vocab_tar_size, embedding_dim, units, BATCH_SIZE)
# attention layer
attention_layer = BahdanauAttention(10)
# 定义优化器和损失函数
optimizer = tf.keras.optimizers.Adam()
loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True, reduction='none')
# 定义检查点（基于对象保存）
checkpoint_dir = '/home/user/tmp/atttion/training_checkpoints'
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
checkpoint = tf.train.Checkpoint(optimizer=optimizer,
                                 encoder=encoder,
                                 decoder=decoder)


def loss_function(real, pred):
    mask = tf.math.logical_not(tf.math.equal(real, 0))
    loss_ = loss_object(real, pred)
    mask = tf.cast(mask, dtype=loss_.dtype)
    loss_ *= mask
    return tf.reduce_mean(loss_)


@tf.function
def train_step(inp, targ, enc_hidden):
    loss = 0
    with tf.GradientTape() as tape:
        enc_output, enc_hidden = encoder(inp, enc_hidden)
        dec_hidden = enc_hidden
        dec_input = tf.expand_dims([targ_lang.word_index['<start>']] * BATCH_SIZE, 1)
        # 教师强制 - 将目标词作为下一个输入
        for t in range(1, targ.shape[1]):
            # 将编码器输出 （enc_output） 传送至解码器
            predictions, dec_hidden, _ = decoder(dec_input, dec_hidden, enc_output)
            loss += loss_function(targ[:, t], predictions)
            # 使用教师强制
            dec_input = tf.expand_dims(targ[:, t], 1)
    batch_loss = (loss / int(targ.shape[1]))
    variables = encoder.trainable_variables + decoder.trainable_variables
    gradients = tape.gradient(loss, variables)
    optimizer.apply_gradients(zip(gradients, variables))
    return batch_loss


@print_exec_time
def training_attention_model():
    for epoch in range(EPOCHS):
        start = time.time()
        enc_hidden = encoder.initialize_hidden_state()
        total_loss = 0
        for batch, (input_batch, target_batch) in enumerate(tfds.as_numpy(train_data)):
            # 样本输入
            sample_hidden = encoder.initialize_hidden_state()
            # encoder
            sample_output, sample_hidden = encoder(input_batch, sample_hidden)
            print('Encoder output shape: (batch size, sequence length, units) {}'.format(sample_output.shape))
            print('Encoder Hidden state shape: (batch size, units) {}'.format(sample_hidden.shape))
            # attention
            attention_result, attention_weights = attention_layer(sample_hidden, sample_output)
            print("Attention result shape: (batch size, units) {}".format(attention_result.shape))
            print("Attention weights shape: (batch_size, sequence_length, 1) {}".format(attention_weights.shape))
            # decoder
            sample_decoder_output, _, _ = decoder(tf.random.uniform((BATCH_SIZE, 1)), sample_hidden, sample_output)
            print('Decoder output shape: (batch_size, vocab size) {}'.format(sample_decoder_output.shape))
            batch_loss = train_step(input_batch, target_batch, enc_hidden)
            total_loss += batch_loss
            if batch % 10 == 0:
                print('Epoch {} Batch {} Loss {:.4f}'.format(epoch + 1,
                                                             batch,
                                                             batch_loss.numpy()))
        # 每 1 个周期（epoch），保存（检查点）一次模型
        if (epoch + 1) % 1 == 0:
            checkpoint.save(file_prefix=checkpoint_prefix)
        print('Epoch {} Loss {:.4f}'.format(epoch + 1, total_loss))
        print('Time taken for 1 epoch {} sec\n'.format(time.time() - start))


def evaluate(sentence):
    max_length_targ = 38  # from TranslateDatasetBuilder
    max_length_inp = 44  # from TranslateDatasetBuilder
    attention_plot = np.zeros((max_length_targ, max_length_inp))
    sentence = TranslateDatasetBuilder.preprocess_sentence(sentence)
    inputs = [inp_lang.word_index[i] for i in sentence.split(' ')]
    inputs = tf.keras.preprocessing.sequence.pad_sequences([inputs],
                                                           maxlen=max_length_inp,
                                                           padding='post')
    inputs = tf.convert_to_tensor(inputs)
    result = ''
    hidden = [tf.zeros((1, units))]
    enc_out, enc_hidden = encoder(inputs, hidden)
    dec_hidden = enc_hidden
    dec_input = tf.expand_dims([targ_lang.word_index['<start>']], 0)
    for t in range(max_length_targ):
        predictions, dec_hidden, attention_weights = decoder(dec_input,
                                                             dec_hidden,
                                                             enc_out)
        # 存储注意力权重以便后面制图
        attention_weights = tf.reshape(attention_weights, (-1,))
        attention_plot[t] = attention_weights.numpy()
        predicted_id = tf.argmax(predictions[0]).numpy()
        result += targ_lang.index_word[predicted_id] + ' '
        if targ_lang.index_word[predicted_id] == '<end>':
            return result, sentence, attention_plot
        # 预测的 ID 被输送回模型
        dec_input = tf.expand_dims([predicted_id], 0)
    return result, sentence, attention_plot


def translate(sentence):
    result, sentence, attention_plot = evaluate(sentence)
    print(f'Input: {sentence}')
    print(f'Predicted translation: {result}')
    attention_plot = attention_plot[:len(result.split(' ')), :len(sentence.split(' '))]
    plot_attention(attention_plot, sentence.split(' '), result.split(' '))


# 注意力权重制图函数
def plot_attention(attention, sentence, predicted_sentence):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.matshow(attention, cmap='viridis')
    fontdict = {'fontsize': 14}
    ax.set_xticklabels([''] + sentence, fontdict=fontdict, rotation=90)
    ax.set_yticklabels([''] + predicted_sentence, fontdict=fontdict)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.show()


if __name__ == '__main__':
    # training_attention_model()
    # 恢复检查点目录（checkpoint_dir）中最新的检查点
    saved_model = checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir))  # 可以查看checkpoint.encoder、optimizer、decoder对象的状态
    # 翻译
    translate("今 天 家 里 下 雪 了 哦")
