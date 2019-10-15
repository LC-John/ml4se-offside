import os
import time

import numpy as np
import tensorflow as tf

from Config import Config
from models.Code2VecCustomModel import Code2VecCustomModel
from models.CustomModel import CustomModel


def main() -> None:
    output_path = os.path.join(os.path.dirname(__file__), "resources", "models", "pre_trained", "model")
    X_train, Y_train = load_data("train_large_")
    X_val, Y_val = load_data("val_large_")
    X_test, Y_test = load_data("test_large_")

    print(Y_train.shape)
    print(Y_val.shape)
    print(Y_test.shape)

    config = Config(set_defaults=True)
    code2Vec = Code2VecCustomModel(config)
    code2Vec.load_weights("resources/models/custom/model")

    model = CustomModel(code2Vec)
    metrics = ['binary_accuracy']
    optimizer = tf.keras.optimizers.Adam()
    model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=metrics)

    callbacks = []
    callbacks.append(tf.keras.callbacks.EarlyStopping(monitor='val_binary_accuracy', min_delta=0, patience=1, restore_best_weights=True))


    batch_size = 1024 * 4
    model.fit(X_train, Y_train, validation_data=[X_val, Y_val], epochs=500, batch_size=batch_size, callbacks=callbacks)

    print(model.evaluate(X_test, Y_test, batch_size=batch_size))

    model.save_weights(output_path)

    print("shutting down")
    time.sleep(120)
    os.system("shutdown -s")


def load_data(prefix):
    Y = np.load("data/" + prefix + "Y.npy")
    path_source_token_idxs = np.load("data/" + prefix + "path_source_token_idxs.npy")
    path_idxs = np.load("data/" + prefix + "path_idxs.npy")
    path_target_token_idxs = np.load("data/" + prefix + "path_target_token_idxs.npy")
    context_valid_masks = np.load("data/" + prefix + "context_valid_masks.npy")
    X = [path_source_token_idxs, path_idxs, path_target_token_idxs, context_valid_masks]

    return X, Y

if __name__ == '__main__':
    main()