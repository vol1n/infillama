from util import *
from examples import dataset_generator

BASE_MODEL = ""

if __name__ == '__main__':
    teacher_base = load_base_model()
    training_params = get_training_params()
    O
    train(teacher_base, training_params, "models/")
