import numpy as np
import tensorflow as tf
from tensorflow.python.keras.engine.base_layer import Layer
__all__ = ['element_cosine_distance','is_nan','is_abnormal_number']

from tensorflow_core.python.framework.ops import EagerTensor


def is_nan(x):
    if isinstance(x, (tf.Tensor, tf.Variable)):
        return tf.math.is_nan(x).any()
    elif isinstance(x,EagerTensor):
         return np.isnan(x.numpy()).any()
    elif isinstance(x,Layer):
        for para in x.weights:
            if tf.math.is_nan(para).any():
                return True
        return False
    elif isinstance(x, np.ndarray):
        return np.isnan(x).any()
    else:
        raise NotImplementedError

def is_abnormal_number(x):
    if isinstance(x,(tf.Tensor, tf.Variable)):
        return tf.math.is_nan(x).any() or  tf.math.is_inf(x).any()or tf.math.is_inf(-x).any()
    elif isinstance(x,Layer):
        for para in x.weights:
            if tf.math.is_nan(para).any() or tf.math.is_inf(para).any()or tf.math.is_inf(-para).any():
                return True
        return False
    elif isinstance(x, np.ndarray):
        return np.isnan(x).any() or np.isinf(x).any() or np.isneginf(x).any()
    else:
        raise NotImplementedError

def element_cosine_distance(v1, v2, axis=1):
    normalize_a = tf.nn.l2_normalize(v1, axis)
    normalize_b = tf.nn.l2_normalize(v2, axis)
    distance = tf.matmul(normalize_a, normalize_b, transpose_b=True)
    return distance
