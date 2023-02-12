import pytest

import pendulum

from src.training_trail_utils.session import Session


@pytest.fixture
def attributs():
    return (
        "datas",
        "date",
        "duration",
        "vma",
        "anaerobie",
        "end_active",
        "end_fond",
        "recup",
    )


def test_can_create_Session(attributs):
    s = Session("2022-2-10 51:54 08:46 27:16 03:31 06:31 05:45")
    for attr in attributs:
        if attr == "datas":
            attr_type = str
        elif attr == "date":
            attr_type = pendulum.DateTime
        else:
            attr_type = pendulum.Duration
        assert isinstance(getattr(s, attr), attr_type)


def test_post_init_dispatch_data_correctly(attributs):
    s = Session("2022-2-10 01:51:54 08:46 27:16 03:31 01:06:31 05:45")
    verif_datas = [
        (2022, 2, 10),
        (1, 51, 54),
        (8, 46),
        (27, 16),
        (3, 31),
        (1, 6, 31),
        (5, 45),
    ]
    for attr in attributs:
        if attr == "datas":
            continue
        elif attr == "date":
            assert s.date == pendulum.local(*verif_datas.pop(0))
        else:
            datas = verif_datas.pop(0)
            if len(datas) == 3:
                kwargs = dict(zip(("hours", "minutes", "seconds"), datas))
            else:
                kwargs = dict(zip(("minutes", "seconds"), datas))
            assert getattr(s, attr) == pendulum.duration(**kwargs)
