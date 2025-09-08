from typing import List

class Phase:
    def __init__(self, phase_type: str, duration: int, title: str, intensity: str):
        self.phase_type = phase_type
        self.duration = duration
        self.title = title
        self.intensity = intensity
        self.intensity_msgs = {
            "low": "Лёгкий темп, дыши спокойно",
            "medium": "Уверенный темп, чувствуй ритм",
            "high": "Полный газ! Ты можешь!"
        }

    def get_msg(self):
        return self.intensity_msgs.get(self.intensity, "")

class TimedFartlekPlan:
    def __init__(self):
        self.phases = [
            Phase("warmup", 30, "Разминка", "low"),
            Phase("run", 180, "Интервал 1", "medium"),
            Phase("rest", 120, "Отдых", "low"),
            Phase("run", 240, "Интервал 2", "medium"),
            Phase("rest", 120, "Отдых", "low"),
            Phase("run", 300, "Интервал 3", "high"),
            Phase("rest", 120, "Отдых", "low"),
            Phase("run", 180, "Финальный интервал", "high"),
            Phase("cooldown", 180, "Заминка", "low")
        ]