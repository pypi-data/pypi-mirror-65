#! -*- coding: utf-8 -*-
# 主要模型

import numpy as np
from tf2_bert.layers import *
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Embedding
import tensorflow as tf
import json
import warnings


class Transformer(object):
    """模型基类
    """
    def __init__(
            self,
            vocab_size,  # 词表大小
            hidden_size,  # 编码维度
            num_hidden_layers,  # Transformer总层数
            num_attention_heads,  # Attention的头数
            intermediate_size,  # FeedForward的隐层维度
            hidden_act,  # FeedForward隐层的激活函数
            dropout_rate=None,  # Dropout比例
            embedding_size=None,  # 是否指定embedding_size
            attention_key_size=None,  # Attention中Q,K的head_size
            keep_tokens=None,  # 要保留的词ID列表
            layers=None,  # 外部传入的Keras层
            name=None,  # 模型名称
            **kwargs):
        if keep_tokens is None:
            self.vocab_size = vocab_size
        else:
            self.vocab_size = len(keep_tokens)
        self.hidden_size = hidden_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.attention_head_size = hidden_size // num_attention_heads
        self.attention_key_size = attention_key_size or self.attention_head_size
        self.intermediate_size = intermediate_size
        self.dropout_rate = dropout_rate or 0
        self.hidden_act = hidden_act
        self.embedding_size = embedding_size or hidden_size
        self.keep_tokens = keep_tokens
        self.attention_mask = None
        self.position_bias = None
        self.layers = {} if layers is None else layers
        self.name = name

    def build(self, **kwargs):
        # 定义model输入
        # inputs为(token_ids, segment_ids)
        self.inputs = self.prepare_inputs()

        # 准备Embedding信号
        outputs = self.prepare_embeddings(self.inputs)
        # 重复搭建num_hidden_layers次
        for i in range(self.num_hidden_layers):
            # Transformer主体结构
            outputs = self.prepare_main_layers(outputs, i)
        # Final
        outputs = self.prepare_final_layers(outputs)
        self.set_outputs(outputs)
        # Model
        self.model = Model(self.inputs, self.outputs, name=self.name)

    # 定义一个Keras层用于计算
    def call(self, inputs, layer=None, arguments=None, **kwargs):
        """
        inputs: 上一层的输出；
        layer: 要调用的层类名；
        arguments: 传递给layer.call的参数；
        kwargs: 传递给层初始化的参数。
        """
        if layer is Dropout and self.dropout_rate == 0:
            return inputs
        arguments = arguments or {}
        name = kwargs.get('name')
        # 把该层存入layers
        if name not in self.layers:
            layer = layer(**kwargs)
            name = layer.name
            self.layers[name] = layer
        # 返回该层计算后的结果
        return self.layers[name](inputs, **arguments)

    # 在Bert类中实现
    def prepare_inputs(self):
        raise NotImplementedError
    # 在Bert类中实现
    def prepare_embeddings(self, inputs):
        raise NotImplementedError
    # 在Bert类中实现
    def prepare_main_layers(self, inputs, index):
        raise NotImplementedError
    # 在Bert类中实现
    def prepare_final_layers(self, inputs):
        raise NotImplementedError

    def compute_attention_mask(self, inputs=None):
        """定义每一层的Attention Mask
        """
        return self.attention_mask

    def compute_position_bias(self, inputs=None):
        """定义每一层的Position Bias（一般相对位置编码用）
        """
        return self.position_bias

    def set_outputs(self, outputs):
        """设置output和oututs属性
        """
        if not isinstance(outputs, list):
            outputs = [outputs]

        outputs = outputs[:]
        self.outputs = outputs
        if len(outputs) > 1:
            self.output = outputs
        else:
            self.output = outputs[0]

    @property
    def initializer(self):
        """默认使用截断正态分布初始化
        """
        return tf.keras.initializers.TruncatedNormal(stddev=0.02)

    def load_variable(self, checkpoint, name):
        """加载单个变量的函数
        """
        return tf.train.load_variable(checkpoint, name)

    def create_variable(self, name, value):
        """在tensorflow中创建一个变量
        """
        return tf.Variable(value, name=name)

    def variable_mapping(self):
        """构建keras层与checkpoint的变量名之间的映射表
        """
        return {}

    # 载入模型参数
    def load_weights_from_checkpoint(self, checkpoint, mapping=None):
        """根据mapping从checkpoint加载权重
        """
        # 获得本项目参数名跟谷歌官方模型参数名映射关系
        mapping = mapping or self.variable_mapping()
        # 如果参数名称跟匹配上就存入mapping中
        mapping = {k: v for k, v in mapping.items() if k in self.layers}

        weight_value_pairs = []
        # 循环mapping中键值对
        for layer_name, variables in mapping.items():
            # 根据层的名称获取该层
            layer = self.layers[layer_name]
            # 获得该层训练参数
            weights = layer.trainable_weights
            # 如果是'MLM-Proba'层，我们直接使用与'Embedding-Token'相同的参数即可
            # 'Embedding-Token'层是将所有字符编号转成对应Embedding信号的层
            # 'MLM-Proba'层相当于是将Embedding信号转成对应字符编号的层，所以'MLM-Proba'层可以跟'Embedding-Token'共用一套权值
            if layer_name == 'MLM-Proba':
                # 获得'Embedding-Token'层的权值
                word_embeddings = self.load_variable(checkpoint,'bert/embeddings/word_embeddings')
                # transpose矩阵转置，'MLM-Proba'层参数跟'Embedding-Token'层参数行列刚好是相反的，所以这里需要转置
                word_embeddings = K.transpose(word_embeddings)
                values = [word_embeddings]
            else:
                # 其他层正常load参数就可以
                values = [self.load_variable(checkpoint, v) for v in variables]
            # 将zip(weights, values)加入weight_value_pairs列表
            weight_value_pairs.extend(zip(weights, values))
        # batch_set_value一次设置多个tensor变量的值，将values的值设置到weights中
        K.batch_set_value(weight_value_pairs)

    # 根据mapping将权重保存为checkpoint格式，用于再次训练后保存ckpt格式模型
    def save_weights_as_checkpoint(self, filename, mapping=None):
        # 获得本项目参数名跟谷歌官方模型参数名映射关系
        mapping = mapping or self.variable_mapping()
        # 定义模型计算图
        with tf.Graph().as_default():
            # 循环mapping中键值对
            for layer, variables in mapping.items():
                # 根据层的名称获取该层
                layer = self.layers[layer]
                # batch_get_value获得layer可训练参数的数值
                values = K.batch_get_value(layer.trainable_weights)
                # 创建tensorflow变量
                for name, value in zip(variables, values):
                    self.create_variable(name, value)
            # 创建会话
            with tf.Session() as sess:
                # 全局变量初始化
                sess.run(tf.global_variables_initializer())
                # 定义Saver用于保存模型
                saver = tf.train.Saver()
                # 模型保存 
                saver.save(sess, filename, write_meta_graph=False)


