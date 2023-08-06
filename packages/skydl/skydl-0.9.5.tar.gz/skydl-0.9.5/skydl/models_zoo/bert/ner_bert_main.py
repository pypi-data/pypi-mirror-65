# -*- coding: utf-8 -*-
import sys
import os
import tensorflow as tf
from skydl.models_zoo.bert.official.nlp.bert_models import classifier_model
from skydl.models_zoo.bert.official.nlp.bert.tokenization import FullTokenizer, printable_text, convert_to_unicode
from transformers import BertConfig
import tensorflow_hub as hub


class InputExample(object):
    """A single training/test example for simple sequence classification."""

    def __init__(self, guid, text, label=None):
        """Constructs a InputExample.

        Args:
          guid: Unique id for the example.
          text_a: string. The untokenized text of the first sequence. For single
            sequence tasks, only this sequence must be specified.
          label: (Optional) string. The label of the example. This should be
            specified for train and dev examples, but not for test examples.
        """
        self.guid = guid
        self.text = text
        self.label = label


class InputFeatures(object):
    """A single set of features of data."""

    def __init__(self, input_ids, input_mask, segment_ids, label_ids,):
        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.label_ids = label_ids
        #self.label_mask = label_mask


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
    def _read_data(cls, input_file):
        """Reads a BIO data."""
        with open(input_file) as f:
            lines = []
            words = []
            labels = []
            for line in f:
                contends = line.strip()
                word = line.strip().split(' ')[0]
                label = line.strip().split(' ')[-1]
                if contends.startswith("-DOCSTART-"):
                    words.append('')
                    continue
                # if len(contends) == 0 and words[-1] == '。':
                if len(contends) == 0:
                    l = ' '.join([label for label in labels if len(label) > 0])
                    w = ' '.join([word for word in words if len(word) > 0])
                    lines.append([l, w])
                    words = []
                    labels = []
                    continue
                words.append(word)
                labels.append(label)
            return lines


class NerProcessor(DataProcessor):
    def get_train_examples(self, data_dir):
        return self._create_example(
            self._read_data(os.path.join(data_dir, "train.txt")), "train"
        )

    def get_dev_examples(self, data_dir):
        return self._create_example(
            self._read_data(os.path.join(data_dir, "dev.txt")), "dev"
        )

    def get_test_examples(self,data_dir):
        return self._create_example(
            self._read_data(os.path.join(data_dir, "test.txt")), "test")


    def get_labels(self):
        # prevent potential bug for chinese text mixed with english text
        # return ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "[CLS]","[SEP]"]
        return ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "X","[CLS]","[SEP]"]

    def _create_example(self, lines, set_type):
        examples = []
        for (i, line) in enumerate(lines):
            guid = "%s-%s" % (set_type, i)
            text = convert_to_unicode(line[1])
            label = convert_to_unicode(line[0])
            examples.append(InputExample(guid=guid, text=text, label=label))
        return examples


def create_bert_model(num_labels=1):
    """run ner model"""
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
    sequence_output.layers[-1].activation = tf.keras.activations.softmax
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


def convert_single_example(ex_index, example, label_map, max_seq_length, tokenizer):
    textlist = example.text.split(' ')
    labellist = example.label.split(' ')
    tokens = []
    labels = []
    # print(textlist)
    for i, word in enumerate(textlist):
        token = tokenizer.tokenize(word)
        # print(token)
        tokens.extend(token)
        label_1 = labellist[i]
        # print(label_1)
        for m in range(len(token)):
            if m == 0:
                labels.append(label_1)
            else:
                labels.append("X")
        # print(tokens, labels)
    # tokens = tokenizer.tokenize(example.text)
    if len(tokens) >= max_seq_length - 1:
        tokens = tokens[0:(max_seq_length - 2)]
        labels = labels[0:(max_seq_length - 2)]
    ntokens = []
    segment_ids = []
    label_ids = []
    ntokens.append("[CLS]")
    segment_ids.append(0)
    # append("O") or append("[CLS]") not sure!
    label_ids.append(label_map["[CLS]"])
    for i, token in enumerate(tokens):
        ntokens.append(token)
        segment_ids.append(0)
        label_ids.append(label_map[labels[i]])
    ntokens.append("[SEP]")
    segment_ids.append(0)
    # append("O") or append("[SEP]") not sure!
    label_ids.append(label_map["[SEP]"])
    input_ids = tokenizer.convert_tokens_to_ids(ntokens)
    input_mask = [1] * len(input_ids)
    #label_mask = [1] * len(input_ids)
    while len(input_ids) < max_seq_length:
        input_ids.append(0)
        input_mask.append(0)
        segment_ids.append(0)
        # we don't concerned about it!
        label_ids.append(0)
        ntokens.append("**NULL**")
        #label_mask.append(0)
    # print(len(input_ids))
    assert len(input_ids) == max_seq_length
    assert len(input_mask) == max_seq_length
    assert len(segment_ids) == max_seq_length
    assert len(label_ids) == max_seq_length
    #assert len(label_mask) == max_seq_length

    if ex_index < 5:
        print("*** Example ***")
        print("guid: %s" % (example.guid))
        print("tokens: %s" % " ".join([printable_text(x) for x in tokens]))
        print("input_ids: %s" % " ".join([str(x) for x in input_ids]))
        print("input_mask: %s" % " ".join([str(x) for x in input_mask]))
        print("segment_ids: %s" % " ".join([str(x) for x in segment_ids]))
        print("label_ids: %s" % " ".join([str(x) for x in label_ids]))
        #print("label_mask: %s" % " ".join([str(x) for x in label_mask]))

    feature = InputFeatures(
        input_ids=input_ids,
        input_mask=input_mask,
        segment_ids=segment_ids,
        label_ids=label_ids,
        #label_mask = label_mask
    )
    return feature


def process_data(max_seq_length=128):
    model_path = sys.path[0] + "/../../datasets/data/bert/tf_hub/bert_zh_L-12_H-768_A-12/1"
    data_dir = sys.path[0] + "/data/ner"
    processor = NerProcessor()
    label_list = processor.get_labels()
    num_labels = len(label_list) + 1
    tokenizer = FullTokenizer(vocab_file=model_path + "/assets/vocab.txt", do_lower_case=True)  # todo
    examples = processor.get_dev_examples(data_dir)
    label_map = {}
    for (i, label) in enumerate(label_list, 1):
        label_map[label] = i
    for (ex_index, example) in enumerate(examples):
        if ex_index % 5000 == 0:
            print("Writing example %d of %d" % (ex_index, len(examples)))
        feature = convert_single_example(ex_index, example, label_map, max_seq_length, tokenizer)


if __name__ == '__main__':
    # bert_model, tokenizer = create_bert_model(num_labels=3)
    process_data(max_seq_length=128)

