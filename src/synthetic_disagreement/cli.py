from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from .generators import generate
from .noise_models import AdversarialNoise, BiasedNoise, DriftNoise, OrdinalSlipNoise, UniformNoise
from .stress_test import degradation_curve, write_agreement_curve_svg

NOISE_MODELS = {
    "uniform": UniformNoise,
    "biased": BiasedNoise,
    "ordinal-slip": OrdinalSlipNoise,
    "adversarial": AdversarialNoise,
    "drift": DriftNoise,
}


def load_items(path: str | Path) -> list[dict[str, Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        payload = payload.get("items")
    if not isinstance(payload, list) or not all(isinstance(item, dict) for item in payload):
        raise ValueError("items input must be a JSON array or an object with an items array")
    return payload


def render_generated(items: list[dict[str, Any]], raters: Sequence[str], model_name: str, rate: float, seed: int) -> dict[str, Any]:
    labels = sorted({item.get("label") for item in items}, key=repr)
    model = NOISE_MODELS[model_name](rate=rate, seed=seed)
    generated = generate(items, raters, model, labels)
    rows = [
        {
            "item_id": str(item_id),
            "rater_id": str(rater_id),
            "label": label,
            "synthetic": True,
            "noise_model": model_name,
            "seed": seed,
        }
        for (item_id, rater_id), label in sorted(generated.items(), key=lambda entry: (str(entry[0][0]), str(entry[0][1])))
    ]
    return {"ok": True, "item_count": len(items), "rater_count": len(raters), "labels": rows}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="synthetic-disagreement")
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="Generate deterministic synthetic reviewer labels.")
    gen.add_argument("--items", required=True, type=Path)
    gen.add_argument("--raters", default="r1,r2,r3")
    gen.add_argument("--noise-model", choices=sorted(NOISE_MODELS), default="uniform")
    gen.add_argument("--rate", type=float, default=0.1)
    gen.add_argument("--seed", type=int, default=0)
    gen.add_argument("--out", type=Path)

    curve = sub.add_parser("stress-curve", help="Generate an IAA stress curve from synthetic disagreement.")
    curve.add_argument("--items", required=True, type=Path)
    curve.add_argument("--raters", default="r1,r2,r3")
    curve.add_argument("--noise-model", choices=sorted(NOISE_MODELS), default="uniform")
    curve.add_argument("--levels", default="0,0.25,0.5")
    curve.add_argument("--seed", type=int, default=0)
    curve.add_argument("--svg-out", type=Path)
    curve.add_argument("--out", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        items = load_items(args.items)
        raters = [rater.strip() for rater in args.raters.split(",") if rater.strip()]
        if args.command == "generate":
            payload = render_generated(items, raters, args.noise_model, args.rate, args.seed)
        else:
            levels = [float(level.strip()) for level in args.levels.split(",") if level.strip()]
            model_cls = NOISE_MODELS[args.noise_model]
            rows = degradation_curve(items, raters, lambda level: model_cls(rate=level, seed=args.seed), levels)
            payload = {
                "ok": True,
                "item_count": len(items),
                "rater_count": len(raters),
                "noise_model": args.noise_model,
                "levels": levels,
                "curve": rows,
            }
            if args.svg_out:
                write_agreement_curve_svg(rows, args.svg_out)
                payload["svg_path"] = str(args.svg_out)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        payload = {"ok": False, "error": str(exc)}
        _write_json(payload, getattr(args, "out", None))
        return 1
    _write_json(payload, args.out)
    return 0


def _write_json(payload: dict[str, Any], out: Path | None) -> None:
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    raise SystemExit(main())
