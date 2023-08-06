# coding=utf-8
import sys
import re
import io
import unicodedata
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow_datasets.core.features import text_feature
from py_common_util.common.annotations import Override
from skydl.datasets.super_tf_dataset_builder import DefaultDatasetBuilderConfig, SuperDatasetBuilder


class TranslateDatasetBuilder(SuperDatasetBuilder):
    """
    参考：https://www.tensorflow.org/tutorials/text/nmt_with_attention
    https://github.com/tensorflow/docs/blob/master/site/zh-cn/tutorials/text/nmt_with_attention.ipynb
    https://github.com/tensorflow/datasets/blob/master/tensorflow_datasets/translate/ted_hrlr.py
    https://rubikscode.net/2019/08/05/transformer-with-python-and-tensorflow-2-0-attention-layers/
    我们将使用http://www.manythings.org/anki/ 提供的一个语言数据集。这个数据集包含如下格式的语言翻译对：
    May I borrow this book? ¿Puedo tomar prestado este libro?
    """
    BUILDER_CONFIGS = [
        DefaultDatasetBuilderConfig(
            name="plain_text",
            version="0.0.1",
            description="Plain text",
        )
    ]
    _VALID_LANGUAGE_PAIRS = (
        ("en", "cn")
    )

    def __init__(self, data_dir=None, config=None):
        super().__init__(data_dir=data_dir, config=config)
        self._num_shards = 1
        self._train_data_file = sys.path[0] + "/data/translate/cmn-eng/cmn.txt"
        self._test_data_file = None
        self._validation_data_file = None

    @Override(SuperDatasetBuilder)
    def _info(self):
        return tfds.core.DatasetInfo(
            builder=self,
            description=("Chinese (Mandarin) - English dataset"),
            features=tfds.features.FeaturesDict({
                lang: text_feature.Text(None, None)
                for lang in self._VALID_LANGUAGE_PAIRS
            }),
            supervised_keys=self._VALID_LANGUAGE_PAIRS,
            urls=["http://www.manythings.org/anki/cmn-eng.zip"],
            citation="@ONLINE {Chinese (Mandarin) - English dataset}"
        )

    @Override(SuperDatasetBuilder)
    def _split_generators(self, dl_manager):
        generator_array = []
        if self._train_data_file:
            generator_array.append(tfds.core.SplitGenerator(
                name=tfds.Split.TRAIN,
                num_shards=3,
                gen_kwargs={
                    "data_path": self._train_data_file
                }))
        if self._test_data_file:
            generator_array.append(tfds.core.SplitGenerator(
                name=tfds.Split.TEST,
                num_shards=1,
                gen_kwargs={
                    "data_path": self._test_data_file
                }))
        if self._validation_data_file:
            generator_array.append(tfds.core.SplitGenerator(
                name=tfds.Split.VALIDATION,
                num_shards=1,
                gen_kwargs={
                    "data_path": self._validation_data_file
                }))
        return generator_array

    @Override(SuperDatasetBuilder)
    def _generate_examples(self, **kwargs):
        """Generate features and target given the directory path.
        Args:
          file_path: path where the csv file is stored
        Yields:
          The features and the target
        """
        # 这里已经手工下载好了zip文件，其实还可以在线下载文件
        # path_to_zip = tf.keras.utils.get_file('cmn-eng.zip', origin='http://www.manythings.org/anki/cmn-eng.zip', extract=True)
        # path_to_file = os.path.dirname(path_to_zip) + "/cmn-eng/cmn.txt"
        data_path = kwargs.get("data_path")
        with tf.io.gfile.GFile(data_path) as f:
            # input_tensor, target_tensor, inp_lang, targ_lang = self.load_dataset(f.name)
            # num_examples = input_tensor.shape[0]
            # for i in range(num_examples):
            #     yield {
            #         "en": target_tensor[i],
            #         "cn": input_tensor[i]
            #     }
            targ_lang, inp_lang = TranslateDatasetBuilder.create_dataset(f.name)
            for idx, (targ, inp) in enumerate(zip(targ_lang, inp_lang)):
                yield {
                    "en": targ,
                    "cn": inp
                }

    def unicode_to_ascii(s):
        """将 unicode 文件转换为 ascii"""
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

    def preprocess_sentence(w, is_chinese=False):
        """
        1. 去除重音符号 2. 清理句子 3. 返回这样格式的单词对：[ENGLISH, CHINESE]
        ```
        e.g.
        en_sentence = u"May I borrow this book?"
        sp_sentence = u"¿Puedo tomar prestado este libro?"
        print(preprocess_sentence(en_sentence))
        print(preprocess_sentence(sp_sentence).encode('utf-8'))
        ```
        :param w:
        :return:
        """
        w = TranslateDatasetBuilder.unicode_to_ascii(w.lower().strip())
        # 在单词与跟在其后的标点符号之间插入一个空格
        # 例如： "he is a boy." => "he is a boy ."
        # 参考：https://stackoverflow.com/questions/3645931/python-padding-punctuation-with-white-spaces-keeping-punctuation
        w = re.sub(r"([？?。.！!，,¿])", r" \1 ", w)
        w = re.sub(r'[" "]+', " ", w)
        # 除了中文汉字与(a-z, A-Z, ".", "?", "!", ",")，将其它所有字符替换为空格
        w = re.sub(r"[^a-zA-Z?.!,¿\u4e00-\u9fa5]+", " ", w)
        w = w.rstrip().strip()
        # 给句子加上开始和结束标记
        # 以便模型知道何时开始和结束预测
        if is_chinese:
            # 把中文句子拆成一个个的字 e.g. '把中文句子拆成一个个的字' -> '把 中 文 句 子 拆 成 一 个 个 的 字'
            w = ' '.join([t for t in w])
        w = '<start> ' + w + ' <end>'
        return w

    def create_dataset(path):
        """
        ```
        cmn.txt文件格式：
        Hi.	嗨。	CC-BY 2.0 (France) Attribution: tatoeba.org #538123 (CM) & #891077 (Martha)
        Hi.	你好。	CC-BY 2.0 (France) Attribution: tatoeba.org #538123 (CM) & #4857568 (musclegirlxyp)
        ```
        :param path:
        :return:
        """
        lines = io.open(path, encoding='UTF-8').read().strip().split('\n')
        word_pairs = [[TranslateDatasetBuilder.preprocess_sentence(w, False if idx < 1 else True) for idx, w in enumerate(l.split('\t')) if idx < 2] for l in lines]
        return zip(*word_pairs)

    def tokenize(lang):
        lang_tokenizer = tf.keras.preprocessing.text.Tokenizer(filters='')
        lang_tokenizer.fit_on_texts(lang)
        tensor = lang_tokenizer.texts_to_sequences(lang)
        tensor = tf.keras.preprocessing.sequence.pad_sequences(tensor, padding='post')
        return tensor, lang_tokenizer

    def load_dataset(path):
        # 创建清理过的输入输出对
        targ_lang, inp_lang = TranslateDatasetBuilder.create_dataset(path)
        return TranslateDatasetBuilder.load_dataset_from_sentences(targ_lang, inp_lang)

    def load_dataset_from_sentences(targ_lang, inp_lang):
        """
        将全局的word生成对应的int tokenize
        :param targ_lang: e.g. ["<start> i m dead tired . <end>", "<start> don t forget smoking is bad for your health . <end>"]
        :param inp_lang:  e.g. ["<start> 我 累 死 了 <end>", "<start> 不 要 忘 记 吸 烟 对 你 的 健 康 有 害 <end>"]
        :return:
        """
        input_tensor, inp_lang_tokenizer = TranslateDatasetBuilder.tokenize(inp_lang)
        target_tensor, targ_lang_tokenizer = TranslateDatasetBuilder.tokenize(targ_lang)
        return input_tensor, target_tensor, inp_lang_tokenizer, targ_lang_tokenizer

    def max_length(tensor):
        """计算目标张量的最大长度（max_length）"""
        return max(len(t) for t in tensor)

    def convert(lang, tensor):
        """
        ```
        返回 e.g.
        1 ----> <start>
        2605 ----> mande
        ```
        :param tensor:
        :return:
        """
        for t in tensor:
            if t != 0:
                print("%d ----> %s" % (t, lang.index_word[t]))


