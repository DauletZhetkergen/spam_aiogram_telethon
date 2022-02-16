from aiogram.dispatcher.filters.state import State, StatesGroup


class SetMessage(StatesGroup):
    # State for setting a message

    message = State()


class SetDelay(StatesGroup):
    # State for setting delay

    delay = State()
