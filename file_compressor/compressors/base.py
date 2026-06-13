"""Abstract base class for document compressors."""

from abc import ABC, abstractmethod
from pathlib import Path


class BaseCompressor(ABC):
    """Strategy interface for compressing a specific document format.

    Each concrete compressor handles one family of file extensions
    (e.g. ``.docx``, ``.pdf``) and implements the ``compress`` method.
    """

    @abstractmethod
    def compress(self, input_path: Path, output_path: Path, image_quality: int) -> Path:
        """Compress the document at *input_path* and write to *output_path*.

        Parameters
        ----------
        input_path:
            Path to the source document (must exist).
        output_path:
            Path where the compressed document will be written.
        image_quality:
            Lossy quality setting (1-100) for embedded images.
            Compressors that don't contain images may ignore this.

        Returns
        -------
        Path
            The *output_path* on success.
        """

    @classmethod
    @abstractmethod
    def supported_extensions(cls) -> set[str]:
        """Return the set of lowercase extensions this compressor handles.

        Example: ``{".docx"}``
        """
