from aiogram.fsm.state import State, StatesGroup


class StaffStates(StatesGroup):
    startState = State()
    username = State()
    password = State()
    admin = State()
    user = State()


class Updates(StaffStates):
    company = State()
    truck = State()
    driver = State()
    issue = State()

    startDoneState = State()
    finishDoneState = State()

    eldNewsState = State()


class AdsStates(StatesGroup):
    titleState = State()
    infoState = State()
    imageState = State()

    miranInfoVideoState = State()
    miranInfoDescState = State()
    miranInfoSaveState = State()


class AdminsStates(StatesGroup):
    adminState = State()
    editAdminState = State()
    removeAdminState = State()

    adminFirstnameState = State()
    adminLastnameState = State()
    adminUsernameState = State()
    adminPasswordState = State()
    adminRuleState = State()
    tg_usernameState = State()
    contactState = State()
    shiftState = State()
    saveState = State()
