import requests
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()
user_roles = {} 
user_login_codes = {}


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
        url = f"http://127.0.0.1:8000/api/api/parenttg/{login_code}/"
    elif role == "student":
        url = f"http://127.0.0.1:8000/api/api/studenttg/{login_code}/"
    elif role == "curator":
        url = f"http://127.0.0.1:8000/api/api/teachertg/{login_code}"
    else:
        await message.answer("Сначала выберите роль в меню!!!")
        return
    

    response = requests.get(url)
    try:
        data = response.json()
    except Exception as e:
            await message.answer("⚠️ Сервер вернул невалидный ответ. Проверь login_code.")
            return


    # report_text = (
    #     f"📊 Отчёт по ученику: {data.get('student')}\n"
    #     f"✅ Посещено: {data.get('present')} дней\n"
    #     f"❌ Пропущено: {data.get('absent')} дней\n"
    #     f"📆 Всего занятий: {data.get('total')}"
    # )

    report_text = (
        f"📊 Отчёт по ученику: {data.get('student')}\n"
        f"✅ Посещено: {data.get('present')} дней\n"
        f"❌ Пропущено: {data.get('absent')} дней\n"
        f"📆 Всего занятий: {data.get('total')}"
    )

    if role == "parent":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            # [InlineKeyboardButton(text="📊 Посмотреть отчёт о посещаемости", callback_data="parent_report")],
            [InlineKeyboardButton(text="📞 Связаться с куратором", callback_data="parent_contact")],
            # [InlineKeyboardButton(text="🗓 Посмотреть расписание", callback_data="parent_schedule")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data= "main_menu")]
        ])
    elif role == "curator":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            # [InlineKeyboardButton(text="✅ Проверить посещаемость учеников", callback_data="curator_check")],
            # [InlineKeyboardButton(text="✉️ Отправить сообщение ученикам", callback_data="curator_msg")],
            # [InlineKeyboardButton(text="📈 Отчёты по посещаемости", callback_data="curator_reports")],
            [InlineKeyboardButton(text="📘 Группы", callback_data="teacher_groups")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
        ])
    elif role == "student":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            # [InlineKeyboardButton(text="📅 Моя посещаемость", callback_data="student_attendance")],
            [InlineKeyboardButton(text="🆘 Запросить помощь", callback_data="student_help")],
            # [InlineKeyboardButton(text="📚 Моё расписание", callback_data="student_schedule")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
        ])
    else:
        kb = None

    user_login_codes.update({message.from_user.id: login_code})

    await message.answer(text=report_text, reply_markup=kb)


@router.callback_query(F.data == "main_menu")
async def go_back_to_role_selection(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨‍👩‍👧 Родитель", callback_data="role_parent")],
        [InlineKeyboardButton(text="🧑‍🏫 Преподаватель", callback_data="role_curator")],
        [InlineKeyboardButton(text="🎓 Ученик", callback_data="role_student")]
    ])
    await callback.message.edit_text("🔙 Выберите вашу роль снова:", reply_markup=kb)
    await callback.answer()



# @router.callback_query(F.data == "parent_report")
# async def show_parent_report(callback: CallbackQuery):
#     login_code = callback.from_user.id
#     url = f"http://127.0.0.1:8000/api/api/parenttg/{login_code}/"
    
#     response = requests.get(url)
    
#     if response.status_code == 200:

#         data = response.json()
#         report_text = (
#             f"📊 Отчёт по ученику: {data.get('student')}\n"
#             f"✅ Посещено: {data.get('present')} дней\n"
#             f"❌ Пропущено: {data.get('absent')} дней\n"
#             f"📆 Всего занятий: {data.get('total')}"
#         )
#     else:
#         print("🔴 Ответ от Django:", response.text) 
#         report_text = (
#             f"⚠️ Ошибка от сервера ({response.status_code})\n"
#             f"Подробности см. в консоли"
#         )

#     #  Telegram лимит = 4096 символов
#     if len(report_text) > 4090:
#         report_text = report_text[:4090] + "..."

