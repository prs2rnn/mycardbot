def format_users(header: list[str], users: list[tuple], limit=10) -> str:
    display_users = users[:limit]
    total = len(users)

    text = '👥 Список пользователей:\n\n'
    text += ', '.join(header)
    text += '\n'
    for i, u in enumerate(display_users, start=1):
        text += f'{i}. '
        text += ', '.join(map(str, u))
        text += '\n'

    if total > limit:
        text += f'\n\n...и ещё {total - limit} человек'

    text += f'\n\nВсего пользователей: {total}'

    return text
