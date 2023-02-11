from src.training_trail_utils.session import Session

import pendulum

def test_can_create_Session():
    s = Session("2022-2-10 51:54 08:46 27:16 03:31 06:31 05:45")
    for k in s.__dict__.keys():
        if k == "datas":
            attr_type = str
        elif k == "date":
            attr_type = pendulum.DateTime
        else:
            attr_type = pendulum.Duration
        assert isinstance(getattr(s, k), attr_type)

def test_post_init_dispatch_data_correctly():
    s = Session("2022-2-10 51:54 08:46 27:16 03:31 06:31 05:45")
    assert s.date == pendulum.local(2022,2,10)
    assert s.duration == pendulum.duration(minutes=51,seconds=54)
    assert s.vma == pendulum.duration(minutes=8,seconds=46)
    assert s.anaerobie == pendulum.duration(minutes=27,seconds=16)
    assert s.end_active == pendulum.duration(minutes=3,seconds=31)
    assert s.end_fond == pendulum.duration(minutes=6,seconds=31)
    assert s.recup == pendulum.duration(minutes=5,seconds=45)
