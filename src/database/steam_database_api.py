from mongoengine import connect
from typing import List
from src.database import steam_database_model

MATCH_IGNORE_FIELDS = {'negative_votes', 'dire_team_complete', 'dire_name', 'flags', 'engine', 'positive_votes',
                       'dire_logo', 'radiant_logo', 'dire_captain', 'radiant_captain', 'radiant_name',
                       'radiant_team_complete'}

DATABASE_NAME = 'Daedalus'

connect(DATABASE_NAME, alias=DATABASE_NAME)

def get_heroes() -> List[steam_database_model.Hero]:
    heroes = steam_database_model.Hero.objects()
    return list(heroes)

def get_hero_ids() -> List[int]:
    heroes = get_heroes()
    return [hero.id for hero in heroes]

def get_hero_by_id(id : int) -> steam_database_model.Hero:
    try:
        hero = steam_database_model.Hero.objects(id = id)[0]
        return hero
    except IndexError:
        pass # TODO: Add logging

def get_hero_by_name(name : str) -> steam_database_model.Hero:
    try:
        hero = steam_database_model.Hero.objects(localized_name = name)[0]
        return hero
    except IndexError:
        pass # TODO: Add logging

def get_max_sequence_number() -> int:
    try:
        max_num = steam_database_model.Match.objects.scalar('match_seq_num').order_by('-match_seq_num')[:1][0]
        return max_num
    except:
        return 0

def get_drafts(limit = None) -> List[steam_database_model.Match]:
    if(limit != None):
        return list(steam_database_model.Match.objects.order_by('-match_seq_num').scalar('players.hero_id', 'players.player_slot', 'radiant_win')[:limit])
    else:
        return list(steam_database_model.Match.objects.order_by('-match_seq_num').scalar('players.hero_id', 'players.player_slot', 'radiant_win'))

def get_drafts_plaintext(limit = None) -> List[dict]:
    if(limit != None):
        return list(steam_database_model.Match.objects.order_by('-match_seq_num').scalar('players.hero_id', 'players.player_slot', 'radiant_win').as_pymongo()[:limit])
    else:
        return list(steam_database_model.Match.objects.order_by('-match_seq_num').scalar('players.hero_id', 'players.player_slot', 'radiant_win').as_pymongo())

def insert_hero(json : dict):
    try:
        hero = steam_database_model.Hero(**json)
        hero.save()
    except:
        pass # TODO: Add logging

def insert_match(json : dict):
    try:
        for field in MATCH_IGNORE_FIELDS:
            json.pop(field, None)
        match = steam_database_model.Match(**json)
        match.save()
    except:
        pass # TODO: Add logging