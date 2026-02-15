"""
Гибридный Телеграм-бот для поиска по истории каналов
- Bot Account для общения с пользователями
- UserBot для чтения каналов
"""

import logging
import asyncio
from telethon import TelegramClient, events, Button
from telethon.tl.types import User
import config_telethon as config

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def main():
    """Запуск гибридного бота"""
    # Проверка конфигурации
    if not config.API_ID or not config.API_HASH:
        logger.error("❌ API_ID или API_HASH не настроены!")
        return
    
    if not config.BOT_TOKEN:
        logger.error("❌ BOT_TOKEN не настроен!")
        return
    
    if not config.PHONE:
        logger.error("❌ PHONE не настроен!")
        return
    
    if not config.CHANNELS:
        logger.error("❌ Список каналов пуст!")
        return
    
    logger.info("🤖 Запуск гибридного бота...")
    logger.info(f"📋 Подключено каналов: {len(config.CHANNELS)}")
    logger.info(f"🔍 Глубина поиска: {config.SEARCH_LIMIT} сообщений")
    
    # КЛИЕНТ 1: Bot Account для общения с пользователями
    bot_client = TelegramClient('bot_account', config.API_ID, config.API_HASH)
    
    # КЛИЕНТ 2: UserBot для чтения каналов
    user_client = TelegramClient(config.SESSION_NAME, config.API_ID, config.API_HASH)
    
    # Подключение Bot Account
    await bot_client.start(bot_token=config.BOT_TOKEN)
    logger.info("✅ Bot Account запущен (для пользователей)")
    
    # Подключение UserBot
    await user_client.start(phone=config.PHONE)
    logger.info("✅ UserBot запущен (для чтения каналов)")
    
    # Получаем информацию о боте
    bot_me = await bot_client.get_me()
    logger.info(f"👤 Бот: @{bot_me.username}")
    
    # ===== ОБРАБОТЧИКИ ДЛЯ BOT ACCOUNT =====
    
    @bot_client.on(events.NewMessage(pattern='/start'))
    async def start_handler(event):
        """Обработчик команды /start"""
        await event.respond(
            "Привет! 👋\n"
            "Я ищу информацию по каналам о китайском языке.\n"
            "Просто напиши слово - и я найду все упоминания!"
        )
    
    @bot_client.on(events.NewMessage(pattern='/help'))
    async def help_handler(event):
        """Обработчик команды /help"""
        channels_list = "\n".join([f"• {ch}" for ch in config.CHANNELS[:10]])
        if len(config.CHANNELS) > 10:
            channels_list += f"\n... и еще {len(config.CHANNELS) - 10} каналов"
        
        await event.respond(
            f"ℹ️ **Как пользоваться ботом:**\n\n"
            f"1️⃣ Отправь любое слово или фразу\n"
            f"2️⃣ Подожди, пока бот проверит все каналы\n"
            f"3️⃣ Получи результаты с кнопками\n\n"
            f"📋 **Подключенные каналы ({len(config.CHANNELS)}):**\n{channels_list}\n\n"
            f"🔍 **Глубина поиска:** {config.SEARCH_LIMIT} последних сообщений"
        )
    
    @bot_client.on(events.NewMessage(pattern='/channels'))
    async def channels_handler(event):
        """Список подключенных каналов"""
        response = "📋 **Подключенные каналы:**\n\n"
        
        for i, channel in enumerate(config.CHANNELS[:20], 1):
            response += f"{i}. {channel}\n"
        
        if len(config.CHANNELS) > 20:
            response += f"\n... и еще {len(config.CHANNELS) - 20} каналов"
        
        await event.respond(response)
    
    @bot_client.on(events.NewMessage())
    async def search_handler(event):
        """Поиск по ключевому слову"""
        # Игнорируем команды
        if event.raw_text.startswith('/'):
            return
        
        query = event.raw_text.lower().strip()
        
        if not query:
            await event.respond("❌ Пожалуйста, отправь ключевое слово для поиска.")
            return
        
        # Сообщение о начале поиска
        search_msg = await event.respond(
            f"🔍 Ищу '{query}' по {len(config.CHANNELS)} каналам...\n"
            f"⏳ Это может занять некоторое время..."
        )
        
        results = []
        channels_checked = 0
        errors = 0
        
        # Разбиваем запрос на слова (для поиска по отдельным словам)
        query_words = query.split()
        
        # ПОИСК ЧЕРЕЗ USERBOT (может читать каналы)
        for channel in config.CHANNELS:
            try:
                logger.info(f"Поиск в канале: {channel}")
                
                # Получение сущности канала через UserBot
                entity = await user_client.get_entity(channel)
                channel_title = getattr(entity, 'title', channel)
                channel_username = getattr(entity, 'username', None)
                
                # Поиск по истории через UserBot
                async for message in user_client.iter_messages(entity, limit=config.SEARCH_LIMIT):
                    if message.text:
                        message_lower = message.text.lower()
                        
                        # Проверяем: есть ли полное совпадение или хотя бы одно слово
                        full_match = query in message_lower
                        word_match = any(word in message_lower for word in query_words) if len(query_words) > 1 else False
                        
                        if full_match or word_match:
                            # Создание ссылки
                            if channel_username:
                                link = f"https://t.me/{channel_username}/{message.id}"
                            else:
                                link = None
                            
                            results.append({
                                'channel': channel,
                                'channel_title': channel_title,
                                'message_id': message.id,
                                'text': message.text,
                                'date': message.date,
                                'link': link,
                                'match_type': 'full' if full_match else 'partial'  # Для сортировки
                            })
                
                channels_checked += 1
                
                # Обновление прогресса каждые 5 каналов
                if channels_checked % 5 == 0:
                    await search_msg.edit(
                        f"🔍 Ищу '{query}'...\n"
                        f"📊 Найдено: {len(results)}"
                    )
                    
            except Exception as e:
                logger.error(f"Ошибка при поиске в канале {channel}: {e}")
                errors += 1
                continue
        
        # Удаление сообщения о поиске
        await search_msg.delete()
        
        # Вывод результатов
        if not results:
            await event.respond(
                f"😔 По запросу '**{query}**' ничего не найдено.\n\n"
                f"📊 Проверено каналов: {channels_checked}\n"
                f"📝 Проверено сообщений: ~{channels_checked * config.SEARCH_LIMIT}\n"
                f"⚠️ Ошибок доступа: {errors}\n\n"
                "💡 Попробуй:\n"
                "• Изменить запрос\n"
                "• Использовать другие ключевые слова"
            )
            return
        
        # Сортировка: сначала полные совпадения, потом частичные, внутри по дате (новые первые)
        results.sort(key=lambda x: (0 if x['match_type'] == 'full' else 1, -x['date'].timestamp()))
        
        # Отправка результатов
        await event.respond(
            f"✅ Найдено результатов: **{len(results)}**\n\n"
            f"📝 Показываю первые {min(len(results), 10)}:"
        )
        
        # Отправка каждого результата
        for i, result in enumerate(results[:10], 1):
            # Полный текст без обрезки
            full_text = result['text']
            
            # Форматирование даты
            date_str = result['date'].strftime('%d.%m.%Y %H:%M')
            
            message_text = (
                f"**Результат {i}** из канала {result['channel_title']}\n"
                f"🕐 {date_str}\n\n"
                f"{full_text}"
            )
            
            await event.respond(message_text)
        
        if len(results) > 10:
            await event.respond(
                f"ℹ️ Показано 10 из {len(results)} результатов.\n"
                "Уточни запрос для более точных результатов."
            )
    
    logger.info("✅ Гибридный бот готов к работе!")
    logger.info(f"💡 Пользователи пишут боту @{bot_me.username}")
    logger.info(f"💡 Поиск идет через UserBot: {config.PHONE}")
    
    # Ожидание событий (оба клиента работают одновременно)
    await bot_client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
