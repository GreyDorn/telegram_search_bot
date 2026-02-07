"""
Телеграм-бот для поиска по истории каналов (Telethon версия)
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
    """Запуск бота"""
    # Проверка конфигурации
    if not config.API_ID or not config.API_HASH:
        logger.error("❌ API_ID или API_HASH не настроены!")
        logger.error("Получи их на https://my.telegram.org")
        return
    
    if not config.PHONE:
        logger.error("❌ PHONE не настроен!")
        return
    
    if not config.CHANNELS:
        logger.error("❌ Список каналов пуст!")
        return
    
    logger.info("🤖 Запуск бота с Telethon...")
    logger.info(f"📋 Подключено каналов: {len(config.CHANNELS)}")
    logger.info(f"🔍 Глубина поиска: {config.SEARCH_LIMIT} сообщений")
    
    # Создание клиента
    client = TelegramClient(config.SESSION_NAME, config.API_ID, config.API_HASH)
    
    # Обработчик команды /start
    @client.on(events.NewMessage(pattern='/start'))
    async def start_handler(event):
        """Обработчик команды /start"""
        # Игнорируем сообщения в группах
        if event.is_group or event.is_channel:
            return
        
        await event.respond(
            "👋 Привет! Я бот для поиска информации по истории каналов.\n\n"
            "📝 Просто отправь мне ключевое слово, и я найду все упоминания.\n\n"
            f"🔍 Поиск ведется по {len(config.CHANNELS)} каналам\n"
            f"📊 Глубина поиска: последние {config.SEARCH_LIMIT} сообщений в каждом канале"
        )
    
    # Обработчик команды /help
    @client.on(events.NewMessage(pattern='/help'))
    async def help_handler(event):
        """Обработчик команды /help"""
        # Игнорируем сообщения в группах
        if event.is_group or event.is_channel:
            return
        
        channels_list = "\n".join([f"• {ch}" for ch in config.CHANNELS[:10]])
        if len(config.CHANNELS) > 10:
            channels_list += f"\n... и еще {len(config.CHANNELS) - 10} каналов"
        
        await event.respond(
            f"ℹ️ **Как пользоваться ботом:**\n\n"
            f"1️⃣ Отправь любое слово или фразу\n"
            f"2️⃣ Подожди, пока бот проверит все каналы\n"
            f"3️⃣ Получи результаты с кнопками\n\n"
            f"📋 **Подключенные каналы ({len(config.CHANNELS)}):**\n{channels_list}\n\n"
            f"🔍 **Глубина поиска:** {config.SEARCH_LIMIT} последних сообщений\n\n"
            f"⚡ **Преимущество:** поиск по истории, а не только по новым сообщениям!"
        )
    
    # Обработчик команды /channels
    @client.on(events.NewMessage(pattern='/channels'))
    async def channels_handler(event):
        """Список подключенных каналов"""
        # Игнорируем сообщения в группах
        if event.is_group or event.is_channel:
            return
        
        if not config.CHANNELS:
            await event.respond("❌ Список каналов пуст!")
            return
        
        response = "📋 **Подключенные каналы:**\n\n"
        
        for i, channel in enumerate(config.CHANNELS[:20], 1):
            response += f"{i}. {channel}\n"
        
        if len(config.CHANNELS) > 20:
            response += f"\n... и еще {len(config.CHANNELS) - 20} каналов"
        
        await event.respond(response)
    
    # Обработчик поиска
    @client.on(events.NewMessage())
    async def search_handler(event):
        """Поиск по ключевому слову"""
        # Игнорируем сообщения в группах и каналах
        if event.is_group or event.is_channel:
            return
        
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
        
        # Поиск в каждом канале
        for channel in config.CHANNELS:
            try:
                logger.info(f"Поиск в канале: {channel}")
                
                # Получение сущности канала
                entity = await client.get_entity(channel)
                channel_title = getattr(entity, 'title', channel)
                channel_username = getattr(entity, 'username', None)
                
                # Поиск по истории сообщений
                async for message in client.iter_messages(entity, limit=config.SEARCH_LIMIT):
                    if message.text and query in message.text.lower():
                        # Создание ссылки на сообщение
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
                            'link': link
                        })
                
                channels_checked += 1
                
                # Обновление прогресса каждые 5 каналов
                if channels_checked % 5 == 0:
                    await search_msg.edit(
                        f"🔍 Ищу '{query}'...\n"
                        f"✅ Проверено: {channels_checked}/{len(config.CHANNELS)}\n"
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
                "• Использовать другие ключевые слова\n"
                "• Проверить доступ к каналам командой /channels"
            )
            return
        
        # Сортировка по дате (новые первые)
        results.sort(key=lambda x: x['date'], reverse=True)
        
        # Отправка результатов
        await event.respond(
            f"✅ Найдено результатов: **{len(results)}**\n\n"
            f"📝 Показываю первые {min(len(results), 10)}:"
        )
        
        # Отправка каждого результата
        for i, result in enumerate(results[:10], 1):
            # Создание превью текста
            preview = result['text'][:config.PREVIEW_LENGTH]
            if len(result['text']) > config.PREVIEW_LENGTH:
                preview += "..."
            
            # Форматирование даты
            date_str = result['date'].strftime('%d.%m.%Y %H:%M')
            
            # Создание кнопок
            buttons = []
            if result['link']:
                buttons.append([Button.url("📖 Читать полностью", result['link'])])
            
            message_text = (
                f"**Результат {i}** из канала {result['channel_title']}\n"
                f"🕐 {date_str}\n\n"
                f"{preview}"
            )
            
            await event.respond(message_text, buttons=buttons if buttons else None)
        
        if len(results) > 10:
            await event.respond(
                f"ℹ️ Показано 10 из {len(results)} результатов.\n"
                "Уточни запрос для более точных результатов."
            )
    
    # Подключение как пользователь (UserBot)
    # Это позволяет читать историю каналов
    await client.start(phone=config.PHONE)
    
    logger.info("✅ Бот запущен и готов к работе!")
    logger.info("💡 Бот может искать по истории сообщений в каналах")
    logger.info(f"👤 Авторизован как пользователь: {config.PHONE}")
    
    # Ожидание событий
    await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
