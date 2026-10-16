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

**How I labelled them:** The first 20 rows are the cold-review block: 6 are
honestly marked `cold`, and 14 are marked `cold_review_required` for me to
review before calling them cold. The remaining rows were originally marked
`checked`. I mapped `evidence_backed` to `analysis` and `unsupported_take` to
`hot_take`, then manually relabeled 33 clearly emotional/event-response posts
as `reaction`. I did not claim unchecked rows were cold labels.

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

**Base model:**

**Settings:** <!-- epochs, learning rate, batch size, seed -->

**Anything I changed from the defaults, and why:**

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->



---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Pre-labelling disclosure:**

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

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

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



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
