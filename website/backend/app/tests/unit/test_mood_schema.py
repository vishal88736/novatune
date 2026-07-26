from app.schemas.mood import MoodCheckinRequest


def test_mood_checkin_request_accepts_text_only():
    req = MoodCheckinRequest(text="feeling great today")
    assert req.mood_tap is None


def test_mood_checkin_request_accepts_tap_only():
    req = MoodCheckinRequest(mood_tap="Euphoric")
    assert req.text is None
