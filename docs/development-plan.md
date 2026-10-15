# Development plan

## Working principle

An experiment may be scientifically valuable without being a prerequisite. Critical-path work establishes feasibility, interpretability, or sufficient reliability for the next intended step. Exploratory work becomes essential when its findings undermine that next step. Progress does not depend on every analogy or initial failure category surviving unchanged.

## Current critical path

1. Question-only interpreter: two generated outputs for the initial question have
   been reviewed and accepted unchanged for a prototype pilot.
2. Interpreter-to-judge pilot: eight existing development responses, twelve calls.
   Advancement requires useful, defensible assessments with no recurring flaw that
   makes the next use uninterpretable. See [procedure](running-the-judge-pilot.md).
3. Try other question wordings from the development data, using a small sample.
   Advance when the interpretation and application respond appropriately to wording
   changes without arbitrary changes in standards.
4. Try several distinct question types. Seek professional epistemological review
   of the evaluation tasks once concrete working examples exist across types.
5. While awaiting feedback, develop the prompt generator, first reviewing topic
   fit for the research sprint. A usable judge and generator remain the pre-sprint
   minimum. Learning scripts and broader coverage can follow during the sprint.

The two repeat and two alternate-interpretation evaluations are small diagnostics,
not reliability estimates. Broader replication is exploratory unless observed
instability undermines the next step. Keep reserved data for a later frozen check.
Human review may lead to general prompt/process changes; it must not silently
replace generated interpretations with individually improved versions.

## Current follow-up

The initial pilot executed successfully but revealed a possible check-coverage gap.
Interpreter 0.3.0 and judge 0.2.0 address general coverage and stage context.
The [four-case follow-up](judge-followup.md) uses two fresh interpretations unchanged
and eight judge calls. Advancement depends on defensible coverage and application,
not reproducing preferred labels.

## Optional sprint branches

- Automate proposals for rubric or example improvements, with human review and separate checks before adoption.
- Add failure modes or domains, validating the new use before claiming transfer.
- Compare judge models or generation strategies at a matched budget.
- Investigate discoveries beyond the original categories.

None is an automatic prerequisite for the initial demonstration. If a branch uncovers invalid representations or unreliable judgments in the current use, fix or narrow that use before advancing.

## Recording a round

Commit the code and criteria being tested. Keep each round's cases and human notes together in `review/round_NN/`. Use a distinct ignored `runs/round_NN/run_name/` for machine outputs. Record the code commit, intended next use, observed limitations, and the decision to proceed, narrow, revise, or stop. Publish selected run evidence deliberately when it is useful; do not commit every exploratory output by default.

