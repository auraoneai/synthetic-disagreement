# synthetic-disagreement

Stress-test an inter-annotator agreement pipeline with deterministic synthetic reviewer labels.

`synthetic-disagreement` is for annotation leads, evaluation methodologists, and test engineers who want to exercise calibration code before collecting real labels. It provides uniform, biased, ordinal-slip, adversarial, and drift noise models, then feeds generated rating matrices into `iaa-kit` to show how agreement changes as noise increases.

## Inspectable Output

- Python API: `generate` returns a deterministic mapping keyed by `(item_id, rater_id)`.
- Installed CLI `generate`: a JSON report whose `labels` rows contain item id, rater id, generated label, noise model, seed, and `synthetic: true`.
- Installed CLI `stress-curve`: a JSON report whose `curve` points contain noise level and Fleiss kappa agreement, with an optional deterministic SVG.

The same inputs, seed, model, and levels produce the same output.

## Runtime Boundary

Generation and stress curves run entirely in the local Python process with NumPy and `iaa-kit`. There are no network requests, model calls, reviewer services, telemetry hooks, or uploaded task data.

## Install

Python library and CLI:

```bash
python -m pip install synthetic-disagreement==0.1.2
```

## Python API Quickstart

```bash
python - <<'PY'
from synthetic_disagreement import UniformNoise, generate

labels = generate(
    [{"item_id": "1", "label": 1}],
    ["r1", "r2"],
    UniformNoise(rate=0.2, seed=7),
    [0, 1],
)
print(labels)
PY
```

## CLI Quickstart

```bash
synthetic-disagreement generate \
  --items examples/synthetic_items.json \
  --raters r1,r2,r3 \
  --noise-model uniform \
  --rate 0.2 \
  --seed 7 \
  --out synthetic-labels.json

synthetic-disagreement stress-curve \
  --items examples/synthetic_items.json \
  --raters r1,r2,r3 \
  --noise-model uniform \
  --levels 0,0.25,0.5 \
  --seed 7 \
  --out agreement-curve.json \
  --svg-out agreement-curve.svg
```

See [`docs/methodology.md`](docs/methodology.md) for noise-model and data-policy details.

## Release Status

Registry and artifact status verified July 13, 2026: version `0.1.2` is published on PyPI and tagged `v0.1.2` in the public repository. The wheel includes the Python API plus the JSON and SVG CLI. The project is alpha software. No reviewer-volume, quality, or adoption claim is made.

## Limits

Synthetic noise is a test fixture, not a model of every real reviewer population. The generated curves do not replace pilot annotation, reviewer training, adjudication, or empirical agreement studies.

## Next Action

Use the Python API or installed CLI to generate seeded labels or a stress curve, confirm the pipeline responds as expected, then compare the result with a real pilot annotation study.
