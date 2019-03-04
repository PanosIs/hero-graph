from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from src.database.steam_database_api import get_hero_ids

class IDEncoder:
    def __init__(self, hero_ids):
        self.labeler = LabelEncoder()
        self.onehot_encoder = OneHotEncoder(categories='auto', sparse=False)
        self.onehot_encoder.fit(self.labeler.fit_transform(hero_ids).reshape(-1,1))

    def encode_label(self, id):
        return self.labeler.transform([id])[0]

    def inverse_label(self, label):
        return self.labeler.inverse_transform(label)

    def encode_onehot(self, id):
        return self.onehot_encoder.transform(self.labeler.transform([id]).reshape(1,1))[0]

    def inverse_onehot(self, onehot):
        return self.labeler.inverse_transform(self.onehot_encoder.inverse_transform(onehot).ravel())[0]

    def encode_list_onehot(self, list):
        return sum(self.onehot_encoder.transform(self.labeler.transform(list).reshape(-1,1)))

encoder = IDEncoder(get_hero_ids())