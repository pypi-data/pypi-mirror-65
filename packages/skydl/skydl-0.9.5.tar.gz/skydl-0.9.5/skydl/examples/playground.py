import tensorflow as tf

# class A(tf.Module):
#     @tf.function
#     def func(self, x: "int"):
#         pass
#
# a = A()
# tf.saved_model.save(a, export_dir="/tmp/xxx")


@tf.function
def add(a, b):
    print("Tracing with....", a)
    return 3 * a ** 2 + b

v = tf.Variable(4.0)
with tf.GradientTape() as tape:
    result = add(v, 3.0)
    print(tape.gradient(result, v))