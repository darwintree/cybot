import random

class Zeus:
    def __init__(self):
        self.atk_bonus = 0
        self.defense_bonus = 0
        self.hp_restore = 0
        self.blind = False
        self.bane = False
        self.storm = False
        self.guard = False
        self.lyric = ""

    def activate_once(self):
        r = random.randint(1, 5)
        if r == 1:
            self.hp_restore += 5
            self.lyric += "你的主战者回复了5点体力！\n"
        elif r == 2:
            self.atk_bonus += 3
            self.blind = True
            self.lyric += "至高神·宙斯获得了+3/+0！ 至高神·宙斯可以无视守护进行攻击！\n"
        elif r == 3:
            self.storm = True
            self.atk_bonus += 2
            self.defense_bonus += 1
            self.lyric += "至高神·宙斯获得了+2/+1！ 至高神·宙斯获得了疾驰！\n"
        elif r == 4:
            self.bane = True
            self.atk_bonus += 1
            self.defense_bonus += 2
            self.lyric += "至高神·宙斯获得了+1/+2！ 至高神·宙斯获得了必杀！\n"
        elif r == 5:
            self.guard = True
            self.defense_bonus += 3
            self.lyric += "至高神·宙斯获得了+0/+3！ 至高神·宙斯获得了守护！\n"

    def activate(self, evolve_count):
        self.lyric += "宙斯的入场曲发动了！\n"
        for i in range(evolve_count):
            self.activate_once()

    def __str__(self):
        txt = self.lyric
        txt += "\n\n"

        txt += "啊，这强大的力量，即使是邪龙林德沃姆也无法企及！\n" if self.storm and self.atk_bonus >= 6 else ""
        txt += "啊，这可靠的身躯，能超越万雷之君的只有他自己！\n" if self.guard and self.defense_bonus >= 6 else ""
        txt += "啊，神王的仁慈，轻而易举便超越了美食天使的全力！\n" if self.hp_restore >= 15 else ""
        txt += "神王的召唤仪式好像出现了什么差错......\n" if self.storm == False and self.guard == False else ""
        # txt += "这溢出的抛瓦啊啊啊啊啊啊啊啊啊啊啊，将要与灭杀之铠一较高下！" if self.storm == False and self.atk_bonus >= 5 and self.defense_bonus >= 2 else ""
        txt += "庆贺吧！他是全知全能，位于诸神顶点的众神之父、万雷之主————至高神·宙斯！\n此刻，他携带着崭新的进化之力降临，让世" \
               "间重现神之荣光！\n" if self.blind and self.bane and self.storm and self.guard else ""
        txt += "至高神·宙斯使你的主战者回复了%d点血量!\n" % self.hp_restore if self.hp_restore != 0 else ""
        txt += "至高神·宙斯具有了异能 " if self.blind or self.bane or self.storm or self.guard else ""
        txt += "无视守护 " if self.blind else ""
        txt += "必杀 " if self.bane else ""
        txt += "疾驰 " if self.storm else ""
        txt += "守护 " if self.guard else ""
        txt += "\n"
        txt += "至高神·宙斯现身为"
        txt += "%d/%d!\n" % (self.atk_bonus+5, self.defense_bonus+5)
        return txt


# def main():
#     print("=================至高神模拟器=================")
#     while True:
#         evolve = int(input("本回合中你的随从已进化次数:\n"))
#         zenx = Zeus()
#         zenx.activate(evolve)
#         print(zenx)
#         print("\n\n")


# if __name__ == '__main__':
#     main()
