# coding=utf-8
import os
import sys
import csv
import collections
import tensorflow as tf
import tensorflow_datasets as tfds
from py_common_util.common.annotations import Override
from skydl.datasets.super_tf_dataset_builder import SuperDatasetBuilder, DefaultDatasetBuilderConfig
from skydl.models_zoo.bert.official.nlp.bert.tokenization import FullTokenizer, printable_text, convert_to_unicode
sys.path.append(os.path.abspath('%s/..' % sys.path[0]))


class ChineseBertClassifierDatasetBuilder(SuperDatasetBuilder):
    """
    中文bert模型用的分类数据集
    参考：https://github.com/NLPScott/bert-Chinese-classification-task/blob/master/run_classifier_word.py
    BERT fine-tuning for Tensorflow 2.0 with Keras API https://medium.com/@brn.pistone/bert-fine-tuning-for-tensorflow-2-0-with-keras-api-9913fc1348f6
    Multi-label Text Classification using BERT – The Mighty Transformer https://medium.com/huggingface/multi-label-text-classification-using-bert-the-mighty-transformer-69714fa3fb3d
    Evaluation and Inference added to run_glue.py #2884 https://github.com/huggingface/transformers/issues/2884 https://github.com/kaushaltrivedi/fast-bert
    """
    BUILDER_CONFIGS = [
        DefaultDatasetBuilderConfig(
            name="plain_text",
            version="0.0.1",
            description="Plain text",
        )
    ]
    # set value of max_seq_length
    MAX_SEQ_LENGTH = 128
    # feature column names
    INPUT_IDS_COLUMN = "input_word_ids"     # input_ids
    INPUT_MASK_COLUMN = "input_mask"        # input_mask
    SEGMENTS_ID_COLUMN = "input_type_ids"   # segments_id
    # target column name
    TARGET_COLUMN = "target"
    # used to change labels to ids
    # LABEL_DICT = collections.OrderedDict([
    #     (i, i) for i in ["0", "1"]
    # ])
    ALL_LABELS = set()  # 自动获取所有的label类别
    # HARD_CODE_NUM_CLASSES = 2  # 根据自动得出的label数写死在这里 e.g. 为2
    # feature column dict
    FEATURE_DICT = collections.OrderedDict([
        ("input_word_ids", (tfds.features.Tensor(shape=(MAX_SEQ_LENGTH,), dtype=tf.int32), SuperDatasetBuilder.convert_to_int)),
        ("input_mask", (tfds.features.Tensor(shape=(MAX_SEQ_LENGTH,), dtype=tf.int32), SuperDatasetBuilder.convert_to_int)),
        ("input_type_ids", (tfds.features.Tensor(shape=(MAX_SEQ_LENGTH,), dtype=tf.int32), SuperDatasetBuilder.convert_to_int)),
        # 在_generate_examples()里单独处理了target列，这里不需要重复定义
    ])

    def __init__(self, data_dir=None, config=None):
        super().__init__(data_dir=data_dir, config=config)
        self._num_shards = 1
        self._train_data_file = sys.path[0] + "/data/bert/classifier/train.tsv"
        self._test_data_file = sys.path[0] + "/data/bert/classifier/test.tsv"
        self._validation_data_file = sys.path[0] + "/data/bert/classifier/dev.tsv"

    @Override(SuperDatasetBuilder)
    def _info(self):
        return tfds.core.DatasetInfo(
            builder=self,
            description=("Chinese dataset: Multi-label Text Classification using BERT"),
            features=tfds.features.FeaturesDict({
                # "label": tfds.features.Tensor(shape=(self.HARD_CODE_NUM_CLASSES,), dtype=tf.float32),
                "label": tf.int64,
                "feature": {name: dtype
                            for name, (dtype, func) in self.FEATURE_DICT.items()},
            }),
            supervised_keys=("feature", "label"),
            urls=["https://github.com/google-research/bert/blob/master/run_classifier.py & https://github.com/tensorflow/models/blob/master/official/nlp/bert/run_classifier.py"],
            citation="@ONLINE {Chinese dataset: Multi-label Text Classification using BERT}"
        )

    @Override(SuperDatasetBuilder)
    def _split_generators(self, dl_manager):
        generator_array = []
        if self._train_data_file:
            generator_array.append(tfds.core.SplitGenerator(
                name=tfds.Split.TRAIN,
                num_shards=3,
                gen_kwargs={
                    "max_seq_length": self.MAX_SEQ_LENGTH,
                    "data_type": "train",
                    "data_path": self._train_data_file
                }))
        if self._test_data_file:
            generator_array.append(tfds.core.SplitGenerator(
                name=tfds.Split.TEST,
                num_shards=1,
                gen_kwargs={
                    "max_seq_length": self.MAX_SEQ_LENGTH,
                    "data_type": "test",
                    "data_path": self._test_data_file
                }))
        if self._validation_data_file:
            generator_array.append(tfds.core.SplitGenerator(
                name=tfds.Split.VALIDATION,
                num_shards=1,
                gen_kwargs={
                    "max_seq_length": self.MAX_SEQ_LENGTH,
                    "data_type": "validation",
                    "data_path": self._validation_data_file
                }))
        return generator_array

    @classmethod
    def readfile(cls, filename):
        '''
        read file
        '''
        lines = []
        with open(filename, "r") as f:
            reader = csv.reader(f, delimiter="\t", quotechar=None)
            for line in reader:
                lines.append(line)
        return lines

    @Override(SuperDatasetBuilder)
    def _generate_examples(self, **kwargs):
        """
        # The convention in BERT is:
        # (a) For sequence pairs:
        #  tokens:   [CLS] is this jack ##son ##ville ? [SEP] no it is not . [SEP]
        #  type_ids: 0   0  0    0    0     0       0 0    1  1  1  1   1 1
        # (b) For single sequences:
        #  tokens:   [CLS] the dog is hairy . [SEP]
        #  type_ids: 0   0   0   0  0     0 0
        #
        # Where "type_ids" are used to indicate whether this is the first
        # sequence or the second sequence. The embedding vectors for `type=0` and
        # `type=1` were learned during pre-training and are added to the wordpiece
        # embedding vector (and position vector). This is not *strictly* necessary
        # since the [SEP] token unambigiously separates the sequences, but it makes
        # it easier for the model to learn the concept of sequences.
        #
        # For classification tasks, the first vector (corresponding to [CLS]) is
        # used as as the "sentence vector". Note that this only makes sense because
        # the entire model is fine-tuned.
        ```
        tokens = []
        segment_ids = []
        tokens.append("[CLS]")
        segment_ids.append(0)
        for token in tokens_a:
            tokens.append(token)
            segment_ids.append(0)
        tokens.append("[SEP]")
        segment_ids.append(0)

        if tokens_b:
            for token in tokens_b:
                tokens.append(token)
                segment_ids.append(1)
            tokens.append("[SEP]")
            segment_ids.append(1)

        input_ids = tokenizer.convert_tokens_to_ids(tokens)

        # The mask has 1 for real tokens and 0 for padding tokens. Only real
        # tokens are attended to.
        input_mask = [1] * len(input_ids)

        # Zero-pad up to the sequence length.
        while len(input_ids) < max_seq_length:
            input_ids.append(0)
            input_mask.append(0)
            segment_ids.append(0)

        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length
        ```
        """
        # model_path = sys.path[0] + "/data/bert/tf_hub/bert_zh_L-12_H-768_A-12/1"
        model_path = "/tony/pycharm_projects/skydl/python/skydl/datasets/data/bert/tf_hub/bert_zh_L-12_H-768_A-12/1"
        tokenizer = FullTokenizer(vocab_file=model_path + "/assets/vocab.txt", do_lower_case=True)
        data_path = kwargs.get("data_path")
        data_type = kwargs.get("data_type")
        max_seq_length = int(kwargs.get("max_seq_length"))
        lines = self.readfile(data_path)
        # create examples
        examples = []
        rows = []

        # auto get all labels
        for (i, line) in enumerate(lines):
            self.ALL_LABELS.add(line[0])
        label_map = {}
        for (i, label) in enumerate(list(self.ALL_LABELS), 0):
            label_map[label] = i

        # handle all lines
        for (i, line) in enumerate(lines):
            if i % 5000 == 0:
                print("Writing example %d of %d" % (i, len(examples)))
            guid = "%s-%s" % (data_type, i)
            textlist = [convert_to_unicode(text) for text in line[1]]
            tokens = []
            label_ids = []
            for idx, word in enumerate(textlist):
                tokens.extend(tokenizer.tokenize(word))
            label_ids.append(label_map[line[0]])
            # Zero-pad up to the sequence length.
            pad_token = "[PAD]"
            cls_token = "[CLS]"
            sep_token = "[SEP]"
            if len(tokens) > max_seq_length - 2:  # 减去[CLS]和[SEP]的标志位
                tokens = tokens[: (max_seq_length - 2)]
            tokens = [cls_token] + tokens + [sep_token]
            padding_length = max_seq_length - len(tokens)
            tokens += [pad_token] * padding_length
            input_ids = tokenizer.convert_tokens_to_ids(tokens)
            # Create the attention mask.
            #   - If a token ID is 0, then it's padding, set the mask to 0.
            #   - If a token ID is > 0, then it's a real token, set the mask to 1.
            input_mask = [int(token_id > 0) for token_id in input_ids]
            # segment_ids = [int(token_id > 0) for token_id in input_ids]
            segment_ids = [0] * len(input_ids)
            assert len(input_ids) == max_seq_length
            assert len(input_mask) == max_seq_length
            assert len(segment_ids) == max_seq_length
            if i < 5:
                print("*** Example ***")
                print("guid: %s" % (guid))
                print("tokens: %s" % " ".join([printable_text(x) for x in tokens]))
                print("input_ids: %s" % " ".join([str(x) for x in input_ids]))
                print("input_mask: %s" % " ".join([str(x) for x in input_mask]))
                print("segment_ids: %s" % " ".join([str(x) for x in segment_ids]))
                print("label_ids: %s" % " ".join([str(x) for x in label_ids]))
                # print("label_mask: %s" % " ".join([str(x) for x in label_mask]))
            row = {
                "input_word_ids": input_ids,
                "input_mask": input_mask,
                "input_type_ids": segment_ids,
                "target": label_ids[0]  # only 1 elements
            }
            rows.append(row)
        for curr_row in rows:
            label_val = curr_row.pop(self.TARGET_COLUMN)
            yield {
                # "label": tf.one_hot(label_val, len(self.ALL_LABELS)).numpy(),
                "label": label_val,
                "feature": {
                    name: self.FEATURE_DICT[name][1](value)
                    for name, value in curr_row.items()
                }
            }


if __name__ == '__main__':
    dataset_name = ChineseBertClassifierDatasetBuilder.camelcase_to_snakecase("ChineseBertClassifierDatasetBuilder")
    print(SuperDatasetBuilder.list_builders())
    batched_datasets = ChineseBertClassifierDatasetBuilder.load_batched_datasets(dataset_name, config_name="plain_text")
    num_examples = ChineseBertClassifierDatasetBuilder.get_num_examples(dataset_name, tfds.Split.TRAIN)
    print(f"num_examples={num_examples}")
    batched_dataset_features = ChineseBertClassifierDatasetBuilder.read_batched_datasets(batched_datasets)
    for features, labels in batched_dataset_features:
        print(f"features={features}, labels={labels}")
    print("end!!")
