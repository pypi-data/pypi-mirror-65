from __future__ import absolute_import
from __future__ import division
from __future__ import print_function



from ray.rllib.models.model import Model
from ray.rllib.models.tf.misc import normc_initializer, get_activation_fn
from ray.rllib.utils.annotations import override
from ray.rllib.utils import try_import_tf

from rslib.algo.transformer.contrib import embedding

tf = try_import_tf()


class FullyConnectedNetwork(Model):
    """Generic fully connected network."""

    @override(Model)
    def _build_layers(self, inputs, num_outputs, options):
        """Process the flattened inputs.

        Note that dict inputs will be flattened into a vector. To define a
        model that processes the components separately, use _build_layers_v2().
        """
        hiddens = options.get("fcnet_hiddens")
        activation = get_activation_fn(options.get("fcnet_activation"))

        step = tf.cast(inputs[:, 0:1], tf.int32)
        feature = inputs[:, 301:]

        # history award emb
        step_emb = embedding(step, vocab_size=10, num_units=32, scale=False, scope='enc_embed')[:, 0]
        inputs = tf.concat([step_emb, feature], axis=1)
        with tf.name_scope("fc_net"):
            i = 1
            last_layer = inputs
            for size in hiddens:
                label = "fc{}".format(i)
                last_layer = tf.layers.dense(
                    last_layer,
                    size,
                    kernel_initializer=normc_initializer(1.0),
                    activation=activation,
                    name=label)
                i += 1
            label = "fc_out"
            output = tf.layers.dense(
                last_layer,
                num_outputs,
                kernel_initializer=normc_initializer(0.01),
                activation=None,
                name=label)
            return output, last_layer
