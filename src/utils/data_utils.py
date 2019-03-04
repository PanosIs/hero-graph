import pickle
from torch.utils.data import Dataset, DataLoader
from typing import List
import torch

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

def get_match_dataset():
    with open("data", "rb") as f:
        input, targets = pickle.load(f)
    return MatchDataset(input, targets)

