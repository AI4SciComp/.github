# Trustworthy AI for scientific computing

AI4SciComp builds small, composable foundations for scientific software and a
traceable research process around them. AI can accelerate investigation, but
its output is not evidence by itself: claims must be reproducible, verified,
and linked to their sources and decisions.

## Three planes

- **Research:** [asc-os](https://github.com/AI4SciComp/asc-os) owns
  model-agnostic research state, bounded contexts, covers, overlaps, evidence,
  decisions, lifecycle records, deterministic restriction and gluing, a CLI,
  and local stdio MCP.
- **Scientific computing:**
  [asc-cpp](https://github.com/AI4SciComp/asc-cpp) and
  [asc-py](https://github.com/AI4SciComp/asc-py) are domain-neutral
  foundations. Private `asc-xde`, `asc-kinetic`, and `asc-lean` repositories
  are current incubation skeletons, not released implementations. `asc-no` is
  planned for future neural-operator models, training, evaluation, and
  benchmarks built on released `asc-py` APIs; it is not implemented.
- **Engineering:** [asc-cmake](https://github.com/AI4SciComp/asc-cmake) owns
  CMake build policy, while
  [asc-devtools](https://github.com/AI4SciComp/asc-devtools) remains a
  dependency-free Go developer CLI for conservative repository operations.

Dependencies point from specialized software to released public foundations.
Foundations never import their downstream users. Research integration is a
sidecar contract through files and commands, not a numerical runtime import.

## Research lifecycle

Work moves through **explore → cover/plan → execute → verify → glue →
project**. Each stage preserves explicit context, provenance, acceptance
criteria, and invalidation state. Generated bundles remain separate from
hand-authored repository instructions.

## Choose a repository

Put build policy in `asc-cmake`, conservative multi-repository developer
operations in `asc-devtools`, reusable domain-neutral numerical foundations in
`asc-cpp` or `asc-py`, and generic research-state behavior in `asc-os`. A
specialized scientific model belongs in its domain repository and must use
released public foundation APIs.

See the [repository map](../docs/repository-map.yaml), [boundary
guide](../docs/repository-boundaries.md), [contribution
guidance](../CONTRIBUTING.md), and [security policy](../SECURITY.md).
