import asyncio

from bilibili import Bilibili
from config import config
from mirrativ import Mirrativ
from openrec import Openrec
from tools import get_logger
from twitcasting import Twitcasting
from youtube import Youtube, start_temp

logger = get_logger()


def gen_process() -> list:
    event_list = []
    if config['youtube']['enable']:
        for user_config in config['youtube']['users']:
            y = Youtube(user_config)
            event_list.append(y)
    if config['twitcasting']['enable']:
        for user_config in config['twitcasting']['users']:
            t = Twitcasting(user_config)
            event_list.append(t)
    if config['openrec']['enable']:
        for user_config in config['openrec']['users']:
            o = Openrec(user_config)
            event_list.append(o)
    if config['mirrativ']['enable']:
        for user_config in config['mirrativ']['users']:
            m = Mirrativ(user_config)
            event_list.append(m)
    if config['bilibili']['enable']:
        for user_config in config['bilibili']['users']:
            b = Bilibili(user_config)
            event_list.append(b)
    return event_list


def create_tasks():
    event_list = gen_process()
    tasks = [event.check() for event in event_list]
    if config['youtube']['enable_temp']:
        tasks.append(start_temp())
    return tasks


async def main():
    tasks = create_tasks()
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
