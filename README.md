# TRACE SIEVE / MACHINE LOG TS-01

Feed the exceptions. Keep the outliers.

The operator freezes a rulebook, declared trigger and effect codebooks, a minimum support threshold, a separate reviewer, and two to eight independently hosted traces. GenLayer validators fetch every source and normalize every trace into only those declared codes. The complete normalized vector and all response-body digests must be reproduced by validators.

## Sieve law

Contract code counts trigger support. Codes meeting the frozen threshold become common triggers. A trace sharing none of them remains an explicit outlier. The deterministic result is `NARROW`, `SPLIT`, or `INSUFFICIENT`; the model cannot select the patch mode. Only the operator may accept a supported result.

Lifecycle: `COLLECTING -> FROZEN -> SIEVED -> ACCEPTED`. A frozen batch can expire permissionlessly; an open or insufficient batch can be retired.

## Inspection run

```text
python -m pytest -q
genvm-lint lint contracts/contract.py
```

The bundled traces and demo wallets are operator-controlled fixtures. They demonstrate the sieve, not independent production telemetry.
