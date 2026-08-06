---
name: format-documents
description: Define, apply, and verify reusable document-format requirements for Word DOCX files, including page geometry, fonts, font sizes, line spacing, paragraph rhythm, title and heading hierarchy, a dedicated Table of Contents page, lists, quotations, captions, headers, footers, page numbers, and table geometry. Use when Codex needs to create a formatted document or template, restyle an existing DOCX without rewriting its content, turn informal format requests into an exact style contract, or audit whether a DOCX follows a required format.
---

# Format Documents

Turn format requests into exact, testable Word styles. Preserve document content unless the user explicitly asks for editing.

## Workflow

1. Resolve the format authority in this order:
   - explicit user requirements;
   - an attached template or organization standard;
   - the default contract in `references/style-spec.md`.
2. Before editing, write a compact format contract covering page, fonts, body, title, headings, Table of Contents, lists, tables, header/footer, and exceptions. Mark unspecified values as defaults, not user-confirmed requirements.
3. For new documents, use semantic Word styles and real numbering definitions. For existing documents, map paragraphs to semantic roles before applying styles; do not infer a heading from font size alone when the role is ambiguous.
   - Number every Heading 1 with real Chinese counting: `一、二、三……`. Do not type Arabic `1/2/3` or a manual Chinese prefix into the heading text.
4. Put the Table of Contents on its own page, bounded by explicit page breaks. Use real Heading 1–3 styles as its source.
5. For a Word-operated workflow, insert a real TOC field and update fields before delivery. For a fully headless workflow, use the `documents` skill static TOC/internal-navigation workflow so the directory is deterministic.
6. Apply exact values. Do not rely on Word defaults, theme inheritance, fake bullets, manual numbering, percentage-width tables, or fixed table-row heights.
7. Run `scripts/audit_format.py` for structural checks.
8. Use the `documents` skill workflow to render the final DOCX to PNG, inspect every page, and iterate. Structural validation is not visual acceptance.

## Default contract

Read `references/style-spec.md` whenever the user has not supplied a complete specification, or when building the sample/template. Treat every deviation as a named override.

The bundled contract is a modern Chinese business-document system:

- A4 portrait;
- `Microsoft YaHei` for title, headings, body, lists, tables, header, and footer;
- 10.5 pt body text, 1.5 line spacing, two-character first-line indent;
- three real heading levels;
- Heading 1 automatically numbered `一、二、三……` with a real Word numbering definition;
- a dedicated one-page directory with three TOC levels, dotted leaders, and right-aligned page numbers;
- real bullet and decimal numbering;
- fixed-width tables with deliberate cell padding and alignment;
- restrained blue-gray palette, callout, caption, running header, and page-number footer.

If Microsoft YaHei is unavailable, keep the DOCX font slots set to Microsoft YaHei when it is an explicit requirement. A fallback font may be used only for layout QA, and that substitution must be disclosed. Never silently claim font fidelity.

## Create a sample or template

Use the Python runtime returned by the workspace dependency loader:

```bash
python scripts/build_sample.py --output /absolute/path/sample.docx
python scripts/audit_format.py /absolute/path/sample.docx
```

`scripts/build_sample.py` intentionally demonstrates a cover, a dedicated Table of Contents page, title, subtitle, body, inline emphasis, Heading 1–3, bullet list, numbered list, quotation/callout, caption, table, header, and footer styles with minimal content.

## Restyle an existing DOCX

Apply the contract without replacing text:

```bash
python scripts/apply_format.py input.docx --output formatted.docx
python scripts/audit_format.py formatted.docx
```

Before running:

- save to a new path;
- inspect paragraph style names and table roles;
- promote title/headings only when their semantics are known;
- preserve direct formatting that carries meaning;
- use `--promote-first-paragraph` only when the first non-empty paragraph is confirmed to be the document title.

After running, inspect exceptions such as cover pages, legal clauses, code blocks, equations, footnotes, and branded tables separately.

## Acceptance

Call the result complete only when all are true:

- the format contract identifies user requirements, defaults, and substitutions;
- the Table of Contents occupies one page, includes the intended heading levels, and has no stale or missing entries;
- structural audit passes or every exception is explained;
- the latest rendered pages show no clipping, overlap, broken wrapping, cramped cells, or awkward page breaks;
- the delivered file is the audited and rendered revision;
- content changes, if any, are separately disclosed.
