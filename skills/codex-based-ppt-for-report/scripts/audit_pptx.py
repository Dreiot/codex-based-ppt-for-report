#!/usr/bin/env python3
"""Audit speaker notes and display-equation objects in a PPTX package."""

from __future__ import annotations

import argparse
import json
import posixpath
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree as ET


A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
DOC_R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
R_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"a": A_NS, "p": P_NS, "r": R_NS, "dr": DOC_R_NS}
PRODUCTION_NOTE_PATTERNS = (
    "项目切换页",
    "这里讲清楚",
    "重点强调",
    "用一句话交代",
)


def numbered_members(names: set[str], pattern: str) -> list[str]:
    matches = [name for name in names if re.fullmatch(pattern, name)]
    return sorted(matches, key=lambda name: int(re.search(r"(\d+)", name).group(1)))


def resolve_part(source_part: str, target: str) -> str:
    if target.startswith("/"):
        return posixpath.normpath(target).lstrip("/")
    return posixpath.normpath(posixpath.join(posixpath.dirname(source_part), target)).lstrip("/")


def relationships(archive: zipfile.ZipFile, names: set[str], source_part: str) -> dict[str, dict[str, str]]:
    source = PurePosixPath(source_part)
    rel_name = str(source.parent / "_rels" / f"{source.name}.rels")
    if rel_name not in names:
        return {}
    root = ET.fromstring(archive.read(rel_name))
    output: dict[str, dict[str, str]] = {}
    for rel in root.findall("r:Relationship", NS):
        rel_id = rel.attrib.get("Id")
        target = rel.attrib.get("Target", "")
        if rel_id:
            output[rel_id] = {
                "type": rel.attrib.get("Type", ""),
                "target": resolve_part(source_part, target),
            }
    return output


def slide_order(archive: zipfile.ZipFile, names: set[str]) -> list[str]:
    presentation = "ppt/presentation.xml"
    if presentation not in names:
        return numbered_members(names, r"ppt/slides/slide\d+\.xml")
    rels = relationships(archive, names, presentation)
    root = ET.fromstring(archive.read(presentation))
    slides: list[str] = []
    for node in root.findall(".//p:sldIdLst/p:sldId", NS):
        rel_id = node.attrib.get(f"{{{DOC_R_NS}}}id")
        target = rels.get(rel_id or "", {}).get("target")
        if target in names:
            slides.append(target)
    return slides or numbered_members(names, r"ppt/slides/slide\d+\.xml")


def text_runs(xml_bytes: bytes) -> list[str]:
    root = ET.fromstring(xml_bytes)
    return [node.text or "" for node in root.findall(".//a:t", NS)]


def notes_body_text(xml_bytes: bytes) -> str:
    root = ET.fromstring(xml_bytes)
    for shape in root.findall(".//p:sp", NS):
        placeholder = shape.find("./p:nvSpPr/p:nvPr/p:ph", NS)
        if placeholder is not None and placeholder.attrib.get("type") == "body":
            return "\n".join(node.text or "" for node in shape.findall(".//a:t", NS)).strip()
    return ""


def shape_texts(xml_bytes: bytes) -> list[str]:
    root = ET.fromstring(xml_bytes)
    values: list[str] = []
    for shape in root.findall(".//p:sp", NS):
        text = "".join(node.text or "" for node in shape.findall(".//a:t", NS)).strip()
        if text:
            values.append(text)
    return values


def looks_like_display_formula(text: str) -> bool:
    compact = re.sub(r"\s+", "", text)
    operators = sum(compact.count(token) for token in ("=", "+", "−", "-", "Σ", "∑", "‖", "∈"))
    structural = bool(re.search(r"\b(?:min|max|argmin|tr)\b", text, re.IGNORECASE))
    norm_or_sum = any(token in text for token in ("Σ", "∑", "‖", "||"))
    simple_equation = bool(re.fullmatch(r"[^=]{1,24}=[^=]{1,48}", compact))
    equation_signal = any(token in compact for token in ("_", "^", "²", "³", "+", "−", "-", "λ", "β", "η", "Φ", "Ω"))
    return structural or norm_or_sum or (simple_equation and equation_signal) or ("=" in compact and operators >= 3)


