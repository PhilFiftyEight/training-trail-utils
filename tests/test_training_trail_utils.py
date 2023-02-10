from src.training_trail_utils.session import Session

def test_can_create_Session():
    s = Session()
    assert isinstance(s, Session)