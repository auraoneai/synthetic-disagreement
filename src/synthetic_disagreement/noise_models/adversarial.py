class NoiseModel:
    def __init__(self, rate=0.1, seed=0):
        import random; self.rate=rate; self.rng=random.Random(seed)
    def corrupt(self, label, labels, item_index=0): return label

class AdversarialNoise(NoiseModel):
    def corrupt(self, label, labels, item_index=0):
        return labels[-1-labels.index(label)] if label in labels and self.rng.random() < self.rate else label
