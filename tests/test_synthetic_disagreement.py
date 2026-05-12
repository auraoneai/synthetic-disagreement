from synthetic_disagreement import AdversarialNoise, BiasedNoise, DriftNoise, OrdinalSlipNoise, UniformNoise, generate

def test_models_deterministic():
    items=[{"item_id":"1","label":1},{"item_id":"2","label":0}]
    for cls in [UniformNoise, BiasedNoise, OrdinalSlipNoise, AdversarialNoise, DriftNoise]:
        out=generate(items,["r1","r2"],cls(rate=0.5, seed=1),[0,1])
        assert len(out)==4
