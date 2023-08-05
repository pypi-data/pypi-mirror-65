import numpy as np
import torch
import torchvision.models as models

from torch.nn import Softmax

from .resnetlabels import LabelDecoder
from ..classifier import Classifier


class _ResnetClassifier(Classifier):

    NAME = None
    _MODEL_CLS = None

    def __init__(self):
        self._model = self.__class__._MODEL_CLS(True, False)
        self._model.eval()  # No training today
        self._model.to(self.device)

    @property
    def device(self):
        return torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    def predict(self, dataset, decode=True, top=5):
        preds = []
        for d in dataset.loader():
            d = d.to(self.device)
            preds.append(
                Softmax(dim=1)(self._model(d)).data.cpu().numpy()
            )
            del d
        if not decode:
            return dict(zip(dataset.paths, np.concatenate(preds)))
        return dict(zip(dataset.paths, self.decode(np.concatenate(preds), top)))

    def decode(self, preds, top=3):
        return LabelDecoder.decode(preds, top=top)


class Resnet18Classifier(_ResnetClassifier):
    NAME = 'resnet18'
    _MODEL_CLS = models.resnet18


class Resnet34Classifier(_ResnetClassifier):
    NAME = 'resnet34'
    _MODEL_CLS = models.resnet34


class Resnet50Classifier(_ResnetClassifier):
    NAME = 'resnet50'
    _MODEL_CLS = models.resnet50


class Resnet101Classifier(_ResnetClassifier):
    NAME = 'resnet101'
    _MODEL_CLS = models.resnet101


class Resnet152Classifier(_ResnetClassifier):
    NAME = 'resnet152'
    _MODEL_CLS = models.resnet152


classifier = _ResnetClassifier.__subclasses__()