if __name__ == '__main__':
    dataset_name = TranslateDatasetBuilder.camelcase_to_snakecase("TranslateDatasetBuilder")
    print(SuperDatasetBuilder.list_builders())
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
        # print(f"features={''.join([feature.decode('utf-8') for feature in features])}, labels={''.join([label.decode('utf-8') for label in labels])}")
    input_tensor, target_tensor, inp_lang, targ_lang = TranslateDatasetBuilder.load_dataset_from_sentences(all_en_sentences, all_cn_sentences)
    # 计算目标张量的最大长度 （max_length）
    max_length_targ, max_length_inp = TranslateDatasetBuilder.max_length(target_tensor), TranslateDatasetBuilder.max_length(input_tensor)
    print(f"max_length_targ={max_length_targ}, max_length_inp={max_length_inp}")
    TranslateDatasetBuilder.convert(inp_lang, input_tensor[0])
    print(f"end!!")
    #dataset = tf.data.Dataset.from_tensor_slices(np.array([1.0, 2.0, 3.0, 4.0, 5.0]))
    dataset = tf.data.Dataset.from_tensor_slices((input_tensor, target_tensor)).batch(64, drop_remainder=True)
    # for input_batch, target_batch in tfds.as_numpy(dataset):
    #     print(input_batch, target_batch)

