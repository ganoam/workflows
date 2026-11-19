# Markdown Style Guide

Conventions for writing prose across repos: documentation in
Markdown, reStructuredText, or AsciiDoc, and prose in code comments.
The rules below bind agents via the pointer in `agents/rules.md`;
this document carries their rationale and the finer detail.

## Basics

### Summary

Prose docs in these repos are written for humans but their content
binds agents too.
Style exists to keep diffs honest and reviews cheap: a reader should
see what changed, not rewrapped noise.
Goals:

- consistent look across repos
- minimal-diff maintenance
- sentence-granular review and editing

### Terminology conventions

- ***must*** / ***do not***: mandatory requirement / prohibition.
- ***recommended*** / ***not recommended***: preferred / unsuitable.
- ***may***: permitted, optional.

### Exceptions

***Deviation is allowed where reality requires it; justify it.***

A generated table, a verbatim upstream quote, or a renderer quirk
can all force a deviation.
Mark non-obvious deviations with a nearby comment so the next reader
does not "fix" them.
Content between generator fences is exempt by construction; fix the
generator or its input, never the output.

## Formatting rules

### One sentence per line

***Every sentence is its own source line; no fixed-column
word-wrapping.***

This applies to all new content.
When an edit touches a document whose existing content does not
adhere, prompt the owner about fixing the file; never fix silently.
Format fixes get their own commits, separate from the content work
at hand, so a rewrap never pollutes a content diff.

#### Why

- A one-sentence change produces a one-line diff.
  Fixed-column wrapping turns the same edit into a paragraph-wide
  reflow that hides what actually changed.
- Sentences can be moved, joined, split, or commented out
  independently.
- Sentence granularity matches review workflows (GitHub suggestions,
  per-line comments).
- Overlong and redundant sentences become visible when each stands
  alone.
- Bulk edits and macros operate cleanly on single lines.

#### What counts

- Split at sentence ends; semicolons and colons inside a sentence
  stay on the same line.
- Bullets follow the same rule; a second sentence starts a new line
  indented under the item.
- Long sentences stay long; the visibility is the point.
- Exempt: code blocks, tables, headings, fenced generated regions,
  code comments. The exemption covers only this section's rule;
  the guide's other rules still apply to everything.

```markdown {.bad}
The README is the repo's front door and its install contract.
Update it whenever work changes what it states: commands,
prerequisites, and architectural decisions all count.
```

```markdown {.good}
The README is the repo's front door and its install contract.
Update it whenever work changes what it states: commands, prerequisites, and architectural decisions all count.
```

### No em-dashes

***Do not use em-dashes in prose, comments, or generated text.***

Use commas, colons, periods, or parentheses instead.
This is an owner style preference enforced uniformly so the prose
voice stays consistent across human- and agent-written docs.

### Terse over tutorial

***One heading per intent, the command or content below it, a gotcha
line only when something actually went wrong.***

Applies to tricks and command references; explanations to the reader
stay compact with no padding.
A doc that lists a working procedure does not retell its history.

### Generated regions

***Content inside generator fences is never hand-edited.***

Fix the source the generator reads and re-run it, or document
outside the fences.
Hand-edits inside fences are silently overwritten on the next
generation run and make the fence marker a lie.

## Conforming edits and legacy content

***When an edit touches a document whose existing content violates a
rule in this guide, prompt the user whether they want the file fixed.
Never fix silently.***

Formatting fixes get their own commits, separate from the work at
hand, so a style cleanup never rides along inside an unrelated
change.

{Rationale}

This applies to every rule in this guide: a document may legitimately
predate any of them, and a sweep is the owner's call, not the
editor's.
Bundled fixes bury formatting churn inside a feature diff, which
makes review harder and history noisier.
A prompt costs a sentence; a silent rewrite costs a tangled commit
and the reader's trust in the diff.

## Appendix: condensed style guide

| Rule | Level | Summary |
|---|---|---|
| One sentence per line | must | each sentence is its own source line |
| No em-dashes | must | commas, colons, periods, parentheses |
| Terse over tutorial | recommended | heading + content, gotcha only if it bit |
| Generated regions | must | never hand-edit fenced content |
| Legacy content | must | prompt user on touch; fixes get own commits |
