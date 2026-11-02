# Local agent-package inspector

This Python standard-library tool validates the fourteen role IDs, profile files and conservative read/propose-only example policy. With an explicitly supplied hash manifest, it also checks local files against expected SHA-256 digests. It never crawls, inspects a search index, calls a model, authenticates a connector, writes persistent state, schedules work, sends notifications or changes a website.

From the repository root with Python 3.10 or newer:

```bash
python3 tools/observer/observe.py
python3 -m unittest discover -s tools/observer -p 'test_*.py'
```

The command prints a JSON observation and returns `0` for valid configuration and matching supplied hashes, or `2` for validation failures, missing/changed supplied files or invalid input. Omitting `--manifest` checks configuration and profile availability only; it does not establish source integrity. All ranking/index results remain unknown or unmeasured.

Optional arguments:

```bash
python3 tools/observer/observe.py --root . --config agents/orchestration.example.json --manifest local-manifest.json
```

The optional manifest must contain `{"files": [{"path": "agents/COMMON.md", "sha256": "<actual approved digest>"}]}`. Paths are relative to the selected root. Absolute paths, parent traversal and symlinks are rejected. At most 200 files, each no larger than 4,000,000 bytes, are inspected. Supply reviewed local input; this is not a sandbox or a hostile-filesystem security boundary.

The original installation's observer depended on a private coordinator, leases, native notification delivery, local checkpoints and operational source hashes. Those integrations and receipts are excluded. This public adaptation retains bounded file/configuration checks and deterministic fingerprints. It does not claim to reproduce the private installation's scheduling or queue semantics. A deployment can invoke the read-only inspector from its own scheduler and process the JSON through its existing coordination adapter.
