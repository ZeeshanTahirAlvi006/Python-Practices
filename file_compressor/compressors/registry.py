"""Registry that maps document file extensions to their compressor."""

from compressors.base import BaseCompressor
from compressors.docx import DocxCompressor
from compressors.pdf import PdfCompressor
from exceptions import UnsupportedFileTypeError


class CompressorRegistry:
    """Maps lowercase file extensions to ``BaseCompressor`` instances.

    Usage::

        registry = create_default_registry()
        compressor = registry.get_compressor(".pdf")
        compressor.compress(input_path, output_path, quality)
    """

    def __init__(self) -> None:
        self._compressors: dict[str, BaseCompressor] = {}

    def register(self, compressor: BaseCompressor) -> None:
        """Register a compressor for all of its declared extensions."""
        for ext in compressor.supported_extensions():
            self._compressors[ext.lower()] = compressor

    def get_compressor(self, extension: str) -> BaseCompressor:
        """Return the compressor for *extension*.

        Raises
        ------
        UnsupportedFileTypeError
            If no compressor is registered for the given extension.
        """
        ext = extension.lower()
        compressor = self._compressors.get(ext)
        if compressor is None:
            raise UnsupportedFileTypeError(ext)
        return compressor

    def supported_extensions(self) -> set[str]:
        """Return every document extension that has a registered compressor."""
        return set(self._compressors.keys())


def create_default_registry() -> CompressorRegistry:
    """Create a registry pre-loaded with all built-in document compressors."""
    registry = CompressorRegistry()
    registry.register(DocxCompressor())
    registry.register(PdfCompressor())
    return registry
