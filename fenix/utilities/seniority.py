from datetime import datetime, timezone
from fenix.system.models import User, Profile

user = User()
profile = Profile()

points = profile.points_balance


def get_points_per_month(seniority):
    seniority_points = {
        "A": 5,
        "B": 10,
        "C": 15,
        "D": 20,
    }
    return seniority_points.get(seniority, 'A')


def accruePoints():
    """Add points according to seniority to every employee"""
    points = 0
    while True:
        if profile.seniority == 'A':
            points += 5
        elif profile.seniority == 'B':
            points += 10
        elif profile.seniority == 'C':
            points += 15
        elif profile.seniority == 'D':
            points += 20
        elif profile.seniority == 'E':
            points += 25
        else:
            return points


def multiplyPoints():
    """Multipy the points of the employee according to their tenure"""
    points = 0
    duration = (datetime.now(timezone.utc) - profile.date_joined).days / 365.25
    print(duration)
    while True:
        if duration <= 2:
            points * 1
        elif duration >= 2 and duration <= 4:
            points * 1.25
        elif duration >= 4:
            points * 1.5
        else:
            return points


accruePoints()
multiplyPoints()
