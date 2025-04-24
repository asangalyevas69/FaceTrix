import requests
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()
user_roles = {} 


@router.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Начать")]],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await message.answer(
        "👋 Добро пожаловать в FaceTrix!\n\n" \
        "Нажмите кнопку ниже, чтобы начать:",
        reply_markup=keyboard
    )


@router.message(F.text.in_(["Начать", "меню", "Меню"]))
async def show_main_menu(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨‍👩‍👧 Родитель", callback_data="role_parent")],
        [InlineKeyboardButton(text="🧑‍🏫 Преподаватель", callback_data="role_curator")],
        [InlineKeyboardButton(text="🎓 Ученик", callback_data="role_student")]
    ])
    await message.answer("Выберите вашу роль:", reply_markup=kb)

@router.callback_query(F.data.startswith("role_"))
async def show_role_actions(callback: CallbackQuery):
    role = callback.data.split("_")[1]
    user_roles[callback.from_user.id] = role 

    await callback.message.answer("🔐 Введите ваш логин-код:\n" \
    "Пример: `/login 123456`", parse_mode="Markdown")
    await callback.answer()

@router.message(Command("login"))
async def login_user(message: Message):
    login_code = message.text.split()[1]
    role = user_roles.get(message.from_user.id)

    if role == "parent":
        url = f"http://127.0.0.1:8000/api/parenttg/{login_code}/"
    elif role == "student":
        url = f"http://127.0.0.1:8000/api/studenttg/{login_code}/"
    else:
        await message.answer("Сначала выберите роль в меню!!!")
        return
    

    response = requests.get(url)
    try:
            data = response.json()
    except Exception:
            await message.answer("⚠️ Сервер вернул невалидный ответ. Проверь login_code.")
            return


    report_text = (
        f"📊 Отчёт по ученику: {data.get('student')}\n"
        f"✅ Посещено: {data.get('present')} дней\n"
        f"❌ Пропущено: {data.get('absent')} дней\n"
        f"📆 Всего занятий: {data.get('total')}"
    )

    await message.answer()


@router.callback_query(F.data.startswith("role_"))
async def show_role_actions(callback: CallbackQuery):
    role = callback.data.split("_")[1]

    if role == "parent":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📊 Посмотреть отчёт о посещаемости", callback_data="parent_report")],
            [InlineKeyboardButton(text="📞 Связаться с куратором", callback_data="parent_contact")],
            [InlineKeyboardButton(text="🗓 Посмотреть расписание", callback_data="parent_schedule")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
        ])
    elif role == "curator":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Проверить посещаемость учеников", callback_data="curator_check")],
            [InlineKeyboardButton(text="✉️ Отправить сообщение ученикам", callback_data="curator_msg")],
            [InlineKeyboardButton(text="📈 Отчёты по посещаемости", callback_data="curator_reports")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
        ])
    elif role == "student":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📅 Моя посещаемость", callback_data="student_attendance")],
            [InlineKeyboardButton(text="🆘 Запросить помощь", callback_data="student_help")],
            [InlineKeyboardButton(text="📚 Моё расписание", callback_data="student_schedule")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
        ])

    await callback.message.edit_text(
        f"Вы выбрали роль: {role.capitalize()}. Вот доступные действия:",
        reply_markup=kb
    )
    await callback.answer()


# @router.callback_query(F.data == "main_menu")
# async def go_main_menu(callback: CallbackQuery):
#     kb = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text="👨‍👩‍👧 Родитель", callback_data="role_parent")],
#         [InlineKeyboardButton(text="🧑‍🏫 Куратор", callback_data="role_curator")],
#         [InlineKeyboardButton(text="🎓 Ученик", callback_data="role_student")]
#     ])
#     await callback.message.edit_text("Выберите вашу роль:", reply_markup=kb)
#     await callback.answer()



@router.callback_query(F.data == "parent_report")
async def show_parent_report(callback: CallbackQuery):
    login_code = callback.from_user.id
    url = f"http://127.0.0.1:8000/api/parenttg/{login_code}/"
    
    response = requests.get(url)
    
    if response.status_code == 200:

        data = response.json()
        report_text = (
            f"📊 Отчёт по ученику: {data.get('student')}\n"
            f"✅ Посещено: {data.get('present')} дней\n"
            f"❌ Пропущено: {data.get('absent')} дней\n"
            f"📆 Всего занятий: {data.get('total')}"
        )
    else:
        print("🔴 Ответ от Django:", response.text) 
        report_text = (
            f"⚠️ Ошибка от сервера ({response.status_code})\n"
            f"Подробности см. в консоли"
        )

    # Безопасность: Telegram лимит = 4096 символов
    if len(report_text) > 4090:
        report_text = report_text[:4090] + "..."

    await callback.message.answer(report_text)
    await callback.answer()




@router.callback_query(F.data == "student_attendance")
async def show_student_report(callback: CallbackQuery):
    login_code = callback.from_user.id
    response = requests.get(f"http://127.0.0.1:8000/api/get-student-by-tg/{login_code}/")
    print("Сервер ответил:", response.text)

    data = response.json()

    report_text = (
        f"📅 Твоя посещаемость:\n"
        f"✅ Посещено: {data.get('present')} дней\n"
        f"❌ Пропущено: {data.get('absent')} дней\n"
        f"📆 Всего занятий: {data.get('total')}"
    )

    await callback.message.answer(report_text)
    await callback.answer()


@router.callback_query(F.data.in_([
    "parent_contact", "parent_schedule",
    "curator_check", "curator_msg", "curator_reports",
    "student_help", "student_schedule"
]))
async def action_stub(callback: CallbackQuery):
    actions = {
        "parent_contact": "Связь с куратором",
        "parent_schedule": "Расписание ученика",
        "curator_check": "Проверка посещаемости",
        "curator_msg": "Сообщение для учеников",
        "curator_reports": "Отчёты по классам",
        "student_help": "Помощь от куратора",
        "student_schedule": "Твоё расписание",
    }
    await callback.message.answer(f"{actions[callback.data]} — функция в разработке 😉")
    await callback.answer()

