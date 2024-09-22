from enum import Enum


class eModuleType(Enum):
    CRON = "cron"
    DAILY = "daily"
    TOOL = "tool"
    # HIDDEN = "hidden"


class eModuleConfItemType(Enum):
    bool = 'bool'
    int = 'int'
    choice_single = 'choice_single'
    choice_multi = 'choice_multi'
    time = 'time'


class eCronOperation(Enum):
    START = "start"
    FINISH = "finish"


class eResultStatus(Enum):
    SUCCESS = "成功"
    SKIP = "跳过"
    WARNING = "警告"
    ABORT = "中止"
    ERROR = "错误"
    PANIC = "致命"


class eGamePlatformId(Enum):
    Android = 0
    IOS = 1
