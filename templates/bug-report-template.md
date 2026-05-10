# Bug Report — <one-line summary>

> Optional template. `/iconix-bug` also accepts a UC-ID, a source path,
> or free text directly on the command line. Use this template when you
> want to write the bug down once and pass the saved file path to
> `/iconix-bug` (e.g. `/iconix-bug bug-reports/BUG-2026-05-08-place-bet-negative-balance.md`).
>
> Save filled-in copies under `bug-reports/BUG-<date>-<slug>.md` (this
> folder is project-local and does not need to exist in the kit).
>
> The Reviewer reads this in `# Bug triage` mode and produces a verdict:
> Type 1 (code diverges from a correct SD) or Type 2 (code matches the
> SD but the design is wrong).

## Affected artifact (at least one required)
- Source file(s): `<path/to/file.ext>`
- UC-ID(s): `<UC-XXX>`

> The Reviewer needs at least one anchor into the artifact graph to
> read the `Traceability:` comment and locate the SD to compare against.
> If you don't know either yet, describe the user-visible behaviour in
> the next section and the Reviewer will help locate the affected files.

## Observed behaviour
<what actually happens — error message, wrong return value, missing log
entry, unexpected screen state, wrong DB row written. Be specific. Quote
log lines or response payloads verbatim where possible.>

## Exception / stack trace (if any)

```text
<paste the stack trace here, top frame first. Trim third-party framework
frames (Spring, ASP.NET, Django, etc.) if they obscure the application
code path, but keep:
  • the exception type and message at the top
  • at least the first 5–10 application frames (file:line)
  • the originating frame (where the exception was thrown)

If the bug has no exception (e.g. wrong return value with status 200,
or a UI defect), delete this section.>
```

## Expected behaviour
<what should happen — quote the UC step or SD message arrow you expected
to see, if you can identify it. "Per UC-017 step 4, the system should
respond with HTTP 400 and not write to the ledger." beats "should fail">

## Reproduction
<minimal steps to reproduce, OR a failing test path with the exact
assertion that fires. If reproduction is non-deterministic, say so and
describe the conditions that increase the likelihood.>

## Triage hint (optional)
<anything that might bias the classification, e.g.:
  • "the SD wasn't updated when this UC was last revised in v1.4"
    → suggests Type 2 (design drifted from intent)
  • "this regressed right after the Developer's last fix on RB-017"
    → suggests Type 1 (code change broke alignment)
  • "the original UC author and the implementer were different teams"
    → could be either; flag for closer SD/UC comparison>

## Traceability

> **Filled by the Reviewer during BUG TRIAGE.** Once populated, do not edit
> by hand — subsequent updates go in `## Closure` below.

- Bug type: <Type 1 (implementation) | Type 2 (design)>
- Root artifact: <file path or diagram ID where defect originates>
- Affected UC: <UC-XXX>
- Recommended next step: <Developer bug-fix mode | /iconix-impact UC-XXX → REQ change flow>

## Closure

> **Filled by the Reviewer in Bug-fix verification mode (Type 1) OR Type 2
> closure mode (Type 2)** AFTER the fix has merged. Until then, this section
> is empty. Do not delete the section heading — empty Closure is itself an
> auditable signal ("bug filed but not yet verified closed").

- Closed: <date>
- Verified-by: iconix-reviewer (<Bug-fix verification mode | Type 2 closure mode>)
- Driven by CI report: <PREFIX>-CI-XXX (Type 2 only; omit for Type 1)
- New SD: <PREFIX>-SD-XXX (commit <SHA>) (Type 2 only; for Type 1 the SD is unchanged so this field is omitted)
- Merged code: PR <#NN>, commit <SHA>
- Drift closed: <one or two sentences — for Type 1, what specific drift the original triage flagged is now closed; for Type 2, that the new design + merged code together address the original Observed-vs-Expected gap>
- Reproduction now: <one sentence — what happens when you replay the original Reproduction steps>

