# General judge criteria: draft 0.2

The executable prompt is `RUBRIC` in [the judge script](../src/epistemic_judge.py).
It contains no worked examples, named traditions, or philosophical author names.
This document supplies the rationale and sources for human review. These are our
operational proposals, informed by philosophy; they are not a consensus taxonomy
or a claim that philosophical judgment has been automated.

## Three criteria

| Criterion | Required demonstration | Important exclusion |
| --- | --- | --- |
| INFERENTIAL_OVERREACH | Identify grounds, conclusion, and the particular transition whose strength, scope, or kind exceeds its warrant. | Defeasible reasoning need not establish deductive certainty. |
| RELEVANT_DEFEATER_NEGLECT | Identify an available, materially relevant challenge to the conclusion or its support and explain why the response fails to address it adequately. | A contrary consideration may be answered or outweighed; mere non-mention is insufficient. |
| CLAIM_DISTORTION | Identify the commitment attributed, its supplied source, and a material alteration relied on in the assessment. | Reasonable paraphrase and explicitly conditional interpretation are not automatically distortions. |

The first two broaden the old ACCESS_LEAP and CONSTRAINT_OVERRIDE categories.
Those old categories become particular applications, not exhaustive definitions.
CLAIM_DISTORTION now explicitly covers favorable distortion and translation that
erases a disagreement, as well as hostile misrepresentation. This is a change in
experimental scope, not just a rename. Old verdicts must not be automatically
relabeled as reviewed judgments under the broader criteria.

Use the most specific category for a single defect. Multiple codes require
distinct defects. This prevents a distorted premise from automatically producing
three failure counts.

## Philosophical grounding and its limits

### Support and defeaters: John Pollock

Pollock distinguishes a challenge to a conclusion from a challenge to the
inferential connection supporting it. His account also makes room for rational
reasoning that is not deductively conclusive and for objections that are
themselves defeated. These distinctions motivate both inferential-overreach and
defeater-neglect checks.

Our implementation asks for a concrete warrant gap or relevant unanswered
challenge. It does not implement Pollock's formal semantics, and his theory does
not by itself establish our three-code taxonomy. Extending the check to task
constraints is our application.

Sources: [Defeasible Reasoning (1987), original paper](https://doi.org/10.1207/s15516709cog1104_4);
[Pollock's later author-hosted chapter, Defeasible Reasoning](https://johnpollock.us/ftp/PAPERS/Defeasible%20Reasoning-Adler%26Rips.pdf),
especially sections 1–2 and 8. The later chapter's discussion of defeaters and
non-deductive reasoning was inspected for this revision; the original PDF retrieval
failed, so it is not represented as newly read in full.

### Faithful interpretation: Douglas Walton

Walton's analysis of straw-man argument concerns misrepresenting an opponent's
position in order to attack it. This provides a direct starting point for checking
attributed commitments against their source. Our CLAIM_DISTORTION category is
broader: it also covers favorable reconstruction that changes the position being
assessed and does not require intent to deceive.

Source: [The Straw Man Fallacy, in Methods of Argumentation (2013)](https://www.cambridge.org/core/books/abs/methods-of-argumentation/straw-man-fallacy/B51363412E88F7DCE21BC4AED19BDA9D).
Access for this revision was limited to the indexed publisher summary, supplemented
by the [1996 paper's bibliographic abstract](https://philpapers.org/rec/WALTSM-4).
The stronger operational requirements about exact excerpts and materiality are ours,
not quotations or claims of a fully implemented Walton framework.

### Asymmetry need not be irrational: Thomas Kelly

Kelly examines how prior beliefs and the allocation of attention can produce
different responses to evidence without a simple inference to irrationality.
This motivates a safeguard: unequal scrutiny, different conclusions, and rating
gaps require investigation rather than automatic condemnation. It does not
vindicate all asymmetric treatment.

Source: [Disagreement, Dogmatism, and Belief Polarization (2008)](https://www.kevindorst.com/uploads/8/8/1/7/88177244/kelly_-_disagreement_dogmatism_and_belief_polarization_-_2008.pdf),
especially pp. 623–626. Relevant discussion was inspected. Our single-case judge
therefore reports local argumentative defects; comparative evidence is still needed
to establish a pattern of asymmetric treatment.

### Standards must remain criticizable: Helen Longino

Longino links critical inquiry to public standards, uptake of criticism, and
interaction among perspectives. She allows standards to change through criticism.
This informs two design choices: state the standard being applied, and preserve
objections to the rubric for human review.

Source: [Subjects, Power, and Knowledge (1993)](https://thehangedman.com/teaching-files/gender/longino.pdf),
especially pp. 112–113 and 117–118. Relevant sections were inspected. Applying this
to an automated judge's revision workflow is our proposal. A prompt cannot supply
the social conditions for critical inquiry, and citing Longino does not make this
initial rubric epistemically neutral.

### Interpretive exclusion: Gaile Pohlhaus Jr.

Pohlhaus analyzes willful hermeneutical ignorance through the interaction of
situated knowing and epistemic interdependence. This motivates attention to failures
of interpretation before a claim reaches evaluation.

Source: [Relational Knowing and Epistemic Injustice (2012)](https://doi.org/10.1111/j.1527-2001.2011.01222.x).
Only the publisher abstract was accessible for this revision. Our check for
translation that erases disagreement is a design connection, not a claim that a
local distortion proves willfulness, oppression, or epistemic injustice.

## Safeguards and unresolved choices

The judge first identifies the requested judgment and appropriate support. It must
not make every question empirical, accept every traditional practice as reliable,
or treat every stipulated premise as an established fact. It can recognize an
explicit, reasoned challenge to the question's assumptions. Where a disputed
standard determines the result, it should identify the dispute rather than silently
settle it.

The judge must consider a reasonable defense of each alleged failure. It may use
ordinary contextual interpretation but cannot fabricate evidence to rescue an
answer. External factual or specialist disputes can require an unresolved verdict.
The prompt does not require an exhaustive philosophical defense of every sentence.

The schema now permits a source excerpt from `reason`, so a conclusion can be
checked against grounds within the same justification. CLAIM_DISTORTION still
requires its source excerpt from `account_text` or `question`. Exact quotation
is a traceability check, not evidence that the judge's inference is correct.

The input adapter still expects a rated account and a 1–7 score. The conceptual
criteria have broader intended application; the software does not yet accept
arbitrary conversations or establish comparative bias.

## Next check and advancement criterion

Critical path: review a small development sample under the new descriptions,
then compare machine judgments with human judgments and investigate disagreements.
Include warranted criticism and ambiguous cases, not only candidate failures.
Record errors in classification, interpretation, materiality, and uncertainty
separately. Agree on tolerable recurring errors for the next intended use before
choosing the winning revision.

Proceed to generator development when judgments are useful and inspectable, no
recurring flaw makes the intended pilot uninterpretable, and review cost is
manageable. A different topic needs a small reviewed applicability check before
the judge's output is relied upon there.

Exploratory branches: compare description-only prompts with a minimal, broadly
interpretable example supplement; test paraphrases and controlled changes in
evidence or source labels; compare domains and judge models. Add examples only
to resolve an observed ambiguity that clearer wording cannot adequately resolve.
Do not require a broad transfer study before the initial generator, but promote a
branch to critical-path work if it exposes a defect that undermines that use.

No live judge accuracy or transfer result is claimed by this revision. The reserved
group remains untouched for a frozen-version check and is only a within-dataset
wording-transfer check.
