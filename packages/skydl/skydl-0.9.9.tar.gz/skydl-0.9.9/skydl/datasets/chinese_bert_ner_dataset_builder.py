# coding=utf-8
import sys
import collections
import tensorflow as tf
import tensorflow_datasets as tfds
from py_common_util.common.annotations import Override
from skydl.datasets.super_tf_dataset_builder import SuperDatasetBuilder, DefaultDatasetBuilderConfig
from skydl.models_zoo.bert.official.nlp.bert.tokenization import FullTokenizer, printable_text, convert_to_unicode


class ChineseBertNerDatasetBuilder(SuperDatasetBuilder):
    """
    中文bert模型用的ner数据集
    参考：https://github.com/ProHiryu/bert-chinese-ner
    https://github.com/huggingface/transformers/blob/master/examples/run_tf_ner.py
    https://github.com/kamalkraj/BERT-NER-TF
    https://github.com/ymcui/Chinese-BERT-wwm
    https://github.com/liloi/bert-tf2
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
    INPUT_IDS_COLUMN = "input_ids"    # input_ids
    INPUT_MASK_COLUMN = "input_mask"  # input_mask
    SEGMENTS_ID_COLUMN = "segments_id"  # segments_id
    # target column name
    TARGET_COLUMN = "target"
    # used to change labels to ids
    LABEL_DICT = collections.OrderedDict([
        (i, i) for i in ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "X", "[CLS]", "[SEP]"]
    ])
    # feature column dict
    FEATURE_DICT = collections.OrderedDict([
        ("input_ids", (tfds.features.Tensor(shape=(MAX_SEQ_LENGTH,), dtype=tf.int32), SuperDatasetBuilder.convert_to_int)),
        ("input_mask", (tfds.features.Tensor(shape=(MAX_SEQ_LENGTH,), dtype=tf.int32), SuperDatasetBuilder.convert_to_int)),
        ("segment_ids", (tfds.features.Tensor(shape=(MAX_SEQ_LENGTH,), dtype=tf.int32), SuperDatasetBuilder.convert_to_int)),
        # 在_generate_examples()里单独处理了target列，这里不需要重复定义
    ])

    def __init__(self, data_dir=None, config=None):
        super().__init__(data_dir=data_dir, config=config)
        self._num_shards = 1
        self._train_data_file = sys.path[0] + "/data/bert/ner/train.txt"
        self._test_data_file = sys.path[0] + "/data/bert/ner/test.txt"
        self._validation_data_file = sys.path[0] + "/data/bert/ner/dev.txt"

    @Override(SuperDatasetBuilder)
    def _info(self):
        return tfds.core.DatasetInfo(
            builder=self,
            description=("Chinese Bert-based Named Entity Recognition dataset"),
            features=tfds.features.FeaturesDict({
                "label": tfds.features.Tensor(shape=(self.MAX_SEQ_LENGTH,), dtype=tf.int32),
                "feature": {name: dtype
                            for name, (dtype, func) in self.FEATURE_DICT.items()},
            }),
            supervised_keys=("feature", "label"),
            urls=["https://github.com/huggingface/transformers/issues/1166"],
            citation="@ONLINE {Chinese Bert-based Named Entity Recognition dataset}"
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
            #label.append(splits[-1][:-1])
            label.append(splits[-1].replace("\n", ""))
        if len(sentence) > 0:
            data.append((sentence, label))
            sentence = []
            label = []
        return data

    @classmethod
    def readfile2(cls, input_file):
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

    @Override(SuperDatasetBuilder)
    def _generate_examples(self, **kwargs):
        model_path = sys.path[0] + "/data/bert/tf_hub/bert_zh_L-12_H-768_A-12/1"
        tokenizer = FullTokenizer(vocab_file=model_path + "/assets/vocab.txt", do_lower_case=True)
        data_path = kwargs.get("data_path")
        data_type = kwargs.get("data_type")
        max_seq_length = int(kwargs.get("max_seq_length"))
        label_map = {}
        for (i, label) in enumerate(list(self.LABEL_DICT.values()), 1):
            label_map[label] = i
        lines = self.readfile(data_path)
        # create examples
        examples = []
        rows = []
        for (i, line) in enumerate(lines):
            if i % 5000 == 0:
                print("Writing example %d of %d" % (i, len(examples)))
            guid = "%s-%s" % (data_type, i)
            textlist = [convert_to_unicode(text) for text in line[0]]
            labellist = [convert_to_unicode(text) for text in line[1]]
            tokens = []
            labels = []
            # print(textlist)
            for idx, word in enumerate(textlist):
                token = tokenizer.tokenize(word)
                # print(token)
                tokens.extend(token)
                label_1 = labellist[idx]
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
            # label_mask = [1] * len(input_ids)
            while len(input_ids) < max_seq_length:
                input_ids.append(0)
                input_mask.append(0)
                segment_ids.append(0)
                # we don't concerned about it!
                label_ids.append(0)
                ntokens.append("**NULL**")
                # label_mask.append(0)
            # print(len(input_ids))
            assert len(input_ids) == max_seq_length
            assert len(input_mask) == max_seq_length
            assert len(segment_ids) == max_seq_length
            assert len(label_ids) == max_seq_length
            # assert len(label_mask) == max_seq_length
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
                "input_ids": input_ids,
                "input_mask": input_mask,
                "segment_ids": segment_ids,
                "target": label_ids
            }
            rows.append(row)
        for curr_row in rows:
            label_val = curr_row.pop(self.TARGET_COLUMN)
            yield {
                "label": label_val,
                "feature": {
                    name: self.FEATURE_DICT[name][1](value)
                    for name, value in curr_row.items()
                }
            }


if __name__ == '__main__':
    dataset_name = ChineseBertNerDatasetBuilder.camelcase_to_snakecase("ChineseBertNerDatasetBuilder")
    print(SuperDatasetBuilder.list_builders())
    batched_datasets = ChineseBertNerDatasetBuilder.load_batched_datasets(dataset_name, config_name="plain_text")
    num_examples = ChineseBertNerDatasetBuilder.get_num_examples(dataset_name, tfds.Split.TRAIN)
    print(f"num_examples={num_examples}")
    batched_dataset_features = ChineseBertNerDatasetBuilder.read_batched_datasets(batched_datasets)
    for features, labels in batched_dataset_features:
        print(f"features={features}, labels={labels}")
    print("end!!")
