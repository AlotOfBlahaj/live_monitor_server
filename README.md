# Live_monitor_server - Vtuber直播监控服务器端

## 介绍

这是由[Auto_Record_Matsuri](https://github.com/fzxiao233/Auto_Record_Matsuri)解耦合后的监控模块，配合worker端使用可实现包括但不限于bot提醒，视频下载，视频上传，同传记录等功能

目前支援如下平台的监控:

- Youtube

- Openrec

- Mirrativ

- Twitcasting

已实现的worker见项目[live_monitor_worker](https://github.com/fzxiao233/live_monitor_worker)

## 特性

- Asyncio下Aiohttp异步并发请求

- 通过redis中间件实现C/S交互

## 部署环境需求

- redis

建议使用docker一键部署docker


## 使用方法

    git clone https://github.com/fzxiao233/live_monitor_server  #克隆本项目

    cd live_monitor_worker  #进入项目目录

    编辑src目录下的config.py文件

    pip install -r requirements.txt  #安装依赖

    python run.py  #启动程序

    ## 推荐使用pm2执行，此次不再介绍




## 配置文件示例

```python
config = {
    'enable_proxy': False, # 是否启用代理
    'proxy': '127.0.0.1:12333', # http代理地址
    'sec': 15, # 检测间隔
    'error_sec': 5, # 错误重试间隔
    # Youtube设定
    'youtube': {
        'enable': True, # 是否启用此模块
        'enable_temp': False, # 是否启用youtube网页端补充监控模块(需求mongodb数据库)
        'api_key': '', # Youtube DATA V3 API KEY （不填入也可使用
        # 监控用户列表，格式为：
        '''
            {
                'target_id': '#此处更换为youtube channel',
                'name': '此处为标识用户名，用于与worker端标识'
            },
        '''
        'users': [
            {
                'target_id': 'UCQ0UDLQCjY0rmuxCDE38FGg',
                'name': 'natsuiromatsuri'
            },
            {
                'target_id': 'UCl_gCybOJRIgOXw6Qb4qJzQ',
                'name': 'uruharushia'
            }
        ]
    },
    'twitcasting': {
        'enable': True,
        'users': [
            {
                'target_id': 'natsuiromatsuri',
                'name': 'natsuiromatsuri'
            }
        ]
    },
    'mirrativ': {
        'enable': True,
        'users': [
            {
                'target_id': '3264432',
                'name': 'natsuiromatsuri'
            }
        ]
    },
    'openrec': {
        'enable': True,
        'users': [
            {
                'target_id': 'natsuiromatsuri',
                'name': 'natsuiromatsuri'
            }
        ]
    },
    'bilibili': {
        'enable': True,
        'users': [
            {
                'target_id': '336731767',
                'name': 'natsuiromatsuri'
            }
        ]
    }
}
```
