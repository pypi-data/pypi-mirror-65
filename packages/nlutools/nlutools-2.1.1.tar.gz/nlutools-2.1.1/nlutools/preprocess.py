# -*- coding: utf-8 -*-

import html
import re

URL_REGEX = re.compile(
    r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>\u4e00-\u9fa5]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’]))',
    re.IGNORECASE)

# URL_REGEX = re.compile(
#     r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4})(?:((/[a-zA-Z0-9\-_]+)|(\.html?)))*(?:\?[a-zA-Z0-9]+=[0-9a-zA-Z]+&?)*)')

EMAIL_REGEX = re.compile(r"[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}", re.IGNORECASE)
WEIBO_REGEX = re.compile(r"(回复)?(//)?\s*@\S*?\s*(:|：| |$)")
PUNC_REGEX = re.compile(r"[，\_《。》、？；：‘’＂“”【「】」、·！@￥…（）—\,\<\.\>\/\?\;\:\'\"\[\]\{\}\~\`\!\@\#$\%\^\&\*\(\)\-\=\+]")

def strQ2B(ustring):
    """把字符串全角转半角"""
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
                inside_code -= 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)

def clear_rare_char(input_char):
    if u'\u4e00' <= input_char <=u'\u9fa5' \
        or re.search(PUNC_REGEX, input_char) \
        or u'\u0030' <= input_char <= u'\u0039' \
        or u'\u0041' <= input_char <= u'\u005A' \
        or u'\u0061' <= input_char <= u'\u007A':
        return input_char
    return ''

#TODO: 去除连续相同字符
def clean_text(text, remove_url=True, email=True, weibo_at=True, weibo_topic=False,
               remove_rare_char=True, emoji=True, norm_html=True, remove_punc=False,
               q2b=False, remove_dup=False):
    if remove_dup:
        text = re.sub(r"([^\u4e00-\u9fa5a-zA-Z0-9])\1{3,}", r"\1", text)
    if remove_url:
        text = re.sub(URL_REGEX, "", text)
    if email:
        text = re.sub(EMAIL_REGEX, "", text)
    if weibo_at:
        text = re.sub(WEIBO_REGEX, "", text)
    if weibo_topic:
        text = re.sub(r"#\S+#[：]?", "", text)
    if emoji:
        text = re.sub(r"\[\S+\]", "", text)
    if norm_html:
        text = html.unescape(text)
    if remove_punc:
        text = re.sub(PUNC_REGEX, "", text)
    if q2b:
        text = strQ2B(text)
    if remove_rare_char:
        new_text = ""
        for char in text:
            new_text += clear_rare_char(char)
        text = new_text
    text = re.sub(r"\s+", " ", text)
    return text.strip()

if __name__ == "__main__":
    from linetimer import CodeTimer

    with CodeTimer("weibo_at & emoji"):
        text = "回复@钱旭明QXM:[嘻嘻][嘻嘻] //@钱旭明QXM:杨大哥[good][good]"
        print(clean_text(text))
    with CodeTimer("weibo_topic & url"):
        text = "【#赵薇#：正筹备下一部电影 但不是青春片....http://t.cn/8FLopdQ http://www.google.com"
        print(clean_text(text, weibo_topic=True))
    text = "&lt;a c&gt;&nbsp;&#x27;&#x27;"
    print(clean_text(text, norm_html=True))
    with CodeTimer("rara_char & q2b"):
        text = "×～~"
        print(clean_text(text, q2b=True, remove_rare_char=True))

    text = "http://study.163.com/course/courseMain.htm?courseId=1459037"
    print(clean_text(text))
    with CodeTimer("long text with url"):
        text = "150集链接：http://study.163.com/course/courseMain.htm?courseId=1459037 全套150集,分初中级:循序渐进(完结)学习目的：为了让自己更有料些,不求于他人,就是这么简单.学习内容：根据实际案例进行解说,直击效果,要的也是这么简单.学习对象：1.从零开始学习透视表。2.需要交互式的汇报人员。---------------------------------------------数据汇总再也不求人了,全网易最全的EXCEL透视表学习对象!简单的,基础的,中级的,深入的基本上都涉及到.基础:从插入到设计选项卡,从排序到组合,从样式到打印,从动态到计算项,全部呈现出来.使用实操深入解析各项功能性的使用.中级:从动态源头切片器到图表,从导入外部数据到PowerPivot及view,从SQL到MicrosoftQuery,展示了它的更高级功能.产出:以案例最终呈现出大家经常看到的一页纸Dashboard的报告呈现,这应该都是学友需要看到的成品效果.------------------(其它章节连接地址:http://study.163.com/u/eeshang)"
        print(clean_text(text))
    text = "链接：https://study.163.com/series/1202823601.htm?courseId=1209142817&share=2&shareId=1025355187购买本套视频教程，送【18G精品素材库】"
    print(clean_text(text))