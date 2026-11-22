# Project roadmap files

Suggested structure for a repo's `ROADMAP.md`, distilled from the hw-commons and workflows roadmaps.
Loosely binding: adopt it when the project's intent fits a phased plan; deviate where the project demands, but keep the spine (goal -> phases -> notes).

## When to use

For work that outlives one sitting: multiple phases, dependencies between workstreams, progress tracked across sessions.
A small or single-purpose repo does not need one: do not cargo-cult it.

## Structure

1. **Goal paragraph.**
   One paragraph stating the end state the whole plan is for, not a feature list.
   Every phase below is ordered toward it.
2. **Phases in dependency order.**
   `## Phase N: name (status)`.
   Each phase produces independently useful output and earlier phases unblock later ones.
   Status in the heading: `done`, `in progress`, or nothing yet.
3. **Checklist items.**
   `- [x]` / `- [ ]`, one terse line each.
   Items are verifiable outcomes, not aspirations ("sim runs end-to-end", not "improve sim").
4. **Ordered table inside a phase** when items within it have their own dependency order (a bench ladder, a capability ladder).
   Same `[x]` convention in the first column.
5. **Known-hard gaps.**
   A phase or section honestly naming what cannot be fixed in this repo.
   Keeps the document from overselling.
6. **Notes and open decisions** at the bottom: gotchas, parked questions, settled decisions worth recording with their why.
7. **Appendices** for reference material that would swamp the phases (reuse maps, big tables).

## Upkeep

- Check items off in the same task that lands them; this is a standing duty in the injected AGENTS.md.
- Mark done honestly: "builds" and "runs end-to-end" are different items.
  If only the weaker one passed, it stays unchecked or the item gets split.
- Retire a phase by checking it off; keep it visible since the order still explains the plan.
- Pivot honestly: when a decision replaces a plan, strike the superseded items through (`~~[x] ...~~`) and add the new items with a dated line recording the pivot and its why.
  Rewriting a checked item to match the new plan pretends the pivot never happened.
- One canonical roadmap per repo.
  When a superseding structure arrives, fold content in and let the old planning file go.

## Examples in the wild

- `hw-commons/ROADMAP.md`: goal, phases 0-5, reuse-map appendix, notes and low-prio.
- This repo's `ROADMAP.md`: goal, workstream sections instead of phases (deviation from the spine: the repo evolves organically, so the phased frame was dropped), notes and open decisions.
