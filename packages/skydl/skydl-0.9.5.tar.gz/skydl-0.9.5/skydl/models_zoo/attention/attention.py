# -*- coding: utf-8 -*-
import tensorflow as tf

######################################################
# ref: https://www.tensorflow.org/tutorials/text/nmt_with_attention
class BahdanauAttention(tf.keras.layers.Layer):

  def __init__(self, units):
    super(BahdanauAttention, self).__init__()
    self.W1 = tf.keras.layers.Dense(units)
    self.W2 = tf.keras.layers.Dense(units)
    self.V = tf.keras.layers.Dense(1)

  def call(self, query, values):
    # 隐藏层的形状 == （批大小，隐藏层大小）
    # hidden_with_time_axis 的形状 == （批大小，1，隐藏层大小）
    # 这样做是为了执行加法以计算分数
    hidden_with_time_axis = tf.expand_dims(query, 1)
    # 分数的形状 == （批大小，最大长度，1）
    # 我们在最后一个轴上得到 1， 因为我们把分数应用于 self.V
    # 在应用 self.V 之前，张量的形状是（批大小，最大长度，单位）
    score = self.V(tf.nn.tanh(self.W1(values) + self.W2(hidden_with_time_axis)))
    # 注意力权重 （attention_weights） 的形状 == （批大小，最大长度，1）
    attention_weights = tf.nn.softmax(score, axis=1)
    # 上下文向量 （context_vector） 求和之后的形状 == （批大小，隐藏层大小）
    context_vector = attention_weights * values
    context_vector = tf.reduce_sum(context_vector, axis=1)
    return context_vector, attention_weights

############################################################
#ref: https://rubikscode.net/2019/08/05/transformer-with-python-and-tensorflow-2-0-attention-layers/
class ScaledDotProductAttentionLayer():
    def calculate_output_weights(self, q, k, v, mask):
      qk = tf.matmul(q, k, transpose_b=True)
      dk = tf.cast(tf.shape(k)[-1], tf.float32)
      scaled_attention = qk / tf.math.sqrt(dk)
      #if mask is not None:
        # scaled_attention_logits += (mask * -1e9)
      weights = tf.nn.softmax(scaled_attention, axis=-1)
      output = tf.matmul(weights, v)
      return output, weights


class MultiHeadAttentionLayer(tf.keras.layers.Layer):

    def __init__(self, num_neurons, num_heads):
      super(MultiHeadAttentionLayer, self).__init__()
      self.num_heads = num_heads
      self.num_neurons = num_neurons
      self.depth = num_neurons // self.num_heads
      self.attention_layer = ScaledDotProductAttentionLayer()

      self.q_layer = tf.keras.layers.Dense(num_neurons)
      self.k_layer = tf.keras.layers.Dense(num_neurons)
      self.v_layer = tf.keras.layers.Dense(num_neurons)

      self.linear_layer = tf.keras.layers.Dense(num_neurons)

    def split(self, x, batch_size):
      x = tf.reshape(x, (batch_size, -1, self.num_heads, self.depth))
      return tf.transpose(x, perm=[0, 2, 1, 3])

    def call(self, v, k, q, mask):
      batch_size = tf.shape(q)[0]

      # Run through linear layers
      q = self.q_layer(q)
      k = self.k_layer(k)
      v = self.v_layer(v)
      # Split the heads
      q = self.split(q, batch_size)
      k = self.split(k, batch_size)
      v = self.split(v, batch_size)
      # Run through attention
      attention_output, weights = self.attention_layer.calculate_output_weights(q, k, v, mask)
      # Prepare for the rest of processing
      output = tf.transpose(attention_output, perm=[0, 2, 1, 3])
      concat_attention = tf.reshape(output, (batch_size, -1, self.num_neurons))
      # Run through final linear layer
      output = self.linear_layer(concat_attention)
      return output, weights
#################################