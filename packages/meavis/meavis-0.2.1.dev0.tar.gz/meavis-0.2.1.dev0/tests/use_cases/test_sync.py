import logging
import os

import dummy_mock
import pytest
import pytest_mock
import yaml

import meavis.instruments
import meavis.loop
import meavis.parameters


@pytest.fixture(scope="module")
def sync_fixture(pytestconfig):
    mocker = pytest_mock.MockFixture(pytestconfig)
    log_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "log_ref", "test_sync.log"
    )
    ch = logging.FileHandler(log_file, mode="w")
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(message)s"))
    logging.getLogger("meavis").addHandler(ch)
    logging.basicConfig(
        filename="test_sync.log",
        filemode="w",
        format="%(message)s",
        level=logging.INFO,
    )

    meavis.instruments.clear("parameters")
    meavis.parameters.inject(dummy_mock.DummyParameter, "  PaRaMeTeR0  ")
    meavis.parameters.inject(dummy_mock.DummyParameter, "  PaRaMeTeR1  ")
    meavis.parameters.inject(dummy_mock.DummyParameter, "  PaRaMeTeR2  ")
    meavis.parameters.inject(dummy_mock.DummyParameter, "  PaRaMeTeR3  ")
    meavis.parameters.inject(dummy_mock.DummyParameter, "  PaRaMeTeR4  ")
    meavis.parameters.inject(dummy_mock.DummyParameter, "  PaRaMeTeR5  ")
    parameters = [
        meavis.parameters.parameter0([0, 1]),
        meavis.parameters.parameter1([2, 3]),
        meavis.parameters.parameter2([4, 5]),
        meavis.parameters.parameter3([6, 7]),
        meavis.parameters.parameter4([8]),
        meavis.parameters.parameter5([10, 11]),
    ]
    parameters[1]._meavis_unit = "parameter1_unit"
    parameters[3]._meavis_unit = "parameter3_unit"
    parameters[5]._meavis_unit = "parameter5_unit"

    meavis.instruments.clear("measurements")
    meavis.measurements.inject(dummy_mock.DummyMeasurement, "  MeAsUrEmEnT0  ")
    meavis.measurements.inject(dummy_mock.DummyMeasurement, "  MeAsUrEmEnT1  ")
    meavis.measurements.inject(dummy_mock.DummyMeasurement, "  MeAsUrEmEnT2  ")
    measurements = [
        meavis.measurements.measurement0(),
        meavis.measurements.measurement1(),
        meavis.measurements.measurement2(),
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

    synchronisers = []
    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "config", "sync.yaml"
        )
    ) as file:
        sync_pattern = yaml.safe_load(file)
        synchronisers.extend(
            meavis.loop.LoopEngine(sync_pattern).synchronisers(
                [parameters[i] for i in [0, 2, 4]]
            )
        )
        synchronisers.extend(
            meavis.loop.LoopEngine(sync_pattern).synchronisers(
                [parameters[i] for i in [3, 5]]
            )
        )

    results = []
    for synchroniser in synchronisers:
        results.extend(synchroniser.pre_synchronise(set()))

    return (
        log_file,
        results,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    )


def test_sync_apply_count(sync_fixture):
    (
        log_file,
        results,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = sync_fixture

    assert parameter_apply_spies[0].call_count == 2
    assert parameter_apply_spies[1].call_count == 0
    assert parameter_apply_spies[2].call_count == 4
    assert parameter_apply_spies[3].call_count == 2
    assert parameter_apply_spies[4].call_count == 1
    assert parameter_apply_spies[5].call_count == 2


def test_sync_trigger_count(sync_fixture):
    (
        log_file,
        results,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = sync_fixture

    for measurement_trigger_spy in measurement_trigger_spies:
        assert measurement_trigger_spy.call_count == 0


def test_sync_wait_count(sync_fixture):
    (
        log_file,
        results,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = sync_fixture

    for measurement_wait_spy in measurement_wait_spies:
        assert measurement_wait_spy.call_count == 0


def test_sync_info_log(sync_fixture):
    (
        log_file,
        results,
        parameter_apply_spies,
        measurement_trigger_spies,
        measurement_wait_spies,
    ) = sync_fixture

    with open(log_file) as file:
        for line_ref in [
            "Register [8136c7cc841ddda3be0f7475853d54b50d4cfa43]",
            "Register [eb76504bc5766fafae7a2bf493083bbbfdab98cf]",
            "Register [23966cd08b7cf5762ec1515ea4d5b7f3b73e083f]",
            "Register [3118c59c80483359c038dee6cfa76bee5da06e8d]",
            "Register [5b58521bc1238155d04d8167d99204e0ad470c01]",
            "Register [1d370a459ae2a5489b1bcaf9cf99caff2833078e]",
            "Register [e3cc2b2062b800a738d723a89e5e881a5ee2f7b4]",
            "Register [b7b3a8c92d00c23b449972ed4aff1ae3dd6202ad]",
            "Register [405dae4e39188c69d1b2d6fcaa8e74e60935523e]",
        ]:
            line = None
            while not line or not line.startswith(line_ref):
                line = file.readline()
                assert line[-1] == "\n"
                line = line[:-1]
