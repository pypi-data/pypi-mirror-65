import tensorflow as tf
from tensorflow.python.keras import backend as K

def compile_model(model,config):
    output_type = config['output_type']
    is_amp = config['is_amp']

    # 正则化
    # if regularizers_l2:
    #     for layer in model.layers:
    #         if hasattr(layer, 'kernel_regularizer'):
    #             layer.kernel_regularizer = regularizers.l2(0.000001)

    # loss
    loss = {
        'multi_class': 'categorical_crossentropy',
        'multi_label': 'binary_crossentropy',
        'regression': 'mean_squared_error',
        'multi_regression': 'mean_squared_error'
    }[output_type]
    # opt
    opt = tf.keras.optimizers.Adam()
    if is_amp:
        opt = tf.train.experimental.enable_mixed_precision_graph_rewrite(opt)
    # metrics
    metrics = {
        'multi_class': ['accuracy'],
        'multi_label': ['binary_accuracy'],
        'regression': ['mae']
    }[output_type]

    model.compile(loss=loss,
                  optimizer=opt,
                  metrics=metrics)

    sess = K.get_session()
    sess.run(tf.compat.v1.local_variables_initializer())
    sess.run(tf.compat.v1.global_variables_initializer())
    sess.run(tf.compat.v1.tables_initializer())
    return model,sess