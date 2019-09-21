import asyncio
import logging
from abc import ABCMeta, abstractmethod

from pub import Publisher

logger = logging.getLogger('run.daemon')


class VideoDaemon(metaclass=ABCMeta):
    def __init__(self, user_config):
        super().__init__()
        self.user_config = user_config
        self.target_id = user_config['target_id']
        self.current_live = None
        self.pub = Publisher()

    async def run(self) -> None:
        while True:
            try:
                await self.check()
            except asyncio.CancelledError:
                raise asyncio.CancelledError
            except Exception:
                logger.exception('Check Failed')

    @abstractmethod
    def check(self):
        pass

    def send_to_sub(self, video_dict: dict, live=True) -> None:
        if not (video_dict['Title'], video_dict['Target']) == self.current_live:
            self.current_live = (video_dict['Title'], video_dict['Target'])
            logger.info(f'Find a live {video_dict}')
            video_dict = self.msg_fml(video_dict, live)
            self.pub.do_publish(video_dict)
        else:
            logger.info(f'drop the same live {video_dict}')

    @staticmethod
    def msg_fml(video_dict: dict, live=True) -> dict:
        if live:
            video_dict[
                'Msg'] = f"[直播提示] {video_dict['Provide']} {video_dict.get('Title')} 正在直播 链接: {video_dict['Target']} [CQ:at,qq=all]"
        else:
            video_dict['Msg'] = f'[{video_dict["Provide"]}] {video_dict.get("Title")} 链接: {video_dict.get("Target")}'
        return video_dict
