from __future__ import annotations

from pathlib import Path


def degradation_curve(items, raters, model_factory, levels):
    from iaa_kit import fleiss_kappa
    rows=[]
    for level in levels:
        generated = __import__('synthetic_disagreement.generators', fromlist=['generate']).generate(items, raters, model_factory(level), sorted({i['label'] for i in items}))
        matrix=[[generated[(item.get('item_id', idx), r)] for r in raters] for idx,item in enumerate(items)]
        rows.append({"noise": level, "agreement": fleiss_kappa(matrix)})
    return rows


def agreement_curve_svg(rows, width: int = 640, height: int = 360) -> str:
    if not rows:
        raise ValueError("rows must contain at least one curve point")
    margin = 44
    plot_width = width - margin * 2
    plot_height = height - margin * 2
    min_noise = min(float(row["noise"]) for row in rows)
    max_noise = max(float(row["noise"]) for row in rows)
    min_agreement = min(float(row["agreement"]) for row in rows)
    max_agreement = max(float(row["agreement"]) for row in rows)
    if max_noise == min_noise:
        max_noise = min_noise + 1.0
    if max_agreement == min_agreement:
        max_agreement = min_agreement + 1.0

    def point(row):
        x = margin + (float(row["noise"]) - min_noise) / (max_noise - min_noise) * plot_width
        y = height - margin - (float(row["agreement"]) - min_agreement) / (max_agreement - min_agreement) * plot_height
        return round(x, 2), round(y, 2)

    points = [point(row) for row in rows]
    polyline = " ".join(f"{x},{y}" for x, y in points)
    markers = "\n".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#176b53" />' for x, y in points)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="agreement versus noise curve">
  <rect width="{width}" height="{height}" fill="#ffffff" />
  <line x1="{margin}" y1="{height - margin}" x2="{width - margin}" y2="{height - margin}" stroke="#182033" />
  <line x1="{margin}" y1="{margin}" x2="{margin}" y2="{height - margin}" stroke="#182033" />
  <text x="{width / 2}" y="{height - 10}" text-anchor="middle" font-family="sans-serif" font-size="13">Noise level</text>
  <text x="14" y="{height / 2}" transform="rotate(-90 14 {height / 2})" text-anchor="middle" font-family="sans-serif" font-size="13">Agreement</text>
  <polyline points="{polyline}" fill="none" stroke="#176b53" stroke-width="3" />
  {markers}
</svg>
"""


def write_agreement_curve_svg(rows, path: str | Path) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(agreement_curve_svg(rows), encoding="utf-8")
    return output
