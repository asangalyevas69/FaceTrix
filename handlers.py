from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

router = Router()

async def greet_and_start(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🚀 Начать")]],
        resize_keyboard=True, 
        one_time_keyboard=False  
    )
    await message.answer(
        "👋 Здравствуйте! Добро пожаловать в Study Controle 📚\n\n"
        "Нажмите кнопку ниже, чтобы начать:",
        reply_markup=keyboard
    )

@router.message(F.text.in_(["🚀 Начать", "меню", "Меню"]))
async def show_main_menu(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨‍👩‍👧 Родитель", callback_data="role_parent")],
        [InlineKeyboardButton(text="🧑‍🏫 Куратор", callback_data="role_curator")],
        [InlineKeyboardButton(text="🎓 Ученик", callback_data="role_student")]
    ])
    await message.answer("Выберите вашу роль:", reply_markup=kb)

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

@router.callback_query(F.data == "main_menu")
async def go_main_menu(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨‍👩‍👧 Родитель", callback_data="role_parent")],
        [InlineKeyboardButton(text="🧑‍🏫 Куратор", callback_data="role_curator")],
        [InlineKeyboardButton(text="🎓 Ученик", callback_data="role_student")]
    ])
    await callback.message.edit_text("Выберите вашу роль:", reply_markup=kb)
    await callback.answer()

@router.callback_query(F.data == "parent_report")
async def show_fake_report(callback: CallbackQuery):
    await callback.message.answer(
        "📊 Отчёт по ученику:\n"
        "✅ Посещено: 18 дней\n"
        "❌ Пропущено: 2 дня\n"
        "📈 Успеваемость: высокая\n"
        "💬 Замечаний нет"
    )
    await callback.answer()

@router.callback_query(F.data.in_([
    "parent_contact", "parent_schedule",
    "curator_check", "curator_msg", "curator_reports",
    "student_attendance", "student_help", "student_schedule"
]))
async def action_stub(callback: CallbackQuery):
    actions = {
        "parent_contact": "Связь с куратором",
        "parent_schedule": "Расписание ученика",
        "curator_check": "Проверка посещаемости",
        "curator_msg": "Сообщение для учеников",
        "curator_reports": "Отчёты по классам",
        "student_attendance": "Твоя посещаемость",
        "student_help": "Помощь от куратора",
        "student_schedule": "Твоё расписание",
    }
    await callback.message.answer(f"{actions[callback.data]} — функция в разработке 😉")
    await callback.answer()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await greet_and_start(message)

@router.message(F.text)
async def greet_and_start_handler(message: Message):
    await greet_and_start(message)