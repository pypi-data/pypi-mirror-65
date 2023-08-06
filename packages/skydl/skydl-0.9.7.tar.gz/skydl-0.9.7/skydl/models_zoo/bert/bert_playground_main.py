"""
https://github.com/ymcui/Chinese-BERT-wwm
https://github.com/liloi/bert-tf2
https://github.com/kamalkraj/BERT-NER-TF
https://medium.com/analytics-vidhya/bert-in-keras-tensorflow-2-0-using-tfhub-huggingface-81c08c5f81d8
Pytorch版本的BERT使用学习笔记  https://blog.csdn.net/ccbrid/article/details/88732857
https://github.com/huggingface/transformers/blob/master/examples/run_tf_ner.py
"""
import sys
import tensorflow as tf
import torch
from skydl.models_zoo.bert.official.nlp.bert.tokenization import FullTokenizer
from transformers import BertConfig, BertModel, BertTokenizer, TFBertModel
import tensorflow_hub as hub


def do_tf_hub_main():
    """
    参考：https://aihub.cloud.google.com/p/products%2F5f7e984e-f2e7-445f-9808-7ce751dcc1da
    https://github.com/tensorflow/models/blob/master/official/nlp/bert/run_classifier.py
    """
    model_path = sys.path[0] + "/../../datasets/data/bert/tf_hub/bert_zh_L-12_H-768_A-12/1"
    max_seq_length = 128  # Your choice here.
    input_word_ids = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32, name="input_word_ids")
    input_mask = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32, name="input_mask")
    segment_ids = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32, name="segment_ids")
    bert_layer = hub.KerasLayer(model_path, trainable=True)
    pooled_output, sequence_output = bert_layer([input_word_ids, input_mask, segment_ids])
    print(pooled_output)
    vocab_file = bert_layer.resolved_object.vocab_file.asset_path.numpy()
    do_lower_case = bert_layer.resolved_object.do_lower_case.numpy()
    tokenizer = FullTokenizer(vocab_file, do_lower_case)
    # Tokenized input
    # tokenizer = BertTokenizer.from_pretrained(str(vocab_file, "utf-8"))
    text = "[CLS] 你 是 谁 ? [SEP] 你 好 Hello [SEP]"
    tokenized_text = tokenizer.tokenize(text)
    print(tokenized_text)
    ###################################################
    # Tokenized input
    text = "[CLS] Who was Jim Henson ? [SEP] Jim Henson was a puppeteer [SEP]"
    tokenized_text = tokenizer.tokenize(text)
    # Mask a token that we will try to predict back with `BertForMaskedLM`
    masked_index = 8
    tokenized_text[masked_index] = '[MASK]'
    # assert tokenized_text == ['[CLS]', 'who', 'was', 'jim', 'henson', '?', '[SEP]', 'jim', '[MASK]', 'was', 'a', 'puppet', '##eer', '[SEP]']
    # 将 token 转为 vocabulary 索引
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    # 定义句子 A、B 索引
    segments_ids = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1]
    # 将 inputs 转为 PyTorch tensors
    tokens_tensor = torch.tensor([indexed_tokens])
    segments_tensors = torch.tensor([segments_ids])
    ###################################################
    # return model
    hidden_dropout_prob = 0.1
    initializer_range = 0.02
    initializer = tf.keras.initializers.TruncatedNormal(stddev=initializer_range)
    output = tf.keras.layers.Dropout(rate=hidden_dropout_prob)(pooled_output)
    num_classes = 10  # TODO
    output = tf.keras.layers.Dense(num_classes,
        kernel_initializer=initializer,
        name='output',
        dtype=tf.float32)(output)
    bert_model = tf.keras.Model(
        inputs={
            'input_word_ids': input_word_ids,
            'input_masks': input_mask,
            'input_segments': segment_ids
        },
        outputs=output)
    bert_model.summary()
    return bert_model, bert_layer


def do_tf_main():
    model_path = sys.path[0] + "/../../datasets//data/bert/tf_hub/bert_zh_L-12_H-768_A-12/1"
    # model = TFBertModel.from_pretrained(model_path)
    # model.summary()

    # # Loading from a TF checkpoint file instead of a PyTorch model (slower)
    # config = BertConfig.from_json_file(model_path + "/assets/bert_config.json")
    # model = BertModel.from_pretrained(model_path + '/variables/variables.index', from_tf=True, config=config)

    model = tf.keras.Model()  # Bert pre-trained model as feature extractor.
    checkpoint = tf.train.Checkpoint(model=model)
    checkpoint.restore(model_path + '/variables/variables.index')
    print(model)

    # Tokenized input
    tokenizer = BertTokenizer.from_pretrained(model_path + "/assets")
    text = "[CLS] 你是谁 ? [SEP] 你 好 puppeteer [SEP]"
    tokenized_text = tokenizer.tokenize(text)
    print(tokenized_text)


def do_pt_main():
    model_path = "hfl/chinese-bert-wwm"
    model = BertModel.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)

    # Tokenized input
    text = "[CLS] Who was Jim Henson ? [SEP] Jim Henson was a puppeteer [SEP]"
    tokenized_text = tokenizer.tokenize(text)


if __name__ == '__main__':
    do_tf_hub_main()




