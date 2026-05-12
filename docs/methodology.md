# Synthetic Disagreement Methodology

`synthetic-disagreement` creates controlled reviewer-label disagreement so teams can stress-test agreement metrics before recruiting reviewers.

## Noise Model Design

- Uniform noise models random independent mistakes.
- Biased noise models label-prevalence skew.
- Ordinal slip models near-miss ratings on ordered scales.
- Adversarial noise models consistently inverted or hostile annotators.
- Drift models increasing disagreement over batches or time.

## Stress Curves

The stress harness feeds generated labels into `iaa-kit` and records how agreement changes as noise increases. The SVG renderer is deterministic so the same seed and parameters produce the same curve.

## Data Policy

Generated labels and examples are synthetic. The library does not require paid annotators or real task data.
