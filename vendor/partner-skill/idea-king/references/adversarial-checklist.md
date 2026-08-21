# Adversarial Review Checklist

Work through these attack surfaces in order; stop collecting after the 3
strongest. Depth beats coverage.

## Premises (wrong step zero)

- Is the problem statement itself inherited rather than verified? Who
  actually has this problem, and how do we know?
- Does the plan assume a capability, API, or behavior that nobody has
  confirmed on this machine / this version?
- Is there a number in the plan (cost, latency, volume) that is a guess
  dressed as a fact?

## Hidden Coupling

- Which two parts are "independent" in the plan but share state, schema,
  config, or timing in reality?
- What breaks in module A when module B is done by a different agent with
  different assumptions?
- Are there implicit ordering dependencies the parallel plan ignores?

## Integration Cost

Coase's account: transaction costs, not task size, set the delegation
boundary — delegation is never free; price the handoff before you send it.

- Sum the boundary costs: handoff writing, context rebuilding, review,
  rework rounds. Does the total still beat doing it in one place?
- Who merges conflicting outputs, and with what authority?
- Is the review gate actually cheaper than doing the work? If reviewing
  the delegated output costs as much as producing it, the split is theater.
- Diff-blind acceptance: does the acceptance step read the diff *and* the
  original task brief, or only the diff? A reviewer given only the diff
  confidently redefines the spec as "consistent with what changed" and
  passes work where the task was never done (Superpowers 6: 0 of 5 missing
  briefs caught). Falsification: hand the reviewer a diff that deliberately
  does half the task, and see if it passes on internal consistency alone.

## Failure Amplifiers

- What is the single point whose failure invalidates everything after it?
- Where would a silent failure (wrong but plausible output) pass the
  current acceptance criteria?
- Murphy audit on acceptance: a verification that only walks the happy
  path verifies the demo, not the change. Enumerate what *can* go wrong
  (malformed input, timeout, partial failure, double-fire, empty state)
  and check each is exercised or consciously waived — whatever can go
  wrong and is never tested will go wrong in production first.
- What happens on partial completion — is the intermediate state safe to
  stop in, or does it strand the repo?

## Incentive & Scope Drift

- Which agent benefits from marking this "done"? What would it cut to get
  there?
- Where can scope quietly grow ("while I'm here...") and who stops it?

## Delegation Prompt Quality

When the plan includes handing work to another agent, attack the packet
itself before attacking the split:

- Vague goal: "make it better" instead of a measurable outcome with a
  check command.
- Bundled tasks: several jobs welded into one prompt that should be
  sequenced as separate rounds with a status check between them.
- Over-constrained toolchain: dictating exact commands instead of stating
  the outcome — you are constraining a model that would have picked a
  better route.
- Review asked to also fix: a review job is read-only; folding "and fix
  everything you find" into it produces neither a good review nor a good
  fix.
- Resume aimed at the wrong session: "continue" without a verified session
  id restarts context from zero while claiming continuity.

## Code-Level Attack Surfaces

When the target is a concrete change (a diff, a migration, a deploy), not
just a plan, prioritize the failures that are expensive, dangerous, or hard
to detect:

- auth, permissions, tenant isolation, and trust boundaries
- data loss, corruption, duplication, and irreversible state changes
- rollback safety, retries, partial failure, and idempotency gaps
- race conditions, ordering assumptions, stale state, and re-entrancy
- empty-state, null, timeout, and degraded-dependency behavior
- version skew, schema drift, migration hazards, compatibility regressions
- observability gaps that would hide the failure or make recovery harder

## Falsification Experiment Quality

A good experiment is: cheap (minutes, not hours), decisive (a clear
pass/fail), and early (runnable before the plan commits). "Run the full
pipeline and see" is not a falsification experiment; it is the failure you
were trying to avoid.
