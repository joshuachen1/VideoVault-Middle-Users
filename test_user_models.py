from datetime import date, datetime, timedelta
from flask import jsonify
import app


def test_new_user():
    date = str(datetime.now())
    profile_pic = "https://upload.wikimedia.org/wikipedia/en/1/13/Stick_figure.png"
    user = app.User('Chris P. Bacon', 'baconator', 'bacon@gmail.com', 'bacon', '123', 10, date, profile_pic)

    assert user.name == 'Chris P. Bacon'
    assert user.username == 'baconator'
    assert user.email == 'bacon@gmail.com'
    assert user.password == 'bacon'
    assert user.card_num == '123'
    assert user.num_slots == 10
    assert user.sub_date == date
    assert user.profile_pic == profile_pic


if __name__ == "__main__":
    test_new_user()
    print("Everything passed")
