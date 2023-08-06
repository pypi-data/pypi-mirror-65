from transformers import *
from transformers.modeling_tf_albert import *
import tensorflow as tf


model_collections = {
    'albert':TFAlbertModel
}

model_type_map = {
    'multi-class':'softmax',
    'multi-label':'sigmoid'
}

class ClassificationModel():

    def __init__(self, model_type, based_on, max_seq_len, num_output_neurons, config=None, pretrained_path=None):
        
        if not config and not pretrained_path:
            print('Error: Give either Pretrained Path or Config Object')

        self.model_type = model_type
        self.based_on = based_on
        self.config = config
        self.max_seq_len = max_seq_len
        self.num_output_neurons = num_output_neurons
        self.pretrained_path = pretrained_path

    def get_model(self):

        input_word_ids = tf.keras.layers.Input(shape=(self.max_seq_len,), name='input_word_ids', dtype=tf.int32)
        
        if self.pretrained_path:
            base_model = model_collections[self.based_on].from_pretrained(self.pretrained_path)
        elif self.config:
            base_model = model_collections[self.based_on](self.config)
        else:
            print('Error: Give either Pretrained Path or Config Object')
        base_model_layer = base_model(input_word_ids)
        output_layer = tf.keras.layers.Dense(self.num_output_neurons, activation=model_type_map[self.model_type])(base_model_layer[1])

        model = tf.keras.Model(input_word_ids, output_layer)
        print(model.summary())
        return model
