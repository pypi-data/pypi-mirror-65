# NLUTOOLS: NLU 工具包

nlutools 是一系列模型与算法的nlu工具包，提供以下功能：
<!-- TOC -->

- [NLUTOOLS: NLU 工具包](#nlutools-nlu-工具包)
    - [常见问题](#常见问题)
    - [TODO](#todo)
    - [安装](#安装)
    - [0 初始化](#0-初始化)
    - [1 切词](#1-切词)
    - [2 切句](#2-切句)
    - [3 词向量](#3-词向量)
        - [3.1 离线词向量](#31-离线词向量)
        - [3.2 在线词向量](#32-在线词向量)
            - [3.2.1 在线请求词向量](#321-在线请求词向量)
            - [3.2.2 获取词向量相似的词](#322-获取词向量相似的词)
            - [3.2.3 获得两个词的相似度](#323-获得两个词的相似度)
    - [4 句向量](#4-句向量)
        - [4.1 基于词向量](#41-基于词向量)
        - [4.2 基于Bert](#42-基于bert)
        - [4.3 基于SentenceBert](#43-基于sentencebert)
    - [5 预训练中文语言模型](#5-预训练中文语言模型)
    - [6 实体](#6-实体)
    - [7 情感分析](#7-情感分析)
    - [8 关键字提取](#8-关键字提取)
    - [9 句子相似度计算](#9-句子相似度计算)
    - [10 动宾提取](#10-动宾提取)
    - [11 句子合理性判别](#11-句子合理性判别)
    - [12 姓名识别服务](#12-姓名识别服务)
    - [13 小样本分类](#13-小样本分类)
    - [14 文本聚类](#14-文本聚类)

<!-- /TOC -->
## 常见问题

1. 以下工具在开发环境不支持：分词，词向量，句向量（Sentence-BERT除外），关键词
2. 以下工具在开发环境下容易超时：情感分析、句子合理性

## TODO

1. 切词增删自定义字典多进程和多实例没法在一次请求中完成配置

## 安装

```bash
# 开发环境
pip install -U -i http://211.148.28.23:59990/simple --trusted-host 211.148.28.23 nlutools
# 线上/测试环境（暂时不能用）
pip install -U -i http://pip.ifchange.com:59990/simple nlutools
# pypi
pip install -U nlutools
# 源码安装
git clone https://gitlab.ifchange.com/nlu/nlutools.git
cd nlutools/python
git checkout dev
python setup.py develop
```

## 0 初始化

```python
from nlutools import NLU
# docker容器内必须手动指定运行环境，容器外可选
# dev=开发，online_stable=线上服务，online_dev=线上调研，test=测试
# 若需要在测试环境测试模型相关服务的性能，请将env设置为online_dev，线上服务建议切换为online_stable
# timeout参数用于控制服务的等待时间，主要适用于机器资源紧张的开发环境，默认为3秒
nlu = NLU(env="dev", timeout=3)
```

## 1 切词

切词工具接口函数：cut(text, mode, pos, cut_all)

其中

* text 为要切词的原始文本

* mode 为分词模式，"fast"

* pos为词性保留选项，True or False (默认开启)

* cut_all为切词粒度控制 True or False (非百科名词短语支持，默认关闭)

调用方式为：

```python
nlu.cut('这是一个能够输出名词短语的分词器，欢迎试用！')
```

返回结果：

```json
{
    'np': ['分词器'],                   // 除去百度百科之外，其他的名词短语
    'entity' : ['名词短语'],            // 百度百科中会出现的词条
    'text': '这是一个能够输出名词短语的分词器，欢迎试用！',         // 原始文本
    'items' : ['这', '是', '一个', '能够', '输出', '名词短语', '的', '分词器', '，', '欢迎', '试用', '！'],  // 分词结果
    'pos': ['r', 'v', 'm', 'v', 'v', 'ne', 'uj', 'np', 'x', 'v', 'vn', 'x']     // 词性
}
```

## 2 切句

切句工具提供两种模式，接口函数：split(text, cut_comma, cut_all)

其中

* text 为需要进行切句的原始文本序列，格式为list

* cut_comma 部分逗号结尾的短句会被切分，默认为False

* cut_all 所有逗号结尾的短句全部会被切分，默认为False

调用方式：

```python
nlu.split(['我喜欢在春天去观赏桃花。在夏天去欣赏荷花 在秋天去观赏红叶。但更喜欢在冬天去欣赏雪景。'])
nlu.split(['我喜欢在春天去观赏桃花, 哈哈哈, 你好呀，嘿嘿哈哈哈哈，诶诶阿法！'], cut_comma=True)
nlu.split(['哈哈哈, 你好呀，嘿嘿哈哈哈哈，诶诶阿法！'], cut_all=True)
```

返回结果：

```json
[['我喜欢在春天去观赏桃花', '在夏天去欣赏荷花 在秋天去观赏红叶', '但更喜欢在冬天去欣赏雪景']]
[['我喜欢在春天去观赏桃花', '哈哈哈, 你好呀，嘿嘿哈哈哈哈', '诶诶阿法']]
[['哈哈哈', '你好呀', '嘿嘿哈哈哈哈', '诶诶阿法']]
```

## 3 词向量

### 3.1 离线词向量

   获得词向量文件，可以根据版本号获取，目前版本号包括：v1.0

   默认是下载最新版。获取到的文件夹下面包含两个文件，一个是词向量文件，一个是字向量文件。

```python
nlu.getW2VFile('v1.0', '/local/path/')
```

### 3.2 在线词向量

支持两个来源的词向量，腾讯版(200维)和e成版(300维)，通过type参数控制('ifchange' or 'tencent', 默认ifchange)

ifchange词向量基于全量cv工作经历，加入了领域相关实体，通过fasttext训练，没有oov问题。参考:https://fasttext.cc

腾讯词向量具体信息参见：https://ai.tencent.com/ailab/nlp/embedding.html

#### 3.2.1 在线请求词向量

```python
# type 默认'ifchange'
nlu.w2v('深度学习')
# 腾讯词向量
nlu.w2v('深度学习', type='tencent')
# 或者传入多个词
nlu.w2v(['深度学习', '机器学习'])
```

#### 3.2.2 获取词向量相似的词

```python
# 默认使用e成词向量
nlu.sim_words('深度学习', topn=10, type="ifchange")  # 10表示最多返回10个最相似的词
# 或者传入多个词
nlu.sim_words(['深度学习', '机器学习'], 10, "tencent")
```

#### 3.2.3 获得两个词的相似度

```python
# 使用腾讯词向量
nlu.word_sim('深度学习', '机器学习', type='tencent')
# 使用ifchange词向量
nlu.word_sim('深度学习', '机器学习', type='ifchange')
```

## 4 句向量

### 4.1 基于词向量

```python
nlu.s2v(['主要负责机器学习算法的研究', '训练模型、编写代码、以及其他一些工作']) # 300维
nlu.s2v(['主要负责机器学习算法的研究', '训练模型、编写代码、以及其他一些工作'], type='tencent') # 200维
```

返回结果：

```json
{
    'dimention': 300,  # 维度
    'veclist': [[0.01, ...,0.56],[0.89,...,-0.08]]
}
```

### 4.2 基于Bert

bert向量有两个版本：

1. 基于哈工大全词mask的预训练句向量表征

2. 基于cv中工作经历全词mask的预训练句向量表征

调用方式：

```python
nlu.bert_vec(['主要负责机器学习算法的研究', '训练模型、编写代码、以及其他一些工作'], mode="wwm_ext")  # 哈工大版
nlu.bert_vec(['主要负责机器学习算法的研究', '训练模型、编写代码、以及其他一些工作'], mode='cv')  # ifchange版本
```

### 4.3 基于SentenceBert

更具语义的句子向量表征，目前的SOTA模型

调用方式：

```python
# 获取句子向量
nlu.bert_encode("句子通用向量表征") # 向量维度512
nlu.bert_encode(["句子通用向量表征", "自然语言处理是人工智能的明珠"])
# 计算两个句子相似度
nlu.bert_sim("句子通用向量表征", "自然语言处理是人工智能的明珠")
# 计算句子集合B中与句子A最相似的句子
nlu.bert_sim("句子通用向量表征", ["自然语言处理是人工智能的明珠", "训练模型、编写代码、以及其他一些工作"])
# 计算两组句子间的两两相似度
nlu.bert_sim(
    ["句子通用向量表征", "自然语言处理是人工智能的明珠"],
    ["主要负责机器学习算法的研究", "训练模型、编写代码、以及其他一些工作"])
```

## 5 预训练中文语言模型

可用的模型有：

* base_cn: Google官方中文Base
* wwm: 哈工大全词MASK_v1
* wwm_ext: 哈工大全词MASK_v2
* ernie_cv: 使用工作经历文本重新训练的ernie模型

调用方式：

```python
# 若给定输出目录，直接进行下载
nlu.bertmodels('wwm_ext', './bert_models')
```

## 6 实体

实体识别(转发自图谱组)

基于输入的自然文本，识别 学校(school)、职能(function)、技能(skill)、学历(degree)、专业(major)、公司(company)、证书(certificate) 七大实体

```python
nlu.ner(["我毕业于北京大学"],'ner')
```

返回结果:

```json
[
    [
        {
        'type': 'school',
        'text': '北京大学',
        'boundary': [4, 8],
        'entityIdCandidates': [{'entityID': '0', 'entityName': '', 'score': 1.0}]
        }
    ]
]
```

## 7 情感分析

返回句子的情感极性，持正向和负向情感

参数说明：

* sentences 输入的文本列表
* prob 值为False，不返回预测句子的情感预测得分，只返回情感类别（pos或者neg）；值为True，则都返回。

调用方式：

```python
nlu.emotion(['这家公司很棒','这家公司很糟糕'], prob=False)
```

返回结果：

```json
{
    'text': ['这家公司很棒','这家公司很糟糕'],
    'labels': ['pos','neg']
}
```

## 8 关键字提取

方法：keywords(content, topk, with_weight, mode)

参数说明：

* content 为输入文本.
* topk 为最大返回关键字个数. 默认3
* with_weight 是否返回关键字的权值. 默认False
* mode 可选"default"和"ai4"，默认"default"

调用方式：

```python
nlu.keywords('主要负责机器学习算法的研究以及搭建神经网络，训练模型，编写代码，以及其他的一些工作', 4, True)
nlu.keywords('主要负责机器学习算法的研究以及搭建神经网络，训练模型，编写代码，以及其他的一些工作', 4, True, "ai4")
```

返回结果：

```json
{'weights': [9.64244, 9.36891, 6.2782, 5.69476], 'keywords': ['机器学习算法', '神经网络', '训练', '模型']}
{'weights': [9.64244, 9.36891, 6.2782, 5.69476], 'keywords': ['机器学习算法', '神经网络', '训练', '模型']}
```

## 9 句子相似度计算

句子相似有2种计算方式，

1. 基于ifchange词向量的句向量的cosine  

2. 基于腾讯词向量的句向量的cosine

方法: sent_sim(text1, text2, precision=100, type='ifchange')

参数说明：

* text1 为待计算句子1
* text2 为待计算句子2
* precision 为计算结果刻度，如1000，则返回0~1000的值
* type : ifchange | tencent

调用方式：

```python
nlu.sent_sim('你家的地址是多少', '你住哪里', 1000, type="ifchange")
```

返回结果:

```json
{'result': 600}
```

## 10 动宾提取

方法: vob(content, mode）

参数说明:

* content 输入文本，str
* mode 提取模式，可选值为 fast 或accurate. 目前仅支持fast，忽略次参数

调用方式：

```python
nlu.vob('要负责机器学习算法的研究以及搭建神经网络，训练模型，编写代码，以及其他的一些工作')
```

返回结果：

```json
{'content': [['编写', ' 代码']]}
```

## 11 句子合理性判别

方法： rationality(text, with_word_prob)

参数说明：

* text, 带判定句子,类型是list
* with_word_prob,返回结果中是否包含每个词合理性的概率，str，取值范围为 'true' 或 'false'。 默认'false'

调用方式：

```python
nlu.rationality(['床前明月光，疑是地上霜', '床前星星光，疑是地上霜', '床前白月光，疑是地上霜'])
```

返回结果：

```json
 {
    'ppl': [63.2965, 187.2091, 71.3999]
 }
```

## 12 姓名识别服务

来自nb2组的姓名识别

调用方式：

```python
nlu.name_ner("刘德华的⽼老老婆叫叶丽倩")
```

返回结果： ['刘德华', '叶丽倩']

## 13 小样本分类

基于sentence-bert的小样本快速分类模型

初始化：Classifier(corpus_path, center_dict)

参数说明:

二者必选其一

* corpus_path: 带有标签的语料文件路径
* center_dict: 不同标签的中心向量字典

方法：infer(sent, show_dist)

参数说明:

* sent: 待分类的文本，字符串或列表皆可
* show_dist: 是否展示详细分类结果, 默认True

你需要准备少量的不同类别的文本作为训练语料，参考格式[example.txt](https://gitlab.ifchange.com/nlu/nlutools/blob/dev/python/test/example.txt)

每一行为"文本\t标签"

调用方式：

```python
from nlutools import Classifier
classifier = Classifier("test/example.txt")
classifier.infer("我要上课", False)
classifier.infer(["我要上课", "我要学习"])
# 获取中心向量
center_dict = classifier.center_dict
```

返回结果：

```python
# show_dist=True时
([[('course', 0.3209079371175785),
   ('drills', 0.36650396955430686),
   ('other', 0.7005756412810639)],
  [('course', 0.48831207045316194),
   ('drills', 0.24168644818793783),
   ('other', 0.6338538862851899)]],
 ['course', 'drills'])
```

## 14 文本聚类

基于sentence-bert和KMeans的简易文本聚类

方法：clutser(corpus, num_clusters)

参数说明:

* corpus: 语料，格式为列表字符串或文件路径
* num_clusters: 聚类个数

语料参考格式[cluster_example.txt](https://gitlab.ifchange.com/nlu/nlutools/blob/dev/python/test/cluster_example.txt)

调用方式：

```python
clustered_sentences = nlu.cluster("test/example.txt", 3)
print(clustered_sentences)
```

返回结果：

```python
[['黑科技', '页面太丑', '你好'],
 ['给我推荐点课程', '有什么好的课程给我推荐一下', '我想上课', '推荐一些热门课程', '找一些关于会计的课给我'],
 ['我要陪练',
  '我要做练习',
  '我要练习话术',
  '做一下话术练习',
  '来几个知识点练习',
  '考察我几个知识点',
  '问我几个知识点',
  '模型训练不出来怎么办']]
```
