"""ESG report PDF -> BERT-ready structured chunks.

Part of the GreenBERT pipeline. This module performs PDF ingestion and text
normalization only. It does not classify, label, filter, or run any ML
models. Output is a JSON file consumed by downstream BERT-family models.

CLI:
    python pdf_to_chunks.py <input.pdf> <output.json>
        [--company NAME] [--year YYYY] [--report-type TYPE]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from statistics import median

import fitz  # PyMuPDF
import pdfplumber
from transformers import AutoTokenizer

import nltk
from nltk.tokenize import sent_tokenize


# Ensure the sentence tokenizer is available. Newer NLTK uses punkt_tab.
def _ensure_punkt() -> None:
    for resource in ("punkt_tab", "punkt"):
        try:
            nltk.data.find(f"tokenizers/{resource}")
            return
        except LookupError:
            try:
                nltk.download(resource, quiet=True)
                nltk.data.find(f"tokenizers/{resource}")
                return
            except Exception:
                continue


_TOKENIZER = None


def _get_tokenizer():
    global _TOKENIZER
    if _TOKENIZER is None:
        _TOKENIZER = AutoTokenizer.from_pretrained("bert-base-uncased")
    return _TOKENIZER


def _n_tokens(text: str) -> int:
    return len(_get_tokenizer().encode(text, add_special_tokens=False))


CAPTION_RE = re.compile(r"^\s*(Figure|Table|Chart|Exhibit)\s+\d", re.IGNORECASE)
LIST_ITEM_RE = re.compile(r"^\s*(?:[-•·●▪◦\*]|\d+[.)]|[a-zA-Z][.)])\s+")
PAGE_NUMBER_RE = re.compile(r"^\s*(?:[-–—]\s*)?\d{1,4}(?:\s*[-–—])?\s*$")
WHITESPACE_RE = re.compile(r"\s+")


# -- Sanity checks ------------------------------------------------------------

def _detect_scanned(doc) -> bool:
    """True if >=50% of pages return <20 chars of text."""
    n = len(doc)
    if n == 0:
        return False
    sparse = 0
    for page in doc:
        if len(page.get_text("text").strip()) < 20:
            sparse += 1
    return (sparse / n) >= 0.5


# -- Block extraction ---------------------------------------------------------

def _extract_blocks(page) -> list[dict]:
    """Per-page block extraction with bbox and font sizes."""
    out: list[dict] = []
    page_dict = page.get_text("dict")
    for block in page_dict.get("blocks", []):
        if block.get("type") != 0:  # 0 == text block
            continue
        text_lines: list[str] = []
        font_sizes: list[float] = []
        for line in block.get("lines", []):
            spans = line.get("spans", [])
            line_text = "".join(span.get("text", "") for span in spans)
            if line_text.strip():
                text_lines.append(line_text)
            for span in spans:
                size = span.get("size")
                if size:
                    font_sizes.append(float(size))
        text = "\n".join(text_lines).strip()
        if not text:
            continue
        out.append({
            "text": text,
            "bbox": [float(v) for v in block.get("bbox", (0.0, 0.0, 0.0, 0.0))],
            "max_font": max(font_sizes) if font_sizes else 0.0,
            "median_font": median(font_sizes) if font_sizes else 0.0,
        })
    return out


def _page_median_font(blocks: list[dict]) -> float:
    sizes = [b["median_font"] for b in blocks if b["median_font"] > 0]
    return median(sizes) if sizes else 10.0


def _classify_block(block: dict, page_median_font_size: float) -> str:
    text = block["text"].strip()
    first_line = text.split("\n", 1)[0]
    if CAPTION_RE.match(first_line):
        return "caption"
    if page_median_font_size > 0 and block["max_font"] >= 1.2 * page_median_font_size:
        # Headings are usually short. Avoid mis-labeling a paragraph that
        # happens to contain a single oversized word (e.g., a pull-quote).
        if len(text) < 200 and "\n" not in text.strip():
            return "heading"
        if len(text) < 120:
            return "heading"
    if LIST_ITEM_RE.match(first_line):
        return "list_item"
    return "paragraph"


def _clean_text(s: str) -> str:
    return WHITESPACE_RE.sub(" ", s).strip()


# -- Chunking -----------------------------------------------------------------

def _chunk_text(text: str, max_tokens: int = 480) -> tuple[list[str], list[str]]:
    """Token-aware chunking on sentence boundaries. Returns (chunks, warnings)."""
    warnings: list[str] = []
    if not text.strip():
        return [], warnings
    if _n_tokens(text) <= max_tokens:
        return [text], warnings

    try:
        sentences = sent_tokenize(text)
    except Exception:
        sentences = re.split(r"(?<=[.!?])\s+", text)

    tokenizer = _get_tokenizer()
    chunks: list[str] = []
    current: list[str] = []
    current_tokens = 0

    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        st = _n_tokens(sent)
        if st > max_tokens:
            if current:
                chunks.append(" ".join(current))
                current, current_tokens = [], 0
            warnings.append(
                f"sentence exceeded {max_tokens} tokens ({st}); "
                f"split on tokens with 50-token overlap"
            )
            ids = tokenizer.encode(sent, add_special_tokens=False)
            step = max(1, max_tokens - 50)
            i = 0
            while i < len(ids):
                window = ids[i:i + max_tokens]
                if not window:
                    break
                chunks.append(tokenizer.decode(window, skip_special_tokens=True))
                if i + max_tokens >= len(ids):
                    break
                i += step
            continue

        if current and current_tokens + st > max_tokens:
            chunks.append(" ".join(current))
            current = [sent]
            current_tokens = st
        else:
            current.append(sent)
            current_tokens += st

    if current:
        chunks.append(" ".join(current))
    return chunks, warnings


# -- Tables -------------------------------------------------------------------

def _table_to_markdown(rows: list[list]) -> str:
    if not rows:
        return ""
    norm = [
        ["" if c is None else str(c).replace("\n", " ").strip() for c in row]
        for row in rows
    ]
    width = max(len(r) for r in norm)
    norm = [r + [""] * (width - len(r)) for r in norm]
    header = norm[0]
    body = norm[1:]
    lines = ["| " + " | ".join(header) + " |",
             "| " + " | ".join(["---"] * width) + " |"]
    for row in body:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def _split_table_by_rows(rows: list[list], max_tokens: int = 480) -> tuple[list[str], list[str]]:
    """Split a table row-wise, replicating the header row in each chunk."""
    warnings: list[str] = []
    if not rows:
        return [], warnings

    full_md = _table_to_markdown(rows)
    if _n_tokens(full_md) <= max_tokens:
        return [full_md], warnings

    header = rows[0]
    body = rows[1:]
    chunks: list[str] = []
    current = [header]
    for row in body:
        candidate = current + [row]
        if _n_tokens(_table_to_markdown(candidate)) > max_tokens and len(current) > 1:
            chunks.append(_table_to_markdown(current))
            current = [header, row]
            # Pathological: a single row + header still exceeds the limit.
            if _n_tokens(_table_to_markdown(current)) > max_tokens:
                warnings.append(
                    f"table row exceeded {max_tokens} tokens after header; "
                    "kept as single oversized chunk"
                )
        else:
            current.append(row)
    if len(current) > 1:
        chunks.append(_table_to_markdown(current))
    return chunks, warnings


def _extract_tables_pdfplumber(pdf_path: str) -> dict[int, list[dict]]:
    """Extract tables per page index (0-based) using pdfplumber."""
    out: dict[int, list[dict]] = defaultdict(list)
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                try:
                    found = page.find_tables()
                except Exception:
                    continue
                for t in found:
                    try:
                        data = t.extract()
                    except Exception:
                        continue
                    if not data:
                        continue
                    if not any(any((c or "").strip() for c in row) for row in data):
                        continue
                    bbox = list(t.bbox) if getattr(t, "bbox", None) else None
                    out[i].append({"data": data, "bbox": bbox})
    except Exception:
        # Tables are best-effort; PyMuPDF text path still runs.
        pass
    return out


# -- Header/footer cleanup ----------------------------------------------------

def _bbox_in_band(bbox, page_height, ratio: float = 0.12) -> bool:
    if page_height <= 0 or not bbox:
        return False
    y0, y1 = bbox[1], bbox[3]
    return y1 < page_height * ratio or y0 > page_height * (1.0 - ratio)


def _clean_headers_footers(
    pages_blocks: list[list[dict]],
    page_heights: list[float],
) -> list[list[dict]]:
    """Remove repeated short text in top/bottom band and standalone page numbers."""
    n_pages = len(pages_blocks)
    if n_pages < 4:
        # Still strip standalone page numbers even on small docs.
        return [_strip_page_numbers(blocks, page_heights[i] if i < len(page_heights) else 0)
                for i, blocks in enumerate(pages_blocks)]

    counter: Counter = Counter()
    for i, blocks in enumerate(pages_blocks):
        ph = page_heights[i] if i < len(page_heights) else 0.0
        seen_on_page = set()
        for b in blocks:
            text = _clean_text(b["text"])
            if not text or len(text) > 80:
                continue
            if not _bbox_in_band(b["bbox"], ph):
                continue
            if text in seen_on_page:
                continue
            seen_on_page.add(text)
            counter[text] += 1

    threshold = max(2, int(n_pages * 0.30))
    repeated = {t for t, c in counter.items() if c >= threshold}

    cleaned: list[list[dict]] = []
    for i, blocks in enumerate(pages_blocks):
        ph = page_heights[i] if i < len(page_heights) else 0.0
        keep: list[dict] = []
        for b in blocks:
            text = _clean_text(b["text"])
            if _bbox_in_band(b["bbox"], ph):
                if text in repeated:
                    continue
                if PAGE_NUMBER_RE.match(text):
                    continue
            keep.append(b)
        cleaned.append(keep)
    return cleaned


def _strip_page_numbers(blocks: list[dict], page_height: float) -> list[dict]:
    keep = []
    for b in blocks:
        text = _clean_text(b["text"])
        if _bbox_in_band(b["bbox"], page_height) and PAGE_NUMBER_RE.match(text):
            continue
        keep.append(b)
    return keep


# -- Geometry helpers ---------------------------------------------------------

def _bbox_iou(a, b) -> float:
    if not a or not b:
        return 0.0
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    ix0, iy0 = max(ax0, bx0), max(ay0, by0)
    ix1, iy1 = min(ax1, bx1), min(ay1, by1)
    iw, ih = max(0.0, ix1 - ix0), max(0.0, iy1 - iy0)
    inter = iw * ih
    if inter == 0:
        return 0.0
    a_area = max(0.0, ax1 - ax0) * max(0.0, ay1 - ay0)
    b_area = max(0.0, bx1 - bx0) * max(0.0, by1 - by0)
    union = a_area + b_area - inter
    return inter / union if union > 0 else 0.0


def _bbox_contained(inner, outer, tol: float = 2.0) -> bool:
    if not inner or not outer:
        return False
    return (inner[0] >= outer[0] - tol and inner[1] >= outer[1] - tol
            and inner[2] <= outer[2] + tol and inner[3] <= outer[3] + tol)


# -- Main entry ---------------------------------------------------------------

def extract_report(pdf_path: str, metadata: dict | None = None) -> dict:
    pdf_path = str(Path(pdf_path).resolve())
    if not Path(pdf_path).exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    metadata = metadata or {}
    warnings: list[str] = []

    _ensure_punkt()
    _get_tokenizer()  # warm cache, surface download errors early

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise RuntimeError(f"Failed to open PDF '{pdf_path}': {e}") from e

    try:
        if doc.is_encrypted and not doc.authenticate(""):
            raise RuntimeError(
                "PDF is encrypted and no password was supplied. "
                "Decrypt the file before re-running."
            )
        if _detect_scanned(doc):
            raise RuntimeError(
                "PDF appears to be scanned. OCR pipeline not implemented. "
                "Use a text-based PDF."
            )

        total_pages = len(doc)

        pages_blocks: list[list[dict]] = []
        page_heights: list[float] = []
        for page_idx, page in enumerate(doc):
            try:
                blocks = _extract_blocks(page)
                pages_blocks.append(blocks)
                page_heights.append(float(page.rect.height))
                if not blocks:
                    warnings.append(f"page {page_idx + 1}: text extraction returned empty")
            except Exception as e:
                pages_blocks.append([])
                page_heights.append(0.0)
                warnings.append(f"page {page_idx + 1}: extraction error: {e}")

        pages_blocks = _clean_headers_footers(pages_blocks, page_heights)
        tables_by_page = _extract_tables_pdfplumber(pdf_path)

        chunks: list[dict] = []
        chunk_idx = 1
        current_heading: str | None = None  # carries across pages

        for page_idx in range(total_pages):
            blocks = pages_blocks[page_idx]
            page_tables = tables_by_page.get(page_idx, [])
            page_median = _page_median_font(blocks) if blocks else 10.0

            # Drop blocks whose bbox is contained within (or heavily overlapping)
            # a detected table — pdfplumber owns those.
            filtered_blocks = []
            for b in blocks:
                covered = False
                for t in page_tables:
                    tbbox = t.get("bbox")
                    if not tbbox:
                        continue
                    if _bbox_contained(b["bbox"], tbbox) or _bbox_iou(b["bbox"], tbbox) > 0.3:
                        covered = True
                        break
                if not covered:
                    filtered_blocks.append(b)

            # Reading-order interleaving of blocks and tables by y-position.
            items: list[tuple[str, float, dict]] = []
            for b in filtered_blocks:
                items.append(("block", b["bbox"][1], b))
            for t in page_tables:
                y = t["bbox"][1] if t.get("bbox") else 0.0
                items.append(("table", y, t))
            items.sort(key=lambda x: (round(x[1], 1), 0))

            for kind, _, item in items:
                if kind == "block":
                    text = _clean_text(item["text"])
                    if not text:
                        continue
                    ctype = _classify_block(item, page_median)
                    if ctype == "heading":
                        current_heading = text

                    pieces, warn = _chunk_text(text)
                    for w in warn:
                        warnings.append(f"page {page_idx + 1}: {w}")
                    for piece in pieces:
                        if not piece.strip():
                            continue
                        chunks.append({
                            "chunk_id": f"chunk_{chunk_idx:04d}",
                            "page_number": page_idx + 1,
                            "content_type": ctype,
                            "text": piece,
                            "token_count": _n_tokens(piece),
                            "bbox": item["bbox"],
                            "heading_context": (
                                current_heading if ctype != "heading" else None
                            ),
                        })
                        chunk_idx += 1
                else:  # table
                    table_chunks, warn = _split_table_by_rows(item["data"])
                    for w in warn:
                        warnings.append(f"page {page_idx + 1}: {w}")
                    for piece in table_chunks:
                        chunks.append({
                            "chunk_id": f"chunk_{chunk_idx:04d}",
                            "page_number": page_idx + 1,
                            "content_type": "table",
                            "text": piece,
                            "token_count": _n_tokens(piece),
                            "bbox": list(item["bbox"]) if item.get("bbox") else None,
                            "heading_context": current_heading,
                        })
                        chunk_idx += 1

        result = {
            "report_metadata": {
                "source_pdf": pdf_path,
                "company": metadata.get("company"),
                "year": metadata.get("year"),
                "report_type": metadata.get("report_type"),
                "total_pages": total_pages,
                "extraction_timestamp": datetime.now(timezone.utc).isoformat(),
            },
            "chunks": chunks,
            "extraction_warnings": warnings,
        }
        return result
    finally:
        doc.close()


# -- CLI ----------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="ESG report PDF -> BERT-ready structured chunks (JSON).",
    )
    ap.add_argument("pdf", help="Input PDF path (text-based, not scanned).")
    ap.add_argument("output", help="Output JSON path.")
    ap.add_argument("--company", default=None)
    ap.add_argument("--year", type=int, default=None)
    ap.add_argument("--report-type", dest="report_type", default=None)
    args = ap.parse_args(argv)

    metadata = {
        "company": args.company,
        "year": args.year,
        "report_type": args.report_type,
    }

    try:
        result = extract_report(args.pdf, metadata)
    except (FileNotFoundError, RuntimeError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))

    n_chunks = len(result["chunks"])
    n_warn = len(result["extraction_warnings"])
    print(f"wrote {n_chunks} chunks to {out_path} ({n_warn} warnings)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
