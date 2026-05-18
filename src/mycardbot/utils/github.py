import json
import logging
import time

import httpx
from core.database import bot_db


async def fetch_json(url: str):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except (httpx.TimeoutException, httpx.HTTPStatusError, httpx.RequestError) as e:
        logging.error(f'Error occurred in fetch_json: {e}')
    except Exception as e:
        logging.error(f'Unexpected error occurred in fetch_json: {e}')


async def get_changelog():
    now = time.time()
    await bot_db.set_cache('changelog')

    data, last_update = await bot_db.get_cache('changelog')

    if data and now - last_update < bot_db.cache_ttl:
        logging.info('Retrieve changelog data from cache')
        return json.loads(data)

    url = 'https://api.github.com/repos/prs2rnn/mycardbot/releases'
    data = await fetch_json(url)
    if not data:
        return []

    result = [
        {'version': r.get('name', 'unknown'), 'text': r.get('body', '')} for r in data
    ][0]

    await bot_db.update_cache('changelog', json.dumps(result), now)

    return result
