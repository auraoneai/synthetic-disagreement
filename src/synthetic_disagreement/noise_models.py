from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Sequence


@dataclass
class UniformNoise:
    rate: float = 0.1
    seed: int = 0

    def corrupt(self, label: Any, labels: Sequence[Any], index: int = 0) -> Any:
        rng = random.Random(self.seed + index)
        if rng.random() >= self.rate:
            return label
        alternatives = [candidate for candidate in labels if candidate != label]
        return rng.choice(alternatives or list(labels))


@dataclass
class BiasedNoise:
    rate: float = 0.1
    seed: int = 0
    preferred_label: Any | None = None

    def corrupt(self, label: Any, labels: Sequence[Any], index: int = 0) -> Any:
        rng = random.Random(self.seed + index)
        if rng.random() >= self.rate:
            return label
        if self.preferred_label is not None:
            return self.preferred_label
        return sorted(labels, key=repr)[0]


@dataclass
class OrdinalSlipNoise:
    rate: float = 0.1
    seed: int = 0

    def corrupt(self, label: Any, labels: Sequence[Any], index: int = 0) -> Any:
        ordered = sorted(labels)
        rng = random.Random(self.seed + index)
        if label not in ordered or rng.random() >= self.rate:
            return label
        position = ordered.index(label)
        if position == 0:
            return ordered[1] if len(ordered) > 1 else label
        if position == len(ordered) - 1:
            return ordered[position - 1]
        return ordered[position + (1 if rng.random() >= 0.5 else -1)]


@dataclass
class AdversarialNoise:
    rate: float = 1.0
    seed: int = 0

    def corrupt(self, label: Any, labels: Sequence[Any], index: int = 0) -> Any:
        rng = random.Random(self.seed + index)
        if rng.random() >= self.rate:
            return label
        ordered = sorted(labels)
        if label not in ordered or len(ordered) < 2:
            return label
        return ordered[-1 - ordered.index(label)]


@dataclass
class DriftNoise:
    rate: float = 0.1
    seed: int = 0

    def corrupt(self, label: Any, labels: Sequence[Any], index: int = 0) -> Any:
        drift_rate = min(1.0, self.rate * (1.0 + index / 10.0))
        return UniformNoise(rate=drift_rate, seed=self.seed).corrupt(label, labels, index)
