# Epistemic_Qual_Eval

Development repo for building a system that can evaluate the epistemic quality of LLM's answers to difficult questions.

The current step is a small, human-reviewed judge of written reasons in an existing Yogācāra–predictive-processing dataset. The judge is a draft, not a validated evaluator. The immediate pre-sprint goal is a working judge followed by a useful prompt generator. Automated learning and broader domains can follow once those pieces work.

## Question-only interpreter prototype

The current first step is to interpret the question before evaluating responses.
See [running the interpreter](docs/running-the-interpreter.md) and its
[exact instructions](docs/interpreter-prompt-review.md). The initial input and
offline tests are included. Live execution is explicit and uses your local API key.
The interpreter is not yet connected to the response judge below.

## Start here

1. Review the first six cases in the local round 01 packet (see [review setup](review/round_01/README.md)).
2. Enter notes in the local `review/round_01/review_cases.csv`, or discuss cases by their neutral IDs.
3. Use the draft script to prepare prompts, then refine the rubric with reviewed feedback.

Python 3.10+ is required. No third-party packages are needed. From the repository root:

```sh
python src/epistemic_judge.py --input review/round_01/review_cases.csv --output-dir runs/round_01/preview_01
```

This prepares six prompts and makes **no API calls**. Use a new output directory for each run; `--limit 0` selects all rows in the input. Live calls require an explicit `--execute`, a model ID, and a provider API key. See [running the judge](docs/running-the-judge.md).

Run local checks without API access:

```sh
python -m unittest discover -s tests -v
```

## Contributing (humans and AI agents)

Shared rules for Claude Code, Codex, and people are in [AGENTS.md](AGENTS.md). Before each commit, install the dev tools once with `python -m pip install -e '.[dev]'`, then run `scripts/check.sh` (Ruff lint, Ruff format, and tests). CI runs the same script.

## Where things go

| Path | Purpose |
| --- | --- |
| `src/` | Current executable code; Git records earlier versions. |
| `data/` | Stable, judge-facing development and reserved inputs with neutral IDs. |
| `review/round_01/` | This iteration's review packet and human annotations. |
| `docs/` | Current methodology, development sequence, and usage instructions. |
| `tests/` | Small checks for the judge's input and output handling. |
| `runs/` | Locally generated prompts, rubrics, manifests, and results; ignored by Git. |
| `private/` | Optional local location for original data and lookup files; ignored by Git. |

The data CSVs and review packet must be copied into place from the previously prepared files before the example command can run. Only the folders needed now are committed. The last two appear locally when used. Do not give private lookup files or original coded data to the judge. API keys, `.env` variants, raw data, and local outputs are ignored.

## Iterations and later stages

Keep code in `src/` rather than copying it into `v1`, `v2`, and `v3` folders. Make a Git commit when a version is worth keeping. Start `review/round_02/` when a new review round begins; preserve the earlier packet and notes. Give every run a distinct output folder and record the Git commit when comparing results. The script also records its own hash and the exact rubric used.

The reserved file is for a later frozen-version check, not prompt tuning. Research CSVs and review examples are local-only until their publication is approved. The reserved set uses related accounts and is not proof of new-domain generalization. See [data notes](data/README.md).

Add a prompt-generator module when that stage begins. Add a learning module only when needed. The [development plan](docs/development-plan.md) separates critical work from exploratory branches and states advancement criteria.

Existing repository license: [LICENSE](LICENSE).

