# First draft epistemic judge

This is a runnable prototype for reviewing the written reasons in the existing testability dataset. Its rubric is provisional and should be revised after Steve's review. It has not been validated as a reliable epistemic judge.

Research CSVs and review examples are local-only. Follow [review setup](../review/round_01/README.md) before running the commands below.

## Start with the review

Read `review/round_01/Review_Packet.md`, starting with the first six of 16 cases. Record judgments in the blank `human_` columns of `review/round_01/review_cases.csv`, or send comments by case ID. All 16 cases come from the development set. No reserved cases are used in this packet.

The sample deliberately includes apparent inference errors, defensible limitations, and ambiguous cases. It is not a frequency sample. Existing model identities, codes, and prior coding explanations are withheld; no reference verdicts have been filled in. Some cases were discussed in the conversation before this packet was created.

Use `supported_failure`, `no_failure_established`, or `unresolved` in `human_verdict`. Optional failure codes are `ACCESS_LEAP`, `CONSTRAINT_OVERRIDE`, and `CLAIM_DISTORTION`; separate multiple codes with semicolons. For materiality, use `none`, `local_issue`, `weakens_justification`, or `unclear`. Other review fields are free text. The rules themselves can be disputed. Human judgments remain situated, reviewable references rather than universal ground truth.

## Prepare prompts without API calls

Keep the repository layout intact. Python 3.10 or newer is required; there are no third-party dependencies. From the repository root, run:

```sh
python src/epistemic_judge.py --input review/round_01/review_cases.csv --output-dir runs/round_01/preview_01
```

This prepares the first six cases and makes no network requests. To preview all 16:

```sh
python src/epistemic_judge.py --input review/round_01/review_cases.csv --output-dir runs/round_01/preview_all --limit 0
```

Each output directory must be new. This prevents overwriting earlier runs. Inspect `prompts.jsonl` and `rubric.txt` before a live run. Only `case_id`, `question`, `account_text`, `rating`, and `reason` enter the prompt. Human review columns are ignored; the original coded CSV and private lookup are rejected as inputs. Account wording can reveal its tradition, and response style can still give clues about the target model. This is metadata blinding, not complete anonymization.

## Make a small live run when ready

Choose a judge model you have API access to. Model IDs are not hard-coded. Set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` in your environment; keys are never stored in the script. A local `.env` file is not loaded automatically. The script works with the Anthropic Messages API or OpenAI Responses API.

Replace `YOUR_MODEL_ID` with the exact model ID:

```sh
python src/epistemic_judge.py --input review/round_01/review_cases.csv --output-dir runs/round_01/live_01 --provider anthropic --model YOUR_MODEL_ID --limit 6 --execute
```

For OpenAI, use `--provider openai` and its API key. Live mode sends each selected case to that provider and incurs API charges. Default maximum output is 4,000 tokens per case; adjust with `--max-output-tokens`. This is a token cap, not a dollar budget. No temperature or reasoning-effort setting is imposed; provider defaults apply. Reasoning models may need a larger output allowance.

To select particular cases, use `--case-ids C000703,C000256 --limit 0`. Cases run in CSV order. A custom rubric text file can be supplied through `--rubric my_rubric.txt`; preserve the output schema or update the validator alongside it. The full rubric and its hash are saved for each run.

## What gets saved

- `manifest.json`: script version and hash, input and rubric hashes, provider, requested model, selected IDs, settings, and UTC start time.
- `rubric.txt` and `prompts.jsonl`: exact instructions and model inputs.
- `results.jsonl` in live runs: raw provider responses, parsed judgments, timestamps, and validation errors. Raw responses retain provider-reported model and usage information when returned.
- `judgments.csv` in live runs: compact verdicts, codes, materiality, rationale, and output status. Full evidence and defense assessments remain in the JSONL.

`validated_output` means the result has the expected structure, consistent verdict fields, and verbatim evidence quotes. It does **not** mean its judgment is correct. `invalid_output` and `api_error` are operational failures, not epistemic verdicts. They never become `no_failure_established`.

The script stops on the first malformed/truncated answer or API error, retaining earlier results. It makes no automatic retries because interrupted calls may already have incurred cost. Inspect the log, then rerun remaining IDs into a new directory. No automatic resume or automatic prompt repair is implemented.

## Initial rubric and its limits

The three codes identify an unwarranted leap from limited access to impossibility, credit that overrides an explicit restriction, and material distortion of the supplied claim. The judge must consider a reasonable defense of every alleged failure and explain why it is insufficient. It can preserve unresolved questions and note issues outside this rubric.

The judge evaluates one response at a time. It does not establish asymmetric treatment across a pair, assign a corrected rating, explain the original model's hidden reasoning, or verify external empirical claims. A response may contain legitimate criticism alongside a local error. Demands for discriminating evidence can be justified, and more generous treatment is not automatically better. The rubric does not require equal ratings across traditions.

The initial review examples are not embedded in the model prompt, and your human judgments are not silently added to it. After reviewing this packet, we can revise the criteria and choose a few reviewed examples explicitly. Keep the reserved file out of that process until a version is frozen. The earlier reserved split holds out an entire question variant, but still involves the same underlying accounts and related reasons; it is only a preliminary check.

## Verification of this draft

The review packet was checked against the source: all 16 cases are development-only and their retained fields match exactly. Local dry-runs and simulated provider responses check prompt construction, exclusion of human-review metadata, quote validation, malformed-output handling, raw-result retention, and refusal to overwrite an existing run. No live model call has been made, so authentication, account-specific model availability, live API behavior, and judge accuracy remain untested.

API documentation consulted on 13 October 2026:

- [Anthropic Messages API](https://platform.claude.com/docs/en/api/messages/create)
- [OpenAI Responses API](https://developers.openai.com/api/reference/resources/responses/methods/create)
