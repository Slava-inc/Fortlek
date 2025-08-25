# training/sessions/fartlek_session.py
from training.plans.timed_fartlek_plan import TimedFartlekPlan, Phase
from messaging.coach import Coach
from user.achievements import AchievementSystem
from user.user import User

class TimedFartlekSession:
    def __init__(self, user_id: int, context, user_storage):
        self.user_id = user_id
        self.context = context
        self.user_storage = user_storage
        self.plan = TimedFartlekPlan()
        self.coach = Coach(context, user_storage)

    async def start(self):
        user = self.user_storage.load_user(self.user_id)
        if not user:
            user = User(id=self.user_id, first_name="Бегун")
            self.user_storage.save_user(user)

        await self.coach.send_fartlek_intro(self.user_id)

        delay = 0
        for phase in self.plan.phases:
            if phase.phase_type == "warmup":
                continue
            elif phase.phase_type == "run":
                self.context.job_queue.run_once(
                    self._send_run,
                    when=delay,
                    data={"chat_id": self.user_id, "phase": phase}
                )
            elif phase.phase_type == "rest":
                self.context.job_queue.run_once(
                    self._send_rest,
                    when=delay,
                    data={"chat_id": self.user_id, "duration": phase.duration}
                )
            elif phase.phase_type == "cooldown":
                self.context.job_queue.run_once(
                    self._send_cooldown,
                    when=delay,
                    data={"chat_id": self.user_id}
                )
            delay += phase.duration

        # Финал
        self.context.job_queue.run_once(
            self._finish,
            when=delay,
            data={"chat_id": self.user_id, "user_id": self.user_id}
        )

    async def _send_run(self, context):
        job = context.job
        phase = job.data["phase"]
        await self.coach.send_interval_message(
            job.data["chat_id"],
            phase.title,
            phase.duration,
            phase.get_msg()
        )

    async def _send_rest(self, context):
        job = context.job
        await self.coach.send_rest_message(job.data["chat_id"], job.data["duration"])

    async def _send_cooldown(self, context):
        job = context.job
        await self.coach.send_cooldown(job.data["chat_id"])

    async def _finish(self, context):
        job = context.job
        user_id = job.data["user_id"]
        user = self.user_storage.load_user(user_id)
        user.complete_training()
        self.user_storage.save_user(user)

        await self.coach.send_completion(job.data["chat_id"])

        for ach in AchievementSystem.check_achievements(user, event="fartlek_completed"):
            self.user_storage.add_achievement(user_id, ach)
            await self.coach.send_achievement(job.data["chat_id"], ach)