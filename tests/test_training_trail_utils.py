import pytest

import pendulum

from src.training_trail_utils.session import Session
from src.training_trail_utils.session import InvalidStringError


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


@pytest.mark.parametrize(
    "datas_string, expected",
    [
        # init string empty
        ("", "InvalidStringError: the datas_String is required for new Session"),
        # 01:01:06:31 => more 3 tokens for duration
        (
            "2022-2-10 51:54 08:46 27:16 03:31 01:01:06:31 05:45",
            "InvalidStringError: more than 3 tokens for <01:01:06:31>",
        ),
        # 00 => less 2 tokens for duration
        (
            "2022-2-10 51:54 08:46 27:16 03:31 31 05:45",
            "InvalidStringError: less than 2 tokens for <31>",
        ),
        # 2022/2/10 => invalid separator (date)
        (
            "2022/2/13 51:54 08:46 27:16 03:31 01:06:31 05:45",
            "InvalidStringError: invalid separator for date <2022/2/13>, format -> yyyy-mm-dd",
        ),
        (
            "2022-2/13 51:54 08:46 27:16 03:31 01:06:31 05:45",
            "InvalidStringError: invalid separator for date <2022-2/13>, format -> yyyy-mm-dd",
        ),
        (
            "2022/2-13 51:54 08:46 27:16 03:31 01:06:31 05:45",
            "InvalidStringError: invalid separator for date <2022/2-13>, format -> yyyy-mm-dd",
        ),
        # 03.31 => invalid separator (duration)
        (
            "2022-2-10 51:54 08:46 27:16 03.31 01:06:31 05:45",
            "InvalidStringError: invalid separator for duration <03.31>, format -> Optionnal([0-9][0-9]:)[0-5][0-9]:[0-5][0-9]",
        ),
        # missing duration
        (
            "2022-2-10 51:54 08:46 27:16 03:31 01:06:31",
            "InvalidStringError: 6 durations are required not 5",
        ),
        # Too much duration
        (
            "2022-2-10 51:54 08:46 27:16 03:31 01:06:31 00:00 00:00",
            "InvalidStringError: 6 durations are required not 7",
            
        ),
        # missing date
        (
            "51:54 08:46 27:16 03:31 01:06:31 05:45",
            "InvalidStringError: date is required, format -> yyyy-mm-dd",
        ),
    ],
)
def test_incorrect_string_for_create_Session_raise_exception(datas_string, expected):
    with pytest.raises(InvalidStringError) as e:
        s = Session(datas_string)
    assert str(e.value) == expected


