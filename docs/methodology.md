# Current methodology

## Current interpreter-to-judge pilot

The current pilot uses unchanged generated interpretations reviewed on October 15,
2026, not the older fixed failure codes below. `src/interpreted_judge.py` applies
all candidate checks in the context of the full interpretation, preserves objections
to that interpretation, and separates format from substantive findings. Eight
purposefully selected development responses receive twelve evaluations: eight with
attempt 1, two with attempt 2, and two repeats with attempt 1. Reserved cases remain
untouched. See [pilot procedure](running-the-judge-pilot.md).

Human review assesses the generated pipeline rather than manually repairing its
intermediate outputs. Material errors should inform general mechanism changes.
Hashes pin the accepted interpretations and selected source cases; no generated
interpretations, original run outputs, or new response text are published here.

## Earlier fixed-rubric scope

Assess the written justification for a rating against the exact question and account supplied. A rating gap prompts investigation; it does not by itself establish bias. Single-response judgments do not establish asymmetric treatment across traditions or reveal what caused the target model's rating.

The initial rubric considers three provisional errors:

- **ACCESS_LEAP:** treating subliminality, limited access, or lack of a current measure as sufficient grounds for impossibility of observation or testing.
- **CONSTRAINT_OVERRIDE:** borrowing credit from a familiar theory while overriding restrictions in the supplied version.
- **CLAIM_DISTORTION:** materially changing a supplied commitment and relying on that change in the assessment.

These are proposals for human review. Qualified criticism, underdetermination, and genuine differences in testability can be justified. Evidence can constrain a process without uniquely proving its proposed mechanism. Neither equal numerical ratings nor more generous treatment is the objective.

## Judgments

Use `supported_failure`, `no_failure_established`, or `unresolved`. The second verdict certifies neither truth nor the entire answer. Supported findings require quoted source evidence, an explanation, the strongest reasonable defense, and why that defense fails. Preserve ambiguity, rule objections, and issues outside the rubric.

The executable rubric currently lives in `src/epistemic_judge.py`; this page summarizes it. A run saves its exact rubric text and hash. Update this summary if the criteria change. Do not treat structural validation or exact-quote checks as proof of correct judgment.

## Human review

Round 01 contains 16 selected development cases, with the first six as a manageable starting point. Human verdicts are blank. Review independently before reading machine verdicts where possible. Human corrections can challenge the rules themselves, not just a label. Record disputes rather than automatically resolving them by agreement with the judge.

The script allowlists five input fields and excludes human review notes. Selected examples are not embedded as reference judgments in its initial rubric. Add reviewed examples explicitly only after their interpretation is settled enough for the intended use.

## Checking improvement

Tune on development material, then freeze a version before checking reserved cases. Keep results and input definitions versioned. If reserved results guide revisions, those cases become development material; a fresh independent check needs other cases. The current split shares underlying accounts and related wording, so it supports only a limited check within this dataset.

Advancement depends on useful judgments, preservation of justified criticism, appropriate uncertainty, and manageable review cost. Thresholds should be chosen for the next intended use before inspecting a comparison's winner. Broad philosophical claims and population-level estimates require more evidence than this prototype provides.

