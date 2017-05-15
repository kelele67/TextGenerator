# -*- coding:utf-8 -*-

'''
This is a Markovgen Text Generator.

The Markovgen class takes a input text to generate output text from  
the default length of the output is 100, but it can be what you enter, 
the default ngram is 3 but it also rely on what you enter

The Generator also sweep the needless symbol, 
upper the first word and add end symbol to make output text looks better
'''

from collections import defaultdict
from random import choice, randint
import re
import string


class Markovgen(object):

    def __init__(self, open_file):
        self.open_file = open(open_file)
        self.text = self.open_file.read()
        self.words = self.text.split()

    def make_ngrams(self, ngram, text_list):
        # 把连续的n个词放进list中make ngram
        # put ngram continuous words into list to make ngram
        for x in range(len(text_list) - ngram):
            yield [text_list[x + i] for i in range(ngram)]

    def make_dict(self, ngram, text_list = None):
        # 对每一个ngram，前ngram - 1个词作为key，最后的作为value
        # for each ngram , the first ngram - 1 word as key, the last one as value
        if text_list is None:
            text_list = self.words

        word_dict = defaultdict(list)
        for wordlist in self.make_ngrams(ngram, text_list):
            last_word = wordlist.pop()
            word_dict[tuple(wordlist)].append(last_word)

        return word_dict

    # sweep多余的符号 “, ”, ``, '', lonely', overspace, tab
    # sweep the needless symbol to make text looks better
    def sweep_qutotes(self, text):
        return re.sub(r"“|”|``|''|\W'", r"", text)

    def sweep_space(self, text):
        return re.sub(r"\s+|\t", r" ", text)

    def sweep_finished(self, text):
        return self.sweep_qutotes(self.sweep_space(text))

    def generate_result(self, length = 100, ngram = 3):
        # 生成结果
        # generate the result
        word_dict = self.make_dict(ngram)

        seed_no = randint(0, len(self.words) - ngram)
        result = [self.words[seed_no + i] for i in range(ngram - 1)]
        for x in range(ngram - 1, length):
            next_word = tuple(result[-(ngram - 1):])
            result.append(choice(word_dict[next_word]))

        result = ' '.join(result)

        # Upper the first word
        result = result[0].capitalize() + result[1:]

        # add end symbol
        end_symbol = [".", "?", "!"]
        if result[-2] in string.punctuation and result[-2] not in end_symbol:
            result = result[:-2] + end_symbol[randint(0, 2)]
        else:
            result += end_symbol[randint(0, 2)]

        return self.sweep_finished(result)


if __name__ == "__main__":
    length = raw_input("Enter the result length：")
    ngram = raw_input("Enter the ngram：")
    m = Markovgen('input.txt')
    text = m.generate_result(int(length), int(ngram))
    f = open("output.txt", 'w+')
    f.write(text)
    f.close()
