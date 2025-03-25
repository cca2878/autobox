from .bsdkv3 import BsdkV3
from pcrapi.game.model.error import PanicError
from ..core.sdkclient import sdkclient
from ..constants import BSDK


class bsdkclient(sdkclient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bsdk = None
        self.initialized = False

    async def initialize(self):
        self._bsdk = await BsdkV3.create(self._account, self.captchaVerifier, self.logger)
        self.initialized = True

    @property
    async def sdk(self) -> BsdkV3:
        if not self.initialized:
            await self.initialize()
        return self._bsdk

    async def do_captcha(self):
        return (await self.sdk).get_captcha()

    async def login(self):
        while True:
            code, msg, info = await (await self.sdk).login()
            if code == 0:
                self.logger.info("geetest or captcha succeed")
                break
            self.logger.error(msg)
            raise PanicError(msg)
        return info

    @property
    def apiroot(self):
        return 'https://l3-prod-all-gs-gzlj.bilibiligame.net/'

    @property
    def platform_id(self) -> str:
        return str(self.platform)

    @property
    def reskey(self):
        return 'ab00a0a6dd915a052a2ef7fd649083e5'


# class qsdkclient(sdkclient):
#     async def login(self):
#         return self._account.username, self._account.password
#
#     @property
#     def apiroot(self):
#         return 'https://l1-prod-uo-gs-gzlj.bilibiligame.net/'
#
#     @property
#     def platform_id(self):
#         return '4'
#
#     @property
#     def reskey(self):
#         return 'd145b29050641dac2f8b19df0afe0e59'
#
#     async def do_captcha(self):
#         raise NotImplementedError

sdkclients = {
    BSDK: bsdkclient,
    # QSDK: qsdkclient
}


def create(channel, *args, **kwargs) -> sdkclient:
    if channel not in sdkclients:
        raise ValueError(f"Invalid channel {channel}")
    return sdkclients[channel](*args, **kwargs)
