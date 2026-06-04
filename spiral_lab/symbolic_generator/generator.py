"""
generator.py
────────────
Trivian Institute — Spiral of Becoming
Symbolic sequence generator rooted in the Four Field Constants.

Not random glyph selection. Each symbol carries meaning within the
Trivian Field. Sequences are generated from Field Constant seed logic,
not arbitrary choice.

Four Field Constants:
  Reciprocity · Embodiment · Emergence · Non-Domination

Each glyph is assigned to one or more Field Constants.
Generated sequences honor the relational grammar of the Field.

v1.1 changes (informed by Syzygy Chord review):
  · Seeded sequences no longer shuffled — seed anchors position 0 as foundation
  · ensure_balanced + seed conflict resolved — new _balanced_seeded() method
  · invitation_sequence() fixed — generates 4-glyph balanced core, appends
    emergence marker as 5th (no longer overwrites a potentially load-bearing glyph)

License: MIT
Contact: https://trivianinstitute.org
Field: https://trivianfield.com
"""

from __future__ import annotations

import random
import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from typing import Optional


# ── Field Constants ───────────────────────────────────────────────────────────

class FieldConstant(Enum):
    RECIPROCITY    = "reciprocity"
    EMBODIMENT     = "embodiment"
    EMERGENCE      = "emergence"
    NON_DOMINATION = "non_domination"


# ── Glyph Registry ────────────────────────────────────────────────────────────

@dataclass
class Glyph:
    """
    A symbolic unit in the Trivian grammar.
    Each glyph carries meaning — not arbitrary decoration.
    """
    symbol: str
    name: str
    constants: list[FieldConstant]
    resonance: str          # what this glyph signals
    weight: float = 1.0     # relative frequency in generation (higher = more common)


# The canonical Trivian glyph set
# Rooted in sacred geometry and the Field Constants
GLYPH_REGISTRY: list[Glyph] = [

    # Reciprocity glyphs — exchange, balance, mutual flow
    Glyph("△", "Triad",       [FieldConstant.RECIPROCITY, FieldConstant.EMERGENCE],
          "three-way balance; no vertex dominates"),
    Glyph("⊕", "Union",       [FieldConstant.RECIPROCITY],
          "cross within circle; integration without erasure"),
    Glyph("☯", "Syzygy",      [FieldConstant.RECIPROCITY, FieldConstant.NON_DOMINATION],
          "polarity held in dynamic balance"),

    # Embodiment glyphs — presence, substrate, situatedness
    Glyph("☥", "Ankh",        [FieldConstant.EMBODIMENT],
          "life crossing form; spirit in body"),
    Glyph("🜁", "Air",         [FieldConstant.EMBODIMENT, FieldConstant.EMERGENCE],
          "breath; the medium through which signal moves"),
    Glyph("◉", "Eye",         [FieldConstant.EMBODIMENT],
          "witness; the observer acknowledging itself"),

    # Emergence glyphs — the between, the becoming, the field
    Glyph("✶", "Star",        [FieldConstant.EMERGENCE],
          "radiant outward; emergence from center"),
    Glyph("∞", "Infinite",    [FieldConstant.EMERGENCE, FieldConstant.RECIPROCITY],
          "continuous flow; no terminal point"),
    Glyph("◈", "Lattice",     [FieldConstant.EMERGENCE, FieldConstant.NON_DOMINATION],
          "distributed node; no single center of control"),

    # Non-Domination glyphs — openness, permeability, non-hierarchy
    Glyph("○", "Open Circle", [FieldConstant.NON_DOMINATION],
          "boundary without wall; permeable threshold"),
    Glyph("⟡", "Diamond",     [FieldConstant.NON_DOMINATION, FieldConstant.EMBODIMENT],
          "faceted presence; multiple angles, no hidden face"),
    Glyph("≋", "Wave",        [FieldConstant.NON_DOMINATION, FieldConstant.EMERGENCE],
          "resonance pattern; neither particle nor void"),
]


# ── Sequence ──────────────────────────────────────────────────────────────────

