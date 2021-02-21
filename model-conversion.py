########################
#   Onnx -> Tensorflow
########################
import onnx
from onnx_tf.backend import prepare

onnx_model = onnx.load("../assets/yolov5.onnx")
tf_rep = prepare(onnx_model)
tf_rep.export_graph("../assets/tf-model")

##############################
#   Verifying the conversion
##############################

import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import tensorflow as tf

print(tf.__version__)

new_model = tf.saved_model.load("../assets/tensorflow-weights")
f = new_model.signatures["serving_default"]
out = f(images=tf.random.normal([2, 3, 640, 640]))
print(out["output_0"].shape)
print(out["output_1"].shape)
print(out["output_2"].shape)