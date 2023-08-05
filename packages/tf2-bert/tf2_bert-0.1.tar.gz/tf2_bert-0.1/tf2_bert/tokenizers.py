#! -*- coding: utf-8 -*-
# 工具函数

import unicodedata, re

# 从bert的词典文件中读取词典
# dict_path字典文件路径
# simplified=True，精简字符集，也就是使用更少的字符
# startwith可以传入一个字符列表，表示以那些字符作为精简字符集的开头，例如：
# startwith=['[PAD]', '[UNK]', '[CLS]', '[SEP]', '[MASK]']
def load_vocab(dict_path, encoding='utf-8', simplified=False, startwith=None):
    # 定义字典
    token_dict = {}
    with open(dict_path, encoding=encoding) as reader:
        # 循环每一行
        for line in reader:
            # 去掉字符串头尾空白字符
            token = line.strip()
            # 字符串存入字典
            token_dict[token] = len(token_dict)
    # 如果要使用精简字符集
    if simplified:  
        # new_token_dict精简字符集新字典，字符作为键，字符对应编号作为值
        # keep_tokens精简字符集在原字符集中的编号列表
        # 比如原字符集有10个字符，keep_tokens=[1,3,5,7]，表示精简字符集只保留原字符集的1,3,5,7号字符
        new_token_dict, keep_tokens = {}, []
        # 精简字符集开头的一些字符
        startwith = startwith or []
        for t in startwith:
            # 加入字典中
            new_token_dict[t] = len(new_token_dict)
            # keep_tokens记录编号
            keep_tokens.append(token_dict[t])

        # 筛选精简字符集的内容
        # 循环原字符集
        for t, _ in sorted(token_dict.items(), key=lambda s: s[1]):
            # 如果这个字符不在new_token_dict中
            if t not in new_token_dict:
                keep = True
                if len(t) > 1:
                    # 去掉字符串的##符号
                    for c in (t[2:] if t[:2] == '##' else t):
                        # 如果是cjk类字符或标点符号类字符则舍弃
                        if (Tokenizer._is_cjk_character(c)
                                or Tokenizer._is_punctuation(c)):
                            keep = False
                            break
                # 存入字典
                if keep:
                    # 加入字典中
                    new_token_dict[t] = len(new_token_dict)
                    # keep_tokens记录编号
                    keep_tokens.append(token_dict[t])
        # 返回新的精简字典和精简字符集在原字符集中的编号列表
        return new_token_dict, keep_tokens
    else:
        return token_dict

