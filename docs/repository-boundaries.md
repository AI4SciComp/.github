# Repository boundaries

| Repository | Plane | Owns | Must not become |
| --- | --- | --- | --- |
| `.github` | engineering | Organization profile, community policy, static repository map. | Runtime registry or scientific source. |
| `asc-os` | research | Model-agnostic state, contexts, covers, overlaps, evidence, decisions, lifecycle, deterministic bundles, CLI, local stdio MCP. | Numerical solver, provider client, unrestricted executor, or domain model library. |
| `asc-devtools` | engineering | Dependency-free Go CLI for conservative repository operations and repository-owned wrappers. | Agent runtime, research schema host, or static-map client. |
| `asc-cmake` | engineering | Reusable CMake build policy. | Python research runtime. |
| `asc-cpp` | scientific computing | Independent C++20 foundation and future optional task-specific native-provider route. | Mandatory parent of ASC XDE/ASC NO, downstream domain package, or research-runtime client. |
| `asc-py` | scientific computing | Domain-neutral Python arrays, backends, conversion, randomness, configuration, logging, errors, data, and safe persistence. | Equation solver, neural-operator package, or research-runtime client. |
| `asc-no` | scientific computing, incubating | Private incubation of neural-operator models, training, evaluation, inference, safe checkpoints, and benchmarks on released public `asc-py`. | PDE solver, ASC XDE runtime client, C++ wrapper, or `asc-os` runtime client. |
| `asc-xde` | scientific computing, incubating | Python equations, discretizations, solvers, diagnostics, simulation, and versioned PDE dataset artifacts on released public `asc-py`. | Neural-operator package, C++ wrapper, or generic research orchestrator. |
| `asc-kinetic` | scientific computing, incubating | Future kinetic methods and models. | Generic research orchestrator. |
| `asc-lean` | scientific computing, incubating | Future formal definitions and proofs. | Generic research orchestrator. |

The [repository map](repository-map.yaml) is descriptive governance data. It
must not be treated as a service-discovery dependency by `asc-devtools` or any
runtime package.

ASC XDE and ASC NO are sibling libraries. ASC XDE produces versioned artifacts
that ASC NO consumes; neither imports or depends on the other's runtime or
source tree. Neither depends on ASC C++ or ASC OS in v0.1. ASC OS remains an
external development sidecar.
