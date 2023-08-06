## CIFAR-10 Web

Load CIFAR-10 from user-specified directory (default /home/USER/data/cifar10 or Windows equivalent). Automatically download to that directory the CIFAR-10 tar file if not present.

### Install

```pip install cifar10_downloader```

### Usage

```
from cifar10_downloader import cifar10

train_images, train_labels, test_images, test_labels = cifar10(path=None)
```
