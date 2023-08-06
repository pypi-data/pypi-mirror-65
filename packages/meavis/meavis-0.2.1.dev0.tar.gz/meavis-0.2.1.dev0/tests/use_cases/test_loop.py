import logging
import os

import pytest
import pytest_mock
import yaml

import meavis.instruments
import meavis.loop


@pytest.fixture(scope="module")
def loop_fixture(pytestconfig):
    mocker = pytest_mock.MockFixture(pytestconfig)
    log_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "log_ref", "test_loop.log"
    )
    ch = logging.FileHandler(log_file, mode="w")
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(message)s"))
    logging.getLogger("meavis").addHandler(ch)
    logging.basicConfig(
        filename="test_loop.log",
        filemode="w",
        format="%(message)s",
        level=logging.INFO,
    )
    meavis.instruments.clear("parameters")
    meavis.instruments.clear("measurements")
    meavis.instruments.clear("instruments")

    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "config",
            "loop_instruments.yaml",
        )
    ) as file:
        instruments_config = yaml.safe_load(file)
        meavis.instruments.inject(instruments_config["instruments"])
        meavis.instruments.register(instruments_config["instances"])

    parameters = [
        meavis.parameters.loop_instance0.parameter0([0, 1]),
        meavis.parameters.loop_instance0.parameter1([2, 3]),
        meavis.parameters.loop_instance1.parameter2([4, 5]),
        meavis.parameters.loop_instance1.parameter3([6, 7]),
    ]

    measurements = [
        meavis.measurements.loop_instance0.measurement0(),
        meavis.measurements.loop_instance0.measurement1(),
        meavis.measurements.loop_instance1.measurement2(),
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
            os.path.dirname(os.path.abspath(__file__)), "config", "loop.yaml"
        )
    ) as file:
        measurement = meavis.loop.LoopEngine(yaml.safe_load(file)).create(
            iter(parameters), iter(measurements)
        )
        measurement.trigger(None)
        measurement.wait(None)

    return (
        log_file,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    )