def slide_vector_pictures(
    archive: zipfile.ZipFile, names: set[str], slide_part: str
) -> tuple[list[str], list[str]]:
    rels = relationships(archive, names, slide_part)
    root = ET.fromstring(archive.read(slide_part))
    all_vectors: list[str] = []
    tagged_equations: list[str] = []
    for picture in root.findall(".//p:pic", NS):
        props = picture.find("./p:nvPicPr/p:cNvPr", NS)
        vector_targets: list[str] = []
        for node in picture.iter():
            rel_id = node.attrib.get(f"{{{DOC_R_NS}}}embed")
            target = rels.get(rel_id or "", {}).get("target", "")
            if target.lower().endswith((".svg", ".emf")):
                vector_targets.append(target)
        if not vector_targets:
            continue
        all_vectors.extend(vector_targets)
        metadata = " ".join(
            (props.attrib.get(key, "") if props is not None else "")
            for key in ("name", "title", "descr")
        ).lower()
        if "equation:" in metadata or "formula:" in metadata or "公式:" in metadata:
            tagged_equations.extend(vector_targets)
    return all_vectors, tagged_equations


def notes_part(archive: zipfile.ZipFile, names: set[str], slide_part: str) -> str | None:
    for rel in relationships(archive, names, slide_part).values():
        if rel["type"].endswith("/notesSlide") and rel["target"] in names:
            return rel["target"]
    return None


def audit(
    path: Path,
    formula_slides: list[int] | None = None,
    inline_math_slides: list[int] | None = None,
    brief_note_slides: list[int] | None = None,
    allow_untagged_vector_formulas: bool = False,
) -> dict[str, object]:
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        slides = slide_order(archive, names)
        missing_notes: list[int] = []
        source_notes: list[int] = []
        production_notes: list[int] = []
        short_notes: list[int] = []
        formula_text_candidates: list[int] = []
        text_only_formula_slides: list[int] = []
        vector_formula_slides: list[int] = []
        untagged_vector_slides: list[int] = []
        office_math_slides: list[int] = []

        for index, slide_name in enumerate(slides, 1):
            slide_xml = archive.read(slide_name)
            note_name = notes_part(archive, names, slide_name)
            if note_name is None:
                missing_notes.append(index)
            else:
                note = notes_body_text(archive.read(note_name))
                if not note:
                    missing_notes.append(index)
                if "[Sources]" in note:
                    source_notes.append(index)
                if any(pattern in note for pattern in PRODUCTION_NOTE_PATTERNS):
                    production_notes.append(index)
                if len(re.sub(r"\s+", "", note)) < 35:
                    short_notes.append(index)

            formula_like = any(looks_like_display_formula(text) for text in shape_texts(slide_xml))
            has_office_math = b"oMath" in slide_xml
            vectors, tagged_equations = slide_vector_pictures(archive, names, slide_name)
            if formula_like:
                formula_text_candidates.append(index)
            if has_office_math:
                office_math_slides.append(index)
            if tagged_equations:
                vector_formula_slides.append(index)
            if vectors and not tagged_equations:
                untagged_vector_slides.append(index)

        invalid_formula_slides: list[int] = []
        inline_math_slides = inline_math_slides or []
        brief_note_slides = brief_note_slides or []
        invalid_inline_math_slides = [
            slide for slide in inline_math_slides if slide < 1 or slide > len(slides)
        ]
        invalid_brief_note_slides = [
            slide for slide in brief_note_slides if slide < 1 or slide > len(slides)
        ]
        overlapping_formula_inline_slides: list[int] = []
        formula_text_on_declared_slides: list[int] = []
        undeclared_formula_text_slides: list[int] = []
        undeclared_formula_object_slides: list[int] = []
        if formula_slides is not None:
            overlapping_formula_inline_slides = sorted(set(formula_slides) & set(inline_math_slides))
            for slide_number in formula_slides:
                if slide_number < 1 or slide_number > len(slides):
                    invalid_formula_slides.append(slide_number)
                    continue
                has_vector = slide_number in vector_formula_slides
                if allow_untagged_vector_formulas and slide_number in untagged_vector_slides:
                    has_vector = True
                if slide_number not in office_math_slides and not has_vector:
                    text_only_formula_slides.append(slide_number)
            formula_text_on_declared_slides = sorted(
                set(formula_text_candidates) & set(formula_slides)
            )
            undeclared_formula_text_slides = sorted(
                set(formula_text_candidates) - set(formula_slides) - set(inline_math_slides)
            )
            undeclared_formula_object_slides = sorted(
                (set(office_math_slides) | set(vector_formula_slides)) - set(formula_slides)
            )

        unapproved_short_notes = sorted(set(short_notes) - set(brief_note_slides))

        return {
            "path": str(path),
            "slide_count": len(slides),
            "missing_notes": missing_notes,
            "source_notes": source_notes,
            "production_instruction_notes": production_notes,
            "short_notes": short_notes,
            "brief_note_slides": brief_note_slides,
            "invalid_brief_note_slides": invalid_brief_note_slides,
            "unapproved_short_notes": unapproved_short_notes,
            "formula_text_candidates": formula_text_candidates,
            "declared_formula_slides": formula_slides,
            "invalid_formula_slides": invalid_formula_slides,
            "inline_math_slides": inline_math_slides,
            "invalid_inline_math_slides": invalid_inline_math_slides,
            "overlapping_formula_inline_slides": overlapping_formula_inline_slides,
            "formula_text_on_declared_slides": formula_text_on_declared_slides,
            "undeclared_formula_text_slides": undeclared_formula_text_slides,
            "undeclared_formula_object_slides": undeclared_formula_object_slides,
            "office_math_slides": office_math_slides,
            "vector_formula_slides": vector_formula_slides,
            "untagged_vector_slides": untagged_vector_slides,
            "text_only_formula_slides": text_only_formula_slides,
        }


