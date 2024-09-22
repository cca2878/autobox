import time
from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, List, Type
from pydantic import BaseModel, Field, computed_field
from httpx import URL
import asyncio

from pcrapi.util.enums import eGamePlatformId


class HostMgr:
    config_init: List[str] = ["https://p.biligame.com"]
    config_login_https: List[str] = ["https://line1-sdk-center-login-sh.biligame.net",
                                     "https://line3-sdk-center-login-sh.biligame.net",
                                     "https://line3-login.biligame.net",
                                     "https://line1-login.biligame.net"]


class AHostMgr:
    class HostConf:
        def __init__(self, alias: str, hosts: List, avail_host: int = 0):
            self.alias = alias
            self.hosts = hosts
            self.avail_host = avail_host
            self.lock = asyncio.Lock()

    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self._data = {}
        self._data.update({
            "config_init": self.HostConf(
                alias="config_init",
                hosts=["https://p.biligame.com"]
            )})
        self._data.update({
            "config_login_https": self.HostConf(
                alias="config_login_https",
                hosts=["https://line1-sdk-center-login-sh.biligame.net",
                       "https://line3-sdk-center-login-sh.biligame.net",
                       "https://line3-login.biligame.net",
                       "https://line1-login.biligame.net"]
            )})

    async def a_get_host(self, key):
        if key in self._data:
            async with self._data[key].lock:
                return self._data[key].hosts[self._data[key].avail_host] if self._data[key].avail_host < len(
                    self._data[key].hosts) else self._data[key].hosts[-1]

    def get_host(self, key):
        return self.loop.run_until_complete(self.a_get_host(key))

    async def a_set_hosts(self, key, value):
        if key in self._data:
            async with self._data[key].lock:
                self._data[key].hosts = value

    def set_hosts(self, key, value):
        return self.loop.run_until_complete(self.a_set_hosts(key, value))

    async def a_toggle_host(self, key):
        if key in self._data:
            async with self._data[key].lock:
                self._data[key].avail_host = (self._data[key].avail_host + 1) % len(self._data[key].hosts)

    def toggle_host(self, key):
        return self.loop.run_until_complete(self.a_toggle_host(key))


host_mgr = AHostMgr()


@dataclass
class ApiInfo:
    """
    url: 请求路径;
    method: 请求方法
    host_alias: 主机名key
    """
    url: str
    method: str
    host_alias: str

    @property
    def URL(self) -> URL:
        return URL(host_mgr.get_host(self.host_alias) + self.url)

    @property
    def ori_domain(self) -> str:
        return host_mgr.get_host(self.host_alias)


class BaseResp(BaseModel):
    code: int = Field(-1)


TResp = TypeVar("TResp", bound=BaseResp)


class BaseReq(BaseModel):
    _api_info: ApiInfo = None
    _resp_type: Type[TResp] = None

    cur_buvid: str = Field("CR_NMSL")
    old_buvid: str = Field("CR_NMSL")
    udid: str = Field("CR_NMSL")
    bd_id: str = Field("cr-nmsl")
    sdk_type: str = Field("1")
    version_code: str = Field("276")
    merchant_id: str = Field("1")
    server_id: str = Field("1592")
    version: str = Field("3")
    domain_switch_count: str = Field("0")
    apk_sign: str = Field("crnmsl")
    platform_type: str = Field("3")
    app_ver: str = Field("7.7.2")
    sdk_log_type: str = Field("1")
    current_env: str = Field("0")
    sdk_ver: str = Field("6.6.2")
    app_id: str = Field("1370")
    platform: str = Field("3")
    channel_id: str = Field("1")
    game_id: str = Field("1370")

    @computed_field
    @property
    def domain(self) -> str:
        return self._api_info.URL.host

    @computed_field
    @property
    def timestamp(self) -> str:
        return str(int(time.time_ns() // 1000000))

    @computed_field
    @property
    def original_domain(self) -> str:
        return self._api_info.ori_domain

    @property
    def api_info(self) -> ApiInfo:
        if self._api_info is None:
            raise NotImplementedError()
        return self._api_info

    @property
    def resp_type(self):
        if self._resp_type is None:
            raise NotImplementedError()
        return self._resp_type


class BsdkExtConfResp(BaseResp):
    config_login_https: str = Field(str)


class BsdkExtConfReq(BaseReq):
    @computed_field
    @property
    def host(self) -> str:
        return self._api_info.URL.host

    _resp_type: Type[TResp] = BsdkExtConfResp
    _api_info: ApiInfo = ApiInfo(
        url="/api/external/config/v3",
        method="post",
        host_alias="config_init"
    )


class BsdkGetCipherV3Resp(BaseResp):
    cipher_key: str = Field(str)
    hash: str = Field(str)


class BsdkGetCipherV3Req(BaseReq):
    cipher_type: str = Field("bili_login_rsa")

    _resp_type: Type[TResp] = BsdkGetCipherV3Resp
    _api_info: ApiInfo = ApiInfo(
        url="/api/external/issue/cipher/v3",
        method="post",
        host_alias="config_login_https"
    )


class BsdkLoginV3Resp(BaseResp):
    need_captch: Optional[int] = Field(int)
    x_nonce: Optional[str] = Field(str, alias="nonce")
    access_key: Optional[str] = Field(str)
    expires_in: Optional[int] = Field(int)
    realname_verified: Optional[int] = Field(int)
    uid: Optional[int] = Field(int)
    uname: Optional[str] = Field(str)



class BsdkCaptLoginV3Resp(BsdkLoginV3Resp):
    ...


class BsdkLoginV3Req(BaseReq):
    bd_info: str = Field('cr_nmsl')
    user_id: str = Field(str)
    pwd: str = Field(str)

    # @computed_field
    # @property
    # def domain(self) -> str:
    #     return self._api_info.URL.host

    _resp_type: Type[TResp] = BsdkLoginV3Resp
    _api_info: ApiInfo = ApiInfo(
        url="/api/external/login/v3",
        method="post",
        host_alias="config_login_https"
    )


class BsdkCaptLoginV3Req(BsdkLoginV3Req):
    captcha_type: str = Field("1")
    seccode: str = Field(str)
    vali: str = Field(str, alias="validate")
    gt_user_id: str = Field(str)
    ctoken: str = Field(str)
    challenge: str = Field(str)


class BsdkStartCaptchaResp(BaseResp):
    captcha_type: int = Field(1)
    gs: int = Field(1)
    gt: str = Field(str)
    challenge: str = Field(str)
    gt_user_id: str = Field(str)


class BsdkStartCaptchaReq(BaseReq):
    version: str = Field("1")

    _resp_type: Type[TResp] = BsdkStartCaptchaResp
    _api_info: ApiInfo = ApiInfo(
        url="/api/client/start_captcha",
        method="post",
        host_alias="config_login_https"
    )


@dataclass
class AccInfo:
    """
    acccountinfo = {
        'acc': '',
        'pwd': '',
        'platform': 2, # indicates android platform
        'channel': 1, # indicates bilibili channel
    }
    """
    acc: str
    pwd: str
    platform: eGamePlatformId = eGamePlatformId.Android
    channel: int = 1
