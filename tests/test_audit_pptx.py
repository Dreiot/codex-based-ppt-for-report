from __future__ import annotations

import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "codex-based-ppt-for-report" / "scripts" / "audit_pptx.py"
SPEC = importlib.util.spec_from_file_location("audit_pptx", SCRIPT)
audit_pptx = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(audit_pptx)


PRESENTATION = """<?xml version="1.0" encoding="UTF-8"?>
<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
 <p:sldIdLst>{slide_ids}</p:sldIdLst>
</p:presentation>
"""

RELATIONSHIPS = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
{relationships}
</Relationships>
"""


def slide_xml(text: str, vector_alt: str | None = None) -> str:
    picture = ""
    if vector_alt is not None:
        picture = f"""
        <p:pic>
          <p:nvPicPr><p:cNvPr id="2" name="Vector" descr="{vector_alt}"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr>
          <p:blipFill><a:blip r:embed="rIdVector"/></p:blipFill>
        </p:pic>"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
    <p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
      xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
      xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
      <p:cSld><p:spTree>
        <p:sp><p:nvSpPr/><p:spPr/><p:txBody><a:p><a:r><a:t>{text}</a:t></a:r></a:p></p:txBody></p:sp>
        {picture}
      </p:spTree></p:cSld>
    </p:sld>"""


def notes_xml(text: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
    <p:notes xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
      xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
      <p:cSld><p:spTree><p:sp><p:nvSpPr><p:cNvPr id="3" name="Notes"/><p:cNvSpPr/><p:nvPr><p:ph type="body"/></p:nvPr></p:nvSpPr><p:txBody><a:p><a:r><a:t>{text}</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld>
    </p:notes>"""


def write_package(
    path: Path,
    *,
    order: list[int],
    texts: dict[int, str],
    notes: dict[int, tuple[int, str]],
    vector_alt: dict[int, str] | None = None,
) -> None:
    vector_alt = vector_alt or {}
    slide_ids = "".join(
        f'<p:sldId id="{255 + index}" r:id="rId{index}"/>' for index, _ in enumerate(order, 1)
    )
    presentation_rels = "".join(
        f'<Relationship Id="rId{index}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{slide_number}.xml"/>'
        for index, slide_number in enumerate(order, 1)
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("ppt/presentation.xml", PRESENTATION.format(slide_ids=slide_ids))
        archive.writestr(
            "ppt/_rels/presentation.xml.rels",
            RELATIONSHIPS.format(relationships=presentation_rels),
        )
        for slide_number, text in texts.items():
            archive.writestr(
                f"ppt/slides/slide{slide_number}.xml",
                slide_xml(text, vector_alt.get(slide_number)),
            )
            note_number, note_text = notes[slide_number]
            slide_rels = [
                f'<Relationship Id="rIdNotes" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" Target="../notesSlides/notesSlide{note_number}.xml"/>'
            ]
            if slide_number in vector_alt:
                slide_rels.append(
                    '<Relationship Id="rIdVector" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image1.svg"/>'
                )
                archive.writestr("ppt/media/image1.svg", "<svg xmlns='http://www.w3.org/2000/svg'/>")
            archive.writestr(
                f"ppt/slides/_rels/slide{slide_number}.xml.rels",
                RELATIONSHIPS.format(relationships="".join(slide_rels)),
            )
            archive.writestr(f"ppt/notesSlides/notesSlide{note_number}.xml", notes_xml(note_text))


class AuditPptxTests(unittest.TestCase):
    def test_presentation_order_and_notes_relationships_are_followed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "reordered.pptx"
            write_package(
                path,
                order=[2, 1],
                texts={1: "Second", 2: "First"},
                notes={1: (8, "Second slide talk track with enough detail for delivery."), 2: (9, "First slide talk track. [Sources]")},
            )
            result = audit_pptx.audit(path, formula_slides=[], brief_note_slides=[1])
            self.assertEqual(result["source_notes"], [1])
            self.assertEqual(result["missing_notes"], [])

    def test_unrelated_vector_does_not_satisfy_formula_requirement(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "logo.pptx"
            write_package(
                path,
                order=[1],
                texts={1: "E = mc²"},
                notes={1: (4, "Explain the energy relation and its current evidence boundary.")},
                vector_alt={1: "Project logo"},
            )
            result = audit_pptx.audit(path, formula_slides=[1])
            self.assertEqual(result["vector_formula_slides"], [])
            self.assertEqual(result["untagged_vector_slides"], [1])
            self.assertEqual(result["text_only_formula_slides"], [1])

    def test_tagged_vector_satisfies_formula_requirement(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "equation.pptx"
            write_package(
                path,
                order=[1],
                texts={1: "Energy relation"},
                notes={1: (5, "Explain the equation from left to right and state its scope.")},
                vector_alt={1: "Equation: energy-identity"},
            )
            result = audit_pptx.audit(path, formula_slides=[1])
            self.assertEqual(result["vector_formula_slides"], [1])
            self.assertEqual(result["text_only_formula_slides"], [])

    def test_simple_equations_are_formula_candidates(self) -> None:
        self.assertTrue(audit_pptx.looks_like_display_formula("E = mc²"))
        self.assertTrue(audit_pptx.looks_like_display_formula("J = A + B"))
        self.assertTrue(audit_pptx.looks_like_display_formula("rho_w = 0"))

    def test_formula_none_does_not_excuse_formula_text(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "undeclared.pptx"
            write_package(
                path,
                order=[1],
                texts={1: "J = A + B"},
                notes={1: (6, "Explain why the two terms are combined and state the evidence boundary.")},
            )
            result = audit_pptx.audit(path, formula_slides=[])
            self.assertEqual(result["undeclared_formula_text_slides"], [1])

    def test_tagged_vector_does_not_excuse_text_formula_on_same_slide(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "mixed.pptx"
            write_package(
                path,
                order=[1],
                texts={1: "J = A + B"},
                notes={1: (7, "Explain the rendered equation and retain the current claim boundary.")},
                vector_alt={1: "Equation: objective"},
            )
            result = audit_pptx.audit(path, formula_slides=[1])
            self.assertEqual(result["formula_text_on_declared_slides"], [1])

    def test_tagged_vector_formula_must_be_declared(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "undeclared-vector.pptx"
            write_package(
                path,
                order=[1],
                texts={1: "Energy relation"},
                notes={1: (10, "Explain the rendered relation and the evidence boundary for this result.")},
                vector_alt={1: "Equation: energy"},
            )
            result = audit_pptx.audit(path, formula_slides=[])
            self.assertEqual(result["undeclared_formula_object_slides"], [1])

    def test_non_body_note_text_does_not_satisfy_notes(self) -> None:
        xml = b'''<p:notes xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><p:sp><p:nvSpPr><p:nvPr><p:ph type="sldNum"/></p:nvPr></p:nvSpPr><p:txBody><a:p><a:r><a:t>1</a:t></a:r></a:p></p:txBody></p:sp></p:notes>'''
        self.assertEqual(audit_pptx.notes_body_text(xml), "")


if __name__ == "__main__":
    unittest.main()
