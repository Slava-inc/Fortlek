class AchievementSystem:
    RULES = {
        "first_fartlek": lambda user, **kwargs: user.trainings_completed >= 1,
        "five_trainings": lambda user, **kwargs: user.trainings_completed >= 5,
        "night_runner": lambda user, **kwargs: kwargs.get("event") == "night_run"
    }

    ACHIEVEMENT_NAMES = {
        "first_fartlek": "🏁 Фортлек-стартер",
        "five_trainings": "🔥 Пять подряд",
        "night_runner": "🌙 Ночной бегун"
    }

    @classmethod
    def check_achievements(cls, user, event=None):
        unlocked = []
        for key, condition in cls.RULES.items():
            if condition(user, event=event) and key not in user.achievements:
                unlocked.append(key)
                user.achievements.append(key)
        return unlocked