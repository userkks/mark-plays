import tensorflow as tf
from dupl import environment
import numpy as np
"""

DESCRIPTION : HERE THE FINAL TRAINED MODEL IS USED TO RUN THE ENVIRONMENT

"""
sess = tf.Session()

saver = tf.train.import_meta_graph("./model/saved_model.meta")
saver.restore(sess , tf.train.latest_checkpoint("./model"))

graph = tf.get_default_graph()
ph = graph.get_tensor_by_name("observation:0")
max = graph.get_tensor_by_name("output_action:0")
#action = graph.get_operation_by_name("output")
env = environment()
state = env.state()
env.control = False

while True :
    state = np.reshape(state , [1 , 5])
    if not env.control :
        act = sess.run(max , feed_dict = {ph : state})[0][0]
        env.action(act)
    env.control = True
    env.core_loop()
    state = env.state()
    env.render()
    env.fps()






