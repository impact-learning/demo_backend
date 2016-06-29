import tensorflow as tf
import rethinkdb as r
import numpy as np
import pandas as pd
from demo_backend.models import db
from demo_backend.settings import ProdConfig
from sklearn.feature_extraction import DictVectorizer


def preprocessing_data():
    conn = r.connect(ProdConfig.DB_HOST, ProdConfig.DB_PORT)
    cursor = db.table('township_village') \
        .pluck(['county', 'township', 'village', 'scores', 'average_income_per_capita']).run(conn)
    villages = []

    for item in cursor:
        incomes = []
        for income in item['average_income_per_capita']:
            data = {}
            data['avg_income'] = np.sum([
                income['distribution']['below_5k'] * 2500,
                income['distribution']['5k_10k'] * (5000 + 10000) / 2,
                income['distribution']['10k_15k'] * (10000 + 15000) / 2,
                income['distribution']['15k_20k'] * (15000 + 20000) / 2,
                income['distribution']['20k_25k'] * (20000 + 25000) / 2,
                income['distribution']['above_25k'] * 25000,
            ])
            data['year'] = income['year']
            incomes.append(data)

        result = pd.merge(pd.DataFrame(incomes), pd.DataFrame(item['scores']), on='year')
        result['township'] = item['township']
        result['village'] = item['village']
        villages.append(result)

    conn.close()
    return pd.concat(villages)


def train_model():
    data = preprocessing_data()

    # Parameters
    learning_rate = 0.01
    training_epochs = 25
    batch_size = 100
    display_step = 1

    # tf Graph Input
    x = tf.placeholder(tf.float32, [None, 21])
    y = tf.placeholder(tf.float32, [None, 1])

    # Set model weights
    w = tf.Variable(tf.zeros([21, 1]))
    b = tf.Variable(tf.zeros([1]))

    # Construct model
    pred = tf.nn.softmax(tf.matmul(x, w) + b)  # Softmax

    # Minimize error using cross entropy
    cost = tf.reduce_mean(-tf.reduce_sum(y * tf.log(pred), reduction_indices=1))
    # Gradient Descent
    optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

    # Initializing the variables
    init = tf.initialize_all_variables()

    # Launch the graph
    with tf.Session() as sess:
        sess.run(init)

        # Training cycle
        for epoch in range(training_epochs):
            avg_cost = 0.
            total_batch = int(len(data['data']) / batch_size)
            # Loop over all batches
            for i in range(total_batch):
                batch_xs, batch_ys = data['data'][:batch_size]
                # Fit training using batch data
                _, c = sess.run([optimizer, cost], feed_dict={x: batch_xs, y: batch_ys})
                # Compute average loss
                avg_cost += c / total_batch
            # Display logs per epoch step
            if (epoch + 1) % display_step == 0:
                print "Epoch:", '%04d' % (epoch + 1), "cost=", "{:.9f}".format(avg_cost)

        print "Optimization Finished!"

        # Test model
        correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
        # Calculate accuracy for 3000 examples
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        print "Accuracy:", accuracy.eval({x: mnist.test.images[:3000], y: mnist.test.labels[:3000]})
