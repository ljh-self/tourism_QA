import csv
import os

from statsmodels.regression.tests.test_rolling import tf
from wordcloud import tokenization


def get_train_examples(self, data_dir):
    """See base class."""
    return self._create_examples(
        self._read_tsv(os.path.join(data_dir, "train.tsv")), "train")


def get_dev_examples(self, data_dir):
    """See base class."""
    return self._create_examples(
        self._read_tsv(os.path.join(data_dir, "dev.tsv")), "dev")


def get_test_examples(self, data_dir):
    """See base class."""
    return self._create_examples(
        self._read_tsv(os.path.join(data_dir, "test.tsv")), "test")


def get_labels(self):
    """See base class."""
    return ["0", "1", "2", "3", "4", "5", "6", "7"]


def _read_csv(self, data_dir, file_name):
    with tf.gfile.Open(data_dir + file_name, "r") as f:
        reader = csv.reader(f, delimiter=",", quotechar=None)
        lines = []
        for line in reader:
            lines.append(line)

    return lines


def _get_train_examples(self, data_dir):
    file_path = os.path.join(data_dir, 'train.csv')
    with open(file_path, 'r') as f:
        reader = f.readlines()
    examples = []
    for index, line in enumerate(reader):
        guid = 'train-%d'%index
        split_line = line.strip().split(',')
        text_a = tokenization.convert_to_unicode(split_line[1])
        text_b = tokenization.convert_to_unicode(split_line[2])
        label = split_line[0]
        examples.append(InputExample(guid = guid, text_a = text_a, text_b = text_b, label = label))
    return examples



def _create_examples(self, lines, set_type):
    """Creates examples for the training and dev sets."""
    examples = []
    for (i, line) in enumerate(lines):
        if i == 0:
            continue
        guid = "%s-%s" % (set_type, i)
        text_a = tokenization.convert_to_unicode(line[3])
        text_b = tokenization.convert_to_unicode(line[4])
        if set_type == "test":
            label = "0"
        else:
            label = tokenization.convert_to_unicode(line[0])
        examples.append(
            InputExample(guid=guid, text_a=text_a, text_b=text_b, label=label))
    return examples
