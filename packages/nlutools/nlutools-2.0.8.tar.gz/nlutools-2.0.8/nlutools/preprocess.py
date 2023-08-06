import html
import re

URL_REGEX = re.compile(
    r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
    re.IGNORECASE)
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

def clean_text(text, remove_url=True, email=True, weibo_at=True, weibo_topic=False,
               remove_rare_char=True, emoji=True, norm_html=False, remove_punc=False,
               q2b=False):
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
    text = "回复@钱旭明QXM:[嘻嘻][嘻嘻] //@钱旭明QXM:杨大哥[good][good]"
    print(clean_text(text))
    text = "【#赵薇#：正筹备下一部电影 但不是青春片....http://t.cn/8FLopdQ"
    print(clean_text(text, weibo_topic=True))
    text = "&lt;a c&gt;&nbsp;&#x27;&#x27;"
    print(clean_text(text, norm_html=True))
    text = "×～~"
    print(clean_text(text, q2b=True, remove_rare_char=True))
