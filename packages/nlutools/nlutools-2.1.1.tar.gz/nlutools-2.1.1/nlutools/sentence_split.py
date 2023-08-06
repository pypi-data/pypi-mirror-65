import re

START_PATTERN = [
    r'\* ',
    r'\d{1,2}\.\d{1,2}\.\d{1,2}',  # 1.2.1
    r'\d+\t',
    r'(?<![:])[1-9]?[0-9][；:、\.\t/]{1}\s?(?![年月日\d+])',
    r'[1-9]?[0-9][)）]{1}、?',
    r'\n[1-9][0-9]',
    r'(?<![A-Za-z0-9/])[A-Za-z]{1}\s?[、\.\)、\t]{1}',
    r'\(1?[1-9]\)',
    r'(?<!周)第?[一二三四五六七八九十]+[、\)\.) \t]{1}',
    r'\([一二三四五六七八九十]+\)\.?',
    r'[①②③④⑤⑥⑦⑧⑨⑩]+'
]
START_PATTERN = re.compile(r'(' + '|'.join(START_PATTERN) + ')+', re.UNICODE)  # 项目序号
END_PATTERN = r'([。！!﹗？\?])([^"”‘\'])'  # 单字符断句符
EN_ELLIPSIS = r'(\.{6})([^"”‘\'])'  # 英文省略号
CN_ELLIPSIS = r'(\…{2})([^"”‘\'])'  # 中文省略号
QUOTE = r'([。！？\?][”’])([^，。！？\?])'  # 双引号内有终止符，引号为句子终点

def split_text(sentence, bullet=True, cut_comma=False, cut_all=False):
    sentence = re.sub(END_PATTERN, r'\1\n\2', sentence)
    sentence = re.sub(EN_ELLIPSIS, r'\1\n\2', sentence)
    sentence = re.sub(CN_ELLIPSIS, r'\1\n\2', sentence)
    sentence = re.sub(QUOTE, r'\1\n\2', sentence)
    if bullet:
        sentence = re.sub(r'(?<=[\u4e00-\u9fa5a-z])(\.)(?=[\u4e00-\u9fa5a-z])', r'\1\n', sentence)
        sentence = re.sub(START_PATTERN, r'\n\1', sentence)
    sentence = re.sub(r'(?<=\n)(\s+)(?=\n)', '', sentence)
    sentence = re.sub(r'\n{2,}|\\n', '\n', sentence)
    sub_sents = [sub.strip() for sub in sentence.split("\n")]
    sub_sents = list(filter(lambda x: len(x) > 1, sub_sents))
    if cut_comma:
        new_sub_sents = []
        for sent in sub_sents:
            new_subs = re.split(r",|，", sent)
            ss = []
            for i in range(len(new_subs)):
                current_sent = new_subs[i]
                if len(current_sent) < 8:
                    if i == len(new_subs) - 1:
                        new_sub_sents.append(current_sent)
                    else:
                        ss.append(current_sent)
                else:
                    new_sub_sents.append(current_sent)
                    ss = []
                if len(ss) > 2:
                    new_sub_sents.append("，".join(ss))
                    ss = []
        sub_sents = new_sub_sents
    if cut_all:
        sub_sents = [ss for sent in sub_sents for ss in re.split(r",|，", sent)]
    return sub_sents

if __name__ == "__main__":
    from linetimer import CodeTimer

    t = "哈哈哈, 你好呀，嘿嘿哈哈哈哈，诶诶阿法！"
    with CodeTimer("cut_comma"):
        print(split_text(t, cut_comma=True))
    with CodeTimer("cut_all"):
        print(split_text(t, cut_all=True))
    with CodeTimer("default"):
        print(split_text(t))
    t = "150集链接：全套150集,分初中级:循序渐进(完结)学习目的：为了让自己更有料些,不求于他人,就是这么简单.学习内容：根据实际案例进行解说,直击效果,要的也是这么简单.学习对象：1.从零开始学习透视表。2.需要交互式的汇报人员。---------------------------------------------数据汇总再也不求人了,全网易最全的EXCEL透视表学习对象!简单的,基础的,中级的,深入的基本上都涉及到.基础:从插入到设计选项卡,从排序到组合,从样式到打印,从动态到计算项,全部呈现出来.使用实操深入解析各项功能性的使用.中级:从动态源头切片器到图表,从导入外部数据到PowerPivot及view,从SQL到MicrosoftQuery,展示了它的更高级功能.产出:以案例最终呈现出大家经常看到的一页纸Dashboard的报告呈现,这应该都是学友需要看到的成品效果.------------------(其它章节连接地址:)"
    with CodeTimer("long_text"):
        print(split_text(t))