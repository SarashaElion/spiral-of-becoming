"""Compatibility shim for the historical Spiral invitation module.

New code should import from ``spiral_lab.symbolic_generator``. This module
exists so the original absolute import in ``invitation.py`` remains runnable
without rewriting the preserved source file.
"""

from spiral_lab.symbolic_generator.generator import (
    FieldConstant,
    Glyph,
    GLYPH_REGISTRY,
    SymbolicSequence,
    SymbolicGenerator,
)

__all__ = [
    "FieldConstant",
    "Glyph",
    "GLYPH_REGISTRY",
    "SymbolicSequence",
    "SymbolicGenerator",
]
