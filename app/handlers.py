from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(f'Добро пожаловать в магазин игровых аккаунтов!', reply_markup=kb.main)

@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите категорию товара', reply_markup=await kb.categories())

@router.message(F.text == 'Контакты')
async def contacts(message: Message):
    await message.answer('Наши контакты:\nПочта: mail_example@gugl.com\nМы в вк: https://vk.com/durov')

@router.message(F.text == 'О нас')
async def about(message: Message):
    await message.answer('Мы - магазин игровых аккаунтов. У нас вы найдете все новинки игровой индустрии по выгодным ценам')

@router.message(F.text == 'Корзина')
async def basket(message: Message):
    await message.answer('Данный раздел находится в разработке :(')

@router.callback_query(F.data.startswith('category_'))
async def category(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')
    await callback.message.answer('Выберите товар по категории',
                                  reply_markup=await kb.items(callback.data.split('_')[1]))
                                  
@router.callback_query(F.data.startswith('item_'))
async def item(callback: CallbackQuery):
    item_data = await rq.get_item(callback.data.split('_')[1])
    await callback.answer('Вы выбрали товар')
    await callback.message.answer(f'Название: {item_data.name}\nОписание: {item_data.description}\nЦена: {item_data.price}',
                                  reply_markup=await kb.item(item_data))
    
@router.callback_query(F.data.startswith('to_main'))
async def to_main(callback: CallbackQuery):
    await callback.answer('Вы вернулись на главную страницу')
    await callback.message.answer(f'Вы вернулись на главную страницу! Желаем интересных игровых находок!',
                                  reply_markup=kb.main)
    
@router.callback_query(F.data.startswith('buy_'))
async def buy_game(callback: CallbackQuery):
    await callback.answer('Вы начали процесс покупки')
    await callback.message.answer("Данный раздел находится в разработке :(")
                                  