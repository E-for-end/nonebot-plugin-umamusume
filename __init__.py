from pathlib import Path
from typing import List, Union

from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    MessageSegment,
    PrivateMessageEvent,
)
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import CommandArg

from .types import ReplyFileTuple, ReplyTuple
from .utils import get_age_calc_api, get_random_dog_pic

__plugin_meta__ = PluginMetadata(
    name = '赛馬娘相关',
    description = '适用于nonebot2 v11的赛馬娘内容插件',
    usage = help_text
)

# region matchers
# 试试看，在 vscode 里，# region ... # endregion 注释之间的代码可以折叠

# 获取当前命令型消息的元组形式命令名，简单说就是 触发的命令（不含命令前缀）
# 你测试的时候，可以看下你 env的配置中的命令起始字符 COMMAND_START，根据你的命令前缀加上cmd的命令词即可。
# 例如 COMMAND_START=["/"]  cmd1的触发命令（【】内的是命令啊，别把【】也打进去了）就是 【/本地图片】 或者 【/本地图片别名】
# 需要传参数的命令，例如cmd3的触发命令就是 【/本地图片含传参 图片1】
local_pic = on_command("本地图片", aliases={"本地图片别名"})
# 那么下面这行就是 触发命令为 狗狗图 或者 狗狗图别名 。 其中 aliases是命令的别名，都可以触发。
dogs_pic = on_command("狗狗图", aliases={"狗狗图别名"})
local_pic_with_args = on_command("本地图片含传参")

# 读取本地文件中的内容返回
local_file = on_command("本地文件含传参")

# 固定命令触发，直接返回固定文本
regular_text = on_command("固定文本")
# 固定命令 追加一个传参 触发，直接返回对应的固定文本
regular_text_with_args = on_command("固定文本含传参")

# 调用别人的API时候，要求你传入一个参数这种。然后以回复的形式返回
# 例子：传入 年-月-日 计算生肖
api_zodiac = on_command("生肖计算")

# 图片+文字 合并转发
forward_msg = on_command("合并转发")

# endregion


# 使用 local_pic 响应器的 handle 装饰器装饰了一个函数_
# _函数会被自动转换为 Dependent 对象，并被添加到 local_pic 的事件处理流程中
@local_pic.handle()
# 这里获取一个 Matcher 对象，用于回复消息等
async def _(matcher: Matcher):
    # 文件路径，这里使用 Path 对象
    # 这里的路径是 插件目录/res/104117310_p0.jpg
    file_path = Path(__file__).parent / "res" / "特别周.jpg"

    # 可以是相对路径（./ 开头，相对于运行 nb run 的目录）
    # file_path = Path("./res/104117310_p0.jpg")

    # 可以是绝对路径（Windows 盘符:/ 开头，Linux / 开头）
    # file_path = Path("C:/res/104117310_p0.jpg")  # Windows
    # file_path = Path("/home/res/104117310_p0.jpg")  # Linux

    try:
        # 使用MessageSegment.image方法创建一个消息段，该消息段包含了文件路径对应的图像文件，并将其赋值给变量msg。
        # 在这个过程中，代码通过file参数将文件路径传递给image方法，以指定要发送的图像文件
        # file支持很多类型 Union[str, bytes, BytesIO, Path]，可以看看源码
        msg = MessageSegment.image(file=file_path)
    except Exception:
        # 打印错误详细信息
        logger.exception("发送失败")
        msg = "\n发送失败喵，请检查后台日志排查问题~"

    # 返回msg信息 结束，并且@触发命令的人（at_sender=True），不需要@可以改为False或者删掉
    await matcher.finish(msg, at_sender=True)