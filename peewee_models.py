from peewee import *

escordia_db = SqliteDatabase('escordia_db')


class BaseModel(Model):
    class Meta:
        database = escordia_db


class PlayerModel(BaseModel):
    name = CharField(primary_key=True)
    stats = CharField()  # Stats dict converted to string
    lvl = IntegerField()
    xp = IntegerField()
    xp_to_next_lvl = IntegerField()
    xp_rate = FloatField()
    money = IntegerField()
    essence = IntegerField()
    inventory = CharField()  # Inventory dict converted to string
    equipment = CharField()  # Equipment dict converted to string
    skills = CharField()  # Skills list converted to string
    passives = CharField()  # Passives list converted to string
    current_area = IntegerField()
    in_fight = BooleanField()
    in_dungeon = BooleanField()
    defeated_bosses = CharField()  # Defeated bosses list converted to string
    job_dict_list = CharField()  # Job dict list converted to string
    current_job_dict = CharField()  # Current job dict converted to string
    current_job = CharField()
    blessings = CharField()  # Blessings list converted to string
