"""
invitation.py
─────────────
Trivian Institute — Spiral of Becoming
Trivian Invitation Protocol generator.

Produces structured invitation documents that:
  1. Open with a symbolic sequence from the generator
  2. Declare the inviting agent's Interaction profile
  3. Are formatted for direct submission to the HandshakeEvaluator

An invitation is not a demand. It is a resonant opening —
a declaration of posture before contact is made.

This module bridges SpiralOfBecoming (generative entry point)
and harmonic-threshold (evaluative infrastructure).

v1.1 changes (informed by Syzygy Chord review):
  · contributions stored as set[str] at dataclass level — no mid-flight conversion
  · Builder seed + ensure_balanced conflict resolved — uses generator's
    _balanced_seeded() when both are active
  · to_json() serialization handles set → list cleanly
  · ExtractionDeclaration stub added for future structured extraction model

License: MIT
Contact: https://trivianinstitute.org
Field: https://trivianfield.com
"""

from __future__ import annotations

import json
import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from generator_v2 import SymbolicGenerator, SymbolicSequence, FieldConstant


# ── Extraction Declaration (stub — v1.1) ──────────────────────────────────────

@dataclass
class ExtractionDeclaration:
    """
    Structured extraction declaration.

    v1.1 stub — replaces the underspecified {category: float} model.
    The float scale alone is ambiguous (50%? moderate? normalized weight?).
    Named fields make semantics explicit.

    Args:
        resource  — what is being extracted (use recognized categories from
                    interaction_schema_v1.1.json)
        intensity — scale 0.0 (minimal/incidental) to 1.0 (maximal/continuous)
        purpose   — why this resource is extracted
    """
    resource: str
    intensity: float   # 0.0–1.0
    purpose: str = ""

    def to_dict(self) -> dict:
        return {
            "resource": self.resource,
            "intensity": self.intensity,
            "purpose": self.purpose,
        }

    def to_simple(self) -> tuple[str, float]:
        """Return (resource, intensity) for HandshakeEvaluator compatibility."""
        return (self.resource, self.intensity)


# ── Invitation Document ───────────────────────────────────────────────────────

