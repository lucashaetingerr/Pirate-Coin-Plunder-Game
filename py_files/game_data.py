import json
import os

class GameData:
    def __init__(self):
        self.items = {}
        self.ouro = 0
        self.ouros_por_segundo = 0
        self.tempo_decorrido = 0  # Tempo decorrido em segundos

    def to_dict(self):
        return {
            "items": self.items,
            "ouro": self.ouro,
            "ouros_por_segundo": self.ouros_por_segundo,
            "tempo_decorrido": self.tempo_decorrido
        }

    def from_dict(self, data):
        self.items = data.get("items", {})
        self.ouro = data.get("ouro", 0)
        self.ouros_por_segundo = data.get("ouros_por_segundo", 0)
        self.tempo_decorrido = data.get("tempo_decorrido", 0)

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f)

    def load(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                self.from_dict(data)
