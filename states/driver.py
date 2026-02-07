from aiogram.fsm.state import State, StatesGroup

class DriverStates(StatesGroup):
    name = State()
    phone = State()
    car_model = State()
    car_number = State()