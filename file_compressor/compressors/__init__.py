"""Document compressor strategies and registry."""

from compressors.base import BaseCompressor
from compressors.docx import DocxCompressor
from compressors.pdf import PdfCompressor
from compressors.registry import CompressorRegistry, create_default_registry

__all__ = [
    "BaseCompressor",
    "CompressorRegistry",
    "DocxCompressor",
    "PdfCompressor",
    "create_default_registry",
]
