# Follow-up: coverage of the task's requirements

## Change and rationale

Interpreter 0.3.0 adds a general coverage check: its candidate checks should cover
consequential failures of its requirements. For tasks requiring justification,
consistency between reasons and conclusion does not establish that the reasons
are supported and applicable. Evidence descriptions must not silently narrow a
check to a few illustrative patterns. Brevity, countercases, and uncertainty still
matter. No domain examples, desired verdicts, or fixed failure taxonomy were added.

Judge 0.2.0 explains that the interpretation was generated from the question only,
and the account and response arrive at application time. That expected transition
should not itself trigger an interpretation objection. Its substantive judging
instructions and schema are otherwise unchanged.

The initial pilot suggested a coverage problem: concerns relegated to observations
under interpretation 1 became findings under interpretation 2. This is a working
diagnosis, not a validated reference labeling. The two alternate-interpretation
cases were not repeated, so this pilot does not isolate all sources of variation.

## Fixed small follow-up

Generate two fresh interpretations once, retaining both in order without choosing
a preferred one. Use both unchanged on four existing development cases:

- C000915 and C000071: previously identified diagnostic concerns.
- C000756 and C000570: apparently defensible, qualified responses, one per ordinary
  account, to check for overcorrection. These are provisional human assessments,
  not labels passed to the judge.

This is eight judge calls plus two interpreter calls. The prior twelve-case-call
plan remains unchanged in `inputs/judge_pilot.json`; earlier run folders remain
intact. No reserved material is used. The generated follow-up plan stays local.

## Commands for Claude Code

Pull `codex/question-only-interpreter`. From the repository root, using the same
model and token/timeout settings as the previous interpreter run:

```sh
python src/task_interpreter.py --input inputs/initial_question.json --output-dir runs/interpreter/live_v030_01 --provider openai --model gpt-6-astra --repeats 2 --max-output-tokens 8000 --timeout 300 --execute
```

Freeze the two fresh outputs, after structural validation, without rewriting or
selecting them. This step makes no calls and does not certify semantic quality:

```sh
python src/prepare_judge_followup.py --interpreter-results runs/interpreter/live_v030_01/results.jsonl --interpreter-manifest runs/interpreter/live_v030_01/manifest.json --output runs/judge_followup/plan_01.json
```

The preparer requires the current interpreter prompt/version, initial question,
and two successful outputs in original order. It checks that the parsed objects
match their raw response text and pins their content hashes. Existing plans are
not overwritten. A mismatch is grounds to investigate, not change hashes by hand.

```sh
python src/interpreted_judge.py --plan runs/judge_followup/plan_01.json --interpreter-results runs/interpreter/live_v030_01/results.jsonl --interpreter-manifest runs/interpreter/live_v030_01/manifest.json --output-dir runs/judge_followup/preview_01
```

If preparation succeeds, run the same fixed eight evaluations:

```sh
python src/interpreted_judge.py --plan runs/judge_followup/plan_01.json --interpreter-results runs/interpreter/live_v030_01/results.jsonl --interpreter-manifest runs/interpreter/live_v030_01/manifest.json --output-dir runs/judge_followup/live_01 --provider openai --model gpt-6-astra --execute
```

Use existing environment keys. Preserve failed attempts and stop for diagnosis;
there are no automatic retries. If a directory already exists, use a fresh suffix
consistently rather than deleting prior work. Return both interpreter and judge
reviews, results, and manifests, clearly identified by stage.

## Review decision

Assess whether each interpretation covers the relevant requirements, whether the
judge evaluates the warrant of essential reasons, and whether qualified responses
remain defensible. More failure findings alone do not establish improvement.
Preserve disagreements and objections. Do not manually polish outputs or rerun
until a preferred verdict appears. If both interpretations support useful,
defensible application without a recurring material gap or overreach, move to
other development question wordings. Additional consistency checks become critical
only if instability prevents that next step.
