import pytest
import yaml

import meavis.instruments


@pytest.fixture
def setup():
    meavis.instruments.clear("parameters")
    meavis.instruments.clear("measurements")
    meavis.instruments.clear("instruments")


def test_measurement(setup):
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
"""
        )
    )

    measurement = (
        meavis.instruments.test_instrument.test_usage.measurements.measurement0
    )
    assert measurement._meavis_name == "measurement0"


def test_measurement_attribute(setup):
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
                    attributes:
                        key: value
"""
        )
    )

    measurement = (
        meavis.instruments.test_instrument.test_usage.measurements.measurement0
    )
    assert measurement._meavis_key == "value"


def test_measurement_kwargs(setup):
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
                    kwargs:
                        key: value
"""
        )
    )

    measurement = (
        meavis.instruments.test_instrument.test_usage.measurements.measurement0
    )
    assert measurement._meavis_kwargs == {"key": "value"}


def test_parameter(setup):
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
            parameters:
                parameter0:
                    name: DummyParameter
                    module: dummy_mock
"""
        )
    )

    parameter = (
        meavis.instruments.test_instrument.test_usage.parameters.parameter0
    )
    assert parameter._meavis_name == "parameter0"


def test_parameter_attribute(setup):
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
            parameters:
                parameter0:
                    name: DummyParameter
                    module: dummy_mock
                    attributes:
                        key: value
"""
        )
    )

    parameter = (
        meavis.instruments.test_instrument.test_usage.parameters.parameter0
    )
    assert parameter._meavis_key == "value"


def test_parameter_kwargs(setup):
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
            parameters:
                parameter0:
                    name: DummyParameter
                    module: dummy_mock
                    kwargs:
                        key: value
"""
        )
    )

    parameter = (
        meavis.instruments.test_instrument.test_usage.parameters.parameter0
    )
    assert parameter._meavis_kwargs == {"key": "value"}
