import argparse

import numpy as np
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score

from Config import Config
from models.Code2VecCustomModel import Code2VecCustomModel
from models.CustomModel import CustomModel

parser = argparse.ArgumentParser()
parser.add_argument(
    "-w", "--weights", default="resources/models/custom3/model", help="path to the weights of the trained network"
)
parser.add_argument(
    "-d", "--dataset", default="data/test_",
    help="path to the train data set of format: <path>/<prefix>. It auto reads in all sub components at that path"
)
parser.add_argument(
    "-t", "--threshold", default="0.5", help="the bug classification threshold"
)
parser.add_argument(
    "-b", "--batch_size", default="1024", help="path to the output folder"
)
args = parser.parse_args()


def main() -> None:
    # Config
    batch_size = int(args.batch_size)
    threshold = float(args.threshold)
    X_test, Y_test = load_data(args.dataset)
    config = Config(set_defaults=True)

    # Load model
    code2Vec = Code2VecCustomModel(config)
    model = CustomModel(code2Vec)
    model.load_weights(args.weights)
    metrics = ['binary_accuracy']
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=metrics)

    # Eval test loss
    test_loss, accuracy = model.evaluate(X_test, Y_test, batch_size=batch_size)

    # Make predictions
    Y_pred = model.predict(X_test, batch_size=batch_size)
    Y_pred = np.where(Y_pred >= threshold, np.ones_like(Y_pred), np.zeros_like(Y_pred))

    # Print results.
    print("confusion_matrix")
    print(confusion_matrix(Y_test, Y_pred))

    print("test_loss")
    print(test_loss)

    print("accuracy")
    print(accuracy)

    print("f1_score")
    print(f1_score(Y_test, Y_pred))

    print("precision_score")
    print(precision_score(Y_test, Y_pred))

    print("recall_score")
    print(recall_score(Y_test, Y_pred))


def load_data(path_to):
    """
    Loads all the sub part in of the data set at onces.
    :param path_to: <PathToFolder>/<Prefix>
    :return:
    """
    Y = np.load(path_to + "Y.npy")
    path_source_token_idxs = np.load(path_to + "path_source_token_idxs.npy")
    path_idxs = np.load(path_to + "path_idxs.npy")
    path_target_token_idxs = np.load(path_to + "path_target_token_idxs.npy")
    context_valid_masks = np.load(path_to + "context_valid_masks.npy")
    X = path_source_token_idxs, path_idxs, path_target_token_idxs, context_valid_masks

    return X, Y


if __name__ == '__main__':
    main()
