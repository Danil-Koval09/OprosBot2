from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, ReplyKeyboardRemove
from database import DataBase
from keyboards import generate_start_button, generate_gender_buttons
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from states import Register

bot = Bot(token='')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DataBase()


@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    chat_id = message.chat.id
    db.create_users_table()
    user = db.get_user_by_chat_id(chat_id)
    if user:
        if user[2] is None or user[3] is None or user[4] is None or user[5] is None or user[6] is None:
            await bot.send_message(chat_id, 'Некорректные данные,пройдите регистрацию заново',
                                   reply_markup=generate_start_button())
        else:
            await bot.send_message(chat_id, 'Вы уже прошли регистрацию, данные сохранены')

    else:
        db.first_registration_user(chat_id)
        await bot.send_message(chat_id, 'Чтобы пройти регистрацию, нажмите на кнопку ниже',
                               reply_markup=generate_start_button())


@dp.message_handler(regexp='Начать регистрацию')
async def start_register(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await Register.full_name.set()
    await bot.send_message(chat_id, 'Введите фамилию и имя:')


@dp.message_handler(state=Register.full_name)
async def get_full_name_gender(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await state.update_data(full_name=message.text)
    await Register.gender.set()
    await bot.send_message(chat_id, 'Выберите свой пол', reply_markup=generate_gender_buttons())


@dp.message_handler(regexp='(М|Ж)', state=Register.gender)
async def get_gender_ask_age(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await state.update_data(gender=message.text)
    await Register.age.set()
    await bot.send_message(chat_id, 'Введите ваш возраст: ', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(regexp='\d\d', state=Register.age)
async def get_age_ask_phone(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await state.update_data(age=message.text)
    await Register.phone.set()
    await bot.send_message(chat_id, 'Введите телефон в формате +99800000000: ')


@dp.message_handler(regexp='crypto|card', state=Register.phone)
async def get_phone_ask_payment_card(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await state.update_data(phone=message.text)
    await Register.payment.set()
    await bot.send_message(chat_id, 'Введите номер карты в формате: 0000 0000 0000 0000')


@dp.message_handler(state=Register.payment)
async def get_payment_save_data(message: Message, state: FSMContext):
    chat_id = message.chat.id
    data = await state.get_data()
    payment = message.text
    db.update_data(chat_id, data['full_name'], data['gender'], data['age'], data['phone'], payment)
    await state.finish()
    await bot.send_message(chat_id, 'Вы успешно зарегистрировались, будем ждать вас на нашем мероприятии')


@dp.message_handler(commands=['export'])
async def export_excel(message: Message):
    chat_id = message.chat.id
    db.get_data_for_excel()
    with open('result.xlsx', mode='rb') as file:
        await bot.send_document(chat_id, file)


executor.start_polling(dp)
