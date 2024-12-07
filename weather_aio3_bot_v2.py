# ВНИМАНИЕ!!! Это вариант бота для работы с aiogram 3-й версии (вер.3.15.0)

import logging
import requests
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from dotenv import load_dotenv
from cachetools import TTLCache
# from aiogram.utils import executor

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем значения из .env файла
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("Бот запущен.")

# Инициализация бота и диспетчера
# bot = Bot(token=TELEGRAM_TOKEN, parse_mode=types.ParseMode.HTML)
# bot = Bot(token=TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
bot = Bot(
    token=TELEGRAM_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Кеш для городов (на 10 минут)
weather_cache = TTLCache(maxsize=100, ttl=600)

# Словарь для перевода погодных условий
weather_descriptions = {
    "clear sky": "Ясное небо",
    "few clouds": "Малооблачно",
    "scattered clouds": "Рассеянные облака",
    "broken clouds": "Переменная облачность",
    "shower rain": "Ливневый дождь",
    "rain": "Дождь",
    "thunderstorm": "Гроза",
    "snow": "Снег",
    "mist": "Туман",
}

# Клавиатура с кнопками "Старт" и "Помощь"
# start_button = KeyboardButton(text='/start')
# help_button = KeyboardButton(text='/help')
# markup = ReplyKeyboardMarkup(resize_keyboard=True).add(start_button, help_button)

# Создание кнопок
start_button = KeyboardButton(text='/start')
help_button = KeyboardButton(text='/help')

# Создание разметки клавиатуры
markup = ReplyKeyboardMarkup(
    keyboard=[[start_button, help_button]],  # Обязательно передать список списков
    resize_keyboard=True
)
# Или, если вы хотите добавлять кнопки, можно использовать метод add:
# markup = ReplyKeyboardMarkup(resize_keyboard=True).add(start_button).add(help_button)

# Функция для перевода погодных условий
def translate_description(description):
    description = description.lower()
    return weather_descriptions.get(description, description.capitalize())

# Команда /start
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    logger.info(f"Получена команда /start от пользователя {message.from_user.id} ({message.from_user.first_name})")
    await message.answer(
        f'Привет, {message.from_user.first_name}!\nНапиши название города, чтобы узнать погоду.',
        reply_markup=markup  # Отправляем клавиатуру с кнопкой
    )

# Команда /help
@dp.message(Command("help"))
async def send_help(message: types.Message):
    logger.info(f"Получена команда /help от пользователя {message.from_user.id}")
    help_text = (
        "Я бот для получения прогноза погоды.\n"
        "Просто отправь название города, и я покажу текущую погоду.\n"
        "Доступные команды:\n"
        "/start - Начать взаимодействие с ботом\n"
        "/help - Получить список доступных команд"
    )
    await message.answer(help_text)

# Обработка текстового сообщения с названием города
@dp.message()
async def get_weather_by_city(message: types.Message):
    city_name = message.text.strip().lower()  # Приведение города к нижнему регистру и удаление лишних пробелов
    logger.info(f"Запрос погоды для города: {city_name} от пользователя {message.from_user.id}")

    # Проверка на наличие данных в кеше
    if city_name in weather_cache:
        logger.info(f"Возвращаем закешированные данные для города: {city_name}")
        await message.answer(weather_cache[city_name])
        return

    try:
        # Установим тайм-аут для запроса в 20 секунд
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
        logger.info(f"Отправка запроса к OpenWeatherMap для города: {city_name}")
        response = requests.get(url, timeout=20)  # Тайм-аут 20 секунд

        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            description_ru = translate_description(description)  # Перевод описания погоды

            # Формируем сообщение с погодой
            weather_message = (
                f"Погода в городе {city_name.capitalize()}:\n"
                f"Температура: {temp}°C\n"
                f"Условия: {description_ru}"
            )
            logger.info(f"Погода для города {city_name.capitalize()} успешно получена.")

            # Сохраняем данные в кеш
            weather_cache[city_name] = weather_message

        else:
            weather_message = 'Не удалось получить данные о погоде. Пожалуйста, проверьте правильность названия города.'
            logger.warning(f"Ошибка получения данных для города: {city_name}. Код ответа API: {response.status_code}")

        await message.answer(weather_message)

    except requests.exceptions.Timeout:
        logger.error(f"Тайм-аут при получении данных о погоде для города {city_name}")
        await message.answer("Превышено время ожидания ответа от сервера. Пожалуйста, попробуйте снова.")

    except Exception as e:
        logger.error(f"Ошибка получения данных о погоде для города {city_name}: {e}")
        await message.answer("Произошла ошибка при получении данных. Попробуйте снова позже.")

if __name__ == '__main__':
    logger.info("Запуск бота в режиме long-polling")
    dp.run_polling(bot, skip_updates=True)