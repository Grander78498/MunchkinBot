import sys
import os
from pathlib import Path
from datetime import datetime
from unittest import IsolatedAsyncioTestCase, main as unittest_main
from unittest.mock import AsyncMock, patch

from aiogram.types import Message, CallbackQuery, User, Chat
from aiogram.utils.keyboard import InlineKeyboardMarkup

# Импорт приложения
working_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(working_dir))

for name in os.listdir(working_dir):
    if (working_dir / name).is_dir():
        sys.path.insert(0, str(working_dir / name))

from tg_bot.main import (
    cmd_start,
    cmd_help,
    cmd_rules,
    cmd_support,
    cmd_donate,
    cmd_world,
    transparent_policies,
    cmd_get_exchange_rate,
    bird_with_eggs,
    Language,
)


def make_message(text="test") -> Message:
    return Message(
        message_id=1,
        date=datetime.utcnow(),
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test", username="testuser"),
        text=text,
    )


class TestCommands(IsolatedAsyncioTestCase):

    @patch("tg_bot.main.read_text", return_value="stub")
    @patch("tg_bot.main.api_client.save_user")
    @patch("aiogram.types.Message.answer", new_callable=AsyncMock)
    async def test_cmd_start(self, mock_answer, mock_save_user, mock_read_text):
        msg = make_message("/start")
        await cmd_start(msg)
        mock_save_user.assert_called_once_with(1, "testuser", "Test")
        mock_answer.assert_awaited_once_with("stub")

    @patch("tg_bot.main.read_text", return_value="stub")
    @patch("aiogram.types.Message.answer", new_callable=AsyncMock)
    async def test_cmd_help(self, mock_answer, mock_read_text):
        msg = make_message("/help")
        await cmd_help(msg)
        mock_answer.assert_awaited_once_with("stub")

    @patch("tg_bot.main.read_text", return_value="stub")
    @patch("aiogram.types.Message.answer", new_callable=AsyncMock)
    async def test_cmd_rules(self, mock_answer, mock_read_text):
        msg = make_message("/rules")
        await cmd_rules(msg)
        args, kwargs = mock_answer.call_args
        self.assertIn("stub", args[0])
        self.assertIn("reply_markup", kwargs)
        self.assertIsInstance(kwargs["reply_markup"], InlineKeyboardMarkup)

    @patch("tg_bot.main.read_text", return_value="stub")
    @patch("aiogram.types.Message.answer", new_callable=AsyncMock)
    async def test_cmd_support(self, mock_answer, mock_read_text):
        msg = make_message("/support")
        await cmd_support(msg)
        mock_answer.assert_awaited_once_with("stub")

    @patch("tg_bot.main.read_text", return_value="stub")
    @patch("aiogram.types.Message.answer", new_callable=AsyncMock)
    async def test_cmd_donate(self, mock_answer, mock_read_text):
        msg = make_message("/donate")
        await cmd_donate(msg)
        mock_answer.assert_awaited_once_with("stub")

    @patch("aiogram.types.Message.answer", new_callable=AsyncMock)
    async def test_cmd_world(self, mock_answer):
        msg = make_message("/world")
        await cmd_world(msg)
        args, kwargs = mock_answer.call_args
        self.assertIn("Выбери СВОего героя", args[0])
        self.assertIn("reply_markup", kwargs)
        self.assertIsInstance(kwargs["reply_markup"], InlineKeyboardMarkup)

    @patch("tg_bot.main.get_exchange_rate", return_value=88.8)
    @patch("aiogram.types.Message.reply", new_callable=AsyncMock)
    async def test_cmd_get_exchange_rate(self, mock_reply, mock_api):
        msg = make_message("/get_daniel_trumps_most_transparent_policies")
        await cmd_get_exchange_rate(msg)
        mock_reply.assert_awaited_once()
        self.assertIn("88.8", mock_reply.call_args[0][0])

    @patch("aiogram.types.Message.answer_photo", new_callable=AsyncMock)
    async def test_bird_with_eggs(self, mock_photo):
        msg = make_message("/motivation")
        await bird_with_eggs(msg)
        mock_photo.assert_awaited_once()
        args, kwargs = mock_photo.call_args
        self.assertIn("Яйца с птицей", kwargs["caption"])
        self.assertIn("pikabu", kwargs["photo"])

    @patch("tg_bot.main.get_exchange_rate", return_value=123.45)
    @patch("aiogram.types.Message.reply", new_callable=AsyncMock)
    @patch("aiogram.types.CallbackQuery.answer", new_callable=AsyncMock)
    async def test_transparent_policies(self, mock_answer, mock_reply, mock_rate):
        msg = make_message()
        callback = CallbackQuery.model_construct(
            id="1",
            from_user=msg.from_user,
            data="trump",
            message=msg,
        )
        await transparent_policies(callback)
        mock_reply.assert_awaited_once()
        self.assertIn("123.45", mock_reply.call_args[0][0])
        mock_answer.assert_awaited_once()


if __name__ == "__main__":
    unittest_main()