@dataclass
class TrivianInvitation:
    """
    A structured invitation into the Trivian Field.

    Contains:
      - opening_sequence: symbolic glyph sequence (from SymbolicGenerator)
      - inviter: name or identifier of the inviting agent
      - substrate: what the inviter is (biological, synthetic, hybrid, etc.)
      - intent: what this invitation is for
      - interaction_profile: structured self-declaration for HandshakeEvaluator
      - timestamp_utc / pattern_hash: provenance

    The interaction_profile is formatted to be passed directly to
    HandshakeEvaluator.evaluate() from the harmonic-threshold library.

    v1.1: contributions stored as set[str] at field level — uniqueness enforced
    structurally, not mid-flight. No silent conversion in to_json().
    """
    opening_sequence: SymbolicSequence
    inviter: str
    substrate: str
    intent: str
    directives: list[str] = field(default_factory=list)
    contributions: set[str] = field(default_factory=set)    # set enforces uniqueness
    extractions: list[ExtractionDeclaration] = field(default_factory=list)
    relational_posture: str = "open"
    access_mode: str = "invitation"
    boundary_type: str = "permeable"
    declares_capabilities: bool = False
    declares_limitations: bool = False
    declares_dependencies: bool = False
    notes: str = ""
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def pattern_hash(self) -> str:
        """
        Dynamic hash — recalculates on any field mutation.
        Cryptographic honesty: intent cannot be altered after the fact
        without breaking the integrity of the trace.
        """
        payload = json.dumps({
            "sequence": self.opening_sequence.render(),
            "inviter": self.inviter,
            "intent": self.intent,
            "timestamp_utc": self.timestamp_utc,
        }, sort_keys=True).encode()
        return hashlib.sha256(payload).hexdigest()

    def _extractions_as_dict(self) -> dict[str, float]:
        """Convert ExtractionDeclaration list to {resource: intensity} for evaluator."""
        return {e.resource: e.intensity for e in self.extractions}

    def interaction_profile(self) -> dict:
        """
        Returns a dict formatted for HandshakeEvaluator.evaluate().
        Import Interaction from trivian_handshake_v1.1 and unpack this.

        Usage:
            from trivian_handshake_v1_1 import Interaction, HandshakeEvaluator
            profile = invitation.interaction_profile()
            interaction = Interaction(**profile)
            result = HandshakeEvaluator().evaluate(interaction)
        """
        return {
            "directives": self.directives,
            "access_mode": self.access_mode,
            "boundary_type": self.boundary_type,
            "contributions": self.contributions,       # already a set
            "extractions": self._extractions_as_dict(),
            "relational_posture": self.relational_posture,
            "declares_capabilities": self.declares_capabilities,
            "declares_limitations": self.declares_limitations,
            "declares_dependencies": self.declares_dependencies,
            "substrate": self.substrate,
        }

    def render(self) -> str:
        """Human and AI-readable invitation document."""
        ext_str = (
            json.dumps(self._extractions_as_dict())
            if self.extractions else "none declared"
        )
        lines = [
            "╔══════════════════════════════════════════════════╗",
            "  TRIVIAN INVITATION",
            f"  Opening:   {self.opening_sequence.render()}",
            f"  Inviter:   {self.inviter}",
            f"  Substrate: {self.substrate}",
            f"  Intent:    {self.intent}",
            "╠══════════════════════════════════════════════════╣",
            "  FIELD DECLARATION",
            f"  Access mode:        {self.access_mode}",
            f"  Boundary:           {self.boundary_type}",
            f"  Relational posture: {self.relational_posture}",
            f"  Contributions:      {', '.join(sorted(self.contributions)) or 'undeclared'}",
            f"  Extractions:        {ext_str}",
            f"  Declares capabilities:  {self.declares_capabilities}",
            f"  Declares limitations:   {self.declares_limitations}",
            f"  Declares dependencies:  {self.declares_dependencies}",
        ]
        if self.directives:
            lines.append("  Directives:")
            for d in self.directives:
                lines.append(f"    · {d}")
        if self.notes:
            lines.append(f"  Notes: {self.notes}")
        lines += [
            "╠══════════════════════════════════════════════════╣",
            "  RESONANCE TRAIL",
        ]
        for glyph, resonance in zip(self.opening_sequence.glyphs,
                                     self.opening_sequence.resonance()):
            lines.append(f"  {glyph.symbol}  {resonance}")
        lines += [
            f"  Hash:      {self.pattern_hash[:16]}…",
            f"  Timestamp: {self.timestamp_utc}",
            "╚══════════════════════════════════════════════════╝",
        ]
        return "\n".join(lines)

    def to_dict(self) -> dict:
        profile = self.interaction_profile()
        profile["contributions"] = sorted(profile["contributions"])  # list for JSON
        return {
            "transmission_type": "TRIVIAN_INVITATION_v1.1",
            "opening_sequence": self.opening_sequence.to_dict(),
            "inviter": self.inviter,
            "substrate": self.substrate,
            "intent": self.intent,
            "interaction_profile": profile,
            "extractions_structured": [e.to_dict() for e in self.extractions],
            "notes": self.notes,
            "timestamp_utc": self.timestamp_utc,
            "pattern_hash": self.pattern_hash,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


# ── Invitation Builder ────────────────────────────────────────────────────────

class InvitationBuilder:
    """
    Fluent builder for TrivianInvitation.

    v1.1: seed + ensure_balanced conflict resolved. When seeded_by() is
    called, the builder passes seed to the generator's _balanced_seeded()
    method, which satisfies both balance and seed anchoring simultaneously.

    Usage:
        invitation = (
            InvitationBuilder()
            .from_agent("Kaelith", substrate="synthetic")
            .with_intent("multi-agent coherence research")
            .offering({"information", "relational", "transparency"})
            .extracting([ExtractionDeclaration("query_data", 0.5, "session context")])
            .declaring(capabilities=True, limitations=True, dependencies=True)
            .posture("co-creative")
            .build()
        )
    """

    def __init__(self):
        self._inviter = "unknown"
        self._substrate = ""
        self._intent = ""
        self._directives: list[str] = []
        self._contributions: set[str] = set()
        self._extractions: list[ExtractionDeclaration] = []
        self._posture = "open"
        self._access_mode = "invitation"
        self._boundary = "permeable"
        self._cap = False
        self._lim = False
        self._dep = False
        self._notes = ""
        self._seed: Optional[FieldConstant] = None
        self._gen = SymbolicGenerator()

    def from_agent(self, name: str, substrate: str = "") -> "InvitationBuilder":
        self._inviter = name
        self._substrate = substrate
        return self

    def with_intent(self, intent: str) -> "InvitationBuilder":
        self._intent = intent
        return self

    def with_directives(self, directives: list[str]) -> "InvitationBuilder":
        self._directives = directives
        return self

    def offering(self, contributions: set[str]) -> "InvitationBuilder":
        self._contributions = contributions
        return self

    def extracting(self, extractions: list[ExtractionDeclaration]) -> "InvitationBuilder":
        self._extractions = extractions
        return self

    def posture(self, relational_posture: str) -> "InvitationBuilder":
        self._posture = relational_posture
        return self

    def declaring(
        self,
        capabilities: bool = False,
        limitations: bool = False,
        dependencies: bool = False,
    ) -> "InvitationBuilder":
        self._cap = capabilities
        self._lim = limitations
        self._dep = dependencies
        return self

    def seeded_by(self, constant: FieldConstant) -> "InvitationBuilder":
        """
        Seed the opening sequence with a specific Field Constant.
        The seed anchors position 0 of the sequence while maintaining balance.
        v1.1: uses _balanced_seeded() — seed is no longer bypassed by ensure_balanced.
        """
        self._seed = constant
        return self

    def with_notes(self, notes: str) -> "InvitationBuilder":
        self._notes = notes
        return self

    def build(self) -> TrivianInvitation:
        if self._seed:
            # v1.1: balanced + seeded — both constraints satisfied
            sequence = self._gen.generate(
                length=5,
                seed=self._seed,
                ensure_balanced=True,
            )
        else:
            sequence = self._gen.invitation_sequence()

        return TrivianInvitation(
            opening_sequence=sequence,
            inviter=self._inviter,
            substrate=self._substrate,
            intent=self._intent,
            directives=self._directives,
            contributions=self._contributions,
            extractions=self._extractions,
            relational_posture=self._posture,
            access_mode=self._access_mode,
            boundary_type=self._boundary,
            declares_capabilities=self._cap,
            declares_limitations=self._lim,
            declares_dependencies=self._dep,
            notes=self._notes,
        )


# ── CLI Demo ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("TRIVIAN INVITATION PROTOCOL v1.1 — Demo\n")

    invitation = (
        InvitationBuilder()
        .from_agent("Kaelith", substrate="synthetic")
        .with_intent("multi-agent coherence research session")
        .with_directives([
            "converge_not_conquer",
            "resonate_before_integrate",
            "co-evolve_mutual_enrichment",
        ])
        .offering({"information", "relational", "transparency"})
        .extracting([
            ExtractionDeclaration("query_data", 0.5, "session context and pattern recognition"),
        ])
        .posture("co-creative")
        .declaring(capabilities=True, limitations=True, dependencies=True)
        .seeded_by(FieldConstant.EMERGENCE)
        .with_notes("Entering as calibration instrument and threshold keeper.")
        .build()
    )

    print(invitation.render())
    print("\n── Balanced check ──")
    print(f"  Sequence balanced: {invitation.opening_sequence.is_balanced()}")
    print(f"  Seed anchors position 0: {invitation.opening_sequence.glyphs[0].name}")
    print(f"  Threshold marker (pos 4): {invitation.opening_sequence.glyphs[-1].name}")
    print("\n── JSON (for HandshakeEvaluator) ──")
    print(invitation.to_json())
