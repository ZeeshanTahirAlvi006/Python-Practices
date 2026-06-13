"""DOCX compression strategy.

A .docx file is a ZIP archive containing XML and media files. This
compressor extracts the archive, compresses embedded images using the
image handler registry, and re-packs the archive with ZIP_DEFLATED.
"""

import logging
import os
import tempfile
import zipfile
from pathlib import Path

from compressors.base import BaseCompressor
from compressors.image_handlers.registry import (
    ImageHandlerRegistry,
    create_default_image_registry,
)

logger = logging.getLogger(__name__)


class DocxCompressor(BaseCompressor):
    """Compresses ``.docx`` files by optimizing embedded images."""

    def __init__(self, image_registry: ImageHandlerRegistry | None = None) -> None:
        self._image_registry = image_registry or create_default_image_registry()

    def compress(self, input_path: Path, output_path: Path, image_quality: int) -> Path:
        with tempfile.TemporaryDirectory() as tempdir:
            # 1. Extract the DOCX ZIP.
            with zipfile.ZipFile(input_path, "r") as zin:
                zin.extractall(tempdir)

            # 2. Compress images inside word/media/.
            media_dir = Path(tempdir, "word", "media")
            if media_dir.exists():
                self._compress_media(media_dir, image_quality)

            # 3. Re-pack into a new DOCX ZIP.
            self._zip_directory(Path(tempdir), output_path)

        logger.info("DOCX compressed: %s -> %s", input_path.name, output_path.name)
        return output_path

    @classmethod
    def supported_extensions(cls) -> set[str]:
        return {".docx"}

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _compress_media(self, media_dir: Path, quality: int) -> None:
        """Iterate over images in *media_dir* and compress each one."""
        supported = self._image_registry.supported_extensions()
        for image_path in media_dir.iterdir():
            if image_path.suffix.lower() in supported:
                self._image_registry.compress_image(image_path, quality)

    @staticmethod
    def _zip_directory(folder: Path, output_path: Path) -> None:
        """Re-create a ZIP archive from *folder* at *output_path*."""
        with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for root, _, files in os.walk(folder):
                root_path = Path(root)
                for file_name in files:
                    file_path = root_path / file_name
                    archive_name = file_path.relative_to(folder)
                    zout.write(file_path, archive_name.as_posix())
