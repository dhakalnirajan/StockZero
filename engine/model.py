import tensorflow as tf

class PolicyValueNetwork(tf.keras.Model):
    def __init__(self, num_moves):
        super(PolicyValueNetwork, self).__init__()
        self.conv1 = tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same', input_shape=(8, 8, 12))
        self.flatten = tf.keras.layers.Flatten()
        self.dense_policy = tf.keras.layers.Dense(num_moves, activation='softmax', name='policy_head')
        self.dense_value = tf.keras.layers.Dense(1, activation='tanh', name='value_head')

    def call(self, inputs):
        x = self.conv1(inputs)
        x = self.flatten(x)
        policy = self.dense_policy(x)
        value = self.dense_value(x)
        return policy, value