class BERT(Transformer):
    """构建BERT模型
    """
    def __init__(
            self,
            max_position,  # 序列最大长度
            with_pool=False,  # 是否包含Pool部分
            with_nsp=False,  # 是否包含NSP部分
            with_mlm=False,  # 是否包含MLM部分
            **kwargs  # 其余参数
    ):
        super(BERT, self).__init__(**kwargs)
        self.max_position = max_position
        self.with_pool = with_pool
        self.with_nsp = with_nsp
        self.with_mlm = with_mlm

    # 定义两个输入
    def prepare_inputs(self):
        # Input-Token是词的编号
        # Input-Segment是句子的编号
        # 比如有两个句子，句子1“我爱”；句子2“学习”，预处理变成：
        # [[CLS], 我, 爱, [SEP], 学, 习, [SEP]]，对应的token_ids可能为:
        # [101, 2769, 4263, 102, 2110, 739, 102]
        # 对应的segment_ids为:
        # [0, 0, 0, 0, 1, 1, 1]
        # 这里的segment_ids表示token_ids中前4个值为句子1，后3个值为句子2
        x_in = Input(shape=(None, ), name='Input-Token')
        s_in = Input(shape=(None, ), name='Input-Segment')
        return [x_in, s_in]

    # 准备embeddings信号
    def prepare_embeddings(self, inputs):
        """BERT的embedding是token、position、segment三者embedding之和
        """
        x, s = inputs

        # 将每个词编号转为向量表示
        x = self.call(inputs=x,
                      layer=Embedding,
                      input_dim=self.vocab_size,
                      output_dim=self.embedding_size,
                      embeddings_initializer=self.initializer,
                      mask_zero=True,
                      name='Embedding-Token')
        # 将每个句子编号转为向量表示
        s = self.call(inputs=s,
                      layer=Embedding,
                      input_dim=2,
                      output_dim=self.embedding_size,
                      embeddings_initializer=self.initializer,
                      name='Embedding-Segment')
        # x,s信号相加
        x = self.call(inputs=[x, s], layer=Add, name='Embedding-Token-Segment')
        # x加上PositionEmbedding信号
        x = self.call(inputs=x,
                      layer=PositionEmbedding,
                      input_dim=self.max_position,
                      output_dim=self.embedding_size,
                      merge_mode='add',
                      embeddings_initializer=self.initializer,
                      name='Embedding-Position')
        # 对x进行LayerNormalization处理
        x = self.call(inputs=x,
                      layer=LayerNormalization,
                      name='Embedding-Norm')
        # Dropout
        x = self.call(inputs=x,
                      layer=Dropout,
                      rate=self.dropout_rate,
                      name='Embedding-Dropout')
        # 如果embedding_size不等于self.hidden_size加个全连接层
        if self.embedding_size != self.hidden_size:
            x = self.call(inputs=x,
                          layer=Dense,
                          units=self.hidden_size,
                          kernel_initializer=self.initializer,
                          name='Embedding-Mapping')

        return x

    # Transformer主体
    def prepare_main_layers(self, inputs, index):
        """BERT的主体是基于Self-Attention的模块
        顺序：
            -----------------------------------------                           ---------------------------------
            ⬆                                      ⬇                          ⬆                               ⬇
          ----> MultiHeadAttention --> Dropout --> Add --> LayerNormalization --> FeedForward --> Dropout --> Add  -->
        """
        x = inputs
        # 起个名字
        attention_name = 'Transformer-%d-MultiHeadSelfAttention' % index
        feed_forward_name = 'Transformer-%d-FeedForward' % index
        # 是否mask
        attention_mask = self.compute_attention_mask()

        # xi通过shortcut传给Add
        # [x, x, x]分别传给query, key, value进行计算
        # bert没用到mask
        xi, x, arguments = x, [x, x, x], {'a_mask': None}
        if attention_mask is not None:
            arguments['a_mask'] = True
            x.append(attention_mask)                
        # MultiHeadAttention计算
        x = self.call(inputs=x,
                      layer=MultiHeadAttention,
                      arguments=arguments,
                      heads=self.num_attention_heads,
                      head_size=self.attention_head_size,
                      key_size=self.attention_key_size,
                      kernel_initializer=self.initializer,
                      name=attention_name)
        # Dropout
        x = self.call(inputs=x,
                      layer=Dropout,
                      rate=self.dropout_rate,
                      name='%s-Dropout' % attention_name)
        # ADD
        x = self.call(inputs=[xi, x],
                      layer=Add,
                      name='%s-Add' % attention_name)
        # 对x进行LayerNormalization处理
        x = self.call(inputs=x,
                      layer=LayerNormalization,
                      name='%s-Norm' % attention_name)

        # Feed Forward层计算
        xi = x
        x = self.call(inputs=x,
                      layer=FeedForward,
                      units=self.intermediate_size,
                      activation=self.hidden_act,
                      kernel_initializer=self.initializer,
                      name=feed_forward_name)
        # Dropout
        x = self.call(inputs=x,
                      layer=Dropout,
                      rate=self.dropout_rate,
                      name='%s-Dropout' % feed_forward_name)
        # Add
        x = self.call(inputs=[xi, x],
                      layer=Add,
                      name='%s-Add' % feed_forward_name)
        # 对x进行LayerNormalization处理 
        x = self.call(inputs=x,
                      layer=LayerNormalization,
                      name='%s-Norm' % feed_forward_name)
        # 输出结果
        return x

    # 最后输出部分
    def prepare_final_layers(self, inputs):
        """根据剩余参数决定输出
        """
        # 如果没有相关参数设置就直接输出信号
        # inputs.shape-(batch, seq_length, embedding_size)
        x = inputs
        outputs = [x]

        if self.with_pool or self.with_nsp:
            # Pooler部分（提取CLS向量）
            x = outputs[0]
            # 每个序列的第一个字符是句子的分类[CLS],该字符对应的embedding可以用作分类任务中该序列的总表示
            # 说白了就是用句子第一个字符的embedding来表示整个句子
            # 取出每个句子的第一个字符对应的embedding
            x = self.call(inputs=x,
                          layer=Lambda,
                          function=lambda x: x[:, 0],
                          name='Pooler')
            # 加个全连接
            x = self.call(inputs=x,
                          layer=Dense,
                          units=self.hidden_size,
                          activation='tanh',
                          kernel_initializer=self.initializer,
                          name='Pooler-Dense')
            # 预测是不是相连的两句话
            if self.with_nsp:
                # Next Sentence Prediction部分
                x = self.call(inputs=x,
                              layer=Dense,
                              units=2,
                              activation='softmax',
                              kernel_initializer=self.initializer,
                              name='NSP-Proba')
            outputs.append(x)

        if self.with_mlm:
            # Masked Language Model部分
            x = outputs[0]
            # 全连接
            x = self.call(inputs=x,
                          layer=Dense,
                          units=self.embedding_size,
                          activation=self.hidden_act,
                          kernel_initializer=self.initializer,
                          name='MLM-Dense')
            # 对x进行LayerNormalization处理  
            x = self.call(inputs=x,
                          layer=LayerNormalization,
                          name='MLM-Norm')
            # 输出每个词的概率
            x = self.call(inputs=x,
                          layer=Dense,
                          units=self.vocab_size,
                          activation='softmax',
                          name='MLM-Proba')
            outputs.append(x)

        if len(outputs) == 1:
            outputs = outputs[0]
        elif len(outputs) == 2:
            outputs = outputs[1]
        else:
            outputs = outputs[1:]

        return outputs

    def load_variable(self, checkpoint, name):
        """加载单个变量的函数
        """
        variable = super(BERT, self).load_variable(checkpoint, name)
        if name in [
                'bert/embeddings/word_embeddings',
                'cls/predictions/output_bias',
        ]:
            if self.keep_tokens is None:
                return variable
            else:
                return variable[self.keep_tokens]
        elif name == 'cls/seq_relationship/output_weights':
            return variable.T
        else:
            return variable

    def create_variable(self, name, value):
        """在tensorflow中创建一个变量
        """
        if name == 'cls/seq_relationship/output_weights':
            value = value.T
        return super(BERT, self).create_variable(name, value)

    def variable_mapping(self):
        """映射到官方BERT权重格式
        """
        mapping = {
            'Embedding-Token': ['bert/embeddings/word_embeddings'],
            'Embedding-Segment': ['bert/embeddings/token_type_embeddings'],
            'Embedding-Position': ['bert/embeddings/position_embeddings'],
            'Embedding-Norm': [
                'bert/embeddings/LayerNorm/beta',
                'bert/embeddings/LayerNorm/gamma',
            ],
            'Embedding-Mapping': [
                'bert/encoder/embedding_hidden_mapping_in/kernel',
                'bert/encoder/embedding_hidden_mapping_in/bias',
            ],
            'Pooler-Dense': [
                'bert/pooler/dense/kernel',
                'bert/pooler/dense/bias',
            ],
            'NSP-Proba': [
                'cls/seq_relationship/output_weights',
                'cls/seq_relationship/output_bias',
            ],
            'MLM-Dense': [
                'cls/predictions/transform/dense/kernel',
                'cls/predictions/transform/dense/bias',
            ],
            'MLM-Norm': [
                'cls/predictions/transform/LayerNorm/beta',
                'cls/predictions/transform/LayerNorm/gamma',
            ],
            'MLM-Proba': ['cls/predictions/output_bias'],
        }

        for i in range(self.num_hidden_layers):
            prefix = 'bert/encoder/layer_%d/' % i
            mapping.update({
                'Transformer-%d-MultiHeadSelfAttention' % i: [
                    prefix + 'attention/self/query/kernel',
                    prefix + 'attention/self/query/bias',
                    prefix + 'attention/self/key/kernel',
                    prefix + 'attention/self/key/bias',
                    prefix + 'attention/self/value/kernel',
                    prefix + 'attention/self/value/bias',
                    prefix + 'attention/output/dense/kernel',
                    prefix + 'attention/output/dense/bias',
                ],
                'Transformer-%d-MultiHeadSelfAttention-Norm' % i: [
                    prefix + 'attention/output/LayerNorm/beta',
                    prefix + 'attention/output/LayerNorm/gamma',
                ],
                'Transformer-%d-FeedForward' % i: [
                    prefix + 'intermediate/dense/kernel',
                    prefix + 'intermediate/dense/bias',
                    prefix + 'output/dense/kernel',
                    prefix + 'output/dense/bias',
                ],
                'Transformer-%d-FeedForward-Norm' % i: [
                    prefix + 'output/LayerNorm/beta',
                    prefix + 'output/LayerNorm/gamma',
                ],
            })

        return mapping

# 载入bert模型
def build_transformer_model(config_path=None,
                            checkpoint_path=None,
                            return_keras_model=True,
                            **kwargs):
    # config_path和checkpoint_path不能为None
    assert config_path != None, "please input config_path"
    assert checkpoint_path != None, "please input checkpoint_path"
    # 载入模型配置信息
    configs = json.load(open(config_path))
    # 有些配置信息名称不同，意思是一样的
    if 'max_position' not in configs:
        configs['max_position'] = configs.get('max_position_embeddings')
    if 'dropout_rate' not in configs:
        configs['dropout_rate'] = configs.get('hidden_dropout_prob')
    # 把configs信息传入BERT中
    transformer = BERT(**configs, **kwargs)
    transformer.build(**configs, **kwargs)

    # 载入checkpoint
    transformer.load_weights_from_checkpoint(checkpoint_path)

    # 返回transformer对象或模型
    if return_keras_model:
        return transformer.model
    else:
        return transformer

