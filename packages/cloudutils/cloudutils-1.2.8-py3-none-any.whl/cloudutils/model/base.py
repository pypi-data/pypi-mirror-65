# Copyright © 2020 Noel Kaczmarek
from spyne.model.complex import ComplexModelBase, ComplexModelMeta


class CloudModel(ComplexModelBase):
    __namespace__ = 'cloud'
    __metaclass__ = ComplexModelMeta