"""
This file contains code that will kick off training and testing processes
"""
import os
import json
import numpy as np

from experiments.UNetExperiment import UNetExperiment
from data_prep.HippocampusDatasetLoader import LoadHippocampusData


class Config:
    """
    Holds configuration parameters
    """

    def __init__(self):
        self.name = "Basic_unet"
        self.root_dir = r"./data/"
        self.n_epochs = 5
        self.learning_rate = 0.0002
        self.batch_size = 8
        self.patch_size = 64
        self.test_results_dir = "./out/"


if __name__ == "__main__":
    # Get configuration

    # TASK: Fill in parameters of the Config class and specify directory where the data is stored and
    # directory where results will go
    c = Config()

    # Load data
    print("Loading data...")

    # TASK: LoadHippocampusData is not complete. Go to the implementation and complete it.
    data = LoadHippocampusData(c.root_dir, y_shape=c.patch_size, z_shape=c.patch_size)

    # Create test-train-val split
    # In a real world scenario you would probably do multiple splits for
    # multi-fold training to improve your model quality

    keys = range(len(data))

    # Here, random permutation of keys array would be useful in case if we do something like
    # a k-fold training and combining the results.

    keys = np.array(keys)
    np.random.shuffle(keys)

    split = dict()

    # TASK: create three keys in the dictionary: "train", "val" and "test". In each key, store
    # the array with indices of training volumes to be used for training, validation
    # and testing respectively.
    train_size = 0.7
    valid_size = 0.2
    test_size = 0.1
    split["train"] = keys[: int(train_size * len(keys))]
    split["val"] = keys[
        int(train_size * len(keys)) : int((train_size + valid_size) * len(keys))
    ]
    split["test"] = keys[int((train_size + valid_size) * len(keys)) :]

    # Set up and run experiment

    # TASK: Class UNetExperiment has missing pieces. Go to the file and fill them in
    exp = UNetExperiment(c, split, data)

    # You could free up memory by deleting the dataset
    # as it has been copied into loaders
    del data

    # run training
    exp.run()

    # prep and run testing

    # TASK: Test method is not complete. Go to the method and complete it
    results_json = exp.run_test()

    results_json["config"] = vars(c)

    with open(os.path.join(exp.out_dir, "results.json"), "w") as out_file:
        json.dump(results_json, out_file, indent=2, separators=(",", ": "))
