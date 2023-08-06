# Copyright (C) 2015-2020 by Vd.
# This file is part of Rocketgram, the modern Telegram bot framework.
# Rocketgram is released under the MIT License (see LICENSE).


import asyncio
import inspect
import logging
from contextlib import suppress
from typing import TYPE_CHECKING, List, Optional

from .context import context2
from .errors import RocketgramRequest429Error, RocketgramStopRequest
from .errors import RocketgramRequestError, RocketgramRequest400Error, RocketgramRequest401Error
from .requests import Request
from .update import Update, UpdateType, Response

if TYPE_CHECKING:
    from .executors import Executor
    from .routers import Router
    from .connectors import Connector
    from .middlewares import Middleware

logger = logging.getLogger('rocketgram.bot')
logger_raw_in = logging.getLogger('rocketgram.raw.in')
logger_raw_out = logging.getLogger('rocketgram.raw.out')


class Bot:
    __slots__ = ('__token', '__name', '__user_id', '__middlewares', '__router', '__own_connector', '__connector')

    def __init__(self, token: str, *, connector: 'Connector' = None, router: 'Router' = None):
        """

        :param token: Bot's token
        :param connector: Connector object. If not specified Bot will try AioHttpConnector
        :param router: Router object. If not specified Bot will try Dispatcher
        """
        self.__token = token

        self.__name = None
        self.__user_id = int(self.__token.split(':')[0])
        self.__middlewares: List['Middleware'] = list()

        self.__router = router
        if self.__router is None:
            from .routers.dispatcher import Dispatcher
            self.__router = Dispatcher()

        self.__own_connector = False
        self.__connector = connector

        if self.__connector is None:
            with suppress(ImportError):
                from .connectors import AioHttpConnector
                self.__own_connector = True
                self.__connector = AioHttpConnector()

        if self.__connector is None:
            with suppress(ImportError):
                from .connectors import TornadoConnector
                self.__own_connector = True
                self.__connector = TornadoConnector()

        if self.__connector is None:
            raise RuntimeError("Can't create Connector object. Tornado or AioHttp should be installed.")

    @property
    def token(self) -> str:
        """Bot's token."""

        return self.__token

    @property
    def name(self) -> str:
        """Bot's username. Can be set one time."""

        return self.__name

    @name.setter
    def name(self, name: str):
        if self.__name is not None:
            raise TypeError('Bot''s name can be set one time.')

        self.__name = name

    @property
    def user_id(self) -> int:
        """Bot's user_id."""

        return self.__user_id

    @property
    def router(self) -> 'Router':
        """Bot's router."""

        return self.__router

    @property
    def connector(self) -> 'Connector':
        """Bot's connector."""

        return self.__connector

    def middleware(self, middleware: 'Middleware'):
        """Registers middleware."""

        self.__middlewares.append(middleware)

    async def init(self):
        """Initializes connector and dispatcher.
        Performs bot initialization authorize bot on telegram and sets bot's name.

        Must be called before any operation with bot."""

        logger.debug('Performing init...')

        context2.bot = self

        if self.__own_connector:
            await self.connector.init()

        await self.router.init()

        for md in self.__middlewares:
            m = md.init()
            if inspect.isawaitable(m):
                await m

        return True

    async def shutdown(self):
        """Release bot's resources.

        Must be called after bot work was done."""

        logger.debug('Performing shutdown...')

        context2.bot = self

        await self.router.shutdown()

        for md in reversed(self.__middlewares):
            m = md.shutdown()
            if inspect.isawaitable(m):
                await m

        if self.__own_connector:
            await self.connector.shutdown()

    async def process(self, executor: 'Executor', update: Update) -> Optional[Request]:
        logger_raw_in.debug('Raw in: %s', update.raw)

        context2.executor = executor
        context2.bot = self

        context2.webhook_requests = list()

        context2.update = update
        context2.message = None
        context2.chat = None
        context2.user = None

        if update.update_type is UpdateType.message:
            context2.message = update.message
            context2.chat = update.message.chat
            context2.user = update.message.user
        elif update.update_type is UpdateType.edited_message:
            context2.message = update.edited_message
            context2.chat = update.edited_message.chat
            context2.user = update.edited_message.user
        elif update.update_type is UpdateType.channel_post:
            context2.message = update.channel_post
            context2.chat = update.channel_post.chat
            context2.user = update.channel_post.user
        elif update.update_type is UpdateType.edited_channel_post:
            context2.message = update.edited_channel_post
            context2.chat = update.edited_channel_post.chat
            context2.user = update.edited_channel_post.user
        elif update.update_type is UpdateType.inline_query:
            context2.user = update.inline_query.user
        elif update.update_type is UpdateType.chosen_inline_result:
            context2.user = update.chosen_inline_result.user
        elif update.update_type is UpdateType.callback_query:
            context2.message = update.callback_query.message
            if update.callback_query.message:
                context2.chat = update.callback_query.message.chat
            context2.user = update.callback_query.user
        elif update.update_type is UpdateType.shipping_query:
            context2.user = update.shipping_query.user
        elif update.update_type is UpdateType.pre_checkout_query:
            context2.user = update.pre_checkout_query.user

        try:
            for md in self.__middlewares:
                mw = md.before_process()
                if inspect.isawaitable(mw):
                    await mw

            await self.router.process()

            webhook_request = None

            for req in context2.webhook_requests:
                # set request to return if it can be processed
                if webhook_request is None and executor.can_process_webhook_request(req):
                    for md in self.__middlewares:
                        req = md.before_request(req)
                        if inspect.isawaitable(req):
                            req = await req
                    webhook_request = req
                    continue

                # fallback and send by hands
                with suppress(Exception):
                    await self.send(req)

            for md in self.__middlewares:
                mw = md.after_process()
                if inspect.isawaitable(mw):
                    await mw

            return webhook_request

        except RocketgramStopRequest as e:
            logger.debug('Request `%s` was interrupted: `%s`', update.update_id, e)
        except asyncio.CancelledError:
            raise
        except Exception as error:
            for md in self.__middlewares:
                with suppress(Exception):
                    m = md.process_error(error)
                    if inspect.isawaitable(m):
                        await m

            logger.exception('Got exception during processing request:')

    async def send(self, request: Request) -> Response:
        try:
            for md in self.__middlewares:
                request = md.before_request(request)
                if inspect.isawaitable(request):
                    request = await request

            response = await self.__connector.send(self.token, request)

            for md in reversed(self.__middlewares):
                response = md.after_request(request, response)
                if inspect.isawaitable(response):
                    response = await response

            if response.ok:
                return response
            if response.error_code == 400:
                raise RocketgramRequest400Error(request, response)
            elif response.error_code == 401:
                raise RocketgramRequest401Error(request, response)
            elif response.error_code == 429:
                raise RocketgramRequest429Error(request, response)
            raise RocketgramRequestError(request, response)
        except asyncio.CancelledError:
            raise
        except Exception as error:
            for md in reversed(self.__middlewares):
                m = md.request_error(request, error)
                if inspect.isawaitable(m):
                    await m
            raise
