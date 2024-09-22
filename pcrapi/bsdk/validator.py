import asyncio
import time
from dataclasses import dataclass
from traceback import print_exception
from typing import Dict

from httpx import AsyncClient
# from typing import Dict
from pydantic import BaseModel
import bili_ticket_gt_python

from .model import BsdkStartCaptchaResp

from pcrapi.bsdk.model import BsdkStartCaptchaReq
# from autopcr.bsdk.bsdkv3 import BsdkHttp
from ..util import questutils


# from ..util import aiorequests, questutils
# from json import loads
# import asyncio
#
class ValiResult(BaseModel):
    challenge: str = ""
    gt: str = ""
    gt_user_id: str = ""
    vali: str = ""


@dataclass
class ValidateInfo:
    id: str = ""
    challenge: str = ""
    gt: str = ""
    userid: str = ""
    url: str = ""
    status: str = ""
    validate: str = ""


async def get_captcha(http_client):
    """尝试获取一次验证码信息"""
    resp: BsdkStartCaptchaResp = await http_client.req(BsdkStartCaptchaReq())
    return resp.gt, resp.challenge, resp.gt_user_id


#
validate_dict: Dict[str, ValidateInfo] = {}
validate_ok_dict: Dict[str, ValidateInfo] = {}


async def Validator(http_client: 'BsdkHttp'):
    info = None
    for validator in [localValidator, remoteValidator, manualValidator]:
        try:
            info = await validator(http_client)
            if info:
                break
        except Exception as e:
            import traceback
            traceback.print_exc()
            pass
    if not info:
        raise ValueError("验证码验证超时")
    return info


async def manualValidator(http_client: 'BsdkHttp'):
    _id = questutils.create_quest_token()
    acc_info = http_client.parent.acc_info
    gt, challenge, userid = await get_captcha(http_client)
    url = f"geetest.html?id={_id}&captcha_type=1&challenge={challenge}&gt={gt}&userid={userid}&gs=1"
    validate_dict[acc_info.acc] = ValidateInfo(
        id=_id,
        challenge=challenge,
        gt=gt,
        userid=userid,
        url=url,
        status="need validate"
    )
    for _ in range(120):
        if _id not in validate_ok_dict:
            await asyncio.sleep(1)
        else:
            ret = ValiResult(
                challenge=validate_ok_dict[_id].challenge,
                gt=gt,
                gt_user_id=validate_ok_dict[_id].userid,
                vali=validate_ok_dict[_id].validate
            )
            del validate_ok_dict[_id]
            break
    else:
        raise ValueError("验证码验证超时")

    return ret


async def localValidator(http_client: 'BsdkHttp'):
    gt_obj = bili_ticket_gt_python.ClickPy()
    n = 5

    def _get_type(_gt, _challenge):
        """获取验证码类型"""
        for i in range(n):
            try:
                return gt_obj.get_type(_gt, _challenge)
            except Exception as e:
                if i == n - 1:
                    raise e
        # 不应达到此处，除非所有尝试均失败且已抛出异常

    def process_click_type(_gt, _challenge):
        """处理点击类型的验证码逻辑"""
        for j in range(n):
            try:
                c, s, args = gt_obj.get_new_c_s_args(_gt, _challenge)
                w = gt_obj.generate_w(gt_obj.calculate_key(args), _gt, _challenge, str(c), s, "abcdefghijklmnop")
                time.sleep(2)
                msg, validate = gt_obj.verify(_gt, _challenge, w)
                return validate
            except Exception as e:
                print_exception(e)
                if j == n - 1:
                    raise e
        # 同样不应达到这里

    try:
        gt, challenge, gt_user_id = await get_captcha(http_client)
        captcha_type = _get_type(gt, challenge)

        if captcha_type == 'click':
            # return process_click_type(gt, challenge)
            validate = process_click_type(gt, challenge)
            return ValiResult(
                challenge=challenge,
                gt=gt,
                gt_user_id=gt_user_id,
                vali=validate
            )
        else:
            # 这里可以添加处理其他类型验证码的逻辑或直接返回None
            pass
    except Exception as e:
        print_exception(e)
        raise e  # 明确地重新抛出异常，确保不会被忽略
    finally:
        # 可选：在此处添加清理资源的代码
        pass

    return None  # 明确指定函数返回值，在所有可能的执行路径上都有返回


async def remoteValidator(_):
    print('use remote validator')

    url = f"https://pcrd.tencentbot.top/geetest_renew"
    header = {"Content-Type": "application/json", "User-Agent": "autopcr/1.0.0"}
    ret = None
    try:
        async with AsyncClient() as client:
            client.headers.update(header)
            # res = await aiorequests.get(url=url, headers=header)
            res = await client.get(url)
            res.raise_for_status()
            res = res.json()
            uuid = res["uuid"]
            msg = [f"uuid={uuid}"]
            ccnt = 0
            up = 5
            while ccnt <= up:
                ccnt += 1
                res = await client.get(url=f"https://pcrd.tencentbot.top/check/{uuid}")
                res.raise_for_status()
                res = res.json()
                # print(res)
                if "queue_num" in res:
                    nu = res["queue_num"]
                    if nu >= 35: raise Exception("Captcha failed")

                    msg.append(f"queue_num={nu}")
                    tim = min(int(nu), 3) * 10
                    msg.append(f"sleep={tim}")
                    print(f"farm:\n" + "\n".join(msg))
                    msg = []
                    print(f'farm: {uuid} in queue, sleep {tim} seconds')
                    await asyncio.sleep(tim)
                    if tim >= 40: ccnt += 2
                else:
                    info = res["info"]
                    if info in ["fail", "url invalid"]:
                        raise Exception("Captcha failed")
                    elif info == "in running":
                        await asyncio.sleep(8)
                    elif 'validate' in info:
                        ret = info
                        break
            else:
                raise Exception("Captcha failed")
    except:
        pass

    return ValiResult(
        challenge=ret["challenge"],
        gt=ret["gt"],
        gt_user_id=ret["gt_user_id"],
        vali=ret["validate"]
    )
