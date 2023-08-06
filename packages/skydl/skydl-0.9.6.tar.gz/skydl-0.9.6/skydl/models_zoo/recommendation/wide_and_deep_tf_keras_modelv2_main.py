# -*- coding: utf-8 -*-
import os, sys
import tensorflow as tf
from tensorflow import keras
from skydl.datasets.recommend_dataset_builder import RecommendDatasetBuilder
from skydl.models_zoo.recommendation.wide_and_deep_tf_keras_modelv2 import WideAndDeepTfKerasModelV2
sys.path.append(os.path.abspath('%s/..' % sys.path[0]))


def training_wide_and_deep_keras_model():
    """
    训练模型-资讯智能推荐系统中用于精排序的模型
    keras现在也有了默认实现: https://www.tensorflow.org/api_docs/python/tf/keras/experimental/WideDeepModel
    """
    # 加载数据集
    train_dataset, validation_dataset, evaluate_dataset, tag_index_count = WideAndDeepTfKerasModelV2().load_data()
    # 定义inputs, outputs
    feature_columns = []
    feature_layer_inputs = {}
    max_seq_length = 20
    vocab_size = tag_index_count  # i.e. tag_index_len, 以前是38958
    embedding_output_dim = 8  # i.e. embedding feature's hidden_size
    # 1. gender: [1, 2]
    gender_fc = RecommendDatasetBuilder.build_one_hot_feature_column(
        RecommendDatasetBuilder.build_categorical_column_with_vocabulary_list("gender", [1,2]))
    feature_columns.append(gender_fc)
    feature_layer_inputs["gender"] = tf.keras.Input(shape=(1,), name='gender', dtype=tf.float32)
    # 2. age_group:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    age_group_fc = RecommendDatasetBuilder.build_one_hot_feature_column(
        RecommendDatasetBuilder.build_categorical_column_with_vocabulary_list("age_group", [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]))
    feature_columns.append(age_group_fc)
    feature_layer_inputs["age_group"] = tf.keras.Input(shape=(1,), name='age_group', dtype=tf.float32)
    # 3. position: [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117]
    position_fc = RecommendDatasetBuilder.build_one_hot_feature_column(
        RecommendDatasetBuilder.build_categorical_column_with_vocabulary_list("position", [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117]))
    feature_columns.append(position_fc)
    feature_layer_inputs["position"] = tf.keras.Input(shape=(1,), name='position', dtype=tf.float32)
    # 4. annual_income: [0,1,2,3,4,5]
    annual_income_fc = RecommendDatasetBuilder.build_one_hot_feature_column(
        RecommendDatasetBuilder.build_categorical_column_with_vocabulary_list("annual_income", [0,1,2,3,4,5]))
    feature_columns.append(annual_income_fc)
    feature_layer_inputs["annual_income"] = tf.keras.Input(shape=(1,), name='annual_income', dtype=tf.float32)
    # 5. address: [0,1]
    address_fc = RecommendDatasetBuilder.build_one_hot_feature_column(
        RecommendDatasetBuilder.build_categorical_column_with_vocabulary_list("address", [0,1]))
    feature_columns.append(address_fc)
    feature_layer_inputs["address"] = tf.keras.Input(shape=(1,), name='address', dtype=tf.float32)
    # 6. account_type: [0,1,2,3]
    account_type_fc = RecommendDatasetBuilder.build_one_hot_feature_column(
        RecommendDatasetBuilder.build_categorical_column_with_vocabulary_list("account_type", [0,1,2,3]))
    feature_columns.append(account_type_fc)
    feature_layer_inputs["account_type"] = tf.keras.Input(shape=(1,), name='account_type', dtype=tf.float32)
    # 7. asset_size: [0,1,2]
    asset_size_fc = RecommendDatasetBuilder.build_one_hot_feature_column(
        RecommendDatasetBuilder.build_categorical_column_with_vocabulary_list("asset_size", [0,1,2,3]))
    feature_columns.append(asset_size_fc)
    feature_layer_inputs["asset_size"] = tf.keras.Input(shape=(1,), name='asset_size', dtype=tf.float32)
    # 8. Investment_risk_preference: [0,1]
    investment_risk_preference_fc = RecommendDatasetBuilder.build_one_hot_feature_column(
        RecommendDatasetBuilder.build_categorical_column_with_vocabulary_list("Investment_risk_preference", [0,1]))
    feature_columns.append(investment_risk_preference_fc)
    feature_layer_inputs["Investment_risk_preference"] = tf.keras.Input(shape=(1,), name='Investment_risk_preference', dtype=tf.float32)
    # 9. Market_preference: [0,1,2,3]
    market_preference_fc = RecommendDatasetBuilder.build_one_hot_feature_column(
        RecommendDatasetBuilder.build_categorical_column_with_vocabulary_list("Market_preference", [0,1,2,3]))
    feature_columns.append(market_preference_fc)
    feature_layer_inputs["Market_preference"] = tf.keras.Input(shape=(1,), name='Market_preference', dtype=tf.float32)
    # 10. content_type: [0,1,2]
    content_type_fc = RecommendDatasetBuilder.build_one_hot_feature_column(
        RecommendDatasetBuilder.build_categorical_column_with_vocabulary_list("content_type", [0,1,2]))
    feature_columns.append(content_type_fc)
    feature_layer_inputs["content_type"] = tf.keras.Input(shape=(1,), name='content_type', dtype=tf.float32)
    # 11. tag_indexs: 多标签，tag_index_len(vocab_size)=33209, max_seq_length=20
    tag_indexs_fc = RecommendDatasetBuilder.build_embedding_feature_column(
        RecommendDatasetBuilder.build_categorical_column_with_identity("tag_indexs", vocab_size + 1), embedding_output_dim)
    feature_columns.append(tag_indexs_fc)
    # feature_layer_inputs["tag_indexs"] = tf.keras.Input(shape=(max_seq_length,), name="tag_indexs", dtype=tf.float32)
    # e.g. embedding_layer = keras.layers.Embedding(vocab_size + 1, embedding_output_dim, input_length=20)

    # 准备训练wide & deep model
    # #Define our wide model with the functional API
    merged_layer = keras.layers.concatenate([v for v in feature_layer_inputs.values()])
    merged_layer = keras.layers.Dense(256, activation='relu')(merged_layer)
    predictions = keras.layers.Dense(1)(merged_layer)
    wide_model = keras.Model(inputs=[v for v in feature_layer_inputs.values()], outputs=predictions)
    wide_model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
    print(wide_model.summary())
    # #Define our deep model with the Functional API
    # deep_inputs = feature_layer_inputs["tag_indexs"]
    deep_inputs = tf.keras.Input(shape=(max_seq_length,), name="tag_indexs", dtype=tf.float32)
    embedding = keras.layers.Embedding(vocab_size + 1, embedding_output_dim, input_length=max_seq_length)(deep_inputs)  # vocab_size + 1, the 1 is just for adding '<UNK>'
    embedding = keras.layers.Flatten()(embedding)
    embed_out = keras.layers.Dense(1)(embedding)
    deep_model = keras.Model(inputs=deep_inputs, outputs=embed_out)
    print(deep_model.summary())
    deep_model.compile(loss='mse',
                       optimizer='adam',
                       metrics=['accuracy'])
    # Combine wide and deep into one model
    merged_out = keras.layers.concatenate([wide_model.output, deep_model.output])
    merged_out = keras.layers.Dense(1)(merged_out)
    # 开始训练模型
    WideAndDeepTfKerasModelV2(
        "recommend_ranking",
        keras_inputs=wide_model.input + [deep_model.input],
        keras_outputs=merged_out
    ).compile(
        loss="mean_squared_error",
        optimizer="adam",
        metrics=['accuracy']
    ).fit(
        loaded_dataset=[train_dataset, validation_dataset, evaluate_dataset]
    ).predict_from_load_weights(member_info=[1222,1.0,2.0,1.0,1.0,0.0,0.0,0.0,1.0,0.0], content_info_list=[33333,2.0,[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]])


if __name__ == '__main__':
    training_wide_and_deep_keras_model()
