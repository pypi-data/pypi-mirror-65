import os
import time

import pytest
import pytest_mock
import yaml

import meavis.instruments
import meavis.loop
import meavis.tasks


@pytest.fixture(scope="module")
def async_fixture(pytestconfig):
    mocker = pytest_mock.MockFixture(pytestconfig)
    meavis.instruments.clear("parameters")
    meavis.instruments.clear("measurements")
    meavis.instruments.clear("instruments")

    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "config",
            "async_instruments.yaml",
        )
    ) as file:
        instruments_config = yaml.safe_load(file)
        meavis.instruments.inject(instruments_config["instruments"])
        meavis.instruments.register(instruments_config["instances"])

    parameters = [
        meavis.parameters.loop_instance0.parameter0(range(10)),
    ]

    measurements = [
        meavis.measurements.loop_instance0.measurement0(),
        meavis.measurements.loop_instance1.measurement1(),
    ]

    parameter_apply_spies = [
        mocker.spy(parameter, "apply") for parameter in parameters
    ]
    measurement_trigger_spies = [
        mocker.spy(measurement, "trigger") for measurement in measurements
    ]
    measurement_wait_spies = [
        mocker.spy(measurement, "wait") for measurement in measurements
    ]

    meavis.loop.LoopEngine.clear()
    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "config",
            "default.yaml",
        )
    ) as file_default:
        meavis.loop.LoopEngine.default_map = yaml.safe_load(file_default)

    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "config", "async.yaml"
        )
    ) as file:
        measurement = meavis.loop.LoopEngine(yaml.safe_load(file)).create(
            parameters, measurements
        )
        clock = time.time()
        measurement.trigger(None)
        measurement.wait(None)
        clock = time.time() - clock

    return (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    )


def test_async_apply_count(async_fixture):
    (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = async_fixture

    assert parameter_apply_spies[0].call_count == 10


def test_async_trigger_count(async_fixture):
    (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = async_fixture

    assert measurement_trigger_spies[0].call_count == 10
    assert measurement_trigger_spies[1].call_count == 10


def test_async_wait_count(async_fixture):
    (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = async_fixture

    assert measurement_wait_spies[0].call_count == 10
    assert measurement_wait_spies[1].call_count == 10


def test_async_clock(async_fixture):
    (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = async_fixture

    assert clock < 1.2 * 10 * 0.1


@pytest.fixture(scope="module")
def invasive_fixture(pytestconfig):
    mocker = pytest_mock.MockFixture(pytestconfig)
    meavis.instruments.clear("parameters")
    meavis.instruments.clear("measurements")
    meavis.instruments.clear("instruments")

    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "config",
            "invasive_instruments.yaml",
        )
    ) as file:
        instruments_config = yaml.safe_load(file)
        meavis.instruments.inject(instruments_config["instruments"])
        meavis.instruments.register(instruments_config["instances"])

    parameters = [
        meavis.parameters.loop_instance0.parameter0(range(10)),
        meavis.parameters.loop_instance0.parameter1(range(1)),
    ]

    measurements = [
        meavis.measurements.loop_instance0.measurement0(),
        meavis.measurements.loop_instance0bis.measurement1(),
        meavis.measurements.loop_instance1.measurement2(),
        meavis.measurements.loop_instance0.measurement3(),
        meavis.measurements.loop_instance0.measurement4(),
        meavis.measurements.loop_instance1.measurement5(),
    ]

    parameter_apply_spies = [
        mocker.spy(parameter, "apply") for parameter in parameters
    ]
    measurement_trigger_spies = [
        mocker.spy(measurement, "trigger") for measurement in measurements
    ]
    measurement_wait_spies = [
        mocker.spy(measurement, "wait") for measurement in measurements
    ]

    meavis.loop.LoopEngine.clear()
    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "config",
            "default.yaml",
        )
    ) as file_default:
        meavis.loop.LoopEngine.default_map = yaml.safe_load(file_default)

    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "config",
            "invasive.yaml",
        )
    ) as file:
        measurement = meavis.loop.LoopEngine(yaml.safe_load(file)).create(
            parameters, measurements
        )
        clock = time.time()
        measurement.trigger(None)
        measurement.wait(None)
        clock = time.time() - clock

    return (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    )


