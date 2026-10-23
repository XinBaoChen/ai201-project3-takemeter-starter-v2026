# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

Milestone 1 community: [r/running](https://www.reddit.com/r/running/), a public
community with training logs, race reports, questions, gear discussions, and
running advice. I read 36 posts before choosing labels. Candidate distinctions
are evidence-backed analysis vs. unsupported takes, personal reports vs.
general advice, questions vs. conclusions, and training/performance vs.
gear/logistics. The full reading notes are in [MILESTONE1.md](MILESTONE1.md);
the final taxonomy will be locked after testing these boundaries on more text.



---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `analysis`

**Definition:** Makes an argument backed by a specific, checkable fact.

**Example 1:**
> "The entry fee went from 45 to 72 over four years. Field size went from
> 3,200 to 3,400. Whatever the extra 27 is paying for, it isn't capacity."

**Example 2:**
> "Split the field by finish time and looked at DNF rates. Under 3:30, about
> 1%. Over 5 hours, about 9%."

### `hot_take`

**Definition:** Makes a confident general claim without offering checkable
support.

**Example 1:**
> "Super shoes have ruined amateur racing. Times mean nothing now and everyone
> knows it."

**Example 2:**
> "The 5k is the only honest distance. Everything longer is a logistics
> competition."

### `reaction`

**Definition:** Gives an immediate emotional response to a recent running event
or experience.

**Example 1:**
> "Missed my goal by eleven seconds. Eleven. I'm going to be thinking about
> that for a month."

**Example 2:**
> "Just signed up for my first marathon and I'm equal parts excited and
> terrified."

### The hardest boundary

**Which two labels:** `analysis` vs. `hot_take`

**The decision rule I used every time:** If the post's main claim can be
checked against a named number, date, quote, comparison, or logged experience
included in the post, label it `analysis`; if it only asserts a broad
conclusion, label it `hot_take`. A number by itself is not enough: "I ran 20
miles and it was awful" is a `reaction` unless the number is used as evidence
for an argument.

### Boundary crash test

I stress-tested the definitions with eight fresh borderline posts. Each one
had one label that won under the rule:

| Boundary post | Label | Why |
|---|---|---|
| "My last four long runs were 18, 19, 20, and 20 miles; my race pace improved each time." | `analysis` | Uses a sequence of checkable observations as evidence. |
| "Long runs are the only training that matters." | `hot_take` | Broad claim with no support. |
| "The watch died at mile 18 and I panicked, but I finished." | `reaction` | Immediate experience and feeling are the main job. |
| "My watch died at mile 18; my final 10k was 40 seconds faster than the first 10k." | `analysis` | The comparison supports an implied conclusion. |
| "I missed the cutoff by 30 seconds and I am furious." | `reaction` | The emotional response dominates. |
| "Missing a cutoff by 30 seconds proves race organizers do not respect runners." | `hot_take` | General accusation without evidence beyond one case. |
| "In my last three races, I slowed after mile 20 by 8%, 6%, and 7%." | `analysis` | Specific repeated measurements make an argument possible. |
| "Every marathon becomes a survival hike after mile 20." | `hot_take` | Confident universal claim, no checkable support offered. |



---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** 216 public posts from r/running, supplied in
`labels.csv`. The file is one unsplit CSV with `text`, `label`, and `note`.

**How I labelled them:** The first 20 rows are marked `cold` as the cold-label
block. The remaining rows were originally marked `checked`. I mapped
`evidence_backed` to `analysis` and `unsupported_take` to `hot_take`, then
manually relabeled 33 clearly emotional/event-response posts as `reaction`.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `analysis` | 51 | 23.6% |
| `hot_take` | 132 | 61.1% |
| `reaction` | 33 | 15.3% |
| **Total** | **216** | **100%** |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* “I am really terrified of my long run this week.”
>
> *Could have been:* `reaction` or `hot_take`
>
> *I chose, because:* The main job is expressing immediate fear about a
> specific upcoming experience, not making a general claim.

**2.**
> *The post:* “Beermile Update!!! Took around 28 minutes and threw up whilst
> drinking the last one.”
>
> *Could have been:* `reaction` or `analysis`
>
> *I chose, because:* The time is background; the post is mainly an immediate
> reaction to a chaotic event.

**3.**
> *The post:* “My last four long runs were 18, 19, 20, and 20 miles; my race
> pace improved each time.”
>
> *Could have been:*
> `analysis` or `hot_take`
>
> *I chose, because:* The repeated, checkable observations support a conclusion,
> so it is `analysis`.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate `2e-5`, batch size `16`, max length `128`,
seed `42`.

**Anything I changed from the defaults, and why:** Nothing. I trained on CPU
(`torch 2.14.1+cpu`).

**Split sizes:** train `150` / validation `33` / test `33`. Test counts were
`analysis`: 8, `hot_take`: 20, and `reaction`: 5. The reaction score will be
jumpy because it has fewer than 8 test examples.

**Saved outputs:** [results.json](results.json) and [test_split.csv](test_split.csv).
The first run reached `0.606` accuracy and `0.252` macro F1; the model predicted
the majority `hot_take` class for every test post.

**Prediction before the baseline:** I predict the trained model will beat the
definition-prompted baseline on overall accuracy because it saw labeled
examples, but the baseline may be better on `analysis` and `reaction` if the
trained model keeps favoring `hot_take`.



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* Help stress-test the boundary between evidence-backed
  analysis and unsupported hot takes.
- *What came back:* Eight borderline running posts with suggested labels and
  explanations.
- *What I changed:* I checked each example against my written rule and kept the
  rule that a checkable fact supports `analysis`; a broad unsupported claim is
  `hot_take`.

**Moment 2**

- *What I asked for:* Help inspect the supplied 216-row CSV and identify posts
  that were mainly immediate emotional reactions.
- *What came back:* Candidate reaction posts and a label-balance check.
- *What I changed:* I reviewed the candidates, relabeled 33 clear
  event-response posts as `reaction`, and kept the final counts at or below the
  70% balance limit.

**Pre-labelling disclosure:** The supplied file already contained labels marked
`checked`. I used AI assistance to suggest mappings and reaction candidates,
then reviewed those changes. The first 20 rows are grouped and marked `cold`
for the required cold-label block.

**Moment 3 — error diagnosis**

- *What I asked for:* Help compare the before and after run metrics and
  confusion patterns without changing my criteria after seeing the results.
- *What came back:* The clearest pattern was a stable majority-class shortcut:
  before weighting, all three seeds sent every test post to `hot_take`; after
  weighting, minority labels appeared, but the accuracy spread reached 0.121
  and `reaction` remained weak.
- *What I changed:* I used that diagnosis to choose one controlled improvement,
  inverse-frequency class-weighted loss, and reported that it improved
  minority-label coverage but did not meet the accuracy or F1 targets.

AI did not make the final training or agreement decisions for me. I checked the
CSV, staff labels, metrics, and confusion matrices against the saved artifacts.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.303 | 0.606 | +0.303 |
| Macro F1 | 0.311 | 0.252 | -0.060 |
| F1 — `analysis` | 0.421 | 0.000 | -0.421 |
| F1 — `hot_take` | 0.240 | 0.755 | +0.515 |
| F1 — `reaction` | 0.273 | 0.000 | -0.273 |

**What I predicted before I looked:**
I predicted the trained model would beat the definition-prompted baseline on
overall accuracy, while the baseline might be better on `analysis` and
`reaction`.

**What the gap actually means:**
Fine-tuning improved accuracy by 0.303 and `hot_take` F1 by 0.515, but the
trained model collapsed to the majority class and lost both `analysis` and
`reaction`. The definition-prompted baseline had better macro F1, so the
training added accuracy without adding balanced label understanding.

**Bare-label comparison:** Without definitions, accuracy was `0.242` and
macro F1 was `0.263`. The written definitions improved the baseline by `0.061`
accuracy and `0.048` macro F1.



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Accuracy | 0.65+ | 0.606 | 0.606 | 0.606 | MISSED |
| 2. Per-label F1 / macro F1 | 0.55+ each / 0.60+ macro | 0.000 / 0.252 | 0.000 / 0.252 | 0.000 / 0.252 | MISSED |
| 3. Balance | max 70%, min 15% | 61.1% / 15.3% | 61.1% / 15.3% | 61.1% / 15.3% | MET |
| 4. Consistency | 24/30 agreement | 30/30 | 30/30 | 30/30 | MET |
| 5. Confidence | 80% at 0.75+, n≥15 | 81.8%, n=11 | 81.8%, n=11 | 81.8%, n=11 | NOT TESTED |

Accuracy was identical across seeds (spread `0.000`), so the majority-class
result was stable rather than a friendly split accident. The `reaction` test
support was only 5 posts, which makes its F1 especially fragile.

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted | analysis | hot_take | reaction |
|---|---|---|---|
| **analysis** | 0 | 8 | 0 |
| **hot_take** | 0 | 20 | 0 |
| **reaction** | 0 | 5 | 0 |

**My biggest off-diagonal number, and what it means:**
Eight real `analysis` posts were called `hot_take`, while zero `hot_take` posts
went the other way. The model learned the majority label, not the boundary.



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.65 in every seed | MISSED | All three seeds were 0.606. |
| 2 | Per-label F1 and macro F1 | ≥ 0.55 per label; ≥ 0.60 macro | MISSED | `analysis` and `reaction` were 0.000 F1; macro F1 was 0.252 in every seed. |
| 3 | Dataset balance | No label over 70%; smallest at least 15% | MET | `hot_take` was 61.1%; `reaction` was 15.3%. |
| 4 | Human consistency | ≥ 24/30 agreement | MET | Staff comparison was 30/30, or 100%. |
| 5 | Confidence usefulness | ≥ 80% correct at 0.75+ confidence with n≥15 | NOT TESTED | The most-confident group had only 11 examples, below the required 15. |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

**Criterion 1 diagnosis:** This was a model/data limitation, not split luck.
Accuracy was exactly 0.606 for all three seeds, and the confusion matrix shows
the model predicted `hot_take` for every test post. The dataset passed the
balance criterion, but 132 of 216 examples were still `hot_take`, so the model
learned the majority shortcut. The three-seed stability rules out a friendly
split as the main cause.

**Criterion 2 diagnosis:** The model could not learn the minority-label
boundaries from this dataset and training setup. Every `analysis` post (8/8)
and every `reaction` post (5/5) was called `hot_take`, while `hot_take` F1 was
0.755. This is not supported as a labeling-consistency problem by the staff
agreement check: I matched all 30 staff labels, so the evidence points more
strongly to a task/model limitation, amplified by only 5 `reaction` examples in
the test split.

**Criterion 5 note:** This criterion was not fairly measurable. The run
reported 11 examples in the most-confident group, not the required 15. The
81.8% figure is descriptive, but it cannot earn a MET verdict under the
original criterion. I am leaving the target unchanged rather than lowering it
after seeing the result.


---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** 30 / 30 = **100%**

I matched the staff label on every post. The set was manageable because the
staff rules were specific enough to make the fact-versus-claim and
reaction-versus-general-claim boundaries consistent.

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

There were no disagreements, so there are no posts to adjudicate or sort into
piles (a), (b), or (c). The perfect match is evidence that I could apply this
written taxonomy consistently on this 30-post check; it does not prove that
every label in my larger dataset was equally consistent.

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**What the pattern in my disagreements tells me:**

There were no disagreements to diagnose. The result supports the written-rule
workflow, while the small sample means I should still treat ambiguous cases in
the 216-post dataset carefully.


---

## The Improvement

**What I changed:**

I changed one training setting: I used inverse-frequency class weights in the
cross-entropy loss. The model now gets a larger penalty for ignoring the
smaller `analysis` and `reaction` labels. I changed no labels, posts, split
seeds, or model architecture.

**Which diagnosis pointed at it:**

The before run predicted `hot_take` for every test post across all three seeds.
That stable majority-class shortcut, plus the missing minority-label F1 scores,
pointed to a training imbalance problem rather than a staff-taxonomy agreement
problem.

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.65 | 0.545 | 0.455 | 0.576 | MISSED |
| 2. Every label F1 and macro F1 | per-label ≥ 0.55; macro ≥ 0.60 | 0.400 / 0.463 | 0.111 / 0.254 | 0.222 / 0.319 | MISSED |
| 3. Label balance | no label > 70%; smallest ≥ 15% | unchanged | unchanged | unchanged | MET |
| 4. Human agreement | ≥ 24/30 | 30/30 | 30/30 | 30/30 | MET |
| 5. Confidence | ≥ 0.75 accuracy with at least 15 examples | 0.364 (11) | 0.636 (11) | 0.727 (11) | NOT TESTED |

**Did it help, and how do I know:**

It helped the model stop predicting only `hot_take`: seed 42 reached an
`analysis` F1 of 0.400 and a macro F1 of 0.463. It did not help the overall
criterion, because accuracy fell from 0.606 in every before run to
0.455–0.576 after weighting, and the three after accuracies spread by 0.121.
So the change improved minority-label coverage but made the measurement less
stable and did not meet the targets. Tiny dataset, big feelings.



---

## What's Still Broken

Criteria 1 and 2 are still missed: the weighted model averages 0.525 accuracy
and 0.345 macro F1 across the three seeds, below the targets. Reaction F1 is
still 0.267, 0, and 0, so the thinnest label remains difficult. The after
spread is over ten percentage points, which means this 216-row, imbalanced
dataset is not a stable measurement yet. Criteria 3 and 4 remain met; criterion
5 is still not tested because each confidence group has only 11 examples,
below the required 15.

If I continued, I would add carefully labeled examples to `reaction` and
rebalance the dataset before trying another training setting. I stopped after
one controlled change so its effect stayed identifiable, rather than turning
the experiment into a mystery stew.



**The gap between what I meant my labels to capture and what the model
learned:**

Before weighting, the model learned that the safest answer was `hot_take` and
sent every test post there, even though 8 `analysis` and 5 `reaction` posts
were present. After weighting, it at least separated some minority examples,
but it traded errors across all three labels and remained especially weak on
`reaction`; the 0.121 accuracy spread shows that the learned boundary is not
reliable yet.



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
