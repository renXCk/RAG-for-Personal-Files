from pathlib import Path
import pypdf
import docx  


def load_pdf(path: Path) -> str:
    reader = pypdf.PdfReader(str(path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def load_docx(path: Path) -> str:
    doc = docx.Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs)

def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")

LOADERS = {
    ".pdf": load_pdf,
    ".docx": load_docx,
    ".txt": load_text,
    ".md": load_text,
}

def extract_files(root_folder: str):
    """Yields the filepath and the raw text for every supported file in the root folder."""
    root = Path(root_folder)
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in LOADERS:
            try:
                text = LOADERS[path.suffix.lower()](path)
                if text.strip():
                    yield str(path), text
                else:
                    print(f"[skip] {path} — no extractable text")
            except Exception as e:
                print(f"[error] {path}: {e}")

if __name__ == "__main__":
    import sys
    for filepath, text in extract_files(sys.argv[1]):
        print(f"--- {filepath} ({len(text)} chars) ---")
        print(text[:200], "...\n")