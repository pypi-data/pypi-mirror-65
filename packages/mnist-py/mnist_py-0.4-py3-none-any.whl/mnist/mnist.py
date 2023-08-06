from collections import namedtuple
from pathlib import Path
from random import choice, shuffle
from typing import Generator
import zlib

import numpy as np
import requests


URL_BASE = 'http://yann.lecun.com/exdb/mnist'
CACHE_DIR = Path('/', 'tmp', 'mnist')


mnist = namedtuple('mnist', 'train test')
dataset = namedtuple('dataset', 'images labels')


def raw_bytes(filename: str, offset: int) -> np.array:
    cached_file = Path(CACHE_DIR, filename)
    if not cached_file.exists():
        with requests.get(f'{URL_BASE}/{filename}') as resp:
            resp.raise_for_status()
            with open(cached_file, 'wb') as f:
                f.write(resp.content)
    with open(cached_file, 'rb') as f:
        raw_bytes = zlib.decompress(f.read(), 15 + 32)
    return np.frombuffer(raw_bytes, '>B', offset=offset)


def images(filename: str) -> np.array:
    """Return zero-to-one scaled images as rows of a matrix."""
    return raw_bytes(filename, offset=16).reshape(-1, 784) / 255


def labels(filename: str) -> np.array:
    """Return one-hot encoded class labels as rows of a matrix."""
    return np.eye(10)[raw_bytes(filename, offset=8)]


def load_mnist() -> namedtuple:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return mnist(
        train=dataset(
            images=images('train-images-idx3-ubyte.gz'),
            labels=labels('train-labels-idx1-ubyte.gz'),
        ),
        test=dataset(
            images=images('t10k-images-idx3-ubyte.gz'),
            labels=labels('t10k-labels-idx1-ubyte.gz'),
        ),
    )


def render(train_or_test: str = 'train') -> None:
    mnist = load_mnist()

    while True:

        if train_or_test == 'train':
            idx = choice(range(60000))
            image = mnist.train.images[idx]
            label = mnist.train.labels[idx]

        elif train_or_test == 'test':
            idx = choice(range(10000))
            image = mnist.test.images[idx]
            label = mnist.test.labels[idx]

        else:
            raise ValueError(f'Unrecognized dataset: {train_or_test}')

        for row in image.reshape(28, 28):
            for col in row:
                if col > 0.5:
                    print('@', end='', flush=True)
                else:
                    print(' ', end='', flush=True)
            print()
        print(f'Label: {label.argmax()}')

        if input('Show another? ([y]/n): ') not in ('Y', 'y', ''):
            break


def minibatches(
    batch_size: int = 256,
    n_epochs: int = 1,
) -> Generator[dataset, None, None]:

    mnist = load_mnist()

    for _ in range(n_epochs):
        images = mnist.train.images
        labels = mnist.train.labels

        together = [(img, lbl) for img, lbl in zip(images, labels)]
        shuffle(together)
        images[:], labels[:] = zip(*together)

        for idx in range(0, len(images), batch_size):
            yield dataset(
                images=images[idx:idx + batch_size],
                labels=labels[idx:idx + batch_size],
            )


def accuracy(
    predicted_labels: np.array,
    actual_labels: np.array,
) -> float:

    return np.mean(
        predicted_labels.argmax(1)
        == actual_labels.argmax(1)
    )
