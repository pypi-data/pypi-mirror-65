import collections
import functools
import hashlib
import inspect
import logging


def hash_setpair(set_pair, debug=False):
    if __debug__ or not debug:
        parameter_isinstance("set_pair", collections.abc.Set)
        return bytes(
            functools.reduce(lambda lhs, rhs: lhs ^ rhs, hash_bytes)
            for hash_bytes in zip(
                *(
                    hashlib.sha1(
                        "{}{}".format(key, value).lower().strip().encode()
                    ).digest()
                    for key, value in set_pair
                )
            )
        ).hex()

    return None


def name_isnotinjected(injected_name, module):
    if __debug__:
        name_split = injected_name.split(".")
        current = module
        for subname in name_split[:-1]:
            if not hasattr(current, subname):
                return
            current = getattr(current, subname)
        if hasattr(current, name_split[-1]):
            message = "{} @ {} is already injected.".format(
                injected_name, module.__name__
            )
            logging.getLogger("meavis").error(message)
            raise AssertionError(message)


def namespace_exists(injected_name, module):
    if __debug__:
        current = module
        for subname in injected_name.split("."):
            if not hasattr(current, subname):
                message = "{} @ {} does't exist.".format(
                    injected_name, module.__name__
                )
                logging.getLogger("meavis").error(message)
                raise AssertionError(message)
            current = getattr(current, subname)


def parameter_isinstance(obj_name, classinfo):
    if __debug__:
        caller = inspect.currentframe().f_back
        if not isinstance(caller.f_locals[obj_name], classinfo):
            message = "{} @ {} is {} should be {}.".format(
                obj_name,
                getattr(
                    caller.f_locals["self"], caller.f_code.co_name
                ).__name__,
                type(caller.f_locals[obj_name]).__name__,
                classinfo.__name__,
            )
            logging.getLogger("meavis").error(message)
            raise AssertionError(message)


def channel_notexist(initialiser):
    if (
        __debug__
        and initialiser._meavis_channel
        in initialiser._meavis_constructor._meavis_channels
    ):
        message = "Channel {} @ {} already used.".format(
            initialiser._meavis_channel,
            initialiser._meavis_constructor._meavis_name,
        )
        logging.getLogger("meavis").error(message)
        raise AssertionError(message)
