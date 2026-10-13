# Development plan

## Working principle

An experiment may be scientifically valuable without being a prerequisite. Critical-path work establishes feasibility, interpretability, or sufficient reliability for the next intended step. Exploratory work becomes essential when its findings undermine that next step. Progress does not depend on every analogy or initial failure category surviving unchanged.

## Current pre-sprint sequence

| Step | Status and output | Advancement criterion |
| --- | --- | --- |
| Prepare existing responses | Done: development and reserved judge-facing CSVs; no new target calls needed. | Exact questions, accounts, ratings, and reasons retained; cases remain traceable privately. |
| Review a small sample | Ready: round 01 has 16 cases and blank review fields. | Review identifies usable failure examples, justified counterexamples, and unresolved boundaries. |
| Build and refine the judge | Draft built; dry-runs and simulated checks only. | A small reviewed check shows useful distinctions, appropriate uncertainty, and no recurring flaw that makes the next use uninterpretable. |
| Choose a prompt-generation topic | Pending sprint-facing topic review. | Topic fits the intended application, and a few manually reviewed cases establish that the judge's task remains meaningful there. |
| Build the prompt generator | Pending judge review. | It produces useful, reviewable cases without requiring near-total manual rewriting; the complete workflow can be demonstrated. |

A working judge and generator are the minimum pre-sprint target. This is a prototype, not a publication-grade study. Preserve the important records and clear component boundaries so collaborators can extend it.

## Optional sprint branches

- Automate proposals for rubric or example improvements, with human review and separate checks before adoption.
- Add failure modes or domains, validating the new use before claiming transfer.
- Compare judge models or generation strategies at a matched budget.
- Investigate discoveries beyond the original categories.

None is an automatic prerequisite for the initial demonstration. If a branch uncovers invalid representations or unreliable judgments in the current use, fix or narrow that use before advancing.

## Recording a round

Commit the code and criteria being tested. Keep each round's cases and human notes together in `review/round_NN/`. Use a distinct ignored `runs/round_NN/run_name/` for machine outputs. Record the code commit, intended next use, observed limitations, and the decision to proceed, narrow, revise, or stop. Publish selected run evidence deliberately when it is useful; do not commit every exploratory output by default.
