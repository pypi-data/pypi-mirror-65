# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import os


from .utils import object_hash


def meta_data_path():
    current_path = os.path.realpath(__file__)
    return current_path.rsplit("/", 1)[0] + "/meta_data/"


def model_path(model_id):
    return "model_id:" + model_id + "/"


def date_path(datetime):
    return "run_data/" + datetime + "/"


def meta_data_name(X, y):
    return "dataset_id:" + object_hash(X) + "_" + object_hash(y) + "_.csv"
