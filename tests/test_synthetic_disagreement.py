from synthetic_disagreement import (
    AdversarialNoise,
    BiasedNoise,
    DriftNoise,
    OrdinalSlipNoise,
    UniformNoise,
    agreement_curve_svg,
    degradation_curve,
    generate,
    write_agreement_curve_svg,
)

def test_models_deterministic():
    items=[{"item_id":"1","label":1},{"item_id":"2","label":0}]
    for cls in [UniformNoise, BiasedNoise, OrdinalSlipNoise, AdversarialNoise, DriftNoise]:
        out=generate(items,["r1","r2"],cls(rate=0.5, seed=1),[0,1])
        assert len(out)==4

def test_stress_curve_uses_iaa_kit_and_writes_svg(tmp_path):
    items = [{"item_id": str(index), "label": index % 2} for index in range(12)]
    rows = degradation_curve(items, ["r1", "r2", "r3"], lambda level: UniformNoise(rate=level, seed=7), [0.0, 0.25, 0.5])
    assert [row["noise"] for row in rows] == [0.0, 0.25, 0.5]
    assert all(-1 <= row["agreement"] <= 1 for row in rows)
    svg = agreement_curve_svg(rows)
    assert "<svg" in svg and "polyline" in svg and "Agreement" in svg
    output = write_agreement_curve_svg(rows, tmp_path / "curve.svg")
    assert output.read_text(encoding="utf-8").startswith("<svg")
