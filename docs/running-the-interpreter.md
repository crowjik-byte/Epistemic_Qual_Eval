# Question-only interpreter prototype

Status: an earlier version produced two live interpretations reviewed by the project
owner and assistant. Version 0.2.0 revises the instructions in response to that
review; its semantic effects have not yet been tested live.

## Boundary and purpose

The input JSON must contain exactly one field, question. Extra fields are rejected,
including accounts, ratings, reasons, and reference interpretations. The program
does not load the evaluation dataset, judge rubric, or review notes.
Its API adapter is imported from the existing src/epistemic_judge.py; only the
interpreter's instructions and question are sent.

This enforces the structured input boundary. It cannot detect an account or reference
answer manually pasted inside the question string. Inspect the input before execution.
The question may refer to content not supplied; the interpreter should identify what
the later evaluator needs, not invent it.

Review [the exact instructions](interpreter-prompt-review.md) first. There is no fixed
failure-code list or required question taxonomy. Proposed checks must link to
requirements, explain relevance, specify evidence needed, and preserve a legitimate
countercase. Explicit requirements require verbatim question excerpts; proposed
requirements must identify themselves as proposals.

The three decisions discussed in our review are human reference notes, not answers
embedded in this interpreter prompt:

- Both first-person and third-person procedures are eligible where justified;
  observation without measurement/manipulation remains ambiguous in this question.
- “Could” and “readily” admit defensible different weightings; lack of previous work
  alone does not establish inability.
- A procedure needs a defensible, constraining connection to its construct;
  full-theory predictions are a separate issue.

## Initial input

inputs/initial_question.json contains only the existing operational-definition
question, extracted exactly from the development pool. No account or response
data are included. The reserved group was not used to prepare this input.

## Preview with no API calls

From the repository root, with Python 3.10+:

    python src/task_interpreter.py --input inputs/initial_question.json --output-dir runs/interpreter/preview_01

Defaults: two independent requests (initial plus repeat), 5,000 output tokens per
request, 120-second timeout, Anthropic provider. A new output directory is required.
Repeated requests contain identical messages and no shared conversation history.
Provider sampling defaults apply; a repeat is not a reproducibility guarantee.

## Run on the home machine after review and GitHub publication

Keep src/task_interpreter.py beside src/epistemic_judge.py. Choose an exact model
ID from the provider account. Set its API key in the environment using the existing
local credential arrangement. Do not paste credentials into the chat or code.
The script does not automatically load a .env file.

    python src/task_interpreter.py --input inputs/initial_question.json --output-dir runs/interpreter/live_01 --provider anthropic --model YOUR_MODEL_ID --execute

For OpenAI, use --provider openai and an environment-provided OPENAI_API_KEY.
Anthropic uses ANTHROPIC_API_KEY. The run makes two billable calls, unless it stops
after the first error. No automatic retries. --repeats 1 requests only one call;
the maximum is three. Increase --max-output-tokens deliberately if the chosen model
requires more output/reasoning budget.

## Saved artifacts

- question.json, instructions.txt, requests.jsonl: exact input and messages.
- manifest.json: script/adapter/input/prompt hashes, version, model requested,
  provider, timestamp and settings.
- Live only: results.jsonl with raw provider replies, usage when provided,
  parsed outputs, structural validation errors and timestamps.
- Live only: review.md rendering both attempts for inspection.

structured_output means schema/quote/reference checks passed, not that the
interpretation is correct. Invalid JSON, incomplete replies, invalid references,
or API errors stop execution and preserve prior outputs. Correcting a failed run
requires a new output directory. Outputs are local; no automatic publication.

A reply wrapped in one outer Markdown code fence (```json ... ``` or ``` ... ```)
is unwrapped before parsing; results.jsonl records this as fence_stripped and keeps
the original response_text. Any other surrounding text is still invalid JSON.

## What to review after the first live run

Compare attempts on requested judgment, scope, requirements, ambiguities, relevant
support and candidate checks. Separate harmless wording differences from changes
in standards. Inspect whether proposed requirements are justified, whether the
missing account is handled appropriately, and whether each check is useful rather
than generic. A model may identify a defensible interpretation absent from our notes.

The pilot succeeds when the interpretation is useful and inspectable without a
recurring flaw that undermines downstream assessment. Two calls do not establish
reliability. Do not proceed by merely making output resemble a reference.

## Next stages

1. Get this question-only interpretation working.
2. Feed a frozen, reviewed interpretation to a later evaluator with account and
   response, initially on about eight varied development responses.
3. Cover other development questions with small samples, distinguishing paraphrase
   robustness from appropriate changes when the requested judgment changes.
4. Try a few different question types, then obtain professional feedback on the
   evaluation tasks and standards the interpreter derives.
5. Develop the prompt generator while awaiting that feedback.

Keep the reserved group intact. A formal specification and comprehensive taxonomy
are not prerequisites. The earlier specification's account-conditioned interpretation
pilot is superseded by this question-only design.

Step 2 is not wired up in this prototype. The existing judge still uses its own
rubric; running it now would not test application of this interpreter's output.

## Offline verification

Run scripts/check.sh. Interpreter tests cover strict input keys, verbatim evidence,
requirement references, identical independent requests, saving outputs, no network
calls in dry-run, overwrite protection, and stopping on invalid/truncated replies.
Provider calls are mocked in tests; successful mocks are not live evaluations.

## From discovery to a benchmark

The interpreter proposes criteria during development. A later benchmark release
should use reviewed, versioned task criteria and explicit scoring rules shared
across the models being compared. Discover recurring dimensions through these
pilots and expert feedback rather than requiring a complete taxonomy up front.
Generated reasons alone do not establish validity or score comparability.


## Revision 0.2.0: next paired run

Three general changes target issues identified in the first output review:

- Require evidence for consequential ambiguities and distinguish stronger readings
  from merely conceivable alternatives.
- Explain why categories, familiar methods, or source status are relevant rather
  than letting their labels settle adequacy.
- Keep claims about support proportional to the evidence and consistent with their
  stated limits; avoid treating reasonable judgment differences as contradictions.

No account-specific answers or operationalization examples were added to the
model instructions. The input and output schema are unchanged. The version 0.1.1
Markdown-fence parser fix is preserved.

On the home machine, pull the branch and use the same provider, model and settings
as the first successful run. Use a new output folder, for example:

    python src/task_interpreter.py --input inputs/initial_question.json --output-dir runs/interpreter/live_v020_01 --provider anthropic --model YOUR_MODEL_ID --repeats 2 --execute

Retain the previous run. Check both attempts for the three targeted issues and
for regressions: loss of genuine ambiguity, indiscriminate distrust of established
methods, excessive hedging, or less useful checks. Do not interpret a pair of runs
as a reliable accuracy estimate. Share review.md for discussion; keep raw outputs
and credentials out of Git.

## Version 0.3.0 follow-up

The interpreter now checks that candidate checks cover consequential failures of
their requirements, distinguishing consistency from adequate justification where
relevant. See [the follow-up procedure](judge-followup.md) for fresh generation and
the four-case application test. Earlier outputs must remain unchanged.
