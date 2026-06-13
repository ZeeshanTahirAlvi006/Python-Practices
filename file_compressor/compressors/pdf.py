"""PDF compression strategy.

Uses pikepdf to re-save the PDF with stream compression enabled,
which reduces file size for PDFs containing embedded images or
uncompressed content streams.
"""

import logging
from pathlib import Path

import pikepdf

from compressors.base import BaseCompressor

logger = logging.getLogger(__name__)


class PdfCompressor(BaseCompressor):
    """Compresses ``.pdf`` files using pikepdf stream optimization."""

    def compress(self, input_path: Path, output_path: Path, image_quality: int) -> Path:
        with pikepdf.open(input_path) as pdf:
            pdf.save(
                output_path,
                compress_streams=True,
                object_stream_mode=pikepdf.ObjectStreamMode.generate,
            )

        logger.info("PDF compressed: %s -> %s", input_path.name, output_path.name)
        return output_path

    @classmethod
    def supported_extensions(cls) -> set[str]:
        return {".pdf"}
