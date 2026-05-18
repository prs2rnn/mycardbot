import json
import logging
import time

from mycardbot.database.cache import cache_repo
from mycardbot.utils.api import fetch_json


async def get_changelog():
    now = time.time()
    await cache_repo.set_cache('changelog')

    data, last_update = await cache_repo.get_cache('changelog')

    if data and now - last_update < cache_repo.cache_ttl:
        logging.info('Retrieve changelog data from cache')
        return json.loads(data)

    url = 'https://api.github.com/repos/prs2rnn/mycardbot/releases'
    data = await fetch_json(url)
    if not data:
        return []

    result = [
        {'version': r.get('name', 'unknown'), 'text': r.get('body', '')} for r in data
    ][0]

    await cache_repo.update_cache('changelog', json.dumps(result), now)

    return result