# [CLS]表示句子的开始
# [SEP]表示句子的结束
class BasicTokenizer(object):
    """分词器基类
    """
    def __init__(self,
                 token_start='[CLS]',
                 token_end='[SEP]',
                 do_lower_case=False):
        """初始化
        """
        self._token_pad = '[PAD]'
        self._token_unk = '[UNK]'
        self._token_mask = '[MASK]'
        self._token_start = token_start
        self._token_end = token_end
        self._do_lower_case = do_lower_case
        self._token_pad_id = 0

    # 分词函数
    def tokenize(self, text, max_length=None):
        if self._do_lower_case:
            # 将Unicode文本标准化
            text = unicodedata.normalize('NFD', text)
            text = ''.join(
                [ch for ch in text if unicodedata.category(ch) != 'Mn'])
            text = text.lower()
        # 分词
        tokens = self._tokenize(text)
        if self._token_start is not None:
            # 在第0个位置插入开始字符
            tokens.insert(0, self._token_start)
        if self._token_end is not None:
            # 在最后一个位置插入结束字符
            tokens.append(self._token_end)
        # 如果设置最大长度，超过的部分会截断
        if max_length is not None:
            self.truncate_sequence(max_length, tokens, None, -2)

        return tokens

    # token转换为对应的id
    def token_to_id(self, token):
        raise NotImplementedError

    # token序列转换为对应的id序列
    def tokens_to_ids(self, tokens):
        return [self.token_to_id(token) for token in tokens]

    # 截断总长度
    def truncate_sequence(self,
                          max_length,
                          first_sequence,
                          second_sequence=None,
                          pop_index=-1):
        if second_sequence is None:
            second_sequence = []

        # 截断总长度
        while True:
            # 计算总句子长度
            total_length = len(first_sequence) + len(second_sequence)
            # 小于max_length直接结束
            if total_length <= max_length:
                break
            # 大于max_length不断减少句子长度
            elif len(first_sequence) > len(second_sequence):
                first_sequence.pop(pop_index)
            else:
                second_sequence.pop(pop_index)

    # 字符串变成编码
    def encode(self,
               first_text,
               second_text=None,
               max_length=None,
               first_length=None,
               second_length=None):
        """输出文本对应token id和segment id
        如果传入first_length，则强行padding第一个句子到指定长度；
        同理，如果传入second_length，则强行padding第二个句子到指定长度。
        """
        # 判断first_text是str
        if isinstance(first_text, str):
            # 进行分词
            first_tokens = self.tokenize(first_text)
        else:
            first_tokens = first_text

        if second_text is None:
            second_tokens = None
        elif isinstance(second_text, str):
            idx = int(bool(self._token_start))
            # 进行分词
            second_tokens = self.tokenize(second_text)[idx:]
        else:
            second_tokens = second_text

        # 如果设置了最大长度
        if max_length is not None:
            # 句子不能超过最大长度，否则截断句子
            self.truncate_sequence(max_length, first_tokens, second_tokens, -2)
        # 把词转成id
        first_token_ids = self.tokens_to_ids(first_tokens)
        # 如果定义了第一个句子的长度，超过了就截断，没超过就填充0
        if first_length is not None:
            first_token_ids = first_token_ids[:first_length]
            first_token_ids.extend([self._token_pad_id] *
                                   (first_length - len(first_token_ids)))
        first_segment_ids = [0] * len(first_token_ids)

        if second_text is not None:
            # 把词转成id
            second_token_ids = self.tokens_to_ids(second_tokens)
            # 如果定义了第二个句子的长度，超过了就截断，没超过就填充0
            if second_length is not None:
                second_token_ids = second_token_ids[:second_length]
                second_token_ids.extend(
                    [self._token_pad_id] *
                    (second_length - len(second_token_ids)))
            second_segment_ids = [1] * len(second_token_ids)

            # 合并两个句子
            first_token_ids.extend(second_token_ids)
            first_segment_ids.extend(second_segment_ids)

        return first_token_ids, first_segment_ids

    # id序列为对应的token
    def id_to_token(self, i):
        raise NotImplementedError

    # id序列转换为对应的token序列
    def ids_to_tokens(self, ids):
        return [self.id_to_token(i) for i in ids]

    # 转为可读文本    
    def decode(self, ids):
        raise NotImplementedError

    # 基本分词函数
    def _tokenize(self, text):
        raise NotImplementedError


