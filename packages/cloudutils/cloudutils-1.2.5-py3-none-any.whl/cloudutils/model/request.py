# Copyright © 2020 Noel Kaczmarek
from spyne.model.complex import ComplexModel
from spyne.model.primitive import Mandatory


class RequestHeader(ComplexModel):
    __namespace__ = 'cloud'

    session = Mandatory.String
    user = Mandatory.String