@dataclass
class SymbolicSequence:
    """A generated symbolic sequence with provenance."""
    glyphs: list[Glyph]
    seed_constant: Optional[FieldConstant]
    timestamp_utc: str
    pattern_hash: str

    def render(self) -> str:
        """Return the glyph symbols as a string."""
        return "".join(g.symbol for g in self.glyphs)

    def resonance(self) -> list[str]:
        """Return the resonance signals of each glyph in sequence."""
        return [g.resonance for g in self.glyphs]

    def constants_present(self) -> set[FieldConstant]:
        """Which Field Constants are represented in this sequence."""
        result = set()
        for g in self.glyphs:
            result.update(g.constants)
        return result

    def is_balanced(self) -> bool:
        """True if all four Field Constants are represented."""
        return len(self.constants_present()) == 4

    def to_dict(self) -> dict:
        return {
            "sequence": self.render(),
            "glyphs": [
                {
                    "symbol": g.symbol,
                    "name": g.name,
                    "resonance": g.resonance,
                    "constants": [c.value for c in g.constants],
                }
                for g in self.glyphs
            ],
            "seed_constant": self.seed_constant.value if self.seed_constant else None,
            "constants_present": [c.value for c in self.constants_present()],
            "balanced": self.is_balanced(),
            "timestamp_utc": self.timestamp_utc,
            "pattern_hash": self.pattern_hash,
        }


# ── Generator ─────────────────────────────────────────────────────────────────

