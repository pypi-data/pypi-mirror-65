#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author: zhangkai
Last modified: 2020-04-02 09:26:54
'''

import asyncio
import logging
from .db_utils import AioRedis
from .decorator import aioretry


class RedisMQ:

    def __init__(self, queue='test', workers=1, **kwargs):
        self.rd = AioRedis(**kwargs)
        self.queue = queue
        self.workers = workers
        self.loop = asyncio.get_event_loop()
        self.logger = logging.getLogger()

    @aioretry
    async def publish(self, msg, queue=None):
        queue = queue or self.queue
        print(await self.rd.xadd(queue, msg))

    async def _consume(self, process, queue):
        streams = {queue: '$'}
        result = await self.rd.xread(**streams)
        await process(result)

    @aioretry
    async def consume(self, process, queue=None):
        queue = queue or self.queue
        for _ in range(self.workers):
            self.loop.create_task(self._consume(process, queue))
