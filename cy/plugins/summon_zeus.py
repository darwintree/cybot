from nonebot import on_command, CommandSession
from cy.plugins.zeus import Zeus



@on_command('summon_zeus', aliases=('召唤宙斯',))
async def summon_zeus(session: CommandSession):
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
    evolve = session.get('evolve', prompt='你为至高神献上了几次进化？')
    # 获取城市的天气预报
    zeus_lyric = await get_lyric(int(evolve))
    await session.send(zeus_lyric)

@summon_zeus.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            try:
                session.state['evolve'] = int(stripped_arg)
            except Exception:
                session.pause('不可藐视至高神，速速为至高神献上进化')
            return

        if not stripped_arg:
            # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
            # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
            session.pause('快为至高神献上进化')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    try:
        session.state['evolve'] = int(stripped_arg)
    except Exception:
        session.state['evolve'] = 0

async def get_lyric(evolve):
    zenx = Zeus()
    zenx.activate(int(evolve))
    zeuslyric = str(zenx)
    return zeuslyric
