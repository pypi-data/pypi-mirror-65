"""
https://github.com/tensorflow/models/tree/master/official/nlp/bert
https://github.com/flairNLP/flair
BERT原理解析 https://zhuanlan.zhihu.com/p/50913043
如何评价 BERT 模型？ https://www.zhihu.com/question/298203515/answer/516170825
colab上基于tensorflow2.0的BERT中文多分类 https://www.debugger.wiki/article/html/1579681412686482
https://github.com/ProHiryu/bert-chinese-ner
https://github.com/bojone/bert4keras
Roberta for NER task https://github.com/huggingface/transformers/issues/1166
[P] Implementing BERT-model for NER https://www.reddit.com/r/MachineLearning/comments/edt3tc/p_implementing_bertmodel_for_ner/
NLP - 基于 BERT 的中文命名实体识别（NER) https://eliyar.biz/nlp_chinese_bert_ner/
https://github.com/macanv/BERT-BiLSTM-CRF-NER
https://github.com/BrikerMan/Kashgari/blob/cf5b6dc10f65362563bedb9e88649a05f1d9136f/kashgari/tasks/labeling/models.py
```
参考数据：https://github.com/FuYanzhe2/Name-Entity-Recognition/tree/master/BERT-BiLSTM-CRF-NER/bert
Using the default training scripts (run_classifier.py and run_squad.py), we benchmarked the maximum batch size on single Titan X GPU (12GB RAM) with TensorFlow 1.11.0:
System	Seq Length	Max Batch Size
BERT-Base	64	64
...	128	32
...	256	16
...	320	14
...	384	12
...	512	6
BERT-Large	64	12
...	128	6
...	256	2
...	320	1
...	384	0
...	512	0
```
=========
Named Entity Recognition https://paperswithcode.com/task/named-entity-recognition-ner
search state of the art ner: https://www.google.com/search?rlz=1C5CHFA_enCN643CN643&sxsrf=ACYBGNQHlUYEKBUD53i0sgKXjOp0mr37xA%3A1581512242277&ei=MvZDXtCsEMXVmAWP5J-oBQ&q=state+of+the+art+ner&oq=state+of+the+art+ner&gs_l=psy-ab.3..35i39j0i203l2j0i8i30l7.13674.15520..17365...0.0..0.109.790.4j4......0....1..gws-wiz.......0i30j0i7i30j0i8i7i30j35i304i39j0i7i30i19j0i8i7i30i19.2zp1E299TAA&ved=0ahUKEwjQjaKbiMznAhXFKqYKHQ_yB1UQ4dUDCAs&uact=5
BioBERT: a pre-trained biomedical language representation model https://github.com/dmis-lab/biobert
https://github.com/huggingface/transformers/tree/master/examples#named-entity-recognition
Implement fine-tuning BERT on CoNLL-2003 named entity recognition task #1275 https://github.com/huggingface/transformers/pull/1275
https://gist.github.com/stefan-it/c39b63eb0043182010f2f61138751e0f
"""