"""Main loop functions for running MeaVis measurements."""
import collections
import importlib
import logging
import sys
import threading

import meavis._detail.debug
import meavis._detail.inject
import meavis.measurements
import meavis.parameters


self_module = sys.modules[__name__]


def clear(module_name):
    """Clear injected names by users."""
    module = importlib.import_module("meavis.{}".format(module_name))
    for injected_name in [
        key
        for key, value in module.__dict__.items()
        if hasattr(value, "_meavis_injected") and value._meavis_injected
    ]:
        delattr(module, injected_name)
        logging.getLogger("meavis").info(
            "Unregister injected class named {}.".format(injected_name)
        )


def inject(instruments):
    """Inject instruments."""
    meavis._detail.debug.parameter_isinstance(
        "instruments", collections.abc.Mapping
    )

    for instrument_name, instrument in instruments.items():
        intrument_cls = meavis._detail.inject.inject_namespace(
            instrument_name, self_module
        )

        constructor_cls = meavis._detail.inject.inject_cls_by_dict(
            instrument,
            intrument_cls,
            "constructor",
            "{}.constructor".format(intrument_cls.__name__),
        )
        constructor_cls._meavis_map = {}

        for usage_name, usage in instrument["usages"].items():
            usage_cls = meavis._detail.inject.inject_namespace(
                usage_name, intrument_cls
            )

            meavis._detail.inject.inject_cls_by_dict(
                usage,
                usage_cls,
                "initialiser",
                "{}.{}.initialiser".format(
                    intrument_cls.__name__, usage_cls.__name__
                ),
            )

            parameters_cls = meavis._detail.inject.inject_namespace(
                "parameters", usage_cls
            )
            if "parameters" in usage:
                for parameter_name, parameter in usage["parameters"].items():
                    meavis._detail.inject.inject_cls_by_dict(
                        parameter,
                        parameters_cls,
                        parameter_name,
                        parameter_name,
                    )

            measurements_cls = meavis._detail.inject.inject_namespace(
                "measurements", usage_cls
            )
            if "measurements" in usage:
                for measurement_name, measurement in usage[
                    "measurements"
                ].items():
                    meavis._detail.inject.inject_cls_by_dict(
                        measurement,
                        measurements_cls,
                        measurement_name,
                        measurement_name,
                    )


def register(instances):
    """Inject instances."""
    meavis._detail.debug.parameter_isinstance(
        "instances", collections.abc.Mapping
    )

    for instance_name, instance in instances.items():
        meavis._detail.debug.name_isnotinjected(
            instance_name, meavis.parameters
        )
        meavis._detail.debug.name_isnotinjected(
            instance_name, meavis.measurements
        )

        instrument_cls = meavis._detail.inject.inject_namespace(
            instance["instrument"], self_module
        )
        constructor = (
            instrument_cls.constructor(**(instance["kwargs"]))
            if "kwargs" in instance
            else instrument_cls.constructor()
        )
        constructor._meavis_hash = meavis._detail.debug.hash_setpair(
            frozenset(constructor._meavis_kwargs.items())
        )
        if constructor._meavis_hash not in constructor._meavis_map:
            constructor._meavis_map[constructor._meavis_hash] = constructor
            constructor._meavis_handler = None
            constructor._meavis_channels = set()
            constructor._meavis_lock = threading.Lock()
            logging.getLogger("meavis").info(
                "Register {} constructor [{}] {{{}}}.".format(
                    instance["instrument"],
                    constructor._meavis_hash if __debug__ else None,
                    ", ".join(
                        "{}: {}".format(key, value)
                        for key, value in constructor._meavis_kwargs.items()
                    ),
                )
            )

        usage_cls = meavis._detail.inject.inject_namespace(
            instance["usage"], instrument_cls
        )
        initialiser = usage_cls.initialiser()
        initialiser._meavis_constructor = constructor._meavis_map[
            constructor._meavis_hash
        ]
        initialiser._meavis_handler = None
        initialiser._meavis_lock = initialiser._meavis_constructor._meavis_lock
        logging.getLogger("meavis").info(
            "Register {} initialiser {{{}}} for {}.".format(
                instance["usage"],
                ", ".join(
                    "{}: {}".format(key, value)
                    for key, value in initialiser._meavis_kwargs.items()
                ),
                instance_name,
            )
        )
        for key, value in instance["attributes"].items():
            setattr(
                initialiser, "_meavis_{}".format(key.lower().strip()), value
            )

        for parameter in [
            value
            for value in usage_cls.parameters.__dict__.values()
            if hasattr(value, "_meavis_injected") and value._meavis_injected
        ]:
            injected_parameter = meavis.parameters.inject(
                parameter,
                "{}.{}".format(instance_name, parameter._meavis_name),
            )
            injected_parameter._meavis_initialiser = initialiser

        for measurement in [
            value
            for value in usage_cls.measurements.__dict__.values()
            if hasattr(value, "_meavis_injected") and value._meavis_injected
        ]:
            injected_measurement = meavis.measurements.inject(
                measurement,
                "{}.{}".format(instance_name, measurement._meavis_name),
            )
            injected_measurement._meavis_initialiser = initialiser
