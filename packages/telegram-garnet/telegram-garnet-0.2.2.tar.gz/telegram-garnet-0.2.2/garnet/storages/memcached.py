import typing
import asyncio
from abc import ABC

import aiomcache

from tgarnet.storages.base import BaseStorage


class MemcachedStorage(BaseStorage, ABC):
    def __init__(self, host: str, port: int, loop: asyncio.BaseEventLoop = None):
        self.__cache = aiomcache.Client(**locals())

    async def close(self):
        await self.__cache.close()

    async def get_state(
        self,
        *,
        chat: typing.Union[str, int, None] = None,
        user: typing.Union[str, int, None] = None,
        default: typing.Optional[str] = None,
    ) -> typing.Optional[str]:
        await self.__cache.get(b"")


async def hello_aiomcache():
    mc = aiomcache.Client("127.0.0.1", 11211)
    await mc.set(b"some_key", b"Some value")
    value = await mc.get(b"some_key")
    print(value)
    values = await mc.multi_get(b"some_key", b"other_key")
    print(values)
    await mc.delete(b"another_key")