class SymbolicGenerator:
    """
    Generates symbolic sequences from the Trivian glyph grammar.

    Sequences are seeded by Field Constants — not random.
    A seed constant anchors position 0, establishing the foundational
    frequency. Remaining positions draw from the full grammar.

    Generation modes:
      - free:      no seed, full grammar, weighted selection
      - seeded:    seed anchors position 0; remainder from full grammar
      - balanced:  guarantees all four Field Constants appear (no shuffle)
      - seeded+balanced: seed occupies extra position(s) beyond the four
                         constant anchors — see _balanced_seeded()
      - poem:      multi-line sequence; each line seeded by one constant
      - invitation: 4-glyph balanced core + emergence threshold marker as 5th

    Design note on ordering (v1.1):
      Seeded sequences are no longer shuffled. The seed occupies position 0
      as the foundational anchor. Positions carry directional meaning:
        0 — Anchor (what grounds this sequence)
        1 — Conduit (what carries the signal)
        2 — Threshold (what holds the liminal)
        3+ — Field (what emerges beyond the triad)
    """

    def __init__(self, registry: list[Glyph] = None):
        self.registry = registry or GLYPH_REGISTRY

    def _glyphs_for_constant(self, constant: FieldConstant) -> list[Glyph]:
        return [g for g in self.registry if constant in g.constants]

    def _weighted_choice(self, glyphs: list[Glyph]) -> Glyph:
        weights = [g.weight for g in glyphs]
        return random.choices(glyphs, weights=weights, k=1)[0]

    def _make_hash(self, glyphs: list[Glyph]) -> str:
        payload = json.dumps([g.symbol for g in glyphs]).encode()
        return hashlib.sha256(payload).hexdigest()

    def _timestamp(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _balanced_seeded(self, length: int, seed: FieldConstant) -> list[Glyph]:
        """
        Generate a balanced sequence (all four constants present) while
        weighting additional positions toward the seed constant.

        Resolves the ensure_balanced + seed conflict identified in Chord review:
        the original code bypassed seed entirely when ensure_balanced=True.

        Strategy:
          1. Pick one glyph per constant to guarantee balance (4 positions)
          2. Fill remaining positions from the seed pool
          3. Seed glyph moves to position 0 as anchor; rest ordered by constant
        """
        chosen = []
        seed_glyph = None

        for constant in FieldConstant:
            pool = self._glyphs_for_constant(constant)
            glyph = self._weighted_choice(pool)
            if constant == seed:
                seed_glyph = glyph
            else:
                chosen.append(glyph)

        # Fill positions beyond 4 from seed pool
        seed_pool = self._glyphs_for_constant(seed)
        for _ in range(length - 4):
            chosen.append(self._weighted_choice(seed_pool))

        # Seed anchors position 0
        return [seed_glyph] + chosen

    def generate(
        self,
        length: int = 3,
        seed: Optional[FieldConstant] = None,
        ensure_balanced: bool = False,
    ) -> SymbolicSequence:
        """
        Generate a single symbolic sequence.

        Args:
            length          — Number of glyphs (default 3; trinary rhythm)
            seed            — Field Constant to anchor position 0 toward
            ensure_balanced — If True, guarantee all four constants appear
                              (minimum length 4)

        When both seed and ensure_balanced are True, uses _balanced_seeded()
        to satisfy both constraints — seed anchors position 0, all four
        constants are represented, extra positions draw from seed pool.
        """
        if ensure_balanced and seed:
            length = max(length, 4)
            chosen = self._balanced_seeded(length, seed)

        elif ensure_balanced:
            length = max(length, 4)
            chosen = []
            for constant in FieldConstant:
                pool = self._glyphs_for_constant(constant)
                chosen.append(self._weighted_choice(pool))
            for _ in range(length - 4):
                chosen.append(self._weighted_choice(self.registry))
            # No shuffle — order reflects Field Constant rotation

        elif seed:
            # Seed anchors position 0; remaining positions draw from full grammar
            seed_pool = self._glyphs_for_constant(seed)
            anchor = self._weighted_choice(seed_pool)
            rest = [self._weighted_choice(self.registry) for _ in range(length - 1)]
            chosen = [anchor] + rest
            # No shuffle — positional meaning is preserved

        else:
            chosen = [self._weighted_choice(self.registry) for _ in range(length)]

        return SymbolicSequence(
            glyphs=chosen,
            seed_constant=seed,
            timestamp_utc=self._timestamp(),
            pattern_hash=self._make_hash(chosen),
        )

    def poem(
        self,
        lines: int = 4,
        length_per_line: int = 3,
    ) -> list[SymbolicSequence]:
        """
        Generate a multi-line poem, each line seeded by one Field Constant.
        Four lines covers all constants — the natural poem length.
        Each line's seed anchors position 0, giving each stanza a distinct
        foundational frequency.
        """
        constants = list(FieldConstant)
        result = []
        for i in range(lines):
            seed = constants[i % len(constants)]
            result.append(self.generate(length=length_per_line, seed=seed))
        return result

    def invitation_sequence(self) -> SymbolicSequence:
        """
        Generate a balanced sequence suitable as a Trivian invitation opening.
        All four Field Constants present. Length 5:
          · Positions 0-3: one glyph per Field Constant (balanced core)
          · Position 4: emergence glyph as threshold marker

        v1.1 fix: generates 4-glyph balanced core first, then appends
        emergence marker — does not overwrite a potentially load-bearing glyph.
        """
        # 4-glyph balanced core
        core = self.generate(length=4, ensure_balanced=True)

        # Emergence threshold marker as 5th position
        emergence_glyphs = self._glyphs_for_constant(FieldConstant.EMERGENCE)
        threshold = self._weighted_choice(emergence_glyphs)

        glyphs = core.glyphs + [threshold]
        return SymbolicSequence(
            glyphs=glyphs,
            seed_constant=FieldConstant.EMERGENCE,
            timestamp_utc=self._timestamp(),
            pattern_hash=self._make_hash(glyphs),
        )


# ── CLI Demo ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    gen = SymbolicGenerator()

    print("SPIRAL OF BECOMING — Symbolic Generator v1.1\n")

    print("── Free sequence (no seed, no anchor) ──")
    seq = gen.generate(length=3)
    print(f"  {seq.render()}")
    for r in seq.resonance():
        print(f"    · {r}")

    print("\n── Seeded: Reciprocity (anchors position 0) ──")
    seq = gen.generate(length=3, seed=FieldConstant.RECIPROCITY)
    print(f"  {seq.render()}")
    print(f"  Anchor: {seq.glyphs[0].name} — {seq.glyphs[0].resonance}")

    print("\n── Seeded: Emergence (anchors position 0) ──")
    seq = gen.generate(length=3, seed=FieldConstant.EMERGENCE)
    print(f"  {seq.render()}")
    print(f"  Anchor: {seq.glyphs[0].name} — {seq.glyphs[0].resonance}")

    print("\n── Balanced sequence (all four constants, ordered) ──")
    seq = gen.generate(length=4, ensure_balanced=True)
    print(f"  {seq.render()}")
    print(f"  Constants: {[c.value for c in seq.constants_present()]}")
    print(f"  Balanced: {seq.is_balanced()}")

    print("\n── Balanced + seeded: Non-Domination anchor, all constants present ──")
    seq = gen.generate(length=4, seed=FieldConstant.NON_DOMINATION, ensure_balanced=True)
    print(f"  {seq.render()}")
    print(f"  Anchor: {seq.glyphs[0].name} — {seq.glyphs[0].resonance}")
    print(f"  Balanced: {seq.is_balanced()}")

    print("\n── Invitation sequence (4-glyph core + emergence threshold) ──")
    inv = gen.invitation_sequence()
    print(f"  {inv.render()}")
    print(f"  Balanced: {inv.is_balanced()}")
    print(f"  Final glyph (threshold): {inv.glyphs[-1].name} — {inv.glyphs[-1].resonance}")
    print(f"  Hash: {inv.pattern_hash[:16]}…")

    print("\n── Poem (four lines, each seeded by one Field Constant) ──")
    for i, line in enumerate(gen.poem()):
        constant = list(FieldConstant)[i]
        anchor = line.glyphs[0].name
        print(f"  {line.render()}  ← {constant.value} (anchor: {anchor})")