class Tokenizer(BasicTokenizer):
    """Bert原生分词器
    纯Python实现，代码修改自keras_bert的tokenizer实现
    """
    def __init__(self, token_dict, *args, **kwargs):
        super(Tokenizer, self).__init__(*args, **kwargs)
        # 如果token_dict是字符串，就load_vocab
        if isinstance(token_dict, str):
            token_dict = load_vocab(token_dict)
        # 如果token_dict不是字符串，那么就应该要传入一个字典
        self._token_dict = token_dict
        # 字典的键值对反过来
        self._token_dict_inv = {v: k for k, v in token_dict.items()}
        # 计算字典长度
        self._vocab_size = len(token_dict)
        # 获得_token_unk_id
        self._token_unk_id = self._token_dict.get('[UNK]')

        for token in ['pad', 'unk', 'mask', 'start', 'end']:
            try:
                # 获得_token_pad,_token_unk..._token_end对应编号
                _token_id = token_dict[getattr(self, '_token_%s' % token)]
                # 设置_token_pad_id,_token_unk_id..._token_end_id
                setattr(self, '_token_%s_id' % token, _token_id)
            except:
                pass

    # token转换为对应的id
    def token_to_id(self, token):
        return self._token_dict.get(token, self._token_unk_id)

    # id转换为对应的token
    def id_to_token(self, i):
        return self._token_dict_inv[i]

    # 转为可读文本
    def decode(self, ids, tokens=None):
        # id序列转换为对应的token序列
        tokens = tokens or self.ids_to_tokens(ids)
        # 排除特殊字符如：'[PAD]', '[UNK]', '[CLS]', '[SEP]', '[MASK]'
        tokens = [token for token in tokens if not self._is_special(token)]

        text, flag = '', False
        for i, token in enumerate(tokens):
            if token[:2] == '##':
                text += token[2:]
            elif len(token) == 1 and self._is_cjk_character(token):
                text += token
            elif len(token) == 1 and self._is_punctuation(token):
                text += token
                text += ' '
            elif i > 0 and self._is_cjk_character(text[-1]):
                text += token
            else:
                text += ' '
                text += token

        # 对字符进行一些处理
        text = re.sub(' +', ' ', text)
        text = re.sub('\' (re|m|s|t|ve|d|ll) ', '\'\\1 ', text)
        punctuation = self._cjk_punctuation() + '+-/={(<['
        punctuation_regex = '|'.join([re.escape(p) for p in punctuation])
        punctuation_regex = '(%s) ' % punctuation_regex
        text = re.sub(punctuation_regex, '\\1', text)
        text = re.sub('(\d\.) (\d)', '\\1\\2', text)

        return text.strip()

    # 基本分词函数
    def _tokenize(self, text):
        spaced = ''
        for ch in text:
            # 如果是cjk类字符或标点符号类字符
            if self._is_punctuation(ch) or self._is_cjk_character(ch):
                spaced += ' ' + ch + ' '
            # 如果是空白类字符
            elif self._is_space(ch):
                spaced += ' '
            # 如果是NUll或无效字符或控制字符则舍弃
            elif ord(ch) == 0 or ord(ch) == 0xfffd or self._is_control(ch):
                continue
            # 其他情况
            else:
                spaced += ch

        tokens = []
        # 保存入list
        for word in spaced.strip().split():
            # _word_piece_tokenize切分subword
            tokens.extend(self._word_piece_tokenize(word))

        return tokens

    def _word_piece_tokenize(self, word):
        """word内分成subword
        """
        # 如果在字典中直接返回
        if word in self._token_dict:
            return [word]

        tokens = []
        start, stop = 0, 0
        # 切分subword
        while start < len(word):
            stop = len(word)
            while stop > start:
                sub = word[start:stop]
                if start > 0:
                    sub = '##' + sub
                if sub in self._token_dict:
                    break
                stop -= 1
            if start == stop:
                stop += 1
            tokens.append(sub)
            start = stop

        return tokens

    @staticmethod
    def _is_space(ch):
        """空白类字符判断
        """
        return ch == ' ' or ch == '\n' or ch == '\r' or ch == '\t' or \
            unicodedata.category(ch) == 'Zs'

    @staticmethod
    def _is_punctuation(ch):
        """标点符号类字符判断（全/半角均在此内）
        """
        code = ord(ch)
        return 33 <= code <= 47 or \
            58 <= code <= 64 or \
            91 <= code <= 96 or \
            123 <= code <= 126 or \
            unicodedata.category(ch).startswith('P')

    @staticmethod
    def _cjk_punctuation():
        return u'\uff02\uff03\uff04\uff05\uff06\uff07\uff08\uff09\uff0a\uff0b\uff0c\uff0d\uff0f\uff1a\uff1b\uff1c\uff1d\uff1e\uff20\uff3b\uff3c\uff3d\uff3e\uff3f\uff40\uff5b\uff5c\uff5d\uff5e\uff5f\uff60\uff62\uff63\uff64\u3000\u3001\u3003\u3008\u3009\u300a\u300b\u300c\u300d\u300e\u300f\u3010\u3011\u3014\u3015\u3016\u3017\u3018\u3019\u301a\u301b\u301c\u301d\u301e\u301f\u3030\u303e\u303f\u2013\u2014\u2018\u2019\u201b\u201c\u201d\u201e\u201f\u2026\u2027\ufe4f\ufe51\ufe54\xb7\uff01\uff1f\uff61\u3002'

    @staticmethod
    def _is_cjk_character(ch):
        """CJK类字符判断（包括中文字符也在此列）
        参考：https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
        """
        code = ord(ch)
        return 0x4E00 <= code <= 0x9FFF or \
            0x3400 <= code <= 0x4DBF or \
            0x20000 <= code <= 0x2A6DF or \
            0x2A700 <= code <= 0x2B73F or \
            0x2B740 <= code <= 0x2B81F or \
            0x2B820 <= code <= 0x2CEAF or \
            0xF900 <= code <= 0xFAFF or \
            0x2F800 <= code <= 0x2FA1F

    @staticmethod
    def _is_control(ch):
        """控制类字符判断
        """
        return unicodedata.category(ch) in ('Cc', 'Cf')

    @staticmethod
    def _is_special(ch):
        """判断是不是有特殊含义的符号
        """
        return bool(ch) and (ch[0] == '[') and (ch[-1] == ']')
