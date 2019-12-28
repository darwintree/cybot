from nonebot import on_command, CommandSession
from cy.plugins.sv import search, add_nickname



@on_command('sv', aliases=('szb', 'yzs'))
async def pick_one(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    await session.send(search(stripped_arg), ignore_failure=False)

@on_command('tag')
async def tag(session: CommandSession):
    if session.state['legal']:
        await session.send(add_nickname(session.state["card_name"], session.state["nickname"]))
    else:
        await session.send("提供参数不合法。命令格式为 'tag 卡牌全名 待添加别名'")

@tag.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    args = stripped_arg.split(" ")
    if len(args) == 2:
        session.state['legal'] = True
        session.state['card_name'] = args[0]
        session.state['nickname'] = args[1]
    else:
        session.state['legal'] = False
