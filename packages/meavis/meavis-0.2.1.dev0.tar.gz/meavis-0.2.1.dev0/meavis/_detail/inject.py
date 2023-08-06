import collections
import importlib
import logging

import meavis._detail.debug


def inject_cls(cls, dst_module, injected_name, meavis_name):
    injected_name_strip = injected_name.lower().strip()
    meavis._detail.debug.name_isnotinjected(injected_name_strip, dst_module)

    meavis_name_strip = meavis_name.lower().strip()

    class Wrapper(cls):
        _meavis_injected = True
        _meavis_name = meavis_name_strip
        _meavis_logger = logging.getLogger("meavis")

        def __init__(self, *args, **kwargs):
            if hasattr(self, "_meavis_kwargs"):
                for key, value in self._meavis_kwargs.items():
                    if key not in kwargs:
                        kwargs[key] = value
            super().__init__(*args, **kwargs)
            self._meavis_kwargs = kwargs
            for key, value in self._meavis_kwargs.items():
                meavis_key = "_meavis_{}".format(key.lower().strip())
                setattr(self, meavis_key, value)
                self._meavis_logger.debug(
                    "\tAdd attribute self.{} = {} to {}.".format(
                        meavis_key, value, self._meavis_name
                    )
                )

    setattr(dst_module, injected_name_strip, Wrapper)
    injected_cls = getattr(dst_module, injected_name_strip)
    injected_cls.__name__ = injected_name_strip
    logging.getLogger("meavis").debug(
        "Inject {} in {} as {}.".format(
            cls.__name__, dst_module.__name__, injected_cls._meavis_name
        )
    )

    return injected_cls


def inject_cls_by_dict(cls_map, dst_module, injected_name, meavis_name):
    meavis._detail.debug.parameter_isinstance(
        "cls_map", collections.abc.Mapping
    )

    injected_cls = inject_cls(
        getattr(importlib.import_module(cls_map["module"]), cls_map["name"]),
        dst_module,
        injected_name,
        meavis_name,
    )

    if "kwargs" in cls_map:
        injected_cls._meavis_kwargs = cls_map["kwargs"]
        logging.getLogger("meavis").debug(
            "\tAdd self._meavis_kwargs to {}.".format(
                injected_cls._meavis_name
            )
        )

    if "attributes" in cls_map:
        for key, value in cls_map["attributes"].items():
            meavis_key = "_meavis_{}".format(key.lower().strip())
            meavis._detail.debug.name_isnotinjected(meavis_key, injected_cls)
            setattr(injected_cls, meavis_key, value)
            logging.getLogger("meavis").debug(
                "\tAdd attribute cls.{} = {} to {}.".format(
                    meavis_key, value, injected_cls.__name__
                )
            )

    return injected_cls


def inject_namespace(name, dst_module):
    result_namespace = dst_module
    if not name:
        return result_namespace

    for subname in [part.lower().strip() for part in name.split(".")]:
        if not hasattr(result_namespace, subname):

            class Namespace:
                _meavis_injected = True

            setattr(result_namespace, subname, Namespace)
            namespace_cls = getattr(result_namespace, subname)
            namespace_cls.__name__ = subname
            logging.getLogger("meavis").debug(
                "Inject {} in {}.".format(
                    namespace_cls.__name__, result_namespace.__name__
                )
            )
            result_namespace = namespace_cls
        else:
            result_namespace = getattr(result_namespace, subname)

    return result_namespace
