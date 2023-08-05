import os
import re
import subprocess
from collections import defaultdict

import numpy as np
from scipy.spatial.distance import cosine
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances
from tqdm import tqdm

from nlutools.config import mapConf, supportConf, bertModelConf
from nlutools.config import getEnvLabel, getLocalIp
from nlutools.online_bert_client import bert_vector
from nlutools.rpc_client import doTask, doCustomTask, doNameEntity
from nlutools.utils import raiseException


def divide_chunks(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]

class Classifier(object):
    def __init__(self, corpus_path="", center_dict={}, env="", dim=512):
        self.nlu = NLU(env)
        self.dim = dim
        self.class_dict = defaultdict(list)
        self.corpus = corpus_path
        if not corpus_path and not center_dict:
            print("Init fail! Please pass in `corpus_path` or `center_dict`")
        else:
            if center_dict:
                self.center_dict = center_dict
                self._build_centers(False)
            else:
                self.center_dict = {}
                print("Building model, please wait...")
                self._build_centers(True)

    def normalize(self, v):
        norm = np.linalg.norm(v)
        if norm == 0: 
            return v
        return v / norm

    def _build_centers(self, build=False):
        if build:
            with open(self.corpus, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                lines = [x.strip().split('\t') for x in lines]
                for line in lines:
                    self.class_dict[line[1]].append(line[0])
                for k, v in self.class_dict.items():
                    embs = np.asarray(self._get_embs(v))
                    center = np.mean(embs, axis=0).squeeze()
                    self.center_dict[k] = center
        tps = list(self.center_dict.items())
        self.centers = [x[1] for x in tps]
        self.classes = [x[0] for x in tps]

    def infer_by_input(self):
        while True:
            sent = input("enter a sentence: ")
            res, pclass = self.infer(sent)
            print(res)
            print("predicted class: {}".format(pclass))

    def infer(self, sent, show_dist=True):
        if isinstance(sent, str):
            results, preds = self._pred_class(sent)
        elif isinstance(sent, list):
            if len(sent) > 1:
                results, preds = self.infer_sents(sent)
            else:
                results, preds = self._pred_class(sent)
        else:
            results = None
            preds = None
            print("Only support `str` and `list` input type")
        if show_dist:
            return results, preds
        else:
            return preds

    def infer_sents(self, sents):
        embs = self._get_embs(sents)
        dists = np.asarray(pairwise_distances(embs, self.centers, metric='cosine'))
        preds = np.argmin(dists, axis=-1).squeeze()
        preds = [self.classes[x] for x in preds]
        results = [list(zip(self.classes, dist)) for dist in dists]
        return results, preds

    def _get_embs(self, sent):
        return self.nlu.bert_encode(sent, False)['vec']

    def _pred_class(self, sent):
        emb = self._get_embs(sent)
        dists = [cosine(emb, center) for center in self.centers]
        maxind = np.argmin(dists)
        results = list(zip(self.classes, dists))
        return results, self.classes[maxind]


class NLU(object):
    def __init__(self, env="", timeout=3):
        self.host_ip = getLocalIp()
        if self.host_ip.startswith("172"):
            if not env:
                print("You are in docker container.")
                print("Please set env variable: dev, online_stable, online_dev, test")
                print("Example：nlu = NLU('dev')")
        else:
            if not env:
                env = getEnvLabel(self.host_ip)
        self.env = env
        self.timeout = timeout

        self.base_dir = os.path.dirname(__file__)
        self.stopwords = [word.strip() for word in open(self.base_dir + "/config/stop_words.txt")]

        print("Current Environment: %s" % self.env)

    def raise_exception(self, e, server_name):
        raiseException('%s exception \nplease contact supporter %s for this exception ! \n%s' % (server_name, supportConf[server_name], e))

    def cut(self, sentence, pos=True, cut_all=False, mode='fast'):
        """名词短语分词"""
        server_name = 'segmentor'
        try:
            if mode in ['fast', 'accurate']:
                if isinstance(pos, bool) and isinstance(cut_all, bool):
                    if sentence == "":
                        res = {"text":"", "items":[], "pos":[], "np":[], "entity":[]}
                    else:
                        data = {'text':sentence, 'mode':mode, 'pos':pos, 'cut_all':cut_all}
                        res = doTask(self.env, server_name, data, self.timeout)
                    return res
                else:
                    return "Please assign boolean value for variables `pos` and `cut_all`"
            else:
                raiseException('Advise: check parameters, make sure value of mode is fast or default, value of pos is true, false or default as well')
        except Exception as e:
            self.raise_exception(server_name, e)

    def getKeywords(self, content, topk, with_weight):
        """关键词抽取"""
        server_name = 'keywords'
        try:
            data = {'content':content, 'topk':topk, 'with_weight':with_weight}
            return doTask(self.env, server_name, data, self.timeout)
        except Exception as e:
            self.raise_exception(server_name, e)
    
    def getKeywordsAI4(self, content, topk, with_weight):
        """ai4组的关键词抽取服务"""
        server_name = "keywords_ai4"
        try:
            if isinstance(content, str):
                content = [content, content]
            data = {"header":[], "request": {"c":0, "m":"", "p":{"corpus":content, "domain":[], "do_weighting":int(with_weight)}}}
            response = doTask(self.env, server_name, data, self.timeout)["response"]
            result = response["results"]
            if result:
                if with_weight:
                    result = sorted(result, key=lambda x: (-x[1], -len(x[0])))
                    keywords, weights = list(zip(*[item for item in result[:topk]]))
                    result = {"keywords": list(keywords), "weights": list(weights)}
                else:
                    result = {"keywords": [item for item in result[:topk]], "weights": []}
            else:
                print(response["err_msg"])
                result = None
            return result
        except Exception as e:
            self.raise_exception(server_name, e)

    def keywords(self, content, topk=3, with_weight=False, mode="default"):
        if mode == "default":
            return self.getKeywords(content, topk, with_weight)
        elif mode == "ai4":
            return self.getKeywordsAI4(content, topk, with_weight)

    def getSubSentences(self, sentence, cut_comma=False, cut_all=False):
        """规则切句"""
        server_name = 'sentence_spliter'
        try:
            data = {'sentence':sentence, 'mode': 0}
            sub_sents = doTask(self.env, server_name, data, self.timeout)
            if cut_comma:
                new_sub_sents = []
                for sent in sub_sents:
                    for s in sent:
                        new_s = []
                        new_subs = re.split(r",|，", s)
                        ss = []
                        for i in range(len(new_subs)):
                            current_sent = new_subs[i]
                            if len(current_sent) < 8:
                                if i == len(new_subs) - 1:
                                    new_s.append(current_sent)
                                else:
                                    ss.append(current_sent)
                            else:
                                new_s.append(current_sent)
                                ss = []
                            if len(ss) > 2:
                                new_s.append("，".join(ss))
                                ss = []
                    new_sub_sents.append(new_s)
                return new_sub_sents
            if cut_all:
                sub_sents = [[ss for s in sent for ss in re.split(r",|，", s)] for sent in sub_sents]
            return sub_sents
        except Exception as e:
            self.raise_exception(server_name, e)

    def split(self, sentence, cut_comma=False, cut_all=False):
        return self.getSubSentences(sentence, cut_comma, cut_all)

    def getW2VFile(self, version_key, localpath):
        """获取词向量文件"""
        server_name = 'w2v'
        version_key = version_key.strip()
        try:
            assert self.env.startswith("online")
        except AssertionError as e:
            raise Exception("only support for online_* env")
        try:
            if not version_key:
                cat = subprocess.Popen(['hadoop', 'fs', '-cat', mapConf['w2v_hdfs_version_file']], stdout=subprocess.PIPE)
                for line in cat.stdout:
                    version_key = bytes.decode(line).strip()
                    break
            if version_key and version_key:
                try:
                    subprocess.call(['hadoop','fs','-get', mapConf['w2v_hdfs_dir'] + version_key.lower(), localpath])
                except Exception as e:
                    self.raise_exception(server_name, e)
        except Exception as e:
            raise Exception('Advise: please install hadoop client before use getW2VFile')
    
    def getWordVec(self, word, type_='ifchange'):
        """获取词向量表征"""
        server_name = 'w2v'
        try:
            if isinstance(word, str):
                word = [word]
            data = {'words':word, 'type':type_}
            return doTask(self.env, server_name, data, self.timeout)
        except Exception as e:
            self.raise_exception(e, server_name)
    
    def getCharacterVec(self, char):
        raise NotImplementedError

    def w2v(self, word, type='ifchange'):
        return self.getWordVec(word, type)

    def getWordSimScore(self, word1, word2, type_='ifchange'):
        """词向量相似度计算"""
        server_name = 'w2v'
        try:
            data = {'word1':word1, 'word2':word2, 'type':type_}
            return float(doTask(self.env, server_name, data))
        except Exception as e:
            self.raise_exception(e, server_name)

    def word_sim(self, word1, word2, type='ifchange'):
        return self.getWordSimScore(word1, word2, type)

    def getMostSimWords(self, word, topn=10, type_='ifchange'):
        """相似词"""
        server_name='w2v'
        try:
            data = {'words':word, 'topn':topn, 'type':type_}
            return doTask(self.env, server_name, data, self.timeout)
        except Exception as e:
            self.raise_exception(e, server_name)

    def sim_words(self, word, topn=10, type='ifchange'):
        return self.getMostSimWords(word, topn, type)

    def getSentenceVec(self, sentences, type_='ifchange'):
        """基于TF—IDF的句向量表征"""
        server_name = 'sentencevec'
        try:
            if isinstance(sentences, str):
                sentences = [sentences]
            data = {'senlist':sentences, 'type':type_}
            return doTask(self.env, server_name, data, self.timeout)
        except Exception as e:
            self.raise_exception(e, server_name)

    def s2v(self, sentences, type='ifchange'):
        return self.getSentenceVec(sentences, type)

    def getSentenceSim(self, text1, text2, precision=100, type_='ifchange'):
        """句子相似度计算"""
        server_name = 'sentencesim'
        try:
            data = {'text1':text1, 'text2':text2, 'precision':precision, 'type':type_}
            return doTask(self.env, server_name, data, self.timeout)
        except Exception as e:
            self.raise_exception(e, server_name)

    def sent_sim(self, text1, text2, precision=100, type='ifchange'):
        return self.getSentenceSim(text1, text2, precision, type)

    def getBertSentenceVec(self, texts, mode='wwm_ext'):
        """基于bert-as-service的bert句向量服务"""
        server_name = 'bert_service'
        try:
            bertVector = bert_vector()
            result = bertVector.parse(texts, mode)
            bertVector.close(mode)
            return result
        except Exception as e:
            self.raise_exception(e, server_name)

    def bert_vec(self, texts, mode='wwm_ext'):
        return self.getBertSentenceVec(texts, mode)

    def getSentenceBertVec(self, text_a, text_b=[], metric="cosine"):
        """Sentence-BERT句向量及相似度计算"""
        server_name = 'sentence_bert'
        try:
            if not isinstance(text_a, list):
                text_a = [text_a]
            if not text_b:
                text_a = divide_chunks(text_a, 32)
                vecs = []
                if len(text_a) > 10:
                    text_a = tqdm(text_a)
                for text in text_a:
                    data = {"text_a": text, "text_b": text_b, "metric": metric}
                    vecs.extend(doTask(self.env, server_name, data)["vec"])
                return {"dim": 512, "msg": "Return %s vectors with dim 512" % len(vecs), "vec": vecs}
            else:
                data = {"text_a": text_a, "text_b": text_b, "metric": metric}
                result = doTask(self.env, server_name, data, self.timeout)
            return result
        except Exception as e:
            self.raise_exception(e, server_name)

    def bert_encode(self, text_a, verbose=True):
        if verbose:
            print("Encoding...")
        return self.getSentenceBertVec(text_a)

    def bert_sim(self, text_a, text_b, metric="cosine"):
        return self.getSentenceBertVec(text_a, text_b, metric)

    def cluster(self, corpus, num_clusters=5, method="bert"):
        if method != "bert":
            print("Sorry! Only supports `bert` method now")
            return None
        else:
            if isinstance(corpus, str):
                corpus = [line.strip() for line in open(corpus, encoding="utf8")]
            if num_clusters > len(corpus):
                print("[error] corpus size must be greater then `num_clusers`")
                return None
            corpus_embeddings = self.bert_encode(corpus)["vec"]
            clustering_model = KMeans(n_clusters=num_clusters)
            print("Model is training...")
            clustering_model.fit(corpus_embeddings)
            cluster_assignment = clustering_model.labels_
            clustered_sentences = [[] for i in range(num_clusters)]
            for sentence_id, cluster_id in enumerate(cluster_assignment):
                clustered_sentences[cluster_id].append(corpus[sentence_id])
            return clustered_sentences

    def predictEmotion(self, sentences, prob=False):
        """BERT情感模型"""
        server_name = 'sentiment'
        try:
            if sentences:
                data = {'text':sentences, 'prob':prob}
                res = doTask(self.env, server_name, data, self.timeout)
                if prob:
                    newlabel = []
                    for l in res['labels']:
                        label, score = l.split('_')
                        score = round(float(int(score[:-1]) / 100), 2)
                        newlabel.append((label, score))
                    res['labels'] = newlabel
                    return res
                else:
                    return res
            return None
        except Exception as e:
            self.raise_exception(e, server_name)

    def emotion(self, sentences, prob=False):
        return self.predictEmotion(sentences, prob)

    def getBertModels(self, model_name, output_dir=None):
        """下载BERT模型"""
        server_name = "bert_service"
        try:
            model_dir = bertModelConf.get(model_name)
            if not model_dir:
                print('Please check pass in valid model_name')
                print('Following models are available:')
                print('base_cn, wwm, wwm_ext, ernie_cv')
            else:
                print('Model Dir: ', model_dir)
                if output_dir:
                    os.system('mkdir -p %s' % output_dir)
                    ret = os.system('hadoop fs -get %s %s' % (model_dir, output_dir))
                    if ret:
                        print('Download succeed!')
                    else:
                        print('Please check whether model exists and concat %s' % supportConf['bert_service'])
        except Exception as e:
            self.raise_exception(e, server_name)

    def bert_models(self, model_name, output_dir=None):
        self.getBertModels(model_name, output_dir)

    def getVOB(self, content, mode='fast'):
        """动宾提取"""
        server_name = 'verbobject'
        try:
            data = {'content':content, 'mode':mode}
            return doTask(self.env, server_name, data, self.timeout)
        except Exception as e:
            self.raise_exception(e, server_name)
    def vob(self, content, mode='fast'):
        return self.getVOB(content, mode)

    def getSentenceRationality(self, text, with_word_prob=False):
        server_name = 'rationality'
        """BERT句子合理性"""
        try:
            data = {'text':text, 'word_prob':with_word_prob}
            return doTask(self.env, server_name, data, self.timeout)
        except Exception as e:
            self.raise_exception(e, server_name)

    def rationality(self, text, with_word_prob=False):
        return self.getSentenceRationality(text, with_word_prob)

    def doEntityTask(self, text, m):
        """AI5组实体服务"""
        server_name = 'entity'
        try:
            return doCustomTask(self.env, server_name, text, m, self.timeout)
        except Exception as e:
            self.raise_exception(e, server_name)

    def ner(self, text, m):
        return self.doEntityTask(text, m)

    def name_ner(self, text):
        """AI2组姓名识别服务"""
        return doNameEntity(self.env, text, self.timeout)
