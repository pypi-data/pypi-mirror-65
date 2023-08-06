# coding=utf-8
"""
参考：Roberta for NER task https://github.com/huggingface/transformers/issues/1166
"""
import sys
import tensorflow as tf
import tensorflow_hub as hub
from skydl.models_zoo.bert.official.nlp import bert_models
from skydl.models_zoo.bert.official.nlp.bert_modeling import BertConfig
from skydl.models_zoo.bert.tf_bert_classifier_keras_lossv2 import TfBertClassifierKerasLossV2
from skydl.models_zoo.bert.bert_classifier_tf_keras_modelv2 import BertClassifierNerTfKerasModelV2


def fine_tune_classifier_model():
    NUM_CLASSES = 2
    config = BertConfig.from_json_file(sys.path[0] + "/bert_config.json")
    bert_classifier_model, core_model = classifier_model(config,
                                                               tf.float32,
                                                               num_labels=NUM_CLASSES,
                                                               max_seq_length=128,
                                                               hub_module_url=sys.path[0] + "/../../datasets/data/bert/tf_hub/bert_zh_L-12_H-768_A-12/1")
    # # build loss, optimizer, metric
    # metrics = [tf.keras.metrics.SparseCategoricalAccuracy("accuracy", dtype=tf.float32)]
    # # loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    # loss = TfBertClassifierKerasLossV2(NUM_CLASSES)
    # # Prepare training: Compile tf.keras model with optimizer, loss and learning rate schedule
    # optimizer = tf.keras.optimizers.Adam(learning_rate=3e-5, epsilon=1e-08, clipnorm=1.0)

    if NUM_CLASSES <= 2:
        loss = "binary_crossentropy"
        optimizer = "adam"
        metrics = ["accuracy"]
    else:
        loss = "sparse_categorical_crossentropy"
        optimizer = "adam"
        metrics = ["sparse_categorical_accuracy"]

    # 加载数据集
    train_dataset, validation_dataset, evaluate_dataset = BertClassifierNerTfKerasModelV2().load_data()
    # 开始训练模型
    BertClassifierNerTfKerasModelV2("bert_classifier", [
        bert_classifier_model
    ]).compile(
        loss=loss,
        optimizer=optimizer,
        metrics=metrics
    ).fit(
        loaded_dataset=[train_dataset, validation_dataset, evaluate_dataset]
    ).predict_from_load_weights()


def classifier_model(bert_config,
                     float_type,
                     num_labels,
                     max_seq_length,
                     final_layer_initializer=None,
                     hub_module_url=None):
    """BERT classifier model in functional API style.
    主要参考了：from skydl.models_zoo.bert.official.nlp import bert_models#classifier_model()
    Construct a Keras model for predicting `num_labels` outputs from an input with
    maximum sequence length `max_seq_length`.
    Args:
    bert_config: BertConfig or AlbertConfig, the config defines the core
      BERT or ALBERT model.
    float_type: dtype, tf.float32 or tf.bfloat16.
    num_labels: integer, the number of classes.
    max_seq_length: integer, the maximum input sequence length.
    final_layer_initializer: Initializer for final dense layer. Defaulted
      TruncatedNormal initializer.
    hub_module_url: TF-Hub path/url to Bert module.
    Returns:
    Combined prediction model (words, mask, type) -> (one-hot labels)
    BERT sub-model (words, mask, type) -> (bert_outputs)
    """
    if final_layer_initializer is not None:
        initializer = final_layer_initializer
    else:
        initializer = tf.keras.initializers.TruncatedNormal(
            stddev=bert_config.initializer_range)

    input_word_ids = tf.keras.layers.Input(
        shape=(max_seq_length,), dtype=tf.int32, name='input_word_ids')
    input_mask = tf.keras.layers.Input(
        shape=(max_seq_length,), dtype=tf.int32, name='input_mask')
    input_type_ids = tf.keras.layers.Input(
        shape=(max_seq_length,), dtype=tf.int32, name='input_type_ids')
    bert_model = hub.KerasLayer(hub_module_url, trainable=True)
    pooled_output, _ = bert_model([input_word_ids, input_mask, input_type_ids])
    output = tf.keras.layers.Dropout(rate=bert_config.hidden_dropout_prob)(
        pooled_output)

    if num_labels <= 2:
        num_classes = 1
        activation = "sigmoid"
    else:
        num_classes = num_labels
        activation = "softmax"

    output = tf.keras.layers.Dense(
        num_classes,
        activation=activation,
        kernel_initializer=initializer,
        name='output',
        dtype=float_type)(
          output)
    return tf.keras.Model(
          inputs={
              'input_word_ids': input_word_ids,
              'input_mask': input_mask,
              'input_type_ids': input_type_ids
          },
          outputs=output), bert_model


if __name__ == '__main__':
    fine_tune_classifier_model()