def parse_slide_list(value: str | None) -> list[int] | None:
    if value is None:
        return None
    if value.strip().lower() == "none":
        return []
    try:
        values = sorted({int(item.strip()) for item in value.split(",") if item.strip()})
    except ValueError as exc:
        raise argparse.ArgumentTypeError("slide list must be comma-separated integers or 'none'") from exc
    if not values:
        raise argparse.ArgumentTypeError("slide list must be comma-separated integers or 'none'")
    return values


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--allow-sources", action="store_true")
    parser.add_argument(
        "--formula-slides",
        type=parse_slide_list,
        required=True,
        help="Comma-separated presentation-order slide numbers, or 'none'.",
    )
    parser.add_argument(
        "--inline-math-slides",
        type=parse_slide_list,
        default=[],
        help="Slides intentionally containing only simple inline math text, or 'none'.",
    )
    parser.add_argument(
        "--brief-note-slides",
        type=parse_slide_list,
        default=[],
        help="Title or divider slides allowed to have notes shorter than 35 characters, or 'none'.",
    )
    parser.add_argument("--allow-untagged-vector-formulas", action="store_true")
    args = parser.parse_args()

    if not args.pptx.is_file():
        parser.error(f"PPTX does not exist: {args.pptx}")

    try:
        result = audit(
            args.pptx,
            args.formula_slides,
            args.inline_math_slides,
            args.brief_note_slides,
            args.allow_untagged_vector_formulas,
        )
    except (zipfile.BadZipFile, ET.ParseError) as exc:
        print(f"ERROR: invalid PPTX package: {exc}", file=sys.stderr)
        return 2

    failures: list[str] = []
    if result["missing_notes"]:
        failures.append("missing speaker notes")
    if result["source_notes"] and not args.allow_sources:
        failures.append("[Sources] blocks present in speaker notes")
    if result["production_instruction_notes"]:
        failures.append("production instructions present in speaker notes")
    if result["invalid_brief_note_slides"]:
        failures.append("brief-note slide is outside the presentation")
    if result["unapproved_short_notes"]:
        failures.append("speaker notes are too short for a usable talk track")
    if result["formula_text_candidates"] and result["declared_formula_slides"] is None:
        failures.append("formula candidates found but --formula-slides was not declared")
    if result["invalid_formula_slides"]:
        failures.append("declared formula slide is outside the presentation")
    if result["invalid_inline_math_slides"]:
        failures.append("inline-math slide is outside the presentation")
    if result["overlapping_formula_inline_slides"]:
        failures.append("a slide cannot be both a display-formula and inline-math exception")
    if result["formula_text_on_declared_slides"]:
        failures.append("declared formula slide still contains text-box formula candidates")
    if result["undeclared_formula_text_slides"]:
        failures.append("formula text candidates are neither declared formulas nor inline-math exceptions")
    if result["undeclared_formula_object_slides"]:
        failures.append("Office Math or tagged vector formulas are missing from --formula-slides")
    if result["text_only_formula_slides"]:
        failures.append("display formulas approximated with text only")

    result["failures"] = failures
    result["passed"] = not failures
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for key, value in result.items():
            print(f"{key}: {value}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
