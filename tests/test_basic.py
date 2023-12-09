from optunacy.oplot import OPlot


def get_dummy_study():
    # Create a study with parameters a, b, c,
    # and objective values x, y, z
    # and user attributes p, q, r
    # with 3 trials
    return {
        "trials": [  # 3 trials
            {
                "user_attrs": {"p": 1, "q": 2, "r": 3},
                "params": {"a": 1, "b": 2, "c": 3},
                "values": [1, 2, 3],
            },
            {
                "user_attrs": {"p": 4, "q": 5, "r": 6},
                "params": {"a": 4, "b": 5, "c": 6},
                "values": [4, 5, 6],
            },
            {
                "user_attrs": {"p": 7, "q": 8, "r": 9},
                "params": {"a": 7, "b": 8, "c": 9},
                "values": [7, 8, 9],
            },
        ]
    }


def test_get_keys():
    study = get_dummy_study()
    oplot = OPlot(study)
    assert oplot.get_keys() == ["a", "b", "c", "p", "q", "r", "x", "y", "z"]


def test_get_values():
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
    study = get_dummy_study()
    oplot = OPlot(study, objective_names=["x", "y", "z"])
    assert oplot.format_value(1) == "1"
    assert oplot.format_value(1.23456789) == "1.2346"
    assert oplot.format_value(0.000123456789) == "1.23e-04"
    assert oplot.format_value(123456789) == "1.23e+08"


def test_describe_trials():
    study = get_dummy_study()
    oplot = OPlot(study, objective_names=["x", "y", "z"])
    assert oplot.describe_trials(study["trials"]) == [
        "Trial: 0<br>a: 1<br>b: 2<br>c: 3<br><i>x: 1</i><br><i>y: 2</i><br><i>z: 3</i>",
        "Trial: 1<br>a: 4<br>b: 5<br>c: 6<br><i>x: 4</i><br><i>y: 5</i><br><i>z: 6</i>",
        "Trial: 2<br>a: 7<br>b: 8<br>c: 9<br><i>x: 7</i><br><i>y: 8</i><br><i>z: 9</i>",
    ]


def test_plot():
    study = get_dummy_study()
    oplot = OPlot(study, objective_names=["x", "y", "z"])
    # just see if it runs without crashing
    oplot.plot("x", "y")
    oplot.plot("a", "y", "z")
    oplot.plot("q", "y", "z", x_range=(0, 10), y_range=(0, 10))
    oplot.plot("x", "y", "z", x_clip=(0, 10))
    oplot.plot("x", "y", "z", y_clip=(0, 10), interpol="linear")

    oplot = OPlot(study, objective_names=["x", "y", "z"], inline_plotting=True)
    # just see if it runs without crashing
    oplot.plot("x", "y")
    oplot.plot("a", "y", "z")
    oplot.plot("q", "y", "z", x_range=(0, 10), y_range=(0, 10))
    oplot.plot("x", "y", "z", x_clip=(0, 10))
    oplot.plot("x", "y", "z", y_clip=(0, 10), interpol="linear")
