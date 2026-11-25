"""Tiny GAN training exercise with synthetic data; no dataset download.
This is an environment check, not a research model or performance benchmark.
"""
import argparse
import numpy as np
import tensorflow as tf

parser = argparse.ArgumentParser()
parser.add_argument("--steps", type=int, default=20)
parser.add_argument("--require-gpu", action="store_true")
args = parser.parse_args()
if args.steps < 1 or args.steps > 1000:
    parser.error("Use 1 to 1000 steps for this small demonstration.")
gpus = tf.config.list_physical_devices("GPU")
if args.require_gpu and not gpus:
    raise SystemExit("No GPU visible. Check the allocated execution environment.")
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
tf.random.set_seed(42)
generator = tf.keras.Sequential([
    tf.keras.Input(shape=(16,)), tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(8)])
discriminator = tf.keras.Sequential([
    tf.keras.Input(shape=(8,)), tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dense(1)])
loss_fn = tf.keras.losses.BinaryCrossentropy(from_logits=True)
g_opt = tf.keras.optimizers.Adam(1e-3)
d_opt = tf.keras.optimizers.Adam(1e-3)
for step in range(args.steps):
    real = tf.random.normal((32, 8), mean=1.0)
    noise = tf.random.normal((32, 16))
    with tf.GradientTape() as gt, tf.GradientTape() as dt:
        fake = generator(noise, training=True)
        real_logits = discriminator(real, training=True)
        fake_logits = discriminator(fake, training=True)
        g_loss = loss_fn(tf.ones_like(fake_logits), fake_logits)
        d_loss = loss_fn(tf.ones_like(real_logits), real_logits) + loss_fn(tf.zeros_like(fake_logits), fake_logits)
    g_opt.apply_gradients(zip(gt.gradient(g_loss, generator.trainable_variables), generator.trainable_variables))
    d_opt.apply_gradients(zip(dt.gradient(d_loss, discriminator.trainable_variables), discriminator.trainable_variables))
    print(f"step={step + 1} generator_loss={float(g_loss):.4f} discriminator_loss={float(d_loss):.4f}", flush=True)
samples = generator(tf.random.normal((4, 16)), training=False).numpy()
np.save("gan-synthetic-samples.npy", samples)
print("Saved gan-synthetic-samples.npy; shape:", samples.shape)
