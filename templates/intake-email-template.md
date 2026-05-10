# Email request: `<subject>` — `<YYYY-MM-DD>`

## Source
- **From:** `<name, role>`
- **To:** `<recipient list>`
- **Thread / ticket:** `<id or link>`
- **Received:** `<date>`

## Verbatim text
> `<Paste the email exactly as received. Do not edit.>`

---

> ⚠️ **Above this line: stakeholder input (do not edit).**
> ⚠️ **Below this line: Product Owner agent output (intake checklist).**
>
> The two halves of this file have different ownership. The verbatim text above
> is what was received and should never be paraphrased or "cleaned up." The
> sections below are the PO agent's restatement, populated by applying the
> intake checklist from `agents/iconix-product-owner.md`. Every `[VERIFY]` tag
> below marks an inference that must be confirmed with a stakeholder before
> the `## Status` block can be ticked `Ready`.

---

## PO restatement
> Fill in the sections below. Mark every inference with `[VERIFY]` — do not invent facts.

### Stated request (paraphrase in one sentence)
`<What the sender asked for, in their terms.>`

### Inferred goal `[VERIFY]`
`<"<Actor> wants to <outcome> so that <benefit>." — restate as observable behaviour, not solution.>`

### Inferred actor(s) `[VERIFY]`
- `<specific role, not "user">` `[VERIFY]`

### Inferred scope
**In:** `<what this request covers>`
**Out:** `<what it does not cover — be explicit>`

### Constraints / NFR seeds
| Category | Stated or inferred | Measurable target |
|---|---|---|
| Performance | `<text>` | `[VERIFY]` |
| Security | `<text>` | `[VERIFY]` |
| Compliance | `<text>` | `[VERIFY]` |

### Ambiguities — must clarify before extraction
- [ ] `<question 1>`
- [ ] `<question 2>`
- [ ] `<question 3 — e.g., "Which role triggers this flow?">`

---

## Candidate artifacts
> Only fill in if the request is unambiguous. Otherwise leave blank and mark as **Blocked**.

**Candidate REQs:**
- The system shall `<observable behaviour — no tech names>`. *(P0 | P1 | P2)*

**Candidate UC stubs:**

| UC title (noun-verb-noun) | Basic course outline |
|---|---|
| `<Actor> <verb> <object>` | User: `<action>` → System: `<response>` |

**Candidate NFRs:**
- `<category>`: `<measurable target>`

---

## Status
- [ ] Blocked — pending clarification (questions above must be answered first)
- [ ] Ready — all `[VERIFY]` items confirmed; proceed to REQ/UC drafting
