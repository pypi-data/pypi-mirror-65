import base64
import importlib
import json
import pickle
from typing import Optional

import attr

from rho_ml.rho_model import RhoModel

# TODO: docstrings for *all* methods


@attr.s(auto_attribs=True, frozen=True)
class StoredModel(object):
    """ This stores the bytes of a serialized model, along with the module and
    qualified class name needed to correctly deserialize the model later.

    If the base_class is provided, that is the class which will be imported,
    and then wrapped with class_name as a subclass which differs from base_class
    only in name.  This is useful for the case where the same underlying model
    is used for multiple separate applications. """
    module_name: str
    class_name: str
    model_bytes: bytes = attr.ib(repr=False)
    base_class: Optional[str] = None

    @classmethod
    def from_model(cls,
                   model: RhoModel,
                   base_class_name: Optional[str] = None):
        return cls(module_name=model.__module__,
                   class_name=model.__class__.__qualname__,
                   model_bytes=model.serialize(),
                   base_class=base_class_name)

    def load_model(self) -> RhoModel:
        """ Use the instantiated StoredPredictor to load the Predictor using
        the appropriate class. """
        predictor_module = importlib.import_module(self.module_name)
        if self.base_class:
            base_cls = getattr(predictor_module, self.base_class)
            predictor_cls = type(self.class_name, (base_cls,), {})
        else:
            predictor_cls = getattr(predictor_module, self.class_name)
        predictor = predictor_cls.deserialize(self.model_bytes)
        predictor.__module__ = self.module_name
        predictor.__class__.__qualname__ = self.class_name
        return predictor

    def to_pickle(self) -> bytes:
        return pickle.dumps(self, protocol=4)

    @classmethod
    def from_pickle(cls, s: bytes) -> 'StoredModel':
        return pickle.loads(s)

    def to_json(self) -> str:
        """ JSON serialize the StoredPredictor so it can be saved to Redis, S3,
        etc. This uses base64 encoding on the predictor bytes, so it is often
        not going to be the most efficient way to store a given model. """
        # todo: deprecate me
        storage_dict = attr.asdict(self)
        storage_dict['model_bytes'] = base64.encodebytes(
            storage_dict['model_bytes']).decode('ascii')
        return json.dumps(storage_dict)

    @classmethod
    def from_json(cls, storage_json: str):
        # todo: deprecate me
        # add logging warning this is being deprecated
        storage_dict = json.loads(storage_json)
        encoded_model = storage_dict['model_bytes'].encode('ascii')
        storage_dict['model_bytes'] = base64.decodebytes(encoded_model)
        return cls(**storage_dict)
