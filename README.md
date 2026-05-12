# synthetic-disagreement

Stress-test your IAA pipeline before recruiting reviewers with deterministic synthetic annotator disagreement.

## Quickstart

```bash
pip install synthetic-disagreement
python -c "from synthetic_disagreement import UniformNoise, generate; print(generate([{'item_id':'1','label':1}], ['r1','r2'], UniformNoise(seed=1), [0,1]))"
```

## IAA Stress Curve

```python
from synthetic_disagreement import UniformNoise, degradation_curve, write_agreement_curve_svg

items = [{"item_id": str(i), "label": i % 2} for i in range(12)]
rows = degradation_curve(items, ["r1", "r2", "r3"], lambda level: UniformNoise(rate=level, seed=7), [0, 0.25, 0.5])
write_agreement_curve_svg(rows, "agreement-vs-noise.svg")
```

The stress harness feeds generated labels into `iaa-kit` and emits a deterministic SVG agreement-vs-noise curve.

## What This Is Not

Not a replacement for real reviewer studies. Examples are synthetic.
