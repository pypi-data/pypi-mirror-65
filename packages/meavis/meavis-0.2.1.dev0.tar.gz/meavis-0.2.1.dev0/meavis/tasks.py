"""MeaVis tasks for threading."""
import logging
import threading
import time

import meavis._detail.debug


def setup_and_acquire(meavis_item):
    """Set meavis_item handler if required."""
    if meavis_item._meavis_handler:
        meavis_item._meavis_lock.acquire()
        return meavis_item._meavis_lock

    if meavis_item._meavis_initialiser:
        initialiser = meavis_item._meavis_initialiser
        initialiser._meavis_lock.acquire()
        if not initialiser._meavis_handler:
            constructor = initialiser._meavis_constructor
            constructor._meavis_handler = constructor.create()
            logging.getLogger("meavis").info(
                "Create handler of {} [{}] with {{{}}}.".format(
                    constructor._meavis_name,
                    constructor._meavis_hash,
                    ", ".join(
                        "{}: {}".format(key, value)
                        for key, value in constructor._meavis_kwargs.items()
                    ),
                )
            )

            meavis._detail.debug.channel_notexist(initialiser)
            initialiser._meavis_handler = initialiser.initialise(
                constructor._meavis_handler, initialiser._meavis_channel
            )
            logging.getLogger("meavis").info(
                "Initialise channel {} on handler of {} with {{{}}}.".format(
                    initialiser._meavis_channel,
                    initialiser._meavis_name,
                    ", ".join(
                        "{}: {}".format(key, value)
                        for key, value in initialiser._meavis_kwargs.items()
                    ),
                )
            )
        meavis_item._meavis_handler = initialiser._meavis_handler
        meavis_item._meavis_lock = initialiser._meavis_lock
    else:
        meavis_item._meavis_handler = meavis_item
        meavis_item._meavis_lock = threading.Lock()
        meavis_item._meavis_lock.acquire()

    return meavis_item._meavis_lock


def settle(parameter, sample, lock_in, lock_out, delay=True):
    """Settle a parameter."""
    lock_in.acquire()
    lock_instrument = setup_and_acquire(parameter)
    parameter.apply(parameter._meavis_handler, sample)
    parameter._meavis_current = sample
    logging.getLogger("meavis").info(
        "Set {} to {}{}.".format(
            parameter._meavis_name,
            sample,
            ""
            if parameter._meavis_unit is None
            else " {}".format(parameter._meavis_unit),
        )
    )
    lock_instrument.release()
    lock_out.release()

    if delay:
        time.sleep(parameter._meavis_delay)
    lock_instrument.acquire()
    cond_is_settle = parameter.is_settled(parameter._meavis_handler)
    lock_instrument.release()
    while not cond_is_settle:
        lock_instrument.acquire()
        cond_is_settle = parameter.is_settled(parameter._meavis_handler)
        lock_instrument.release()
        if delay:
            time.sleep(parameter._meavis_delay)


def trigger_wait(measurement, lock_in, lock_out, lock_barrier):
    """Trigger & wait for a measurement."""
    lock_in.acquire()
    lock_instrument = setup_and_acquire(measurement)
    measurement.trigger(measurement._meavis_handler)
    if hasattr(measurement, "_meavis_name"):
        logging.getLogger("meavis").info(
            "Trigger {}, waiting for data.".format(measurement._meavis_name)
        )
    if not measurement._meavis_invasive:
        lock_out.release()
    lock_instrument.release()

    lock_barrier.acquire()

    lock_instrument.acquire()
    measurement.wait(measurement._meavis_handler)
    lock_instrument.release()

    if measurement._meavis_invasive:
        lock_out.release()
