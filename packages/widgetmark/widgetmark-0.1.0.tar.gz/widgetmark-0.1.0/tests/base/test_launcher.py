import widgetmark


def test_use_case_param_resolution_two_entries():
    params = {
        "a": [0, 1],
        "b": [0, 1, 2],
    }
    result = widgetmark.Launcher.get_params_combination(params)
    expected = [
        {"a": 0, "b": 0},
        {"a": 0, "b": 1},
        {"a": 0, "b": 2},
        {"a": 1, "b": 0},
        {"a": 1, "b": 1},
        {"a": 1, "b": 2},
    ]
    assert expected == result


def test_use_case_param_resolution_three_entries():
    params = {
        "a": [0, 1],
        "b": [0, 1, 2],
        "c": [0],
    }
    result = widgetmark.Launcher.get_params_combination(params)
    expected = [
        {"a": 0, "b": 0, "c": 0},
        {"a": 0, "b": 1, "c": 0},
        {"a": 0, "b": 2, "c": 0},
        {"a": 1, "b": 0, "c": 0},
        {"a": 1, "b": 1, "c": 0},
        {"a": 1, "b": 2, "c": 0},
    ]
    assert expected == result


def test_use_case_param_resolution_single_entry():
    params = {
        "a": [0],
    }
    result = widgetmark.Launcher.get_params_combination(params)
    expected = [{"a": 0}]
    assert expected == result


def test_use_case_param_resolution_no_entries():
    params = {}
    result = widgetmark.Launcher.get_params_combination(params)
    expected = [{}]
    assert expected == result
