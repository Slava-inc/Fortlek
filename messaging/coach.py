# messaging/coach.py
from messaging.templates import TEMPLATES
from user.achievements import AchievementSystem
from user.user import User

class Coach:
    def __init__(self, context, user_storage):
        self.context = context
        self.user_storage = user_storage

    async def send_start(self, update):
        user = update.effective_user
        text = TEMPLATES["start"].format(name=user.first_name)
        await update.message.reply_text(text)

    async def send_fartlek_intro(self, chat_id: int):
        await self.context.bot.send_message(chat_id=chat_id, text=TEMPLATES["fartlek_start"])

    async def send_interval_message(self, chat_id: int, title: str, duration: int, intensity_msg: str):
        text = TEMPLATES["interval"].format(title=title, duration=duration, intensity_msg=intensity_msg)
        await self.context.bot.send_message(chat_id=chat_id, text=text)

    async def send_rest_message(self, chat_id: int, duration: int):
        text = TEMPLATES["rest"].format(duration=duration)
        await self.context.bot.send_message(chat_id=chat_id, text=text)

    async def send_cooldown(self, chat_id: int):
        await self.context.bot.send_message(chat_id=chat_id, text=TEMPLATES["cooldown"])

    async def send_completion(self, chat_id: int):
        await self.context.bot.send_message(chat_id=chat_id, text=TEMPLATES["completed"])

    async def send_achievement(self, chat_id: int, achievement_id: str):
        name = AchievementSystem.ACHIEVEMENT_NAMES.get(achievement_id, achievement_id)
        text = TEMPLATES["achievement"].format(name=name)
        await self.context.bot.send_message(chat_id=chat_id, text=text)