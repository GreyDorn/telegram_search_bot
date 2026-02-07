"""
Телеграм-бот для поиска по каналам
"""

import logging
from datetime import datetime
from collections import deque
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from telegram.error import TelegramError
import config

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Хранилище сообщений из каналов (в памяти)
# Структура: {channel_id: deque([{message_id, text, date, link}, ...])}
channel_messages = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    await update.message.reply_text(
        "👋 Привет! Я бот для поиска информации по каналам.\n\n"
        "📝 Просто отправь мне ключевое слово, и я найду все упоминания в подключенных каналах.\n\n"
        f"🔍 Поиск ведется по {len(config.CHANNELS)} каналам."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    total_messages = sum(len(msgs) for msgs in channel_messages.values())
    channels_count = len(channel_messages)
    
    await update.message.reply_text(
        "ℹ️ <b>Как пользоваться ботом:</b>\n\n"
        "1️⃣ Отправь любое слово или фразу\n"
        "2️⃣ Получи результаты поиска\n"
        "3️⃣ Нажми на кнопку для просмотра полного сообщения\n\n"
        f"📊 <b>Статистика:</b>\n"
        f"• Сохранено сообщений: {total_messages}\n"
        f"• Активных каналов: {channels_count}\n"
        f"• Лимит на канал: {config.SEARCH_LIMIT} сообщений\n\n"
        "⚠️ <b>Важно:</b> Бот сохраняет только новые сообщения, "
        "которые приходят после его запуска.",
        parse_mode='HTML'
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Статистика по сохраненным сообщениям"""
    if not channel_messages:
        await update.message.reply_text("📊 Пока нет сохраненных сообщений.")
        return
    
    stats_text = "📊 <b>Статистика по каналам:</b>\n\n"
    
    for channel_id, messages in channel_messages.items():
        if messages:
            channel_name = messages[0]['channel_name']
            stats_text += f"• {channel_name}: {len(messages)} сообщений\n"
    
    total = sum(len(msgs) for msgs in channel_messages.values())
    stats_text += f"\n<b>Всего:</b> {total} сообщений"
    
    await update.message.reply_text(stats_text, parse_mode='HTML')


async def channel_post_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик новых сообщений из каналов"""
    if not update.channel_post:
        return
    
    post = update.channel_post
    channel_id = post.chat.id
    channel_username = post.chat.username
    
    # Инициализация хранилища для канала
    if channel_id not in channel_messages:
        channel_messages[channel_id] = deque(maxlen=config.SEARCH_LIMIT)
    
    # Сохранение сообщения
    if post.text:
        message_link = None
        if channel_username:
            message_link = f"https://t.me/{channel_username}/{post.message_id}"
        
        message_data = {
            'message_id': post.message_id,
            'text': post.text,
            'date': post.date,
            'link': message_link,
            'channel_name': f"@{channel_username}" if channel_username else str(channel_id)
        }
        
        channel_messages[channel_id].append(message_data)
        logger.info(f"Сохранено сообщение из канала {channel_id}")


async def search_in_channels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Поиск по ключевому слову в каналах"""
    query = update.message.text.lower().strip()
    
    if not query:
        await update.message.reply_text("❌ Пожалуйста, отправь ключевое слово для поиска.")
        return
    
    # Проверка наличия данных
    if not channel_messages:
        await update.message.reply_text(
            "⚠️ Пока нет сообщений для поиска.\n\n"
            "Бот сохраняет сообщения из каналов в реальном времени.\n"
            "Подожди немного, пока накопятся данные."
        )
        return
    
    # Отправка сообщения о начале поиска
    searching_msg = await update.message.reply_text(f"🔍 Ищу '{query}'...")
    
    results = []
    
    # Поиск по всем сохраненным сообщениям
    for channel_id, messages in channel_messages.items():
        for msg in messages:
            if query in msg['text'].lower():
                results.append(msg)
    
    # Сортировка по дате (новые первые)
    results.sort(key=lambda x: x['date'], reverse=True)
    
    # Удаление сообщения о поиске
    await searching_msg.delete()
    
    # Вывод результатов
    if not results:
        total_messages = sum(len(msgs) for msgs in channel_messages.values())
        await update.message.reply_text(
            f"😔 По запросу '<b>{query}</b>' ничего не найдено.\n\n"
            f"📊 Проверено сообщений: {total_messages}\n"
            f"📋 Каналов: {len(channel_messages)}\n\n"
            "💡 Попробуй:\n"
            "• Изменить запрос\n"
            "• Использовать другие ключевые слова",
            parse_mode='HTML'
        )
        return
    
    # Отправка результатов
    await update.message.reply_text(
        f"✅ Найдено результатов: <b>{len(results)}</b>\n\n"
        f"📝 Показываю первые {min(len(results), 10)}:",
        parse_mode='HTML'
    )
    
    # Отправка каждого результата
    for i, result in enumerate(results[:10], 1):
        # Создание превью текста
        preview = result['text'][:config.PREVIEW_LENGTH]
        if len(result['text']) > config.PREVIEW_LENGTH:
            preview += "..."
        
        # Создание кнопки для просмотра полного сообщения
        keyboard = []
        if result['link']:
            keyboard.append([InlineKeyboardButton("📖 Читать полностью", url=result['link'])])
        
        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None
        
        # Форматирование даты
        date_str = result['date'].strftime('%d.%m.%Y %H:%M')
        
        await update.message.reply_text(
            f"<b>Результат {i}</b> из канала {result['channel_name']}\n"
            f"🕐 {date_str}\n\n"
            f"{preview}",
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    
    if len(results) > 10:
        await update.message.reply_text(
            f"ℹ️ Показано 10 из {len(results)} результатов.\n"
            "Уточни запрос для более точных результатов."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(f"Ошибка: {context.error}")
    if update and update.message:
        await update.message.reply_text(
            "❌ Произошла ошибка. Попробуй позже или обратись к администратору."
        )


def main() -> None:
    """Запуск бота"""
    if not config.BOT_TOKEN or config.BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        logger.error("❌ Токен бота не настроен! Проверь файл config.py или .env")
        return
    
    if not config.CHANNELS:
        logger.error("❌ Список каналов пуст! Добавь каналы в config.py или .env")
        return
    
    logger.info(f"🤖 Запуск бота...")
    logger.info(f"📋 Подключено каналов: {len(config.CHANNELS)}")
    
    # Создание приложения
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    
    # Обработчик сообщений из каналов
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, channel_post_handler))
    
    # Обработчик поисковых запросов от пользователей
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE, search_in_channels))
    
    # Обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запуск бота
    logger.info("✅ Бот запущен и готов к работе!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
