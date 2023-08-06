import pytest
import yaml

import meavis.instruments


@pytest.fixture
def setup():
    meavis.instruments.clear("parameters")
    meavis.instruments.clear("measurements")
    meavis.instruments.clear("instruments")

    meavis.instruments.inject(
        yaml.safe_load(
            """
test_instrument:
    name: DummyConstructor
    module: dummy_mock
    usages:
        test_usage:
            name: DummyInitialiser
            module: dummy_mock
            measurements:
                measurement0:
                    name: DummyMeasurement
                    module: dummy_mock
            parameters:
                parameter0:
                    name: DummyParameter
                    module: dummy_mock
"""
        )
    )


def test_measurement(setup):
    meavis.instruments.register(
        yaml.safe_load(
            """
test_instance:
    instrument: test_instrument
    usage: test_usage
    kwargs:
        addr: localhost0
    attributes:
        channel: 0
"""
        )
    )

    measurement = meavis.measurements.test_instance.measurement0
    assert measurement._meavis_name == "measurement0"


def test_parameter(setup):
    meavis.instruments.register(
        yaml.safe_load(
            """
test_instance:
    instrument: test_instrument
    usage: test_usage
    kwargs:
        addr: localhost0
    attributes:
        channel: 0
"""
        )
    )

    parameter = meavis.parameters.test_instance.parameter0
    assert parameter._meavis_name == "parameter0"
