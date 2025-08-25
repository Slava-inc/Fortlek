from abc import ABC, abstractmethod

class TrainingSession(ABC):
    def __init__(self, user_id: int, plan):
        self.user_id = user_id
        self.plan = plan

    @abstractmethod
    async def start(self, context): pass

    @abstractmethod
    async def finish(self, context): pass