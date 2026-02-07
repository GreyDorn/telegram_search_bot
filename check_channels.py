"""
Скрипт для проверки доступности каналов
"""

import asyncio
import sys
from telethon import TelegramClient
import config_telethon as config

# Исправление кодировки для Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

async def check_channels():
    client = TelegramClient(config.SESSION_NAME, config.API_ID, config.API_HASH)
    await client.start(phone=config.PHONE)
    
    print(f"\nПроверяю доступность {len(config.CHANNELS)} каналов...\n")
    
    available = []
    unavailable = []
    
    for i, channel in enumerate(config.CHANNELS, 1):
        try:
            entity = await client.get_entity(channel)
            title = getattr(entity, 'title', channel)
            username = getattr(entity, 'username', 'Без username')
            
            # Проверяем подписку
            try:
                await client.get_messages(entity, limit=1)
                available.append((channel, title))
                print(f"[OK] {i}. {channel} - {title}")
            except Exception as e:
                unavailable.append((channel, f"Нет доступа: {str(e)[:50]}"))
                print(f"[WARN] {i}. {channel} - Найден, но нет доступа к сообщениям")
                
        except Exception as e:
            unavailable.append((channel, f"Не найден: {str(e)[:50]}"))
            print(f"[ERR] {i}. {channel} - НЕ НАЙДЕН или НЕТ ДОСТУПА")
    
    print(f"\n\nИТОГО:")
    print(f"Доступно: {len(available)}")
    print(f"Недоступно: {len(unavailable)}")
    
    if unavailable:
        print(f"\n\nНЕДОСТУПНЫЕ КАНАЛЫ:")
        for ch, reason in unavailable[:10]:
            print(f"  - {ch}: {reason}")
        if len(unavailable) > 10:
            print(f"  ... и еще {len(unavailable) - 10}")
    
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(check_channels())
