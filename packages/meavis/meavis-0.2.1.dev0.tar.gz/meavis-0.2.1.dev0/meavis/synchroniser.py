"""Synchronisation of MeaVis parameters."""
import collections
import itertools
import logging
import threading

import meavis._detail.debug
import meavis.tasks


class LoopSynchroniser:
    """Define a looper to pre-synchronise instruments."""

    def __init__(self, state_parameters, loop_parameters, synchronisers):
        """Ceate a loop synchroniser."""
        meavis._detail.debug.parameter_isinstance(
            "state_parameters", collections.abc.Sequence
        )
        meavis._detail.debug.parameter_isinstance(
            "loop_parameters", collections.abc.Sequence
        )
        meavis._detail.debug.parameter_isinstance(
            "synchronisers", collections.abc.Sequence
        )

        self.state_parameters = state_parameters
        self.loop_parameters = loop_parameters
        self.synchronisers = synchronisers

        self._meavis_logger = logging.getLogger("meavis")

    def pre_synchronise(self, states):
        """Run the loop."""
        meavis._detail.debug.parameter_isinstance(
            "states", collections.abc.MutableSet
        )

        for samples in itertools.product(
            *(parameter.data for parameter in self.loop_parameters)
        ):
            parameter_tasks = []
            parameter_locks = [threading.Lock()]
            for parameter, sample in zip(self.loop_parameters, samples):
                if sample == parameter._meavis_current:
                    continue
                parameter_locks.append(threading.Lock())
                parameter_locks[-1].acquire()
                parameter_tasks.append(
                    threading.Thread(
                        target=meavis.tasks.settle,
                        args=(
                            parameter,
                            sample,
                            parameter_locks[-2],
                            parameter_locks[-1],
                            False,
                        ),
                    )
                )
                parameter_tasks[-1].start()

            self._meavis_logger.debug("\tJoin parameter tasks.")
            for task in parameter_tasks:
                task.join()

            if self.synchronisers:
                for synchroniser in self.synchronisers:
                    states = synchroniser.pre_synchronise(states)
            else:
                state = frozenset(
                    (parameter._meavis_name, parameter._meavis_current)
                    for parameter in self.state_parameters
                )
                if state in states:
                    continue
                self._meavis_logger.info(
                    "Register [{}] {{{}}} to synchronise.".format(
                        meavis._detail.debug.hash_setpair(state, debug=True),
                        ", ".join(
                            "{}: {}".format(key, value) for key, value in state
                        ),
                    )
                )
                states.add(state)

        return states
