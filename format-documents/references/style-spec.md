# Default Chinese Business Document Style Contract

Use this contract only for values the user or controlling template has not specified. Record any change as a named override.

## 1. Page and color

| Token | Exact value |
|---|---|
| Paper | A4 portrait, 210 × 297 mm |
| Margins | top 22 mm; bottom 20 mm; left/right 24 mm |
| Header/footer distance | 12.5 mm |
| Content width | 162 mm / 9184 DXA |
| Primary ink | `#202124` |
| Deep blue | `#17365D` |
| Heading blue | `#365F91` |
| Muted gray | `#667085` |
| Pale blue fill | `#EAF2F8` |
| Table stripe | `#F4F7FA` |
| Table border | `#B7C9DA` |

## 2. Font policy

Set Latin and East Asian font slots explicitly. The default contract uses one family throughout.

| Role | All font slots |
|---|---|---|
| Title and headings | `Microsoft YaHei` |
| Body, list, caption, note | `Microsoft YaHei` |
| Table header and body | `Microsoft YaHei` |
| Header, footer, fields | `Microsoft YaHei` |

Set `ascii`, `hAnsi`, `eastAsia`, and `cs` to `Microsoft YaHei`; some renderers ignore the East Asian slot. If the font is not installed locally, keep the DOCX requirement unchanged and record any temporary QA substitution. Do not package or redistribute a font file unless the user supplies it and its license permits redistribution.

## 3. Paragraph styles

| Style | Typeface | Size | Weight/color | Alignment | Before / after | Line spacing | Other |
|---|---|---:|---|---|---|---|---|
| Title | heading | 24 pt | bold, deep blue | center | 0 / 8 pt | 1.0 | keep with next |
| Subtitle | body | 11 pt | regular, muted gray | center | 0 / 16 pt | 1.2 | no indent |
| Heading 1 | heading | 16 pt | bold, deep blue | left | 18 / 8 pt | 1.15 | real Chinese numbering `一、二、三……`; keep with next |
| Heading 2 | heading | 13 pt | bold, heading blue | left | 14 / 6 pt | 1.15 | keep with next |
| Heading 3 | heading | 11.5 pt | bold, primary ink | left | 10 / 4 pt | 1.15 | keep with next |
| Normal | body | 10.5 pt | regular, primary ink | justified | 0 / 6 pt | 1.5 | first line 7.4 mm |
| Body No Indent | body | 10.5 pt | regular, primary ink | justified | 0 / 6 pt | 1.5 | no indent |
| Lead | body | 11.5 pt | regular, deep blue | left | 0 / 10 pt | 1.35 | no indent |
| Quote | body | 10.5 pt | italic, deep blue | left | 8 / 8 pt | 1.35 | pale blue fill, left rule |
| Caption | body | 9 pt | regular, muted gray | center | 4 / 6 pt | 1.15 | keep with next |
| Note | body | 8.5 pt | regular, muted gray | left | 3 / 3 pt | 1.2 | no indent |
| Directory Title | body | 18 pt | bold, deep blue | center | 0 / 20 pt | 1.0 | keep with next |
| TOC 1 | body | 11 pt | bold, deep blue | left | 8 / 5 pt | 1.3 | dotted leader, page number right |
| TOC 2 | body | 10.5 pt | regular, primary ink | left | 4 / 4 pt | 1.3 | left indent 7 mm |
| TOC 3 | body | 10 pt | regular, muted gray | left | 3 / 3 pt | 1.25 | left indent 14 mm |

Bold is the default inline emphasis. Use italics for book titles, terms, and quotations. Do not use underline for general emphasis.

## 4. Lists

Use real Word numbering definitions.

Heading 1 uses a separate real numbering definition with `chineseCounting` and marker pattern `%1、`. Keep the heading text free of manually typed Arabic numbers or Chinese-number prefixes so numbering and TOC entries do not duplicate.

| List | Marker aligned | Text indent | Hanging | After | Line spacing |
|---|---:|---:|---:|---:|---:|
| Bullet level 0 | 6.4 mm | 12.7 mm | 6.3 mm | 4 pt | 1.35 |
| Decimal level 0 | 6.4 mm | 12.7 mm | 6.3 mm | 4 pt | 1.35 |

Wrapped lines align under item text. Never type bullet characters or manual numbers into paragraph text.

## 5. Tables

- Full table width: 9184 DXA.
- Table indent: 120 DXA.
- Use fixed DXA geometry; `tblW`, `tblGrid`, and every `tcW` must agree.
- Default three-column sample widths: 1500 / 3000 / 4684 DXA.
- Cell margins: top/bottom 100 DXA; start/end 120 DXA.
- Border: single, 4 eighth-points, `#B7C9DA`.
- Header: deep-blue fill, white bold 9.5 pt, centered vertically and horizontally.
- Body: 9.5 pt, 1.2 line spacing, 0 pt before / 2 pt after.
- Apply pale alternate-row fill beginning with the second data row.
- Center dates, status, short numbers, and codes; left-align narrative fields.
- Allow rows to expand. Never use fixed row heights that can clip content.
- Repeat the header row when a table spans pages.

## 6. Page furniture

- Running header: 8.5 pt muted gray; document label left, “格式规范示例” right; no border.
- Use the same running header on odd and even pages.
- Footer: centered 8.5 pt muted gray, real `PAGE` field.
- The Table of Contents must occupy a dedicated page with an explicit page break before and after it.
- Use Heading 1–3 as directory sources. In Word-operated workflows use a real TOC field and update it before delivery; in headless workflows use a deterministic static TOC with internal links.
- Use dotted leaders and right-aligned page numbers. Keep the directory to one page; if it overflows, reduce included levels or shorten headings before reducing text below 9.5 pt.
- A cover page is optional. When used, place the dedicated TOC page immediately after it.
- Keep a title with its subtitle and opening paragraph.

## 7. Format contract template

Before implementation, resolve:

```yaml
format_contract:
  authority: user | attached_template | default
  page: {paper: A4, orientation: portrait, margins_mm: [22, 24, 20, 24]}
  fonts: {all_roles: Microsoft YaHei}
  body: {size_pt: 10.5, line_spacing: 1.5, first_line_mm: 7.4}
  headings: {title_pt: 24, h1_pt: 16, h2_pt: 13, h3_pt: 11.5, h1_numbering: "chineseCounting %1、"}
  toc: {dedicated_page: true, levels: [1, 2, 3], page_numbers: right, leader: dots}
  lists: real_word_numbering
  tables: {width_dxa: 9184, fixed_geometry: true}
  substitutions: []
  named_overrides: []
```
