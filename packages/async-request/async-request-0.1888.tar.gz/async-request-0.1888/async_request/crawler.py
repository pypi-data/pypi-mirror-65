# coding=utf-8

import asyncio
import functools

import requests as _requests
from requests.exceptions import ConnectionError, Timeout

from async_request.request import Request
from async_request.response import Response
from async_request.utils import iter_outputs, get_logger, coro_wrapper


def _run_in_executor(func):
    @functools.wraps(func)
    def wrapped(crawler, *args):
        return crawler.loop.run_in_executor(None, func, crawler, *args)

    return wrapped


class Crawler(object):

    def __init__(self,
                 start_requests=None,
                 result_back=None,
                 handle_cookies=True,
                 download_delay=0,
                 concurrent_requests=10,
                 max_retries=3,
                 priority=1,
                 log_level='DEBUG',
                 log_file=None,
                 loop=None):
        """
        :param result_back: function to process the result
        :param handle_cookies: handle the cookies or not
        :param download_delay: delayed time before download
        :param concurrent_requests: max concurrent requests
        :param priority: -1: first in first out, breadth-first
                          1: last in first out, depth-first
        :param log_level: logs level
        :param log_file: if not None, logs will save to it
        :param loop: async event loop
        """
        if priority == -1:
            self._queue = asyncio.Queue()
        elif priority == 1:
            self._queue = asyncio.LifoQueue()
        else:
            raise ValueError(f'Argument priority expect 1 or -1, got {priority}')
        if handle_cookies:
            self.session = _requests.Session()
        else:
            self.session = _requests
        for request in start_requests or []:
            self.put_request(request)
        self.result_back = result_back
        self.download_delay = download_delay
        self.concurrent_requests = concurrent_requests
        self.max_retries = max_retries
        self.loop = loop or asyncio.get_event_loop()
        self.logger = get_logger('asyncrequest.Crawler', level=log_level, file_path=log_file)

    def put_request(self, request):
        self._queue.put_nowait(request)

    def run(self, close_loop=True):
        self.loop.run_until_complete(self._run())
        self.close(close_loop)

    def close(self, close_loop=True):
        if isinstance(self.session, _requests.Session):
            self.session.close()
        if close_loop:
            self.loop.close()

    async def crawl(self, request):
        await asyncio.sleep(self.download_delay)
        response = await self.download(request)
        if response is not None:
            await self.process_response(response, request)

    def _iter_crawl_tasks(self):
        try:
            for _ in range(self.concurrent_requests):
                request = self._queue.get_nowait()
                yield self.crawl(request)
        except asyncio.queues.QueueEmpty:
            pass

    async def _run(self):
        while self._queue.qsize():
            await asyncio.gather(*self._iter_crawl_tasks())

    @_run_in_executor
    def download(self, request):
        retries = request.meta.get('retry_times')
        if retries:
            self.logger.debug(
                f'Retrying download: {request} (retried {retries - 1} times)'
            )
        try:
            r = self.session.request(**request.requests_kwargs())
            return Response(r, request)
        except Exception as e:
            if isinstance(e, (ConnectionError, Timeout,)):
                self.logger.error(e)
                self.loop.create_task(self.retry_request(request))
            else:
                self.logger.exception(e)

    async def retry_request(self, request, max_retries=None):
        if max_retries is None:
            max_retries = self.max_retries
        retries = request.meta.get('retry_times', 0)
        if retries < max_retries:
            request.meta['retry_times'] = retries + 1
            await self._queue.put(request)
        else:
            self.logger.debug(f'Gave up retry {request}')

    async def process_response(self, response, request):
        self.logger.debug(f'Downloaded: {response!r}')
        if not request.callback:
            return self.logger.warning(f'No function to parse {request}')
        try:
            outputs = request.callback(response)
            outputs = await coro_wrapper(outputs)
            await self.process_output(outputs, response)
        except Exception as e:
            return self._log_parse_error(e, response)

    async def process_output(self, outputs, response):
        try:
            async for output in iter_outputs(outputs):
                if output is None:
                    continue
                if isinstance(output, Request):
                    await self._queue.put(output)
                else:
                    await self.process_result(output)
        except Exception as e:
            self._log_parse_error(e, response)

    async def process_result(self, result):
        self.logger.debug(f'Crawled result: {result}')
        if not self.result_back:
            return
        try:
            await coro_wrapper(self.result_back(result))
        except Exception as e:
            self.logger.error(f'Error happened when processing result: {result}, cause: {e}')
            self.logger.exception(e)

    def _log_parse_error(self, e, response):
        self.logger.error(f'Error happened when parsing: {response!r}, cause: {e}')
        self.logger.exception(e)

    def __del__(self):
        self.close()
