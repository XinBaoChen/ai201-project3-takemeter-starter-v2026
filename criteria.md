# TakeMeter capstone acceptance criteria

These are my targets for Shape C. I wrote them before running the new review
mode. No results have been used to move the goalposts. The goalposts are
already busy doing their job.

## 1. Every prediction leaves a useful record

Across **three runs of 33 held-out posts**, at least **99 of 99 prediction
records** must contain a timestamp, the original input, the predicted label,
the confidence score, the `needs_review` decision, and `duration_ms`.

**Why this target:** The whole point of the extension is to find predictions
that need a second look. If the record is missing the input or the decision,
the second look becomes a treasure hunt. I chose 99 because three full runs
should produce one record for every test post.

## 2. The review queue must be useful, not ridiculous

With the review threshold set to **0.75**, each of the three runs must send
between **20% and 80%** of the 33 posts to review.

**Why this target:** A queue below 20% may miss too many uncertain posts. A
queue above 80% means the system is basically handing the whole job back to a
human with a tiny robot assistant attached. This range leaves room for review
without making the feature pointless.

## 3. Trusted predictions must be better than a coin toss

In each of the three runs, predictions not marked `needs_review` must reach at
least **0.65 accuracy**, using at least **10 trusted predictions**.

**Why this target:** The extension should make the remaining automatic answers
more useful, not just add a warning label. Three labels make random guessing
about 0.33, so 0.65 is a meaningful improvement. The minimum of 10 trusted
predictions stops one lucky answer from winning the argument.

## 4. Bad input must fail loudly and leave evidence

For **three invalid-input trials**, the command must exit with a nonzero status
within **10 seconds** and append a `run_error` record containing a timestamp,
an error type, an error message, and `duration_ms` to the structured log.

**Why this target:** A broken run should not disappear like a sock in a dryer.
The error record tells me that the command failed and why. Ten seconds is
long enough for normal file handling but short enough to catch a command that
gets stuck instead of reporting the bad input.

## 5. The run must stay affordable on this laptop

Across **three runs**, the average full-run time must be no more than **5
seconds per held-out post**. Each completion record must also include separate
times for model loading, prediction, and logging or other work.

**Why this target:** This is a local CPU system, so seconds of compute are its
real cost. Five seconds per post keeps a 33-post check under three minutes,
even if the model decides to take the scenic route. The stage times make the
stretch latency breakdown measurable instead of guesswork.

## Self-check

Each criterion has a number, a clear way to test it, and a failure condition.
At least three criteria are about the new review extension. Criterion 4 covers
the bad path. I will not change these targets after seeing the results.
