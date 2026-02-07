from aiogram.fsm.state import State, StatesGroup

class ClientStates(StatesGroup):
    people_count = State()
    address = State()
    price = State()
    direction = State()
    location = State()
    confirm = State()