import pytest
from unittest.mock import AsyncMock, MagicMock

from services.bot.app.states.subscription import SubscriptionState
from services.bot.app.handlers.payment.start_payment_process import start_payment_process


@pytest.mark.asyncio
async def test_start_payment_process_success(monkeypatch):
    # --- Arrange ---
    # Mock callback
    callback = MagicMock()
    callback.from_user.id = 123
    callback.message.answer = AsyncMock()

    # Mock state
    state = AsyncMock()
    state.get_data = AsyncMock(return_value={
        "email": "test@example.com",
        "price": 100,
        "duration": 3
    })

    # Mock payment_service
    fake_payment = MagicMock()
    fake_payment.id = "pay_123"
    fake_payment.confirmation.return_url = "https://pay.link"
    payment_service_mock = AsyncMock()
    payment_service_mock.add_payment.return_value = fake_payment
    monkeypatch.setattr("app.handlers.payment.payment_service", payment_service_mock)

    # Mock user_service
    fake_user = MagicMock()
    fake_user.id = 42
    user_service_mock = AsyncMock()
    user_service_mock.get_user_for_tg_id.return_value = fake_user
    monkeypatch.setattr("app.handlers.payment.user_service", user_service_mock)

    # Mock order_service
    fake_order = MagicMock()
    order_service_mock = AsyncMock()
    order_service_mock.create_order.return_value = fake_order
    monkeypatch.setattr("app.handlers.payment.order_service", order_service_mock)

    # Mock payment_keyboard
    monkeypatch.setattr("app.handlers.payment.payment_keyboard", MagicMock(return_value="keyboard"))

    # Mock failure_handler (чтобы не мешал)
    monkeypatch.setattr("app.handlers.payment.failure_handler", AsyncMock())

    # --- Act ---
    await start_payment_process(callback, state)

    # --- Assert ---
    payment_service_mock.add_payment.assert_awaited_once()
    user_service_mock.get_user_for_tg_id.assert_awaited_once_with(123)
    order_service_mock.create_order.assert_awaited_once_with(
        user_id=42,
        platform="",
        order_price=100,
        is_paid=False,
        payment_id="pay_123",
        duration=3
    )
    state.set_state.assert_awaited_once_with(SubscriptionState.confirming)
    state.update_data.assert_awaited_once_with(payment_id="pay_123")
    callback.message.answer.assert_awaited_once()
