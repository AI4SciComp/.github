# Repository boundaries

| Repository | Plane | Owns | Must not become |
| --- | --- | --- | --- |
| `.github` | engineering | Organization profile, community policy, static repository map. | Runtime registry or scientific source. |
| `asc-os` | research | Model-agnostic state, contexts, covers, overlaps, evidence, decisions, lifecycle, deterministic bundles, CLI, local stdio MCP. | Numerical solver, provider client, unrestricted executor, or domain model library. |
| `asc-devtools` | engineering | Dependency-free Go CLI for conservative repository operations and repository-owned wrappers. | Agent runtime, research schema host, or static-map client. |
| `asc-cmake` | engineering | Reusable CMake build policy. | Python research runtime. |
| `asc-cpp` | scientific computing | Domain-neutral C++ foundation. | Downstream domain package or research-runtime client. |
| `asc-py` | scientific computing | Domain-neutral Python foundation and optional backend contracts. | Neural-operator package or research-runtime client. |
| `asc-no` | scientific computing, planned | Future neural-operator models, data, training, evaluation, and benchmarks on released `asc-py`. | Empty placeholder, foundation dependency, or `asc-os` runtime client. |
| `asc-xde` | scientific computing, incubating | Future equation/discretization/solver layer. | Generic research orchestrator. |
| `asc-kinetic` | scientific computing, incubating | Future kinetic methods and models. | Generic research orchestrator. |
| `asc-lean` | scientific computing, incubating | Future formal definitions and proofs. | Generic research orchestrator. |

The [repository map](repository-map.yaml) is descriptive governance data. It
must not be treated as a service-discovery dependency by `asc-devtools` or any
runtime package.
