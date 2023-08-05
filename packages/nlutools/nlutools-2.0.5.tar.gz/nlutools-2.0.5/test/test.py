import sys

mode = sys.argv[1]
if mode == "local":
    sys.path.append(".")
from nlutools import NLU
from nlutools import Classifier

nlu = NLU(timeout=10)

# 分句
sents = [
    '我喜欢在春天去观赏桃花。在夏天去欣赏荷花 在秋天去观赏红叶。但更喜欢在冬天去欣赏雪景。',
    "可是啊。对的",
    "1. 接待客户，根据客户需求推荐相关产品，为客户讲解各种产品的特色；2) 根据特殊客户的需求，为客户单独设计产品或产品修改；三、盘点产品、日常报表，产品及柜台日常清洁等。",
    "“emmm.....”我说。“看看这个分句行不行。” 1. 机器学习 2. 深度学习",
    "哈哈哈, 你好呀，嘿嘿哈哈哈哈，诶诶阿法！"
]
res = nlu.split(sents)
assert len(res[0]) == 3
assert len(res[1]) == 2
assert len(res[2]) == 3
assert len(res[3]) == 4
assert len(res[4]) == 1
sents = ["哈哈哈, 你好呀，嘿嘿哈哈哈哈，诶诶阿法！"]
res = nlu.split(sents, cut_all=True)
assert len(res[0]) == 4
res = nlu.split(sents, cut_comma=True)
assert len(res[0]) == 2
print("nlu.split OK")

if nlu.env != "dev":
    # 分词
    line1 = "这是一个能够输出名词短语的分词器，欢迎试用！"
    line2 = "这是一个能够输出名词短语的分词器，欢迎试用，这里有神经网络，自然语言处理，和很多机器学习,tensorflow, pytorch"
    line3 = ""
    line4 = "欢迎"
    # line5 = "擅长红白案和本帮菜的厨师优先考虑"
    res = nlu.cut(line1)
    assert len(res['items']) == 12
    assert len(res['pos']) == 12
    assert res['np'][0] == '分词器'
    assert res['entity'][0] == '名词短语'
    res = nlu.cut(line1, pos=False)
    assert 'pos' not in res
    res = nlu.cut(line2)
    assert len(res['entity']) == 4
    res = nlu.cut(line3)
    assert res["items"] == []
    res = nlu.cut(line4)
    assert res["items"][0] == "欢迎"
    # res = nlu.cut("add", words=[["红白案", 100, "np"], ["本帮菜", 100, "np"]], user="test")
    # res = nlu.cut(line5)
    # assert "红白案" in res["items"] and "本帮菜" in res["items"]
    # res = nlu.cut("del", user="test")
    # res = nlu.cut(line5)
    # assert "红白案" not in res["items"] and "本帮菜" not in res["items"]
    print("nlu.cut OK")

    # 词向量
    res = nlu.w2v('深度学习')
    assert len(res) == 1
    assert len(res[0]) == 300
    res = nlu.w2v('深度学习', type='tencent')
    assert len(res) == 1
    assert len(res[0]) == 200
    res = nlu.w2v(['深度学习', '机器学习'])
    assert len(res) == 2
    assert len(res[0]) == 300
    res = nlu.w2v(['深度学习','机器学习'], type='tencent')
    assert len(res) == 2
    assert len(res[0]) == 200
    res = nlu.sim_words('深度学习', 10)
    assert len(res) == 10
    assert len(res[0]) == 2
    res = nlu.sim_words('深度学习', 10, type='tencent')
    assert len(res) == 10
    assert len(res[0]) == 2
    res = nlu.sim_words(['深度学习', '机器学习'], 10)
    assert len(res) == 2
    assert len(res[0]) == 10
    assert len(res[0][0]) == 2
    res = nlu.sim_words(['深度学习', '机器学习'], 10, type='tencent')
    assert len(res) == 2
    assert len(res[0]) == 10
    assert len(res[0][0]) == 2
    res = nlu.word_sim('深度学习', '机器学习', type='tencent')
    assert res > 0.5
    res = nlu.word_sim('深度学习', '机器学习')
    assert res > 0.5
    print("nlu.w2v OK")

    # 普通句向量
    res = nlu.s2v(['主要负责机器学习算法的研究', '训练模型、编写代码、以及其他一些工作', "", "我"])
    assert res['dimention'] == 300
    assert len(res['veclist']) == 4
    assert len(res['veclist'][0]) == 300
    assert sum(res['veclist'][2]) == 0.
    assert sum(res['veclist'][3]) != 0.

    res = nlu.s2v(['主要负责机器学习算法的研究', '训练模型、编写代码、以及其他一些工作', "", "我"], type='tencent')
    assert res['dimention'] == 200
    assert len(res['veclist']) == 4
    assert len(res['veclist'][0]) == 200

    # bert句向量 from bert-as-service
    res = nlu.bert_vec(['主要负责机器学习算法的研究', '训练模型、编写代码、以及其他一些工作'])
    assert res.shape == (2, 768)
    res = nlu.bert_vec(['主要负责机器学习算法的研究', '训练模型、编写代码、以及其他一些工作'], mode='cv')
    assert res.shape == (2, 768)
    print("nlu.bert_vec OK")

