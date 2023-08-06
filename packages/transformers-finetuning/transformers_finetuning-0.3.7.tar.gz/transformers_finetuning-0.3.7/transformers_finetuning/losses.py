import tensorflow as tf

def binary_crossentropy(y_actual, y_pred, from_logits=True, loss_factor=1.0):

    total_loss = tf.keras.backend.binary_crossentropy(y_actual,y_pred,from_logits=from_logits)
    total_loss*=loss_factor

loss_collections = {
    'binary_crossentropy':binary_crossentropy
}

def main_loss_fn(loss_fn, max_seq_length=384, from_logits=True, loss_factor=1.0):

    def _loss_fn(labels, model_outputs):
        return loss_fn(labels, model_outputs, 
                        from_logits=from_logits, 
                        loss_factor=loss_factor)
    return _loss_fn

class Loss():
    def __init__(self,name):
        self.name = name

    def get_loss_fn(self, max_seq_length=384, from_logits=True, loss_factor=1.0):
        loss_fn = loss_collections[self.name]

        if loss_fn:
            return main_loss_fn(loss_fn, max_seq_length, from_logits, loss_factor)
        else:
            print('Loss Function Name not Found !')
            return None
    
    def get_loss_collection_names(self):

        return list(loss_collections.keys())
