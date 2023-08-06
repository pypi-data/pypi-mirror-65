import asyncio
from time import time
from datetime import timedelta
from unittest import mock

import pytest

from sanic import Sanic
# from aiohttp import web
# from aiohttp.web_urldispatcher import UrlMappingMatchInfo
# from aiohttp.test_utils import make_mocked_request, make_mocked_coro
from multidict import CIMultiDict
from yarl import URL

from sanic_sockjs import Session, SessionManager, transports
from sanic_sockjs.route import SockJSRoute

from tests.utils import make_mocked_coro, make_mocked_request


@pytest.yield_fixture
def app():
    app =  Sanic("pytest%s" % str(time()))
    yield app

@pytest.fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))

@pytest.fixture
def make_fut():
    def maker(val, makemock=True):
        loop = asyncio.get_event_loop()
        fut = loop.create_future()
        fut.set_result(val)

        if makemock:
            m = mock.Mock()
            m.return_value = fut
            return m
        else:
            return fut

    return maker


@pytest.fixture
def make_handler():
    def maker(result, coro=True, exc=False):
        if result is None:
            result = []
        output = result

        def handler(msg, s):
            if exc:
                raise ValueError((msg, s))
            output.append((msg, s))

        if coro:
            return asyncio.coroutine(handler)
        else:
            return handler

    return maker


@pytest.fixture
def make_route(make_handler, app):
    def maker(handlers=transports.handlers):
        handler = make_handler([])
        sm = SessionManager("sm", app, handler)
        return SockJSRoute("sm", sm, "http:sockjs-cdn", handlers, (), True)

    return maker


@pytest.fixture
def make_request(app):
    def maker(method, path, query_params=None, headers=None):
        nonlocal app
        path = URL(path)
        if query_params:
            path = path.with_query(query_params)

        if headers is None:
            headers = CIMultiDict(
                {
                    "HOST": "server.example.com",
                    "UPGRADE": "websocket",
                    "CONNECTION": "Upgrade",
                    "SEC-WEBSOCKET-KEY": "dGhlIHNhbXBsZSBub25jZQ==",
                    "ORIGIN": "http://example.com",
                    "SEC-WEBSOCKET-PROTOCOL": "chat, superchat",
                    "SEC-WEBSOCKET-VERSION": "13",
                }
            )

        writer = mock.Mock()
        writer.write_headers = make_mocked_coro(None)
        writer.write = make_mocked_coro(None)
        writer.drain = make_mocked_coro(None)
        transport = mock.Mock()
        transport._drain_helper = make_mocked_coro()
        loop = asyncio.get_event_loop()
        ret = make_mocked_request(method, str(path).encode(), headers, writer=writer, loop=loop, app=app)
        return ret

    return maker


@pytest.fixture
def make_session(make_handler, make_request):
    def maker(
        name="test", timeout=timedelta(10), request=None, handler=None, result=None
    ):
        if request is None:
            request = make_request("GET", "/TestPath/")

        if handler is None:
            handler = make_handler(result)
        return Session(name, handler, request, timeout=timeout, debug=True)

    return maker


@pytest.fixture
def make_manager(app, make_handler, make_session):
    def maker(handler=None):
        if handler is None:
            handler = make_handler([])
        return SessionManager("sm", app, handler, debug=True)

    return maker
