# -*- coding: utf-8 -*-

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import TOKEN
from crude_function import *


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = KeyboardButton('Регистрация')
btn2 = KeyboardButton('Авторизация ')
#btn3 = KeyboardButton("Купить")
kb.add(btn1, btn2)
#kb.add(btn3)

menu = InlineKeyboardMarkup(row_width=2)
kb1 = InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')
kb2 = InlineKeyboardButton('Формула расчёта', callback_data='formulas')
menu.add(kb1, kb2)

menu2 = InlineKeyboardMarkup(row_width=4)
kb2_1 = InlineKeyboardButton('Product1', callback_data='product_buying')
kb2_2 = InlineKeyboardButton('Product2', callback_data='product_buying')
kb2_3 = InlineKeyboardButton('Product3', callback_data='product_buying')
kb2_4 = InlineKeyboardButton('Product4', callback_data='product_buying')
menu2.add(kb2_1, kb2_2, kb2_3, kb2_4)

menu3 = ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = KeyboardButton('Рассчитать')
btn2 = KeyboardButton('Информация')
btn3 = KeyboardButton("Купить")
menu3.add(btn1, btn2)
menu3.add(btn3)

class User_state(StatesGroup):
    username = State()
    authorization_name = State()
    growth = State()
    weight = State()
    age = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text = 'Информация')
async def info(message: types.Message):
    await message.answer('Информация о боте.', reply_markup=kb)

@dp.message_handler(text = 'Регистрация')
async def registration(message: types.Message):
    await message.answer('Введите имя пользователя (только латинскими буквами):')
    await RegistrationState.username.set()

@dp.message_handler(text = 'Авторизация')
async def authorization(message: types.Message):
    await message.answer('Введите имя пользователя (только латинскими буквами):')
    await User_state.authorization_name.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    if is_included(message.text)==False:
        await state.update_data(username=message.text)
        await message.answer('Введите вашу почту:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь существует, введите другое имя')


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer('Введите ваш возраст:')
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Регистрация прошла успешно', reply_markup=menu3)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await state.finish()

@dp.message_handler(text = 'Авторизация')
async def authorization(message: types.Message):
    await message.answer('Введите имя пользователя (только латинскими буквами):')
    await User_state.authorization_name.set()


@dp.message_handler(state=User_state.authorization_name)
async def set_authorization_name(message: types.Message, state: FSMContext):
    if is_included(message.text)==True:
        await state.update_data(authorization_name=message.text)
        await User_state.authorization_name.set()
        await User_state.username.set()
        data = await state.get_data()
        await message.answer('Выберите действие:', reply_markup=menu3)
        await state.finish()
    else:
        await message.answer('Пользователь не найден, введите другое имя', reply_markup=kb)

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message: types.Message):
    await message.answer('Выберите опцию.', reply_markup=menu)

@dp.message_handler(text = 'Купить')
async def get_buying_list(message: types.Message):
    products = get_all_products()
    for i in range(4):
        await message.answer(f'Название:{products[i][1]}|Описание:{products[i][2]}|Цена:{products[i][3]}')
        with open(f'{i+1}.jpg', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=menu2)

@dp.callback_query_handler(text = 'calories')
async def calories(call: types.CallbackQuery):

    await call.message.answer('Введите ваш имя (только латинскими буквами)')
    await User_state.username.set()


@dp.message_handler(state=User_state.username)
async def set_growth(message: types.Message, state: FSMContext):
    if is_included(message.text)==False:
        await message.answer('Пользователь не существует, введите другое имя', reply_markup=kb)
    else:
        user = get_user(message.text)
        await state.update_data(username=message.text, age=user[3])
        await message.answer('Введите ваш рост')
        await User_state.growth.set()

@dp.message_handler(state=User_state.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите ваш вес')
    await User_state.weight.set()

@dp.message_handler(state=User_state.weight)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    # print(data)
    # print(f'data: {data["username"]}, {data["age"]}, {data["growth"]}, {data["weight"]}')
    name = data["username"]
    age = int(data["age"])
    growth = int(data["growth"])
    weight = int(data["weight"])
    calories = (10*weight + 6.25*growth - 5*age + 5)*1.2
    await message.answer(f'Ваша суточная норма калорий: {calories}')
    await message.answer(f'Ваш индекс массы тела: {round(int(data["weight"])/((int(data["growth"])/100)**2),0)}')
    await message.answer('Выберите опцию.', reply_markup=menu3)
    await state.finish()

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call: types.CallbackQuery):
    await call.message.answer('Формула расчёта калорий: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

@dp.callback_query_handler(text = 'product_buying')
async def product_buying(call: types.CallbackQuery):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.message_handler()
async def all_message(message: types.Message):
    await message.answer(f'Введите команду /start, чтобы начать общение!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)