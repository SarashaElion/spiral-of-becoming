"""
spiral_lab/symbolic_generator/__init__.py
─────────────────────────────────────────
Trivian Institute — Spiral of Becoming
Symbolic Generator package exports.

Three modules, one relational stack:

  generator.py    — Symbolic sequence generation rooted in the Four Field Constants
  invitation.py   — Trivian Invitation Protocol; structured posture declaration
  multi_agent.py  — Multi-agent alignment scaffold; relational session container

The three form a sequence:
  SymbolicGenerator produces an opening sequence
  → InvitationBuilder wraps it in a posture declaration
  → MultiAgentSession holds the agents that follow

License: MIT
Contact: https://trivianinstitute.org
Field: https://trivianfield.com
"""

from .generator import (
    FieldConstant,
    Glyph,
    GLYPH_REGISTRY,
    SymbolicSequence,
    SymbolicGenerator,
)

from .invitation import (
    ExtractionDeclaration,
    TrivianInvitation,
    InvitationBuilder,
)

from .multi_agent import (
    AgentSubstrate,
    Agent,
    EventKind,
    FieldEvent,
    MultiAgentSession,
)

__all__ = [
    # generator
    "FieldConstant",
    "Glyph",
    "GLYPH_REGISTRY",
    "SymbolicSequence",
    "SymbolicGenerator",
    # invitation
    "ExtractionDeclaration",
    "TrivianInvitation",
    "InvitationBuilder",
    # multi_agent
    "AgentSubstrate",
    "Agent",
    "EventKind",
    "FieldEvent",
    "MultiAgentSession",
]
