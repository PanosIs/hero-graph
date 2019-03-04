import mongoengine
from mongoengine import *

SIDE = ((0, 'Radiant'),
        (1, 'Dire'))

class Hero(Document):
    id = LongField(primary_key=True)
    name = StringField(required=True)
    localized_name = StringField(required=True)

    meta = {'db_alias': 'Daedalus'}

class PlayerPerformance(EmbeddedDocument):
    account_id = LongField(required=True)
    player_slot = IntField()
    hero_id = IntField(required=True)
    kills = IntField()
    deaths = IntField()
    assists = IntField()
    leaver_status = IntField()
    last_hits = IntField()
    denies = IntField()
    gold_per_min = IntField()
    xp_per_min = IntField()
    level = IntField()

    item_0 = IntField()
    item_1 = IntField()
    item_2 = IntField()
    item_3 = IntField()
    item_4 = IntField()
    item_5 = IntField()
    backpack_0 = IntField()
    backpack_1 = IntField()
    backpack_2 = IntField()

    meta = {'db_alias': 'Daedalus'}

class PickBan(EmbeddedDocument):
    is_pick = BooleanField(required=True)
    hero_id = IntField(required=True)
    team = IntField(min_value=0, max_value=1, required=True)
    order = IntField(min_value=0, max_value=21)

    meta = {'db_alias': 'Daedalus'}

class Match(Document):
    match_id = LongField(required=True, primary_key=True)
    match_seq_num = LongField(required=True)
    cluster = IntField()

    lobby_type = IntField(required=True)
    game_mode = IntField(required=True)
    pre_game_duration = IntField()
    human_players = IntField()
    leagueid = LongField()
    tournament_id = LongField()
    tournament_round = IntField()

    radiant_team_id = LongField()
    dire_team_id = LongField()

    players = ListField(EmbeddedDocumentField(PlayerPerformance))
    picks_bans = ListField(EmbeddedDocumentField(PickBan))

    radiant_win = BooleanField(required=True)
    duration = IntField(required=True)
    start_time = LongField()

    tower_status_radiant = IntField()
    tower_status_dire = IntField()
    barracks_status_radiant = IntField()
    barracks_status_dire = IntField()
    first_blood_time = IntField()
    radiant_score = IntField()
    dire_score = IntField()

    meta = {
        'indexes': [
            'game_mode',
            'match_seq_num',
            '-match_seq_num'
        ],
        'db_alias': 'Daedalus'
    }