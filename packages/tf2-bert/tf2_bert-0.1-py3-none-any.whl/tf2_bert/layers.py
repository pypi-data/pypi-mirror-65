#! -*- coding: utf-8 -*-
# 自定义层

import numpy as np
import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.keras import initializers, activations
from tensorflow.keras.layers import *
from tf2_bert import *

class Layer(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super(Layer, self).__init__(**kwargs)
        # 本项目的自定义层均可mask
        self.supports_masking = True  

# 定义MultiHeadAttention层
class MultiHeadAttention(Layer):
    """多头注意力机制
    """
    def __init__(self,
                 heads,
                 head_size,
                 key_size=None,
                 use_bias=True,
                 scaled_dot_product=True,
                 kernel_initializer='glorot_uniform',
                 **kwargs):
        super(MultiHeadAttention, self).__init__(**kwargs)
        self.heads = heads
        self.head_size = head_size
        self.out_dim = heads * head_size
        self.key_size = key_size or head_size
        self.use_bias = use_bias
        self.scaled_dot_product = scaled_dot_product
        self.kernel_initializer = initializers.get(kernel_initializer)


    def build(self, input_shape):
        # 固定程序，作用是设置 self.built = True
        super(MultiHeadAttention, self).build(input_shape)
        # 定义q,k,v权值矩阵和输出权值矩阵
        self.q_dense = Dense(units=self.key_size * self.heads,
                             use_bias=self.use_bias,
                             kernel_initializer=self.kernel_initializer)
        self.k_dense = Dense(units=self.key_size * self.heads,
                             use_bias=self.use_bias,
                             kernel_initializer=self.kernel_initializer)
        self.v_dense = Dense(units=self.out_dim,
                             use_bias=self.use_bias,
                             kernel_initializer=self.kernel_initializer)
        self.o_dense = Dense(units=self.out_dim,
                             use_bias=self.use_bias,
                             kernel_initializer=self.kernel_initializer)

    def call(self, inputs, mask=None, a_mask=None, p_bias=None):
        """实现多头注意力
        bert没用到mask
        q_mask: 对输入的query序列的mask。
                主要是将输出结果的padding部分置0。
        v_mask: 对输入的value序列的mask。
                主要是防止attention读取到padding信息。
        a_mask: 对attention矩阵的mask。
                不同的attention mask对应不同的应用。
        p_bias: 在attention里的位置偏置。
                一般用来指定相对位置编码的种类。
        """
        # 传入的3个信号是一样的，数据都是(批次，序列长度，embedding信号)
        q, k, v = inputs[:3]
        q_mask, v_mask, n = None, None, 3
        if mask is not None:
            if mask[0] is not None:
                q_mask = K.cast(mask[0], K.floatx())
            if mask[2] is not None:
                v_mask = K.cast(mask[2], K.floatx())
        if a_mask:
            a_mask = inputs[n]
            n += 1
        # 全连接层计算
        qw = self.q_dense(q)
        kw = self.k_dense(k)
        vw = self.v_dense(v)
        # 形状变换变成4维:
        # (批次大小，序列长度，heads数量，self.attention的特征向量)
        qw = K.reshape(qw, (-1, K.shape(q)[1], self.heads, self.key_size))
        kw = K.reshape(kw, (-1, K.shape(k)[1], self.heads, self.key_size))
        vw = K.reshape(vw, (-1, K.shape(v)[1], self.heads, self.head_size))
        # Attention
        # 下面这一步就是queries点乘keys，只不过是多个batch多个heads同时进行，看起来复杂一点
        # einsum爱因斯坦求和，例如传入qw(32,100,16,64)和kw(32,100,16,64)
        # 输出a(2,16,100,100)
        # 32为batch，16为heads，我们可以先不考虑，那么:
        # qw(100,64)和kw(100,64)，100为序列长度，可以理解为句子有100个字符，64是self.attention的特征向量长度
        # 所以这里相当于是做了一个矩阵乘法dot(qw,kw.T),也就是dot((100,64),(64,100))->(100,100)
        # 得到的结果(100,100)就是100个字符对100个字符的attention
        # 最后输出a(32,16,100,100)也就是一个批次，多个heads的，多个字符相互之间的attention数值
        # bjhd代表qw中的4个维度，bkhd代表kw中的4个维度，->bhjk表示计算后得到的数据维度
        a = tf.einsum('bjhd,bkhd->bhjk', qw, kw)
        # 减小a的数值
        if self.scaled_dot_product:
            a = a / self.key_size**0.5
        # softmax计算
        a = K.softmax(a)
        # 完成输出
        # 举例a(32,16,100,100),vw(32,100,16,64)->o(32,100,16,64)
        # 同样我们假装看不见batch-32和heads-16，那么a的shape(100,100),vw的shape(100,64)
        # dot(a,vw)->dot((100,100),(100,64))->(100,64)，得到100个字符每个字符的self.attention特征
        o = tf.einsum('bhjk,bkhd->bjhd', a, vw)
        # reshape(批次, 序列长度, heads * head_size)
        o = K.reshape(o, (-1, K.shape(o)[1], self.out_dim))
        # 加个全连接
        o = self.o_dense(o)
        # 返回结果
        return o

    def compute_output_shape(self, input_shape):
        return (input_shape[0][0], input_shape[0][1], self.out_dim)

    def compute_mask(self, inputs, mask):
        return mask[0]

    def get_config(self):
        config = {
            'heads': self.heads,
            'head_size': self.head_size,
            'key_size': self.key_size,
            'use_bias': self.use_bias,
            'scaled_dot_product': self.scaled_dot_product,
            'kernel_initializer': initializers.serialize(self.kernel_initializer),
        }
        base_config = super(MultiHeadAttention, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

# 定义LayerNormalization层
class LayerNormalization(Layer):
    def __init__(self,
                 center=True,
                 scale=True,
                 epsilon=None,
                 **kwargs):
        super(LayerNormalization, self).__init__(**kwargs)
        self.center = center
        self.scale = scale
        self.epsilon = epsilon or 1e-12

    def build(self, input_shape):
        # 固定程序，作用是设置 self.built = True
        super(LayerNormalization, self).build(input_shape)

        shape = (input_shape[-1], )
        # 定义标准化后线性变化的两个参数
        if self.center:
            self.beta = self.add_weight(shape=shape,
                                        initializer='zeros',
                                        name='beta')
        if self.scale:
            self.gamma = self.add_weight(shape=shape,
                                         initializer='ones',
                                         name='gamma')

    def call(self, inputs):
        if self.center:
            beta = self.beta
        if self.scale:
            gamma = self.gamma
        outputs = inputs
        # 标准化处理并进行线性变换
        if self.center:
            # 特征减去均值
            mean = K.mean(outputs, axis=-1, keepdims=True)
            outputs = outputs - mean
        if self.scale:
            # 特征除以方差再乘gamma
            variance = K.mean(K.square(outputs), axis=-1, keepdims=True)
            std = K.sqrt(variance + self.epsilon)
            outputs = outputs / std
            outputs = outputs * gamma
        if self.center:
            # 特征加beta
            outputs = outputs + beta
        return outputs

    # 使用get_config方法可以返回一些跟layer相关的一些信息
    def get_config(self):
        config = {
            'center': self.center,
            'scale': self.scale,
            'epsilon': self.epsilon
        }
        base_config = super(LayerNormalization, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

# 定义PositionEmbedding层
class PositionEmbedding(Layer):
    # 定义位置Embedding，这里的Embedding是可训练的，跟原始论文不同
    def __init__(self,
                 input_dim,
                 output_dim,
                 merge_mode='add',
                 embeddings_initializer='zeros',
                 **kwargs):
        super(PositionEmbedding, self).__init__(**kwargs)
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.merge_mode = merge_mode
        self.embeddings_initializer = initializers.get(embeddings_initializer)

    def build(self, input_shape):
        # 固定程序，作用是设置 self.built = True
        super(PositionEmbedding, self).build(input_shape)
        # 创建该层的训练权值
        self.embeddings = self.add_weight(
            name='embeddings',
            shape=(self.input_dim, self.output_dim),
            initializer=self.embeddings_initializer,
        )

    def call(self, inputs):
        # 获得inputs的shape
        input_shape = K.shape(inputs)
        # 获得批次大小和序列长度
        batch_size, seq_len = input_shape[0], input_shape[1]
        # 取出跟序列相关的权值，序列长度seq_len<input_dim(max_position)
        pos_embeddings = self.embeddings[:seq_len]
        # 0位置增加一个维度，跟inputs维度匹配
        pos_embeddings = K.expand_dims(pos_embeddings, 0)
        # 位置信息直接跟inputs相加
        if self.merge_mode == 'add':
            return inputs + pos_embeddings
        # 位置信息跟inputs信息拼接concat
        else:
            # 在批次的维度把pos_embeddings复制batch_size份
            # pos_embeddings得到跟inputs相同的shape
            pos_embeddings = K.tile(pos_embeddings, [batch_size, 1, 1])
            # 跟inputs信息拼接concat
            return K.concatenate([inputs, pos_embeddings])

    def compute_output_shape(self, input_shape):
        # 信息相加的方式shape不变
        if self.merge_mode == 'add':
            return input_shape
        # concat方式，每个字符的特征数等于input_shape[2] + self.output_dim
        else:
            print(input_shape[:2] + (input_shape[2] + self.output_dim, ))
            return input_shape[:2] + (input_shape[2] + self.output_dim, )

    # 使用get_config方法可以返回一些跟layer相关的一些信息
    def get_config(self):
        config = {
            'input_dim': self.input_dim,
            'output_dim': self.output_dim,
            'merge_mode': self.merge_mode,
            'embeddings_initializer': initializers.serialize(self.embeddings_initializer),
        }
        base_config = super(PositionEmbedding, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

# 定义FeedForward层
class FeedForward(Layer):
    """FeedForward层，其实就是两个Dense层的叠加
    """
    def __init__(self,
                 units,
                 activation='relu',
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 **kwargs):
        super(FeedForward, self).__init__(**kwargs)
        self.units = units
        self.activation = activations.get(activation)
        self.use_bias = use_bias
        self.kernel_initializer = initializers.get(kernel_initializer)

    def build(self, input_shape):
        # 固定程序，作用是设置 self.built = True
        super(FeedForward, self).build(input_shape)
        # FeedForward层输出不改变信号shape
        output_dim = input_shape[-1]
        # 两个隐藏层
        self.dense_1 = Dense(units=self.units,
                             activation=self.activation,
                             use_bias=self.use_bias,
                             kernel_initializer=self.kernel_initializer)
        self.dense_2 = Dense(units=output_dim,
                             use_bias=self.use_bias,
                             kernel_initializer=self.kernel_initializer)

    def call(self, inputs):
        x = inputs
        # 两个全连接计算
        x = self.dense_1(x)
        x = self.dense_2(x)
        return x

    # 使用get_config方法可以返回一些跟layer相关的一些信息
    def get_config(self):
        config = {
            'units': self.units,
            'activation': activations.serialize(self.activation),
            'use_bias': self.use_bias,
            'kernel_initializer': initializers.serialize(self.kernel_initializer),
        }
        base_config = super(FeedForward, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

custom_objects = {
    'MultiHeadAttention': MultiHeadAttention,
    'LayerNormalization': LayerNormalization,
    'PositionEmbedding': PositionEmbedding,
    'FeedForward': FeedForward,
}

tf.keras.utils.get_custom_objects().update(custom_objects)
