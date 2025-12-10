from aiogram.dispatcher.filters.state import State, StatesGroup

class AskState(StatesGroup):
    waiting_for_question = State()
