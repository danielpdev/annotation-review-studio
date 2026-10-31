# Demo walkthrough

## Start

```bash
make setup
make demo
make test
make eval
```

## What to show

Two distinct annotators label an example. An independent reviewer resolves the label with a reason. Export includes only adjudicated examples; later review decisions append to history.

## Failure case to discuss

Independent reviewer enforcement, two-annotation prerequisite, immutable annotation labels, disagreement detection and revised adjudication history.

## Evidence

Open the JSON evaluation report alongside the implementation. Distinguish synthetic fixture outputs, synthetic trace timing, actual elapsed evaluation time, and local model inference. Do not present a tiny test set as a production benchmark.

## Closing tradeoff

Demo identities are text fields, not authenticated accounts. This is a tool for labeling work, not a claim of native Spanish or medical annotation expertise. The UI is not a blind annotation study interface.

The repository's `docs/demo.webm` or `docs/demo.mp4`, when present, records the demonstration. A terminal replay is also available for focused projects as `docs/demo.cast`.
