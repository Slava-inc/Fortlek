class User:
    def __init__(self, id: int, first_name: str, level: str = "beginner", trainings_completed: int = 0):
        self.id = id
        self.first_name = first_name
        self.level = level
        self.trainings_completed = trainings_completed
        self.achievements = []

    def complete_training(self):
        self.trainings_completed += 1