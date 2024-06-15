from aiogram.fsm.state import State, StatesGroup

class Translate(StatesGroup):
    word = State()
    lang = State()
    active = State()
    quiz = State()
    
