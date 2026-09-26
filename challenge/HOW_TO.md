# How to take the WBS↔LINK Challenge

The challenge is meant to feel like a controls problem, not a coding exam.

You have several project records that describe the same work differently: an owner WBS, schedule activities, cost information and supporting contractor/fabricator records. Your job is to build the relationship back to the owner WBS.

## 1. Start with Practice

Download the Practice set first. Its reference mapping is public, so you can try your approach, run the local scorer and see where your logic differs.

Use whatever you would actually use: Excel, Power Query, SQL, Python, AI, or a combination. The method is up to you.

## 2. Build your crosswalk

For each record, return either:

- the applicable WBS `Cell ID`;
- `NO_WBS` when the record is valid but no owner WBS element applies;
- `NEW_SCOPE` when the record appears to represent scope outside the current WBS;
- `UNSURE` when the evidence does not support a defensible mapping.

If one record genuinely spans two WBS cells, use `A|B`.

The important part is not to force an answer. If the data conflicts, say so.

## 3. Add confidence

For every mapping, choose `high`, `med` or `low`.

A high-confidence mapping that is wrong is treated more seriously than an unresolved item. In a reporting environment, a blank creates a question. A confident wrong mapping can quietly flow through the process.

## 4. Score Practice locally

From the extracted Practice folder:

`python scorer/score.py my_answers.csv --set practice --exceptions my_exceptions.csv`

The Practice set is repeatable. Use it to understand the format before taking the hidden Challenge.

## 5. Take the hidden Challenge once

When you are ready, complete the Challenge set and submit through GitHub. The hidden set allows one scored attempt per GitHub user. Editing the issue does not trigger another score.

## 6. Tell us what the benchmark is missing

Your score is only part of the point.

After the mapping, the submission form asks a few short questions about what evidence you relied on, how you think mapping risk should be treated, what makes this harder on real projects, and how much effort this kind of reconciliation takes today.

Those answers will help shape future versions of the benchmark and WBS↔LINK. Keep examples general: do not share client, employer or confidential project information.

## Where this is going

WBS↔LINK is an early-stage concept for a secure, AI-enabled project-controls mapping workflow: connect schedule, cost, WBS and contractor records; propose mappings; surface uncertainty for review; reuse approved relationships in later reporting cycles; and export a standard Excel/CSV crosswalk for teams that want to continue working in their existing tools.

The public challenge is how we pressure-test the problem before pretending the product is finished.
