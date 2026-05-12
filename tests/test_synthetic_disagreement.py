from synthetic_disagreement import generate
from synthetic_disagreement.noise_models import UniformNoise, BiasedNoise, OrdinalSlipNoise, AdversarialNoise, DriftNoise

def test_models_deterministic():
    items=[{"item_id":"1","label":1},{"item_id":"2","label":0}]
    for cls in [UniformNoise, BiasedNoise, OrdinalSlipNoise, AdversarialNoise, DriftNoise]:
        out=generate(items,["r1","r2"],cls(rate=0.5, seed=1),[0,1])
        assert len(out)==4
