"""Small TensorFlow GPU check. Run only on an allocated GPU."""
import tensorflow as tf

print("TensorFlow:", tf.__version__)
gpus = tf.config.list_physical_devices("GPU")
print("Visible GPUs:", gpus)
if not gpus:
    raise SystemExit("No GPU visible: check allocation, driver and runtime compatibility.")
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
with tf.device("/GPU:0"):
    x = tf.ones((512, 512))
    y = tf.linalg.matmul(x, x)
    print("Device:", y.device, "Checksum:", float(tf.reduce_sum(y).numpy()))
