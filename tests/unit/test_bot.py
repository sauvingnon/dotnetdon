import pytest
from unittest.mock import AsyncMock, MagicMock

from services.bot.app.handlers.start import cmd_start
from services.bot.app.states.subscription import Step

@pytest.mark.asyncio
async def test_cmd_start_success(monkeypatch):
    # --- Arrange ---
    # подделываем message
    message = MagicMock()
    message.from_user.id = 123
    message.from_user.username = "grisha"
    message.from_user.first_name = None
    message.answer = AsyncMock()

    # подделываем state
    state = AsyncMock()

    # подделываем user_service
    fake_user = {"id": 123, "name": "grisha"}
    user_service_mock = AsyncMock()
    user_service_mock.create_user.return_value = fake_user
    monkeypatch.setattr("services.bot.handlers.user_service", user_service_mock)

    # подделываем resources
    monkeypatch.setattr("services.bot.handlers.resources", MagicMock(welcome_message="hi!"))

    # подделываем get_main_menu
    monkeypatch.setattr("services.bot.handlers.get_main_menu", MagicMock(return_value="keyboard"))

    # --- Act ---
    await cmd_start(message, state)

    # --- Assert ---
    user_service_mock.create_user.assert_awaited_once_with(123, "grisha")
    state.set_state.assert_awaited_once_with(Step.show_menu)
    message.answer.assert_any_call("hi!")  # проверяем, что бот отправил welcome_message
    message.answer.assert_any_call("Выбери пункт меню:", reply_markup="keyboard")
