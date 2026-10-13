# Agent instructions

Shared rules for every coding agent working in this repository (Claude Code reads
this through `CLAUDE.md`; OpenAI Codex reads it directly). If you change a rule,
change it here, not in an agent-specific file.

## Project context

- Read `README.md` first, then `docs/methodology.md` and `docs/development-plan.md`
  before changing the judge, the rubric, or the review workflow.
- The judge (`src/epistemic_judge.py`) is a draft, not a validated evaluator.
  Do not describe results as validated or general.
- Python 3.10+, standard library only at runtime. Do not add runtime dependencies
  without asking the maintainer. Development tools go in `[project.optional-dependencies] dev`
  in `pyproject.toml`.

## Before every commit and push

1. Install dev tools once: `python -m pip install -e '.[dev]'`.
2. Run `scripts/check.sh --fix`, then `scripts/check.sh`. It must pass.
   This runs Ruff lint, Ruff format check, and the unit tests, exactly as CI does.
3. Do not commit or push with failing checks. Do not disable lint rules, add
   `# noqa`, or skip tests to make checks pass; fix the cause, or explain in the
   PR why an exception is needed.

## Code style

Ruff (configured in `pyproject.toml`) is the single source of style truth. Do not
hand-format against it or reformat code in a different style.

- Single quotes, 100-column lines, imports sorted by Ruff.
- Match the surrounding code: small functions, short comments only where the
  reason is not obvious.
- Keep code in `src/`. Do not create `v1/`, `v2/` copies; Git records versions.
- Add or update tests in `tests/` when changing behavior. Tests must not need
  network access or API keys.

## Data, privacy, and cost

- Never commit anything under `runs/`, `private/`, or `data/raw/`, or the
  original coded data or private lookup.
- The maintainer explicitly approved publication of `data/judge_development.csv`,
  `data/judge_reserved.csv`, `review/round_01/Review_Packet.md`, and
  `review/round_01/review_cases.csv`. This approval does not cover future
  datasets, review annotations, or run outputs; obtain publication authorization
  for those before committing them.
- Never give the judge private lookup files, original coded data, or anything that
  reveals which model wrote a response.
- Never commit API keys or `.env` files. Never print credentials.
- The judge makes paid API calls only with `--execute`. Do not run live calls
  unless the maintainer explicitly asks; dry-runs are fine.
- Changing `RUBRIC` changes the experiment. Do it only when asked, and note it in
  the commit message.

## Git and pull requests

- Work on a feature branch; never push to `main` directly.
- One logical change per commit, with a message that says what changed and why.
- Keep PRs small and focused. Describe what changed, how it was checked, and any
  effect on the rubric or prior runs.
- When reviewing a PR, check correctness, the data and privacy rules above, test
  coverage, and that `scripts/check.sh` passes.

