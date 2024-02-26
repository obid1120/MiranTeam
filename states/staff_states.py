from aiogram.fsm.state import State, StatesGroup, StatesGroupMeta


class StaffStates(StatesGroup):
    username = State()
    password = State()
    admin = State()


class Updates(StaffStates):
    company = State()
    truck = State()
    driver = State()
    issue = State()

    startDoneState = State()
    finishDoneState = State()


class AdsStates(StatesGroup):
    titleState = State()
    infoState = State()
    imageState = State()
