import asyncio
import logging
import time

from lxml.html import etree

from config import config
from daemon import VideoDaemon
from tools import get


class Openrec(VideoDaemon):
    def __init__(self, target_id):
        super().__init__(target_id)
        self.logger = logging.getLogger('run.openrec')
        self.module = 'Openrec'

    async def is_live(self):
        html = await get(f'https://www.openrec.tv/user/{self.target_id}')
        dom = etree.HTML(html)
        try:
            is_live = dom.xpath('/html/body/div[1]/div[2]/div[18]/div[2]/div/div[3]/ul/li[1]/div/text()')[0]
        except IndexError:
            return None
        if 'Live' in is_live:
            info = dom.xpath('/html/body/div[1]/div[2]/div[18]/div[2]/div/div[3]/ul/li[1]/ul/li/a[2]')[0]
            ref = info.xpath('@href')[0]
            title = dom.xpath('/html/body/div[1]/div[2]/div[18]/div[2]/div/div[3]/ul/li[1]/ul/li/a[2]/text()')[0]
            target = ref
            date = time.strftime("%Y-%m-%d", time.localtime())
            live_dict = {'Title': title,
                         'Ref': ref,
                         'Target': target,
                         'Date': date}
            return live_dict
        return None

    async def check(self):
        while True:
            is_live = await self.is_live()
            if is_live:
                video_dict = is_live
                video_dict['Provide'] = self.module
                video_dict['User'] = self.user_config['name']
                self.send_to_sub(video_dict)
            else:
                self.logger.info(f'{self.target_id}: Not found Live')
            await asyncio.sleep(config['sec'])
