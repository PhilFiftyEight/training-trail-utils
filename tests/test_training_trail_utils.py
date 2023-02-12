import pytest

import pendulum

from src.training_trail_utils.session import Session


def _fields():
    return (
        "date",
        "duration",
        "vma",
        "anaerobie",
        "end_active",
        "end_fond",
        "recup",
    )


@pytest.fixture
def fields():
    return ("datas", *_fields())


def test_can_create_Session(fields):
    s = Session("2022-2-10 51:54 08:46 27:16 03:31 06:31 05:45")
    for field in fields:
        if field == "datas":
            field_type = str
        elif field == "date":
            field_type = pendulum.DateTime
        else:
            field_type = pendulum.Duration
        assert isinstance(getattr(s, field), field_type)


@pytest.mark.parametrize(
    "field, expected",
    list(
        zip(
            _fields(),
            [
                pendulum.local(2022, 2, 10),
                pendulum.duration(hours=1, minutes=51, seconds=54),
                pendulum.duration(minutes=8, seconds=46),
                pendulum.duration(minutes=27, seconds=16),
                pendulum.duration(minutes=3, seconds=31),
                pendulum.duration(hours=1, minutes=6, seconds=31),
                pendulum.duration(minutes=5, seconds=45),
            ],
        )
    ),
)
def test_post_init_dispatch_data_correctly(field, expected):
    s = Session("2022-2-10 01:51:54 08:46 27:16 03:31 01:06:31 05:45")
    assert getattr(s, field) == expected
