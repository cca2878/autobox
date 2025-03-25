from enum import Enum
from typing import Tuple, Coroutine, Any, List, Callable
from abc import abstractmethod
from ..bsdk.model import AccInfo
from ..bsdk.validator import Validator
from copy import deepcopy
from ..constants import DEFAULT_HEADERS, IOS_HEADERS
from ..util.enums import eGamePlatformId
from ..util.logger import instance as logger


async def _defaultLogger(msg):
    print(msg)

class sdkclient:
    
    def __init__(self, info: AccInfo, captchaVerifier=Validator, errlogger=_defaultLogger):
        self.captchaVerifier = captchaVerifier
        self.logger = logger
        if info.platform == eGamePlatformId.Android:
            self.platform = '2'
        elif info.platform == eGamePlatformId.IOS:
            self.platform = '1000'
        else:
            raise ValueError(f"Invalid platform {info.platform}")
        self._account = info
        self.post_login_evts: List[Callable[[], Coroutine[Any, Any, None]]] = []

    def append_post_login(self, evt: Callable[[], Coroutine[Any, Any, None]]):
        self.post_login_evts.append(evt)

    '''
    returns: uid, access_key
    '''
    @abstractmethod
    async def login(self) -> Tuple[str, str]: ...

    async def invoke_post_login(self):
        for evt in self.post_login_evts:
            await evt()
        self.post_login_evts.clear()

    @abstractmethod
    async def do_captcha(self): ...
        # cap = await captch()
        # return await self.captchaVerifier(self.account, cap['gt'], cap['challenge'], cap['gt_user_id'])
        # async with BsdkHttp(channel=self._account.channel) as http_client:
        #     return await self.captchaVerifier(http_client)

    def header(self):
        if self._account.platform == eGamePlatformId.Android:
            headers = deepcopy(DEFAULT_HEADERS)
        elif self._account.platform == eGamePlatformId.IOS:
            headers = deepcopy(IOS_HEADERS)
        else:
            raise ValueError(f"Invalid platform {self._account.platform}")
        
        headers['RES-KEY'] = self.reskey
        headers['PLATFORM'] = self.platform
        headers['PLATFORM-ID'] = self.platform_id
        headers['CHANNEL-ID'] = self.channel

        return headers

    @property
    @abstractmethod
    def apiroot(self) -> str: ...

    @property
    @abstractmethod
    def platform_id(self) -> str: ...

    @property
    def channel(self):
        return '1'

    @property
    def account(self):
        return self._account.acc
    
    @property
    @abstractmethod
    def reskey(self) -> str: ...