#     await callback.message.answer(report_text)
#     await callback.answer()





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


# @router.callback_query(F.data == "teacher_groups")
# async def show_teacher_groups(callback: CallbackQuery):
#     login_code = user_roles.get(callback.from_user.id)
#     url = f"http://127.0.0.1:8000/api/api/teacher-groups/{login_code}/"
#     response = requests.get(url)
#     groups = response.json()

#     if not groups:
#         await callback.message.answer("У вас пока нет назначенных групп.")
#         return

#     kb = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text=group["name"], callback_data=f"group_{group['id']}")] for group in groups
#     ])
#     await callback.message.answer("Ваши группы:", reply_markup=kb)
#     await callback.answer()

@router.callback_query(F.data.startswith("group_"))
async def show_group_attendance(callback: CallbackQuery):
    group_id = callback.data.split("_")[1]
    url = f"http://127.0.0.1:8000/api/api/group-attendance/{group_id}/"
    response = requests.get(url)
    data = response.json()

    if "error" in data:
        await callback.message.answer("Не удалось получить посещаемость.")
        return

    attendance_lines = [
        f"👤 {a['student']} — {'✅ Был' if a['was_present'] else '❌ Отсутствовал'}"
        for a in data["attendance"]
    ]
    text = (
        f"📚 Предмет: {data['subject']}\n"
        f"🕒 Дата: {data['datetime']}\n\n"
        "📊 Посещаемость:\n" + "\n".join(attendance_lines)
    )

    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data == "teacher_groups")
async def teacher_groups(callback: CallbackQuery):
    # login_code = user_roles.get(callback.from_user.id) 
    login_code = user_login_codes[callback.message.chat.id]
    url = f"http://127.0.0.1:8000/api/api/teacher-groups/{login_code}/"
    response = requests.get(url)
    data = response.json()

    buttons = [[InlineKeyboardButton(text=g["name"], callback_data=f"group_{g['id']}")] for g in data["groups"]]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.answer("📚 Ваши группы:", reply_markup=markup)
    await callback.answer()

@router.callback_query(F.data.startswith("group_"))
async def group_attendance(callback: CallbackQuery):
    group_id = int(callback.data.split("_")[1])
    response = requests.get(f"http://127.0.0.1:8000/api/api/group-attendance/{group_id}/")  # создадим это API ниже
    data = response.json()

    message = f"📝 Последняя посещаемость группы:\n"
    for student in data["students"]:
        status = "✅" if student["present"] else "❌"
        message += f"{status} {student['name']}\n"

    await callback.message.answer(message)
    await callback.answer()



@router.callback_query(F.data == "curator_check")
async def show_teacher_groups(callback: CallbackQuery):
    teacher_login = login_codes.get(callback.from_user.id)
    # login_code = user_roles.get(callback.from_user.id)

    response = requests.get(f"http://127.0.0.1:8000/api/api/teacher_groups/{teacher_login}/")
    if response.status_code != 200:
        await callback.message.answer("Ошибка при получении групп.")
        return

    data = response.json()
    groups = data.get("groups", [])
    
    if not groups:
        await callback.message.answer("Нет доступных групп.")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=group['name'], callback_data=f"group_{group['id']}")]
        for group in groups
    ])
    await callback.message.answer("Выберите группу для просмотра посещаемости:", reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("group_"))
async def show_group_attendance(callback: CallbackQuery):
    group_id = int(callback.data.split("_")[1])

    response = requests.get(f"http://127.0.0.1:8000/api/api/group_attendance/{group_id}/")
    if response.status_code != 200:
        await callback.message.answer("Ошибка при получении посещаемости.")
        return

    data = response.json()
    text = f"📝 Последнее занятие группы:\n\n"
    for item in data["attendance"]:
        status = "✅" if item["attendance"] else "❌"
        text += f"{status} {item['student']}\n"

    await callback.message.answer(text)
    await callback.answer()

