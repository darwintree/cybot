from peewee import SqliteDatabase, Model, CharField, IntegerField, ForeignKeyField, BooleanField

db = SqliteDatabase("sv.db")

class BaseModel(Model):
    class Meta:
        database = db

class Cardpack(BaseModel):
    cardpack_id = IntegerField(primary_key=True)
    cardpack_name = CharField(null=True)
    short = CharField(null=True)
    short_cn = CharField(null=True)

class Card(BaseModel):
    card_id = IntegerField(primary_key=True)
    card_name = CharField(null=True)
    tp = CharField(default="-")
    job = CharField(null=True)
    rarity = CharField(null=True)
    category = CharField(null=True)
    cv = CharField(null=True)
    cardpack = ForeignKeyField(Cardpack, backref="cards",null=True)
    cost = IntegerField(null=True)
    attack = IntegerField(null=True)
    hp = IntegerField(null=True)
    attack_ev = IntegerField(null=True)
    hp_ev = IntegerField(null=True)
    ability = CharField(null=True) #进化前异能
    ability_ev = CharField(null=True)
    description = CharField(null=True) # 卡牌文本
    description_ev = CharField(null=True) # 进化后卡牌文本
    index_word = CharField(null=True) # 用于模糊搜索卡牌的字符串

#黑话
class Nickname(BaseModel):
    card = ForeignKeyField(Card, backref="nicknames")
    nn = CharField()