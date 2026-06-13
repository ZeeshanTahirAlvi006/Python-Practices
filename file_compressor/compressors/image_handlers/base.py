"""Abstract base class for image compression handlers."""

from abc import ABC, abstractmethod
from pathlib import Path


class BaseImageHandler(ABC):
    """Strategy interface for compressing a single image format in-place.

    Each concrete handler knows how to compress images of specific
    extensions while preserving the original file extension (critical
    for DOCX internal references).
    """

    @abstractmethod
    def compress(self, image_path: Path, quality: int) -> None:
        """Compress the image at *image_path* in-place.

        Parameters
        ----------
        image_path:
            Absolute path to the image file inside the extracted DOCX.
        quality:
            Lossy quality setting (1-100). Lossless formats may ignore this.
        """

    @classmethod
    @abstractmethod
    def supported_extensions(cls) -> set[str]:
        """Return the set of lowercase extensions this handler supports.

        Example: ``{".jpg", ".jpeg"}``
        """
