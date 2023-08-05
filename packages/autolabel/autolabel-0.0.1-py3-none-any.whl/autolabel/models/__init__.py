__all__ = [
    'models'
]


from .resnet import classifier as resnet_classifier

models = {
    cls.NAME: cls
    for cls in resnet_classifier
}
