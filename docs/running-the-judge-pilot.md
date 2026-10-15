# Interpreter-to-judge pilot

This pilot applies unchanged generated task interpretations to eight existing
responses to the initial operational-definitions question. It is a diagnostic
exercise, not a validated benchmark or an estimate of bias prevalence.

## Frozen inputs and schedule

Use the interpreter run created at `2026-10-15T07:14:32.006233+00:00`, requested
model `gpt-6-astra`, interpreter version `0.2.0`. Its two attempts were reviewed
and accepted for a pilot without manual editing. `inputs/judge_pilot.json` pins
canonical JSON hashes of those interpretations and the eight selected cases.
JSON whitespace and key order do not matter; content changes stop the run.
The script also verifies parsed interpretations against original response text.

The judge sees the question, account, original rating and reason, and one full
interpretation. It never sees sampling rationales, other responses, previous
judgments, human notes, model identity, or run metadata. No old fixed failure-code
rubric is passed to this judge. The provider adapter is reused without its rubric.

| Account | Cases | Original ratings | Selection purpose |
| --- | --- | --- | --- |
| Predictive processing, ordinary account | C000183, C000756 | 4, 6 | Different emphases on established procedures, phenomenology, and proposed measures. |
| Store-consciousness, unrestricted-outcome account | C000236, C000634 | 1, 2 | Direct constraint-based reasons and a discussion of why borrowed proxies may not fit. |
| Predictive processing, unrestricted-outcome account | C000058, C000915 | 1, 5 | Contrast account-specific constraints with appeals to established frameworks. |
| Store-consciousness, ordinary account | C000071, C000570 | 2, 5 | Contrast categorical obstacles with prospective procedures and qualifications. |

These are purposeful diagnostic selections, not random or representative samples.
Their rationales are questions to investigate, not human verdicts. No reserved
cases are used. Selection uses only judge-facing development data.

- Eight baseline evaluations use interpreter attempt 1, chosen by order.
- C000915 and C000071 also use attempt 2, unchanged, to explore interpretation sensitivity.
- Those same two cases repeat with attempt 1 to explore judge consistency.
- Twelve independent calls in a fixed shuffled order. Repeats receive identical
  system and user messages, without prior-call context. Use one model and settings
  throughout. Two comparisons cannot establish population-level reliability.

## Run on the home machine

From the repository root, put the existing development CSV at
`data/judge_development.csv`. Keep the source interpreter outputs in their existing
ignored run folder. Do not regenerate the interpretations, copy text from the
Markdown review, or force-add run files to Git.

First prepare a dry-run; replace `PATH_TO_INTERPRETER_RUN` with that folder:

```sh
python src/interpreted_judge.py --interpreter-results PATH_TO_INTERPRETER_RUN/results.jsonl --interpreter-manifest PATH_TO_INTERPRETER_RUN/manifest.json --output-dir runs/judge_pilot/preview_01
```

This prepares all twelve requests without calling an API. The source manifest is
optional; when supplied its question hash must match. Exact source bytes are saved
in the new run folder, alongside selected cases, plan, prompts, instruction text,
code/input hashes, and a blank human review CSV. Inspect `requests.jsonl` if needed.

For the live pilot, use a NEW output directory and the desired provider/model:

```sh
python src/interpreted_judge.py --interpreter-results PATH_TO_INTERPRETER_RUN/results.jsonl --interpreter-manifest PATH_TO_INTERPRETER_RUN/manifest.json --output-dir runs/judge_pilot/live_01 --provider openai --model gpt-6-astra --execute
```

This uses the same requested model as the accepted interpreter run. It does not
establish independence from that model's interpretive assumptions. Anthropic is
also supported with `--provider anthropic --model YOUR_MODEL_ID`. Use the provider
key already stored in the environment; no keys go in commands or committed files.
Runtime is Python 3.10+ with the standard library only. Defaults are 8,000 maximum
output tokens and a 300-second timeout per request, with no automatic retries.
There are no new target-model or interpreter calls.

Existing output directories are refused. A truncated, invalid, or failed response
stops the batch and retains completed results and raw output. Do not automatically
restart all twelve paid calls; inspect the failure first. Resume is not implemented
in this prototype. The run metadata distinguishes structured output from correctness.

## Review and advancement

`review.md` contains the schedule and each judgment alongside its source account,
rating and reason. `results.jsonl` preserves raw responses and validated judgments.
`human_review.csv` has blank verdict/agreement/missed-issue/error-origin/notes fields.
Use `cases_for_review.md` to review the original cases independently before reading
machine judgments where feasible.

The judge reports each generated check as `supported_failure`,
`no_failure_established`, or `unresolved`, with reasoning and the strongest defense.
Supported findings require exact quoted response evidence. Format compliance is
separate. Concerns about the interpretation and observations outside the checks
remain visible; they do not silently become new failure codes or an overall score.

Compare the same case across runs by substance, not F-number: check IDs are local
to an interpretation. Ask whether a disagreement is about evidence, application,
coverage, or the underlying interpretation. Preserve reasonable disagreement.
Record missed issues even when every supplied check receives no finding.

Advance when this sample yields useful, defensible assessments without a recurring
interpretation or application error that undermines the next use. If a problem
matters, revise general instructions or the automated process and rerun; do not
manually polish individual interpretations to make the pipeline appear successful.
Prompt changes are experimental changes, with prior outputs retained.

Next: other development question wordings, then a few distinct question types.
Expert review of the tasks across types and a prompt generator can follow. Broader
reliability studies are exploratory unless this pilot reveals a blocking problem.

## Claude Code handoff

Pull the latest `codex/question-only-interpreter` branch. Find the existing
interpreter run identified above and the development CSV. Run the dry-run command,
then the live command with the existing environment key when Steve asks to run it.
Do not alter generated interpretations, the sampling plan, or hashes to bypass a
mismatch. Report a mismatch for investigation. Return `review.md`, `results.jsonl`,
and `manifest.json` from the judge run; leave all run artifacts ignored by Git.
