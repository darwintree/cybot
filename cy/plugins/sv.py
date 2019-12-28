from fuzzywuzzy import process, fuzz
from model.card import Card, Cardpack, Nickname
from pprint import pprint
from peewee import JOIN

cards = Card.select().join(Cardpack)
nicknames = Nickname.select().join(Card)
keywords = list(map(lambda a: a.index_word, cards))
names = list(map(lambda a: a.card_name, cards))

# eg1
# 不败剑圣 传说卡 极斗之巅UCL
# 消费1 皇家 士兵
# 进化前 0-1
# 謝幕曲 如果是自己的回合，則會給予自己的主戰者「自己的回合開始時，召喚1個不敗劍聖‧景光到戰場上並使其進化，而後失去此能力」效果。
# 入場曲 爆能強化 3； 獲得+2/+0與突進 效果。
# 进化后 1-1
# 攻擊時 獲得+X/+X效果。X為「這場對戰中，自己的從者進化的次數」。
# eg2
# 全神贯注 青铜卡 极斗之巅UCL
# 消费0 复仇者 -
# 給予自己的主戰者「自己的回合結束時，如果自己剩餘的PP為1以上，則會抽取1張卡片。如果為3以上，則會由原本的抽取1張轉變為抽取2張，並回復自己的主戰者2點生命值。自己的回合結束時，失去此能力」效果。（主戰者可以重複疊加此效果）
def output_card(card):
    o = ""
    if card.category == "从者卡":
        o = "%s %s %s%s\n消费%s %s %s\n进化前 %s-%s\n%s\n进化后 %s-%s\n%s"%(card.card_name, card.rarity, \
            card.cardpack.cardpack_name, card.cardpack.short, card.cost, card.job, card.tp, card.attack, card.hp, \
                card.ability.replace("<br>", "\n"), card.attack_ev, card.hp_ev, card.ability_ev.replace("<br>", "\n"))
    else:
        o = "%s %s %s%s\n消费%s %s %s\n%s"%(card.card_name, card.rarity, card.cardpack.cardpack_name, card.cardpack.short, 
            card.cost, card.job, card.tp, card.ability.replace("<br>", "\n"))
    o += "\n Portal:https://shadowverse-portal.com/card/%s?lang=zh-tw"%card.card_id
    return o

def fuzzyfinder(user_input, collection, scorer_=fuzz.token_set_ratio):
    suggestions = process.extractBests(user_input, collection, limit=5, scorer=scorer_)
    return [
        (x,r) for x, r in
        filter(
            lambda a: a[1] > 0,
            sorted(suggestions, key=lambda a: a[1], reverse=True)
        )
    ]

def search(s):
    is_single_word = s.split(" ")[0] == s
    if is_single_word:
            # xjb写的
        print("searching nickname...")
        search_result = [(item.card.card_name, 100) for item in nicknames.where(Nickname.nn == s)]
        if not search_result:
            print("no nickname")
            search_result = fuzzyfinder(s, names)
    else:
        search_result = fuzzyfinder(s, keywords)

    if search_result:
        results = [cards.where((Card.card_name if is_single_word else Card.index_word) == key[0])[0] \
            for key in search_result]
        o = output_card(results[0])
        if len(search_result) > 1:
            o += "\n\n其他可能的卡片有："
            for i in range(1, len(results)):
                o += results[i].card_name+" "
            o += "\n如果没有合适的结果，尝试添加更多参数进行搜索（用空格隔开）\n如:皇家护卫 112 黄金卡 指挥官"
        return o
    else:
        return "没有合适的结果，尝试添加更多参数进行搜索（用空格隔开）\n如:皇家 112 金 指挥官"

def add_nickname(_card_name, _nickname):
    try:
        c_id = Card.get(Card.card_name==_card_name)
        Nickname.create(card_id=c_id, nn=_nickname)
        global nicknames
        nicknames = Nickname.select().join(Card)
        return "成功为「%s」添加别名「%s」"%(_card_name, _nickname)
    except:
        return "添加别名失败。请确认卡牌名称是否完整或者别名是否已存在"
        

