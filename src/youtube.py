import asyncio
import json
import logging
import re
from time import strftime, localtime, time

from config import config
from daemon import VideoDaemon
from tools import get, Database

logger = logging.getLogger('run.youtube')


class Youtube(VideoDaemon):

    def __init__(self, user_config):
        super().__init__(user_config)
        self.module = 'Youtube'
        self.api_key = config['youtube']['api_key']

    @staticmethod
    async def get_video_info_by_html(url):
        """
        The method is using yfconfig to get information of video including title, video_id, data and thumbnail
        :rtype: dict
        """
        video_page = await get(url)
        try:
            ytplayer_config = json.loads(re.search(r'ytplayer.config\s*=\s*([^\n]+?});', video_page).group(1))
            player_response = json.loads(ytplayer_config['args']['player_response'])
            video_details = player_response['videoDetails']
            # assert to verity live status
            if 'isLive' not in video_details:
                is_live = False
            else:
                is_live = True
            title = video_details['title']
            vid = video_details['videoId']
            target = f"https://www.youtube.com/watch?v={vid}"
            thumbnails = video_details['thumbnail']['thumbnails'][-1]['url']
            return {'Title': title,
                    'Ref': vid,
                    'Date': strftime("%Y-%m-%d", localtime(time())),
                    'Target': target,
                    'Thumbnails': thumbnails,
                    'Is_live': is_live}
        except KeyError:
            logger.exception('Get keys error')
            return {'Is_live': False}

    async def check(self):
        while True:
            video_dict = await self.get_video_info_by_html(f'https://www.youtube.com/channel/{self.target_id}/live')
            if video_dict['Is_live']:
                video_dict['Provide'] = self.module
                video_dict['User'] = self.user_config['name']
                self.send_to_sub(video_dict)
            else:
                logger.info(f'{self.target_id}: Not found Live')
                await asyncio.sleep(config['sec'])


class YoutubeTemp(Youtube):
    def __init__(self, vinfo):
        super().__init__(config['youtube']['users'][0])
        self.vinfo = vinfo
        self.db = Database('Queues')
        self.logger = logging.getLogger('run.youtube.temp')

    @staticmethod
    def get_temp_vid(vlink):
        reg = r"watch\?v=([A-Za-z0-9_-]{11})"
        idre = re.compile(reg)
        _id = vlink["_id"]
        vid = vlink["Link"]
        vid = re.search(idre, vid).group(1)
        return {'Vid': vid,
                'Id': _id}

    async def check(self):
        self.vinfo = self.get_temp_vid(self.vinfo)
        vid = self.vinfo['Vid']
        _id = self.vinfo['Id']
        video_dict = await self.get_video_info_by_html(f"https://www.youtube.com/watch?v={vid}")
        if video_dict['Is_live']:
            video_dict['Provide'] = self.module
            video_dict['User'] = self.user_config['name']
            self.send_to_sub(video_dict)
            await self.db.delete(_id)
        else:
            logger.info(f'{self.vinfo}Not found Live')


async def start_temp():
    db = Database('Queues')
    logger = logging.getLogger('run.youtube.temp')
    while True:
        temp_tasks = []
        for video in await db.select():
            y = YoutubeTemp(video)
            temp_tasks.append(y.check())
        await asyncio.gather(*temp_tasks)
        logger.info('Finished a check')
        await asyncio.sleep(config['sec'])
