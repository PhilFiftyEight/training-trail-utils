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
