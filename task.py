import numpy as np
import tensorflow as tf
from tensorflow.contrib.layers import fully_connected
from dupl import environment
"""

DESCRIPTION : THIS CODE IS USED TO FINALLY TRAIN THE MODEL

"""
def normalize_rewards(reward_list , decay_rate) :
    new_list = []
    for index , each in enumerate(reward_list) :
        sum = 0
        count = 0
        for e in reward_list[index : len(reward_list)] :
            sum = sum + (decay_rate ** count) * e
            count = count + 1
        new_list.append(sum)
    std = np.std(new_list)
    mean = np.mean(new_list)
    list = [(element - mean) /std for element in new_list]
    return list



grad_l = []
reward_l = []
l_rate = 0.01###change is made here
n_iteration = 100000
gamma = 0.95
batch_size = 2000########case sensitive
n_step = 2000
done = False
epsilon_max = 1.0
epsilon_min = 0.0
eps_decay_steps = 400
step = 0

observation = tf.placeholder(tf.float32 , [None , 5] , name = "observation")
result = tf.placeholder(tf.float32 , [None , 4])

layer_1 = fully_connected(observation , 10 , activation_fn = tf.nn.tanh )############changing
mid_layer = fully_connected(layer_1 , 5 , activation_fn = tf.nn.relu)
layer_2 = fully_connected(mid_layer , 4 , activation_fn = tf.nn.relu )
softmax_probability = tf.nn.softmax(logits = layer_2)
max_softmax = tf.argmax(softmax_probability , axis = 1 , name = "max_softmax")
action = tf.multinomial(tf.log(softmax_probability) , 1 )
output_action = tf.multiply(action , 1 , name = "output_action")


loss = tf.nn.softmax_cross_entropy_with_logits(logits = layer_2 , labels = result)
optimizer = tf.train.AdamOptimizer(l_rate)
grads_vars = optimizer.compute_gradients(loss)
grads = [grad for grad , var in grads_vars]
placeholder_var = [(tf.placeholder(tf.float32 , grad.get_shape()) , var) for grad , var in grads_vars]
placeholder_list = [placeholder for placeholder , var in placeholder_var]
training_op = optimizer.apply_gradients(placeholder_var)

saver = tf.train.Saver()

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

all_rewards = []
all_grad_list = []
b_size = 0

for iteration in range(n_iteration) :
    env = environment()
    obs = env.state()   ### left_distance , front_distance , right_distance , dist_ball , angle_ball
    total_rewards = 0

    while True:
        obs = np.reshape(obs , [1 , 5])
        #env.render()
        act = sess.run(action , feed_dict= {observation : obs})###changed here
        res = np.zeros([1, 4])
        res[0][act[0][0]] = 1
        grad_list = sess.run(grads, feed_dict={observation: obs, result: res})###change made here
        env.action(act[0][0])
        env.control = True
        while env.control :
            env.core_loop()
        obs = env.state()
        reward = env.reward
        if step == n_step :
            done = True
            step = 0
            reward = -1
        total_rewards = total_rewards + reward
        grad_l.append(grad_list)
        reward_l.append(reward)
        b_size = b_size + 1
        if done :
            all_rewards.append(normalize_rewards(reward_l , gamma))
            reward_l = []
            all_grad_list.append(grad_l)
            grad_l = []
            print("Iteration : " , iteration , "Score : " , total_rewards)
            done = False
            break
        step = step + 1
    if b_size > batch_size :
        for index , episode in enumerate(all_rewards) :
            for ind , re in enumerate(episode) :
                all_grad_list[index][ind] = [element * re for element in all_grad_list[index][ind]]
        new_grad_list = []
        for index , element in enumerate(all_grad_list) :
            for ind , ele in enumerate(element):
                new_grad_list.append(ele)
        new_grad_list = np.mean(new_grad_list , axis = 0 )
        dict = {}
        for index , ph in enumerate(placeholder_list) :
            dict[ph] = new_grad_list[index]
        sess.run(training_op , feed_dict = dict)
        b_size = 0
        all_rewards = []
        all_grad_list = []
        print("############################Gradients are upgraded")
        saver.save(sess, "./model/saved_model")
        #print("***************************model saved********************************")













