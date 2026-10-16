# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.

The fine-tuned classifier reaches at least **0.65 overall accuracy** on the
held-out test set.

**Why this target:** With three labels, random guessing is about 0.33. A 0.65
target means the model is useful more often than not while leaving room for
genuinely ambiguous running posts.



---

## 2.

Each label reaches at least **0.55 F1**, and the model reaches at least **0.60
macro F1**, on the held-out test set.

**Why this target:** Overall accuracy could hide a model that ignores
`reaction` or confuses every `hot_take` with `analysis`. The per-label floor
protects each category, while macro F1 rewards balanced performance.



---

## 3.

No label contains more than **70%** of the labeled posts, and the smallest
label contains at least **15%** of the data.

**Why this target:** The 70% ceiling follows the project requirement and
prevents majority-label guessing. The 15% floor gives the smallest category
enough examples to appear meaningfully in the train, validation, and test
splits.



---

## 4.

On a blind second labeling of **30 posts**, the original and repeat labels
agree on at least **24 of 30 posts (0.80 agreement)**.

**Why this target:** This checks whether the taxonomy is clear enough to apply
twice, not merely whether a model can imitate one inconsistent labeling pass.
Disagreements will be recorded instead of quietly edited away.



---

## 5.

Predictions with confidence of at least **0.75** are correct on at least **80%**
of those test examples, with at least **15 examples** in that confidence group.

**Why this target:** Confidence should help identify predictions that can be
trusted and predictions that need review. The minimum group size prevents one
lucky prediction from making the criterion look successful.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
