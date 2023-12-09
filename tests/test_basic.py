from optunacy.oplot import OPlot


def test_commandline_installed():
    optuna_dummy = {}
    see = OPlot(optuna_dummy)
    assert see is not None