def test_loop_apply_count(loop_fixture):
    (
        log_file,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = loop_fixture

    assert parameter_apply_spies[0].call_count == 2
    assert parameter_apply_spies[1].call_count == 4
    assert parameter_apply_spies[2].call_count == 8
    assert parameter_apply_spies[3].call_count == 16


def test_loop_trigger_count(loop_fixture):
    (
        log_file,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = loop_fixture

    assert measurement_trigger_spies[0].call_count == 4
    assert measurement_trigger_spies[1].call_count == 16
    assert measurement_trigger_spies[2].call_count == 16


def test_loop_wait_count(loop_fixture):
    (
        log_file,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = loop_fixture

    assert measurement_wait_spies[0].call_count == 4
    assert measurement_wait_spies[1].call_count == 16
    assert measurement_wait_spies[2].call_count == 16


def test_loop_set_log(loop_fixture):
    (
        log_file,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = loop_fixture

    with open(log_file) as file:
        for line_ref in [
            "Set parameter0 to 0.",
            "Set parameter1 to 2 parameter1_unit.",
            "Set parameter2 to 4.",
            "Set parameter3 to 6 parameter3_unit.",
            "Set parameter3 to 7 parameter3_unit.",
            "Set parameter2 to 5.",
            "Set parameter3 to 6 parameter3_unit.",
            "Set parameter3 to 7 parameter3_unit.",
            "Set parameter1 to 3 parameter1_unit.",
            "Set parameter2 to 4.",
            "Set parameter3 to 6 parameter3_unit.",
            "Set parameter3 to 7 parameter3_unit.",
            "Set parameter2 to 5.",
            "Set parameter3 to 6 parameter3_unit.",
            "Set parameter3 to 7 parameter3_unit.",
            "Set parameter0 to 1.",
            "Set parameter1 to 2 parameter1_unit.",
            "Set parameter2 to 4.",
            "Set parameter3 to 6 parameter3_unit.",
            "Set parameter3 to 7 parameter3_unit.",
            "Set parameter2 to 5.",
            "Set parameter3 to 6 parameter3_unit.",
            "Set parameter3 to 7 parameter3_unit.",
            "Set parameter1 to 3 parameter1_unit.",
            "Set parameter2 to 4.",
            "Set parameter3 to 6 parameter3_unit.",
            "Set parameter3 to 7 parameter3_unit.",
            "Set parameter2 to 5.",
            "Set parameter3 to 6 parameter3_unit.",
            "Set parameter3 to 7 parameter3_unit.",
        ]:
            line = None
            while line != line_ref:
                line = file.readline()
                assert line[-1] == "\n"
                line = line[:-1]


def test_loop_register_log(loop_fixture):
    (
        log_file,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = loop_fixture

    with open(log_file) as file:
        lines = file.readlines()
        lines[:-1] = [line[:-1] for line in lines[:-1]]
        for line_ref in [
            "Register parameter0 as parameter"
            " named loop_instance0.parameter0.",
            "Register parameter1 as parameter"
            " named loop_instance0.parameter1.",
            "Register measurement0 as measurement"
            " named loop_instance0.measurement0.",
            "Register measurement1 as measurement"
            " named loop_instance0.measurement1.",
            "Register parameter2 as parameter named"
            " loop_instance1.parameter2.",
            "Register parameter3 as parameter named"
            " loop_instance1.parameter3.",
            "Register measurement2 as measurement"
            " named loop_instance1.measurement2.",
        ]:
            assert line_ref in lines


def test_loop_register_constructor_log(loop_fixture):
    (
        log_file,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = loop_fixture

    with open(log_file) as file:
        lines = file.readlines()
        lines[:-1] = [line[:-1] for line in lines[:-1]]
        for line_ref in [
            "Register loop_instrument constructor"
            " [4a1f29961c54401f4c55259b83df876230c2dc8c] {addr: localhost0}.",
            "Register loop_instrument constructor"
            " [244eabc3476d3c42961a11d7192538c8762999a8] {addr: localhost1}.",
        ]:
            assert line_ref in lines


def test_loop_register_initialiser_log(loop_fixture):
    (
        log_file,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = loop_fixture

    with open(log_file) as file:
        lines = file.readlines()
        lines[:-1] = [line[:-1] for line in lines[:-1]]
        for line_ref in [
            "Register loop_use_name0 initialiser {} for loop_instance0.",
            "Register loop_use_name1 initialiser {} for loop_instance1.",
        ]:
            assert line_ref in lines


def test_loop_trigger_order(loop_fixture):
    (
        log_file,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = loop_fixture

    with open(log_file) as file:
        for line_ref in [
            "Trigger measurement0, waiting for data.",
            "Trigger measurement1, waiting for data.",
            "Trigger measurement2, waiting for data.",
            "Trigger measurement1, waiting for data.",
            "Trigger measurement2, waiting for data.",
            "Trigger measurement1, waiting for data.",
            "Trigger measurement2, waiting for data.",
            "Trigger measurement1, waiting for data.",
            "Trigger measurement2, waiting for data.",
            "Trigger measurement0, waiting for data.",
            "Trigger measurement1, waiting for data.",
            "Trigger measurement2, waiting for data.",
            "Trigger measurement1, waiting for data.",
            "Trigger measurement2, waiting for data.",
            "Trigger measurement1, waiting for data.",
            "Trigger measurement2, waiting for data.",
            "Trigger measurement1, waiting for data.",
            "Trigger measurement2, waiting for data.",
            "Trigger measurement0, waiting for data.",
            "Trigger measurement1, waiting for data.",
            "Trigger measurement2, waiting for data.",
            "Trigger measurement1, waiting for data.",
            "Trigger measurement2, waiting for data.",
            "Trigger measurement1, waiting for data.",
            "Trigger measurement2, waiting for data.",
            "Trigger measurement1, waiting for data.",
            "Trigger measurement2, waiting for data.",
            "Trigger measurement0, waiting for data.",
            "Trigger measurement1, waiting for data.",
            "Trigger measurement2, waiting for data.",
            "Trigger measurement1, waiting for data.",
            "Trigger measurement2, waiting for data.",
            "Trigger measurement1, waiting for data.",
            "Trigger measurement2, waiting for data.",
            "Trigger measurement1, waiting for data.",
            "Trigger measurement2, waiting for data.",
        ]:
            line = None
            while line != line_ref:
                line = file.readline()
                assert line[-1] == "\n"
                line = line[:-1]


def test_loop_initialise_order(loop_fixture):
    (
        log_file,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = loop_fixture

    with open(log_file) as file:
        for line_ref in [
            "Initialise channel 0 on handler of"
            " loop_instrument.loop_use_name0.initialiser with {}.",
            "Initialise channel 0 on handler of"
            " loop_instrument.loop_use_name1.initialiser with {}.",
        ]:
            line = None
            while line != line_ref:
                line = file.readline()
                assert line[-1] == "\n"
                line = line[:-1]


def test_loop_create_order(loop_fixture):
    (
        log_file,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = loop_fixture

    with open(log_file) as file:
        for line_ref in [
            "Create handler of loop_instrument.constructor"
            " [4a1f29961c54401f4c55259b83df876230c2dc8c]"
            " with {addr: localhost0}.",
            "Create handler of loop_instrument.constructor"
            " [244eabc3476d3c42961a11d7192538c8762999a8]"
            " with {addr: localhost1}.",
        ]:
            line = None
            while line != line_ref:
                line = file.readline()
                assert line[-1] == "\n"
                line = line[:-1]


def test_loop_LoopEngine_maps(loop_fixture):
    (
        log_file,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = loop_fixture

    assert len(meavis.loop.LoopEngine.parameters_map) == 4
    assert len(meavis.loop.LoopEngine.measurements_map) == 4


def test_loop_name_injection(loop_fixture):
    (
        log_file,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = loop_fixture

    assert "first_loop" in meavis.loop.LoopEngine.measurements_map


def test_loop_attribute_injection(loop_fixture):
    (
        log_file,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = loop_fixture

    assert hasattr(
        meavis.loop.LoopEngine.parameters_map["parameter0"], "_meavis_dummy"
    )
    assert hasattr(
        meavis.loop.LoopEngine.measurements_map["measurement0"],
        "_meavis_dummy",
    )
