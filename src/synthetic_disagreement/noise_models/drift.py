class NoiseModel:
    def __init__(self, rate=0.1, seed=0):
        import random; self.rate=rate; self.rng=random.Random(seed)
    def corrupt(self, label, labels, item_index=0): return label

class DriftNoise(NoiseModel):
    def corrupt(self, label, labels, item_index=0):

        effective=min(1.0,self.rate*(1+item_index/10))
        return self.rng.choice(labels) if self.rng.random() < effective else label
