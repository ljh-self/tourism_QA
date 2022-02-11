import tensorflow as tf  # pip install "tensorflow>=1.15,<2.0"
import tensorflow_hub as hub  # pip install --upgrade tensorflow-hub
from bert.tokenization import FullTokenizer  # pip install bert-tensorflow==1.0.1
from tensorflow.keras.models import Model
import numpy as np

print('tf.__version__:', tf.__version__)

# 创建模型
max_seq_length = 128
input_word_ids = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32,
                                       name="input_word_ids")
input_mask = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32,
                                   name="input_mask")
segment_ids = tf.keras.layers.Input(shape=(max_seq_length,), dtype=tf.int32,
                                    name="segment_ids")
bert_layer = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/2",
                            trainable=True)
# bert_layer = hub.KerasLayer("D:/download/bert_en_uncased_L-12_H-768_A-12_2",
#                             trainable=True)
pooled_output, sequence_output = bert_layer([input_word_ids, input_mask, segment_ids])

model = Model(inputs=[input_word_ids, input_mask, segment_ids], outputs=[pooled_output, sequence_output])


# 获取bert的输入
def get_masks(tokens, max_seq_length):
    """Mask for padding"""
    if len(tokens) > max_seq_length:
        raise IndexError("Token length more than max seq length!")
    return [1] * len(tokens) + [0] * (max_seq_length - len(tokens))


def get_segments(tokens, max_seq_length):
    """Segments: 0 for the first sequence, 1 for the second"""
    if len(tokens) > max_seq_length:
        raise IndexError("Token length more than max seq length!")
    segments = []
    current_segment_id = 0
    for token in tokens:
        segments.append(current_segment_id)
        if token == "[SEP]":
            current_segment_id = 1
    return segments + [0] * (max_seq_length - len(tokens))


def get_ids(tokens, tokenizer, max_seq_length):
    """Token ids from Tokenizer vocab"""
    token_ids = tokenizer.convert_tokens_to_ids(tokens)
    input_ids = token_ids + [0] * (max_seq_length - len(token_ids))
    return input_ids


# 用bert提取特征向量
s = "This is a nice sentence."
tokenizer = FullTokenizer('D:/download/bert_en_uncased_L-12_H-768_A-12_2/assets/vocab.txt')
stokens = tokenizer.tokenize(s)
stokens = ["[CLS]"] + stokens + ["[SEP]"]

input_ids = get_ids(stokens, tokenizer, max_seq_length)
input_masks = get_masks(stokens, max_seq_length)
input_segments = get_segments(stokens, max_seq_length)

pool_embs, all_embs = model.predict([[input_ids], [input_masks], [input_segments]])

# 查看结果
print(pool_embs.shape, all_embs.shape)