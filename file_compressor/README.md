# File Compressor

A simple Python project to compress PDF and DOCX files with a PyQt5 user interface.

## Features

- Compress PDF files using `pikepdf`.
- Compress DOCX files by optimizing images inside the document package.
- Simple GUI for selecting files, setting output folder, and running compression.

## Setup

1. Create a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Notes

- This tool works best with modern `.docx` files.
- PDF compression is handled via `pikepdf` and is most effective on documents containing images.
- `.doc` files are not directly supported.
