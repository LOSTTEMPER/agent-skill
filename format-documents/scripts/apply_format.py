#!/usr/bin/env python3
"""Apply the default style contract to an existing DOCX without rewriting text."""

from __future__ import annotations

import argparse
from pathlib import Path

from docx import Document

from format_core import configure_document, style_existing_tables


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--promote-first-paragraph",
        action="store_true",
        help="Apply Title to the first non-empty paragraph only when its role is confirmed.",
    )
    args = parser.parse_args()

    source = args.input.resolve()
    target = args.output.resolve()
    if source == target:
        raise SystemExit("Output must be a new path; in-place overwrite is not allowed.")

    doc = Document(source)
    configure_document(doc, header_label=source.stem)
    style_existing_tables(doc)

    if args.promote_first_paragraph:
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                paragraph.style = "Title"
                break

    target.parent.mkdir(parents=True, exist_ok=True)
    doc.save(target)
    print(f"Created {target}")


if __name__ == "__main__":
    main()

