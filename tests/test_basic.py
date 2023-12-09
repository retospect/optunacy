from optunacy.oplot import OPlot
import unittest.mock as mock


def get_dummy_study():
    # Create a mock study with parameters a, b, c,
    # and objective values x, y, z
    # and user attributes p, q, r
    # with 3 trials
    # Should allow for dummy.trials[0].params["a"] == 1
    # and dummy.trials[0].values[0] == 1
    # and dummy.trials[0].user_attrs["p"] == 1
    # Should allow for dummy.trials[1].params["a"] == 4 etc.
    # Use mocking framework

    # Create a mock study
    study = mock.Mock()
    trials = []
    for i in range(3):
        trial = mock.Mock()
        trial.number = i
        trial.state = "COMPLETE"
        trial.params = {"a": i + 1, "b": i + 2, "c": i + 3}
        trial.values = [i + 1, i + 2, i + 3]
        trial.user_attrs = {"p": i + 1, "q": i + 2, "r": i + 3}
        study.trials.append(trial)
    # the trials attribute is a list of trials
    study.trials = trials

    return study


def test_get_keys():
    return  # skip
    study = get_dummy_study()
    oplot = OPlot(study)
    assert oplot.get_keys() == ["a", "b", "c", "p", "q", "r", "x", "y", "z"]


def test_get_values():
    return  # skip
    study = get_dummy_study()
    oplot = OPlot(study)
    assert oplot.get_values(study["trials"], "a") == [1, 4, 7]
    assert oplot.get_values(study["trials"], "b") == [2, 5, 8]
    assert oplot.get_values(study["trials"], "c") == [3, 6, 9]
    assert oplot.get_values(study["trials"], "p") == [1, 4, 7]
    assert oplot.get_values(study["trials"], "q") == [2, 5, 8]
    assert oplot.get_values(study["trials"], "r") == [3, 6, 9]
    assert oplot.get_values(study["trials"], "x") == [1, 4, 7]
    assert oplot.get_values(study["trials"], "y") == [2, 5, 8]
    assert oplot.get_values(study["trials"], "z") == [3, 6, 9]


def test_format_value():
    return  # skip
    study = get_dummy_study()
    oplot = OPlot(study, objective_names=["x", "y", "z"])
    assert oplot.format_value(1) == "1"
    assert oplot.format_value(1.23456789) == "1.2346"
    assert oplot.format_value(0.000123456789) == "1.23e-04"
    assert oplot.format_value(123456789) == "1.23e+08"


def test_describe_trials():
    return  # skip
    study = get_dummy_study()
    oplot = OPlot(study, objective_names=["x", "y", "z"])
    assert oplot.describe_trials(study["trials"]) == [
        "Trial: 0<br>a: 1<br>b: 2<br>c: 3<br><i>x: 1</i><br><i>y: 2</i><br><i>z: 3</i>",
        "Trial: 1<br>a: 4<br>b: 5<br>c: 6<br><i>x: 4</i><br><i>y: 5</i><br><i>z: 6</i>",
        "Trial: 2<br>a: 7<br>b: 8<br>c: 9<br><i>x: 7</i><br><i>y: 8</i><br><i>z: 9</i>",
    ]


def test_plot_2d():
    return  # skip
    study = get_dummy_study()
    oplot = OPlot(study, objective_names=["x", "y", "z"])
    # just see if it runs without crashing
    oplot.plot("x", "y")


def test_plot_3d():
    return  # skip
    study = get_dummy_study()
    oplot = OPlot(study, objective_names=["x", "y", "z"])
    # just see if it runs without crashing
    oplot.plot("x", "y", "z")


def test_plot_3d_x_range():
    return  # skip
    study = get_dummy_study()
    oplot = OPlot(study, objective_names=["x", "y", "z"])
    # just see if it runs without crashing
    oplot.plot("x", "y", "z", x_range=(0, 10))


def test_plot_3d_y_range():
    return  # skip
    study = get_dummy_study()
    oplot = OPlot(study, objective_names=["x", "y", "z"])
    # just see if it runs without crashing
    oplot.plot("x", "y", "z", y_range=(0, 10))


def test_plot_3d_z_clip():
    return  # skip
    study = get_dummy_study()
    oplot = OPlot(study, objective_names=["x", "y", "z"])
    # just see if it runs without crashing
    oplot.plot("x", "y", "z", z_clip=(0, 10))


def test_plot_3d_all_range_and_clip():
    return  # skip
    study = get_dummy_study()
    oplot = OPlot(study, objective_names=["x", "y", "z"])
    # just see if it runs without crashing
    oplot.plot("x", "y", "z", x_range=(0, 10), y_range=(0, 10), z_clip=(0, 10))
