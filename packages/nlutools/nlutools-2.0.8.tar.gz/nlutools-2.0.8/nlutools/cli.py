import argparse
import os
import sys

from nlutools import NLU

base_dir = os.path.dirname(__file__)
NLUTOOLS_VERSION = open(f"{base_dir}/config/version.txt").read().strip()
nlu = NLU(verbose=False)

def main():
    arg_parser = argparse.ArgumentParser(description='HanLP: Han Language Processing v{}'.format(NLUTOOLS_VERSION))
    arg_parser.add_argument('-v', '--version', required=False, action='store_true',
                            help='show installed versions of NLUTools')
    task_parser = arg_parser.add_subparsers(dest='task', help='which task to perform?')
    preprocess_parser = task_parser.add_parser(name='clean', help='text preprocessing')
    segment_parser = task_parser.add_parser(name='cut', help='word segmentation')
    sentence_spliter_parser = task_parser.add_parser(name='split', help='sentence segmentation')
    sentiment_parser = task_parser.add_parser(name='emotion', help='sentence emotion predcition')
    keyword_parser = task_parser.add_parser(name='keywords', help='keyword extraction')
    keyword_parser.add_argument('-m', '--mode', type=str, default='default',
                                help='name of method e.g. ai4')
    sentence_sim_parser = task_parser.add_parser(name='sent_sim', help='sentence text similarity')
    sentence_sim_parser.add_argument('-m', '--mode', type=str, default='bert',
                                     help='name of method e.g. bert, ifchange, tencent')
    word_sim_parser = task_parser.add_parser(name='word_sim', help='word similarity')
    word_sim_parser.add_argument('-m', '--mode', type=str, default='ifchange',
                                  help='name of method e.g. ifchange, tencent')
    rationality_parser = task_parser.add_parser(name='rationality', help='sentence rationality score')

    if '-v' in sys.argv or '--version' in sys.argv:
        print(f"NLUTOOLS version: {NLUTOOLS_VERSION}")
        exit(0)
    
    args = arg_parser.parse_args()

    def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    def die(msg):
        eprint(msg)
        exit(1)

    if args.task == 'clean':
        print("请键入文本")
        for line in sys.stdin:
            line = line.strip()
            print(nlu.clean(line))
    if args.task == 'cut':
        print("请键入文本")
        for line in sys.stdin:
            line = line.strip()
            print(nlu.cut(line))
    elif args.task == 'split':
        print("请键入文本")
        for line in sys.stdin:
            line = line.strip()
            print(nlu.split(line)[0])
    elif args.task == 'emotion':
        print("请键入文本")
        for line in sys.stdin:
            line = [line.strip()]
            print(nlu.emotion(line, True)["labels"][0])
    elif args.task == 'keywords':
        print("请键入文本")
        for line in sys.stdin:
            line = line.strip()
            print(nlu.keywords(line, with_weight=True, mode=args.mode))
    elif args.task == 'sent_sim':
        print("请键入文本，空格分割")
        for line in sys.stdin:
            sent1, sent2 = line.strip().split()
            if args.mode in ["ifchange", "tencent"]:
                score = nlu.sent_sim(sent1, sent2, type=args.mode)["result"] / 100
            elif args.mode == "bert":
                score = round(nlu.bert_sim(sent1, sent2)["sim"], 2)
            print(score)
    elif args.task == 'word_sim':
        print("请键入文本，空格分割")
        for line in sys.stdin:
            word1, word2 = line.strip().split()
            score = round(nlu.word_sim(word1, word2, type=args.mode), 2)
            print(score)
    elif args.task == 'rationality':
        print("请键入文本")
        for line in sys.stdin:
            line = line.strip()
            print(nlu.rationality([line])["ppl"][0])


if __name__ == '__main__':
    main()
