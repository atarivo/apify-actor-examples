"""Printable Puzzle PDF Generator: one PDF (puzzles + answer key), one dataset row per puzzle.
The first 3 puzzles of every run are free, so this example costs nothing in events.

    pip install apify-client && export APIFY_TOKEN=...
    python printable_puzzle_pdf_generator.py      # writes sudoku.pdf
"""
import os
import pathlib

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("atarivo/printable-puzzle-pdf-generator").call(
    run_input={"puzzle": "sudoku", "count": 3, "difficulty": "hard", "seed": 42},
)
rows = list(client.dataset(run.default_dataset_id).iterate_items())
for r in rows:
    print(r["title"], "| page", r["page"], "| answer page", r["answer_page"])
rec = client.key_value_store(run.default_key_value_store_id).get_record(rows[0]["pdf_key"])
pathlib.Path("sudoku.pdf").write_bytes(rec["value"])
print(f"sudoku.pdf: {rows[0]['pdf_pages']} pages, {pathlib.Path('sudoku.pdf').stat().st_size} bytes")
