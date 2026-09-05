# Status

- **Class:** experimental symbolic / relational reference implementation
- **Maturity:** research prototype
- **Validation:** not independently validated
- **Canonical TRIA runtime:** no
- **Machine entrypoint:** `spiral_lab.symbolic_generator`
- **Verification:** `python -m unittest discover -s tests -v`

The repository encodes Trivian symbolic grammar and relational concepts into Python objects and machine-readable records. Symbolic terms are not empirical claims by default. Treat them as authored conceptual primitives unless a behavior is explicitly implemented and tested.

Current technical goal: preserve the symbolic register while keeping generation, invitation, and multi-agent session behavior reproducible and inspectable.
