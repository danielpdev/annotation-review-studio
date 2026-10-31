# Design record

## Decision

Two distinct annotators label an example. An independent reviewer resolves the label with a reason. Export includes only adjudicated examples; later review decisions append to history.

## Failure model

Independent reviewer enforcement, two-annotation prerequisite, immutable annotation labels, disagreement detection and revised adjudication history.

## Tradeoffs

Demo identities are text fields, not authenticated accounts. This is a tool for labeling work, not a claim of native Spanish or medical annotation expertise. The UI is not a blind annotation study interface.

## Next change to defend in review

Add authenticated roles, blinded task assignment, sampling and inter-annotator agreement statistics.

## Reproducibility

`uv.lock` pins Python dependencies; the web lockfile pins the React build where present. Model-backed evaluations use a separately installed local service. Dataset examples are synthetic and intentionally small. Reported timing is a local observation, not a throughput SLA. Run `make test` after changing state transitions and `make eval` after changing decisions. Keep inference quality separate from deterministic invariant checks.
