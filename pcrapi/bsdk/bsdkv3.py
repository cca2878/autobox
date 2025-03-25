import base64
from hashlib import md5 as hashlib_md5
from traceback import print_exception

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from httpx import AsyncClient, Headers
from .model import BaseReq, BsdkExtConfReq, host_mgr, BsdkGetCipherV3Req, BsdkLoginV3Req, BsdkStartCaptchaReq, \
    BsdkStartCaptchaResp, BsdkCaptLoginV3Req, BsdkLoginV3Resp, AccInfo
from .validator import Validator
from pcrapi.game.model.error import PanicError


class BsdkHttp:
    def __init__(self, parent: 'BsdkV3'):
        self._init_http_client()
        self.parent = parent
        # self.app_key = app_key if app_key else 'fe8aac4e02f845b8ad67c427d48bfaf1'
        # self.channel = channel
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()

    async def aclose(self):
        await self.http_client.aclose()

    def _init_http_client(self):
        client = AsyncClient()
        client.headers = {
            "User-Agent": "Mozilla/5.0 BSGameSDK",
            "Content-Type": "application/x-www-form-urlencoded",
            "accept-encoding": "gzip",
            "cversion": "1"
        }
        self.http_client = client

    async def req(self, req: BaseReq, extra_headers: Headers = None):
        req.channel_id = str(self.parent.acc_info.channel)
        # BSdkV3安卓端以下两项值为3，意义不明，暂时搁置
        # req.platform = self.acc_info.platform
        # req.platform_type = self.acc_info.platform
        req = req.model_validate(req)
        data = req.model_dump(by_alias=True)
        data['sign'] = self._urlencoded_signer(data)
        httpx_req = self.http_client.build_request(req.api_info.method, req.api_info.URL,
                                                   data=data, headers=extra_headers)
        httpx_resp = await self.http_client.send(httpx_req)
        resp: req.resp_type = req.resp_type.model_validate(httpx_resp.json())
        return resp

    def _urlencoded_signer(self, data) -> str:
        return hashlib_md5((''.join(str(data[k]) for k in sorted(data)) + self.parent.app_key).encode()).hexdigest()


class BsdkV3:
    def __init__(self, acc_info: AccInfo, captchaVerifier=None, errlogger=print, app_key: str = None):
        self.pwd_hash = None
        self.app_key = app_key if app_key else 'fe8aac4e02f845b8ad67c427d48bfaf1'
        self.pwd_cipher = None
        self.acc_info = acc_info
        self.captchaVerifier = captchaVerifier
        self.errlogger = errlogger
        self.http_client = BsdkHttp(self)

    @classmethod
    async def create(cls, acc_info: AccInfo, captchaVerifier=None, errlogger=print, app_key: str = None):
        self = cls(acc_info, captchaVerifier, errlogger, app_key)
        await self.get_config()
        return self

    async def get_config(self):
        req = BsdkExtConfReq()
        resp: req.resp_type = await self.http_client.req(req)
        await host_mgr.a_set_hosts('config_login_https', resp.config_login_https.split(','))
        req = BsdkGetCipherV3Req()
        resp: req.resp_type = await self.http_client.req(req)
        self.pwd_hash = resp.hash
        # self.pwd_cipher = rsa.PublicKey.load_pkcs1_openssl_pem(resp.cipher_key.encode('utf-8'))
        self.pwd_cipher = PKCS1_v1_5.new(RSA.importKey(resp.cipher_key))

    def encrypt_pwd(self, pwd: str) -> str:
        # return base64.b64encode(rsa.encrypt((self.pwd_hash + pwd).encode('utf-8'), self.pwd_cipher)).decode('utf-8')
        return base64.b64encode(self.pwd_cipher.encrypt((self.pwd_hash + pwd).encode('utf-8'))).decode('utf-8')

    async def get_captcha(self) -> BsdkStartCaptchaResp:
        return await self.http_client.req(BsdkStartCaptchaReq())

    async def login(self):
        try:
            resp = None
            login1_req = BsdkLoginV3Req(user_id=self.acc_info.acc, pwd=self.encrypt_pwd(self.acc_info.pwd))
            login1_resp: login1_req.resp_type = await self.http_client.req(login1_req)
            if login1_resp.need_captch == 1:
                n = 3
                for i in range(n):
                    try:
                        vali_info = await Validator(self.http_client)
                        break
                    except Exception as e:
                        print_exception(e)
                        if i == n - 1:
                            raise ValueError("captcha failed")
                        continue
                login2_req = BsdkCaptLoginV3Req.model_validate(
                    {**login1_req.model_dump(),
                     **{
                         'captcha_type': '1',
                         'seccode': vali_info.vali + '|jordan',
                         'validate': vali_info.vali,
                         'gt_user_id': vali_info.gt_user_id,
                         'ctoken': vali_info.gt_user_id,
                         'challenge': vali_info.challenge
                     }})
                login2_resp = await self.http_client.req(login2_req)
                resp = login2_resp
            elif login1_resp.code == 0:
                resp = login1_resp
            resp: BsdkLoginV3Resp
            if not resp.code == 0:
                raise PanicError(resp.code)
            else:
                return 0, 'success', (resp.uid, resp.access_key)
        except Exception as e:
            return -1, e, (None, None)

    # async def login(self):
    #     while True:
    #         resp = await login(self.acc_info.acc, self.acc_info.pwd, self.captchaVerifier)
    #         if resp['code'] == 0:
    #             await self.errlogger("geetest or captcha succeed")
    #             break
    #         self.errlogger(resp['message'])
    #         raise ValueError(resp['message'])
    #
    #     return resp['uid'], resp['access_key']
