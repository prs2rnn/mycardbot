def format_users(user_data: dict) -> str:
    text = '👥 Список пользователей\n\n'
    text += '  ' + '\t\t'.join(map(lambda h: f'<b>{h}</b>', user_data['header'])) + '\n'
    for user in user_data['rows']:
        text += '• ' + '\t\t'.join(map(str, user))
        text += '\n'
    text += f'\n\n<i>Всего пользователей: {user_data["count"]}</i>'
    return text
