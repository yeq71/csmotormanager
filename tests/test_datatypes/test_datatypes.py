from csmotormanager.datatypes.datatypes import Parameter


def test_Parameter():
    name = "XY_skew"
    value = 0.985

    param = Parameter(name, value)

    assert param.name == name
    assert param.value == value

    string = param.__str__()

    assert string == "XY_skew: 0.985"
