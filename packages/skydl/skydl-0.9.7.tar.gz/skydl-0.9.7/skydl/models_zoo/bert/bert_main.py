# -*- coding: utf-8 -*-
import sys
import os
import tensorflow as tf
from skydl.models_zoo.bert.official.nlp.bert_models import classifier_model
from skydl.models_zoo.bert.official.nlp.bert.tokenization import FullTokenizer
from transformers import BertConfig
import tensorflow_hub as hub


def readfile(filename):
    '''
    read file
    '''
    f = open(filename)
    data = []
    sentence = []
    label = []
    for line in f:
        if len(line) == 0 or line.startswith('-DOCSTART') or line[0] == "\n":
            if len(sentence) > 0:
                data.append((sentence, label))
                sentence = []
                label = []
            continue
        splits = line.split(' ')
        sentence.append(splits[0])
        label.append(splits[-1][:-1])

    if len(sentence) > 0:
        data.append((sentence, label))
        sentence = []
        label = []
    return data


class DataProcessor(object):
    """Base class for data converters for sequence classification data sets."""

    def get_train_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the train set."""
        raise NotImplementedError()

    def get_dev_examples(self, data_dir):
        """Gets a collection of `InputExample`s for the dev set."""
        raise NotImplementedError()

    def get_labels(self):
        """Gets the list of labels for this data set."""
        raise NotImplementedError()

    @classmethod
    def _read_tsv(cls, input_file, quotechar=None):
        """Reads a tab separated value file."""
        return readfile(input_file)


class InputExample(object):
    """A single training/test example for simple sequence classification."""

    def __init__(self, guid, text_a, text_b=None, label=None):
        """Constructs a InputExample.

        Args:
            guid: Unique id for the example.
            text_a: string. The untokenized text of the first sequence. For single
            sequence tasks, only this sequence must be specified.
            text_b: (Optional) string. The untokenized text of the second sequence.
            Only must be specified for sequence pair tasks.
            label: (Optional) string. The label of the example. This should be
            specified for train and dev examples, but not for test examples.
        """
        self.guid = guid
        self.text_a = text_a
        self.text_b = text_b
        self.label = label


class NerProcessor(DataProcessor):
    """Processor for the CoNLL-2003 data set."""

    def get_train_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "train.txt")), "train")

    def get_dev_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "valid.txt")), "dev")

    def get_test_examples(self, data_dir):
        """See base class."""
        return self._create_examples(
            self._read_tsv(os.path.join(data_dir, "test.txt")), "test")

    def get_labels(self):
        return ["O", "B-MISC", "I-MISC",  "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "[CLS]", "[SEP]"]

    def _create_examples(self, lines, set_type):
        examples = []
        for i, (sentence, label) in enumerate(lines):
            guid = "%s-%s" % (set_type, i)
            text_a = ' '.join(sentence)
            text_b = None
            label = label
            examples.append(InputExample(guid=guid, text_a=text_a, text_b=text_b, label=label))
        return examples

def create_bert_model(num_labels=1):
    model_path = sys.path[0] + "/../../datasets/data/bert/tf_hub/bert_zh_L-12_H-768_A-12/1"
    # load config
    config = BertConfig.from_json_file(sys.path[0] + "/bert_config.json")
    MAX_SEQUENCE_LENGTH = config.max_position_embeddings
    HIDDEN_DROPOUT_PROB = config.hidden_dropout_prob
    INITIALIZER_RANGE = config.initializer_range
    USE_AMP = False
    # define inputs, outputs
    input_word_ids = tf.keras.layers.Input(shape=(MAX_SEQUENCE_LENGTH,), dtype=tf.int32, name="input_word_ids")
    input_masks = tf.keras.layers.Input(shape=(MAX_SEQUENCE_LENGTH,), dtype=tf.int32, name="input_masks")
    segment_ids = tf.keras.layers.Input(shape=(MAX_SEQUENCE_LENGTH,), dtype=tf.int32, name="segment_ids")
    # build model
    bert_model = hub.KerasLayer(model_path, trainable=True)
    # pooled_output用于分类，sequence_output用于序列相关的预测
    pooled_output, sequence_output = bert_model([input_word_ids, input_masks, segment_ids])
    pooled_output.layers[-1].activation = tf.keras.activations.softmax # TODO
    output = tf.keras.layers.Dropout(rate=HIDDEN_DROPOUT_PROB)(pooled_output)
    output = tf.keras.layers.Dense(num_labels,
                                   kernel_initializer=tf.keras.initializers.TruncatedNormal(stddev=INITIALIZER_RANGE),
                                   name='output',
                                   dtype=tf.float32)(output)
    # build tokenizer
    vocab_file = bert_model.resolved_object.vocab_file.asset_path.numpy()
    do_lower_case = bert_model.resolved_object.do_lower_case.numpy()
    tokenizer = FullTokenizer(vocab_file, do_lower_case)
    # build classifier model
    classifier_model = tf.keras.Model(
        inputs=[input_word_ids, input_masks, segment_ids],
        outputs=output)
    # compile model
    metric = tf.keras.metrics.SparseCategoricalAccuracy("accuracy")
    if num_labels == 1:
        loss = tf.keras.losses.MeanSquaredError()
    else:
        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    # Prepare training: Compile tf.keras model with optimizer, loss and learning rate schedule
    optimizer = tf.keras.optimizers.Adam(learning_rate=3e-5, epsilon=1e-08, clipnorm=1.0)
    if USE_AMP:
        # loss scaling is currently required when using mixed precision
        optimizer = tf.keras.mixed_precision.experimental.LossScaleOptimizer(optimizer, "dynamic")
    classifier_model.compile(optimizer=optimizer, loss=loss, metrics=[metric])
    classifier_model.summary()
    return classifier_model, bert_model


def process_data():
    processor = NerProcessor()
    label_list = processor.get_labels()
    num_labels = len(label_list) + 1
    print(f"num_labels={num_labels}")


if __name__ == '__main__':
    process_data()
    # bert_model, tokenizer = create_bert_model(num_labels=3)
    # Already been converted into WordPiece token ids
    # input_word_ids = tf.constant([[31, 51, 99], [15, 5, 0]])
    # input_mask = tf.constant([[1, 1, 1], [1, 1, 0]])
    # input_type_ids = tf.constant([[0, 0, 1], [0, 2, 0]])
    # pooled_output, sequence_output = bert_model.fit([input_word_ids, input_mask, input_type_ids])

