from src.database.steam_database_api import get_drafts_plaintext
from torch.utils.data import Dataset
from typing import List
from src.utils.id_normalizer import encoder
import numpy
import torch
import pickle


HERO_POOL_SIZE = 116

class DraftDataset(Dataset):
    def __init__(self, drafts : List[List[int]]):
        self.drafts = drafts

    def __getitem__(self, index):
        draft_index, hero_index = divmod(index, 5)
        draft = self.drafts[draft_index]


        context = draft[:hero_index] + draft[hero_index + 1:]
        target = draft[hero_index]

        context = torch.LongTensor(context)

        return context, target

    def __len__(self):
        return len(self.drafts) * 5


class MatchDataset(Dataset):
    def __init__(self, matches, targets):
        self.matches = matches
        self.targets = targets

    def __getitem__(self, index):
        return self.matches[index], self.targets[index]

    def __len__(self):
        pass


def load_draft_dataset(limit = 5000, type = 'onehot') -> DraftDataset:
    normalized_drafts = []
    if(type == 'onehot'):
        for draft in get_drafts_plaintext(limit):
            try:
                radiant = [i['hero_id'] for i in draft['players'][0:5]]
                dire = [i['hero_id'] for i in draft['players'][5:10]]

                radiant = encoder.encode_list_onehot(radiant)
                dire = encoder.encode_list_onehot(dire)

                normalized_drafts.append(radiant)
                normalized_drafts.append(dire)
            except ValueError:
                print("Invalid draft found.")

        return DraftDataset(normalized_drafts)

    elif(type == 'labeled'):
        pass

def load_match_dataset(limit = 5000, type = 'onehot', embeddings = None) -> MatchDataset:
    if(type == 'onehot'):
        data, targets = [], []
        for draft in get_drafts_plaintext(limit):
            try:
                radiant = [i['hero_id'] for i in draft['players'][0:5]]
                dire = [i['hero_id'] for i in draft['players'][5:10]]

                radiant = encoder.encode_list_onehot(radiant)
                dire = encoder.encode_list_onehot(dire)

                data.append(numpy.concatenate((radiant, dire)))
                targets.append(draft['radiant_win'])
            except ValueError:
                print("Invalid draft found.")
        return MatchDataset(data, targets)

    elif(type == 'labeled'):
        pass
    elif(type == 'embedded'):
        pass