"""MeaVis parameters namespace for user-defined injection."""
import logging
import sys

import meavis._detail.debug


self_module = sys.modules[__name__]


def inject(cls, name):
    """Wrap and inject user-defined parameter in this namespace."""
    name_split = name.split(".")
    parameter_cls = meavis._detail.inject.inject_cls(
        cls,
        meavis._detail.inject.inject_namespace(
            ".".join(name_split[:-1]), self_module
        ),
        name_split[-1],
        name_split[-1],
    )
    logging.getLogger("meavis").info(
        "Register {} as parameter named {}.".format(
            cls.__name__,
            ".".join([part.lower().strip() for part in name_split]),
        )
    )
    return parameter_cls
