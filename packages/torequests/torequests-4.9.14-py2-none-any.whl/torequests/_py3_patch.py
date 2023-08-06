# here for python3 patch avoid of python2 SyntaxError
import asyncio
import json
from typing import Tuple, Type
from functools import wraps
# python3.7+ 's asyncio.all_tasks'
try:
    _py36_all_task_patch = asyncio.all_tasks
except (ImportError, AttributeError):
    _py36_all_task_patch = asyncio.Task.all_tasks


def _new_future_await(self):
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, self.result, self._timeout)
    for i in future:
        yield i
    return self.x


class NewResponse(object):
    """Wrap aiohttp's ClientResponse like requests's Response."""
    __slots__ = ('r', 'encoding', 'referer_info')

    def __init__(self, r, encoding=None, referer_info=None):
        self.r = r
        self.encoding = encoding or self.r.get_encoding()
        self.referer_info = referer_info

    def __getattr__(self, name):
        return getattr(self.r, name)

    @property
    def url(self):
        return str(self.r.url)

    @property
    def status_code(self):
        return self.r.status

    def __repr__(self):
        return "<NewResponse [%s]>" % (self.status_code)

    def __bool__(self):
        return self.ok

    def __iter__(self):
        """Allows you to use a response as an iterator."""
        return self.iter_content(128)

    @property
    def ok(self):
        return self.status_code in range(200, 400)

    @property
    def is_redirect(self):
        """True if this Response is a well-formed HTTP redirect that could have
        been processed automatically (by :meth:`Session.resolve_redirects`).
        """
        return "location" in self.headers and self.status_code in range(
            300, 400)

    @property
    def content(self):
        return self._body

    @property
    def text(self):
        return self._body.decode(self.encoding)

    def json(self, encoding=None, loads=json.loads):
        return loads(self.content.decode(encoding or self.encoding))


def retry(tries=1,
          exceptions: Tuple[Type[BaseException]] = (Exception,),
          catch_exception=False):

    def wrapper(function):

        @wraps(function)
        def retry_sync(*args, **kwargs):
            for _ in range(tries):
                try:
                    return function(*args, **kwargs)
                except exceptions as err:
                    error = err
            if catch_exception:
                return error
            raise error

        @wraps(function)
        async def retry_async(*args, **kwargs):
            for _ in range(tries):
                try:
                    return await function(*args, **kwargs)
                except exceptions as err:
                    error = err
            if catch_exception:
                return error
            raise error

        if asyncio.iscoroutinefunction(function):
            return retry_async
        else:
            return retry_sync

    return wrapper
