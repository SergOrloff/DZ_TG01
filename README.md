# Weather_aio_bot

## Описание

Weather_aio_bot — это телеграм-бот, который предоставляет текущую информацию о погоде в указанном пользователем городе. Бот построен с использованием библиотеки `aiogram` версии 3.15.0 и использует API OpenWeatherMap для получения данных о погоде.


## Функциональные возможности

- Получение текущей погоды по названию города.
- Перевод погодных условий с английского на русский.
- Кэширование результатов запросов для снижения нагрузки на API и ускорения ответов.

## Установка

### Требования

- Python 3.10 или выше
- Установленный и настроенный аккаунт на платформе Telegram
- Токен Telegram Bot API
- API-ключ OpenWeatherMap

### Шаги установки

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/ваш_репозиторий/DZ_TG01.git
   cd DZ_TG01
   ```

2. **Создайте виртуальное окружение и активируйте его:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # для Linux/MacOS
   venv\Scripts\activate  # для Windows
   ```

3. **Установите зависимости:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте переменные окружения:**

   Создайте файл `.env` в корневой директории проекта и добавьте в него следующие строки:

   ```
   TELEGRAM_TOKEN=ваш_токен_телеграм_бота
   WEATHER_API_KEY=ваш_ключ_api_openweathermap
   ```

5. **Запустите бота:**

   ```bash
   python weather_aio3_bot.py
   или
   python weather_aio3_bot_v2.py
   ```

## Использование

После запуска бот будет ждать команды от пользователей. Поддерживаются следующие команды:

- `/start` — приветствие и инструкция по использованию
- `/help` — список доступных команд и инструкции

Для получения погоды просто отправьте название города в чат с ботом.

## Логирование

Бот ведет логирование своих действий, записывая информацию в файл `bot.log`. Логирование поможет отследить ошибки и действия пользователей.

## Кеширование

Для оптимизации работы OpenWeatherMap бот использует кеширование данных о погоде. Информация о погоде в городах хранится в кеше в течение 10 минут. Это позволяет уменьшить количество запросов к API 

## Обработка ошибок

В случае возникновения ошибок при запросе данных о погоде, бот отправит пользователю сообщение с просьбой повторить попытку позже. Все ошибки логируются в `bot.log`.

## Зависимости

- `aiogram==3.15.0`
- `requests`
- `python-dotenv`
- `cachetools`

## Дополнительно

Для корректной работы бота необходимо, чтобы токен и API-ключ были действительными. Убедитесь, что ваши ключи и токены не просочились в публичный доступ.

## Контрибьюции

Если вы хотите внести свой вклад в проект, пожалуйста, создайте issue или pull request в репозитории на GitHub. Ваш вклад поможет улучшить проект и сделать его более функциональным.

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности можно найти в файле LICENSE в корневой директории проекта.
