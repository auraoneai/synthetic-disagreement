# synthetic-disagreement

Stress-test your IAA pipeline before recruiting reviewers with deterministic synthetic annotator disagreement.

## Quickstart

```bash
pip install synthetic-disagreement
python -c "from synthetic_disagreement import generate; from synthetic_disagreement.noise_models import UniformNoise; print(generate([{'item_id':'1','label':1}], ['r1','r2'], UniformNoise(seed=1), [0,1]))"
```

## What This Is Not

Not a replacement for real reviewer studies. Examples are synthetic.