# sentence bert句向量及相似度
res = nlu.bert_encode(['主要负责机器学习算法的研究', '训练模型、编写代码、以及其他一些工作'])
assert len(res['vec']) == 2
assert len(res['vec'][0]) == 512
res = nlu.bert_encode(['训练模型、编写代码、以及其他一些工作'] * 400)
assert len(res['vec']) == 400
res = nlu.bert_encode("tencenthttp//keqqcom/course/276671")
assert len(res["vec"]) == 1
print("nlu.bert_encode OK")
res = nlu.bert_sim("句子通用向量表征", "自然语言处理是人工智能的明珠")
assert res["sim"] < 0.18
res = nlu.bert_sim("句子通用向量表征", ["自然语言处理是人工智能的明珠", "句子表征哪个模型厉害？"])
assert res["sim"][0][0] == "句子表征哪个模型厉害？"
res = nlu.bert_sim(["句子通用向量表征", "自然语言处理这几年发展很快"], ["自然语言处理是人工智能的明珠", "句子表征哪个模型厉害？"])
assert res["sim"][1][0] > 0.6
res = nlu.bert_encode(['主要负责机器学习算法的研究'] * 100)
assert len(res['vec']) == 100
print("nlu.bert_sim OK")

# 小样本多分类
corpus = "test/example.txt"
classifier = Classifier(corpus)
res = classifier.infer("我要上课", False)
assert res == "course"
res = classifier.infer("我要上课")
assert res[1] == "course"
res = classifier.infer(["我要上课", "我要学习"])
assert res[1][0] == "course" and res[1][1] == "drills"
cd = classifier.center_dict
classifier1 = Classifier(center_dict=cd)
res = classifier1.infer("我要上课", False)
assert res == "course"
res = classifier1.infer("我要上课")
assert res[1] == "course"
res = classifier1.infer(["我要上课", "我要学习"])
assert res[1][0] == "course" and res[1][1] == "drills"
print("classifier.infer OK")

# 文本聚类
result = [
    ['黑科技', '页面太丑', '你好'],
    ['给我推荐点课程', '有什么好的课程给我推荐一下', '我想上课', '推荐一些热门课程', '找一些关于会计的课给我'],
    ['我要陪练', '我要做练习', '我要练习话术', '做一下话术练习', '来几个知识点练习', '考察我几个知识点', '问我几个知识点', '模型训练不出来怎么办']]
clustered_sents = nlu.cluster("test/cluster_example.txt", 3)
assert len(clustered_sents) == 3
# result = [sorted(item) for item in result]
# clustered_sents = sorted(clustered_sents, key=lambda x: len(x))
# clustered_sents = [sorted(item) for item in clustered_sents]
# assert result == clustered_sents
print("nlu.cluster OK")

# nlu.bertmodels('wwm_ext', './bert_models')

# AI5组 实体服务
res = nlu.ner(["我毕业于北京大学"], 'ner')
assert res[0][0]['text'] == "北京大学"
print("nlu.entity OK")

# 情感分析
res = nlu.emotion(['这家公司很棒','这家公司很糟糕'])
assert res['labels'][0] == 'pos'
assert res['labels'][1] == 'neg'
res = nlu.emotion(['这家公司很棒','这家公司很糟糕'], prob=True)
assert res['labels'][0][0] == 'pos'
assert res['labels'][1][0] == 'neg'
assert res['labels'][0][1] == 0.88
assert res['labels'][1][1] == 0.82
print("nlu.emotion OK")

res = nlu.keywords(
    [
        "管理者情商提升基础认知",
        "究竟什么是情商？管理者为何要注重情商修炼？情商的修炼对于管理者的领导境界有什么提升和帮助？如何科学正确的认识情绪的产生、控制？职场人士面对高压正确的心态应该是什么"
    ], mode="ai4")
assert sorted(res["keywords"]) == sorted(["管理者情商", "领导", "科学"])
res = nlu.keywords(
    [
        "主要负责机器学习算法的研究以及搭建神经网络，训练模型，编写代码，以及其他的一些工作",
        "主要负责机器学习算法的研究以及搭建神经网络，训练模型，编写代码，以及其他的一些工作"
    ], 2, True, "ai4")
assert sorted(res["keywords"]) == sorted(["模型", "机器学习算法"])
assert len(res["weights"]) == 2
print("nlu.keywords_ai4 OK")

if nlu.env != "dev":
    # 关键词
    res = nlu.keywords('主要负责机器学习算法的研究以及搭建神经网络，训练模型，编写代码，以及其他的一些工作', 4, True)
    assert len(res['keywords']) == 4
    assert len(res['weights']) == 4
    res = nlu.keywords('主要负责机器学习算法的研究以及搭建神经网络，训练模型，编写代码，以及其他的一些工作', 4)
    assert len(res['keywords']) == 4
    assert len(res['weights']) == 0
    res = nlu.keywords('主要负责机器学习算法的研究以及搭建神经网络，训练模型，编写代码，以及其他的一些工作')
    assert len(res['keywords']) == 3
    assert len(res['weights']) == 0
    print("nlu.keywords OK")

    # 句子相似度
    res = nlu.sent_sim('你家的地址是多少', '你住哪里', 1000)
    assert res['result'] > 500
    res = nlu.sent_sim('你家的地址是多少', '', 1000, type="tencent")
    assert res['result'] == 0
    print("nlu.sent_sim OK")

    # 动宾提取
    res = nlu.vob('要负责机器学习算法的研究以及搭建神经网络，训练模型，编写代码，以及其他的一些工作')
    assert len(res) > 0
    print("nlu.vob OK")

# 句子合理性
res = nlu.rationality(['床前明月光，疑是地上霜', '床前星星光，疑是地上霜', '床前白月光，疑是地上霜'])
assert len(res['ppl']) == 3
print("nlu.rationality OK")

# AI2组 姓名识别
res = nlu.name_ner("刘德华的⽼老老婆叫叶丽倩")
assert len(res) == 2
print("nlu.name_ner OK")