def test_invasive_apply_count(invasive_fixture):
    (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = invasive_fixture

    assert parameter_apply_spies[0].call_count == 10
    assert parameter_apply_spies[1].call_count == 1


def test_invasive_trigger_count(invasive_fixture):
    (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = invasive_fixture

    assert measurement_trigger_spies[0].call_count == 10
    assert measurement_trigger_spies[1].call_count == 10
    assert measurement_trigger_spies[2].call_count == 10
    assert measurement_trigger_spies[3].call_count == 10


def test_invasive_wait_count(invasive_fixture):
    (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = invasive_fixture

    assert measurement_wait_spies[0].call_count == 10
    assert measurement_wait_spies[1].call_count == 10
    assert measurement_wait_spies[2].call_count == 10
    assert measurement_wait_spies[3].call_count == 10


def test_invasive_clock(invasive_fixture):
    (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = invasive_fixture

    assert 0.9 * 40 * 0.1 < clock < 1.2 * 40 * 0.1


@pytest.fixture(scope="module")
def settle_fixture(pytestconfig):
    mocker = pytest_mock.MockFixture(pytestconfig)
    meavis.instruments.clear("parameters")
    meavis.instruments.clear("measurements")
    meavis.instruments.clear("instruments")

    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "config",
            "settle_instruments.yaml",
        )
    ) as file:
        instruments_config = yaml.safe_load(file)
        meavis.instruments.inject(instruments_config["instruments"])
        meavis.instruments.register(instruments_config["instances"])

    parameters = [
        meavis.parameters.loop_instance0.parameter0(range(10)),
        meavis.parameters.loop_instance0.parameter1(range(2)),
    ]

    measurements = [
        meavis.measurements.loop_instance0.measurement0(),
        meavis.measurements.loop_instance0.measurement1(),
    ]

    parameter_apply_spies = [
        mocker.spy(parameter, "apply") for parameter in parameters
    ]
    measurement_trigger_spies = [
        mocker.spy(measurement, "trigger") for measurement in measurements
    ]
    measurement_wait_spies = [
        mocker.spy(measurement, "wait") for measurement in measurements
    ]

    meavis.loop.LoopEngine.clear()
    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "config",
            "default.yaml",
        )
    ) as file_default:
        meavis.loop.LoopEngine.default_map = yaml.safe_load(file_default)

    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "config", "settle.yaml"
        )
    ) as file:
        measurement = meavis.loop.LoopEngine(yaml.safe_load(file)).create(
            parameters, measurements
        )
        clock = time.time()
        measurement.trigger(None)
        measurement.wait(None)
        clock = time.time() - clock

    return (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    )


def test_settle_apply_count(settle_fixture):
    (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = settle_fixture

    assert parameter_apply_spies[0].call_count == 10
    assert parameter_apply_spies[1].call_count == 20


def test_settle_trigger_count(settle_fixture):
    (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = settle_fixture

    assert measurement_trigger_spies[0].call_count == 20
    assert measurement_trigger_spies[1].call_count == 20


def test_settle_wait_count(settle_fixture):
    (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = settle_fixture

    assert measurement_wait_spies[0].call_count == 20
    assert measurement_wait_spies[1].call_count == 20


def test_settle_clock(settle_fixture):
    (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = settle_fixture

    assert 0.9 * 20 * 0.1 < clock < 1.2 * 20 * 0.1


@pytest.fixture(scope="module")
def lock_instrument_fixture(pytestconfig):
    mocker = pytest_mock.MockFixture(pytestconfig)
    meavis.instruments.clear("parameters")
    meavis.instruments.clear("measurements")
    meavis.instruments.clear("instruments")

    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "config",
            "lock_instruments.yaml",
        )
    ) as file:
        instruments_config = yaml.safe_load(file)
        meavis.instruments.inject(instruments_config["instruments"])
        meavis.instruments.register(instruments_config["instances"])

    parameters = [
        meavis.parameters.loop_instance0.parameter0(range(10)),
    ]

    measurements = [
        meavis.measurements.loop_instance0.measurement0(),
        meavis.measurements.loop_instance0.measurement1(),
    ]

    parameter_apply_spies = [
        mocker.spy(parameter, "apply") for parameter in parameters
    ]
    measurement_trigger_spies = [
        mocker.spy(measurement, "trigger") for measurement in measurements
    ]
    measurement_wait_spies = [
        mocker.spy(measurement, "wait") for measurement in measurements
    ]

    meavis.loop.LoopEngine.clear()
    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "config",
            "default.yaml",
        )
    ) as file_default:
        meavis.loop.LoopEngine.default_map = yaml.safe_load(file_default)

    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "config", "lock.yaml"
        )
    ) as file:
        measurement = meavis.loop.LoopEngine(yaml.safe_load(file)).create(
            parameters, measurements
        )
        clock = time.time()
        measurement.trigger(None)
        measurement.wait(None)
        clock = time.time() - clock

    return (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    )


def test_lock_apply_count(lock_instrument_fixture):
    (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = lock_instrument_fixture

    assert parameter_apply_spies[0].call_count == 10


def test_lock_trigger_count(lock_instrument_fixture):
    (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = lock_instrument_fixture

    assert measurement_trigger_spies[0].call_count == 10
    assert measurement_trigger_spies[1].call_count == 10


def test_lock_wait_count(lock_instrument_fixture):
    (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = lock_instrument_fixture

    assert measurement_wait_spies[0].call_count == 10
    assert measurement_wait_spies[1].call_count == 10


def test_lock_clock(lock_instrument_fixture):
    (
        clock,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = lock_instrument_fixture

    assert 0.9 * 20 * 0.1 < clock < 1.2 * 20 * 0.1
