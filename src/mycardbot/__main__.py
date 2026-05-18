import asyncio
import logging

from mycardbot.app import main


def run():
    try:
        asyncio.run(main())
    except KeyboardInterrupt, SystemExit:
        logging.error('Bot stopped manually!')


if __name__ == '__main__':
    run()
