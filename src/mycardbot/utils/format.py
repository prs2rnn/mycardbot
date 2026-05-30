import re


def format_users(user_data: dict) -> str:
    text = '👥 Список пользователей\n\n'
    text += '  ' + '\t\t'.join(map(lambda h: f'<b>{h}</b>', user_data['header'])) + '\n'
    for user in user_data['rows']:
        text += '• ' + '\t\t'.join(map(str, user))
        text += '\n'
    text += f'\n\n<i>Всего пользователей: {user_data["count"]}</i>'
    return text


def markdown_to_html(text: str) -> str:
    # Headings
    text = re.sub(r'^### (.+)$', r'🔹 <b>\1</b>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'🔸 <b>\1</b>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'📌 <b>\1</b>', text, flags=re.MULTILINE)

    # Bold
    text = re.sub(r'\*(.*?)\*', r'<b>\1</b>', text)

    # Italic
    text = re.sub(r'\_(.*?)\_', r'<i>\1</i>', text)

    # Code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)

    return text
