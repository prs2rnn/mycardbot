from aiogram import Bot
from aiogram.types import Message


def get_send_methods(bot: Bot, header: str, content_data: dict):
    send_methods = {
        'photo': lambda chat_id: bot.send_photo(
            chat_id,
            photo=content_data['photo_file_id'],
            caption=f'{header}{content_data["caption"]}',
        ),
        'document': lambda chat_id: bot.send_document(
            chat_id,
            document=content_data['document_file_id'],
            caption=f'{header}{content_data["caption"]}',
        ),
        'video': lambda chat_id: bot.send_video(
            chat_id,
            video=content_data['video_file_id'],
            caption=f'{header}{content_data["caption"]}',
        ),
        'video_note': lambda chat_id: bot.send_video_note(
            chat_id,
            video_note=content_data['video_note_file_id'],
        ),
        'voice': lambda chat_id: bot.send_voice(
            chat_id,
            voice=content_data['voice_file_id'],
            caption=f'{header}{content_data["caption"]}',
        ),
        'audio': lambda chat_id: bot.send_audio(
            chat_id,
            audio=content_data['audio_file_id'],
            caption=f'{header}{content_data["caption"]}',
            title=content_data.get('title'),
            performer=content_data.get('performer'),
        ),
        'text': lambda chat_id: bot.send_message(
            chat_id, text=f'{header}\n{content_data["text"]}'
        ),
    }
    return send_methods


async def extract_content_from_message(message: Message) -> tuple[dict, str]:
    content_data = {}
    content_type = None

    if message.photo:
        content_type = 'photo'
        content_data['caption'] = message.caption or 'Фото без описания'
        content_data['photo_file_id'] = message.photo[-1].file_id
    elif message.document:
        content_type = 'document'
        content_data['caption'] = (
            message.caption or f'Документ: {message.document.file_name}'
        )
        content_data['document_file_id'] = message.document.file_id
        content_data['file_name'] = message.document.file_name
    elif message.video:
        content_type = 'video'
        content_data['caption'] = message.caption or 'Видео без описания'
        content_data['video_file_id'] = message.video.file_id
    elif message.video_note:
        content_type = 'video_note'
        content_data['video_note_file_id'] = message.video_note.file_id
    elif message.voice:
        content_type = 'voice'
        content_data['caption'] = message.caption or 'Голосовое сообщение'
        content_data['voice_file_id'] = message.voice.file_id
        content_data['duration'] = message.voice.duration
    elif message.audio:
        content_type = 'audio'
        content_data['caption'] = (
            message.caption or f'Аудио: {message.audio.title or "Без названия"}'
        )
        content_data['audio_file_id'] = message.audio.file_id
        content_data['title'] = message.audio.title
        content_data['performer'] = message.audio.performer
    elif message.text:
        content_type = 'text'
        content_data['text'] = message.text
    else:
        await message.answer('Этот тип сообщения не поддерживается')

    return content_data, content_type
