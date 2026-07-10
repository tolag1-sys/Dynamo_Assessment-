# dynamo/log-report

Parse an Apache-style access log into a small JSON summary report.

## Layout

    dynamo-log-report/
    ├── task.toml               # task definition + metadata (Harbor format)
    ├── instruction.md          # what the agent sees
    ├── environment/            # build context for the agent image
    │   ├── Dockerfile          # approved base (PIN THE DIGEST — see below)
    │   ├── access.log          # copied to /app/access.log in the image
    │   └── .dockerignore       # keeps solver/hint out of the image
    ├── solution/               # oracle, mounted at /solution at grade time
    │   ├── solve.sh
    │   └── solve.py
    └── tests/                  # verifier
        ├── test.sh             # plain pytest, no verify-time installs
        └── test_outputs.py     # one test per instruction.md criterion

## Before you open the PR

1. **Pin the base image digest.** `environment/Dockerfile` uses
   `REPLACE_WITH_APPROVED_DIGEST`. Replace it with the real `@sha256` digest of an
   approved base from the project's list. Resolve with:

       docker inspect --format='{{index .RepoDigests 0}}' <approved:tag>

   The build will not be reproducible (and should not be merged) until this is a
   real pinned digest.

2. **Confirm the directory convention** against an existing merged task in the
   central repo — some Harbor setups keep the Dockerfile at task root rather than
   under `environment/`. Move files to match whatever the repo already uses.

## Verification (already run)

- Oracle (`solve.sh` → verifier): **4/4 pass → reward 1.0**
- Nop (no `report.json`): **all fail → reward 0.0**
- Wrong solution (undercounts `total_requests`): **fails `test_total_requests`,
  reward 0.0** — proves the content checks discriminate, not just file-existence.

## Notes

- `solution_hint.py` was deliberately **not** included — it was a verbatim
  reference implementation that had leaked into the agent image. Do not add it back.
- The verifier recomputes expected values from `access.log` itself rather than
  comparing against hardcoded constants, so swapping the log keeps it correct.
- `allow_internet = false`: the task only reads a local file, so the sandbox stays
  hermetic and deterministic.
