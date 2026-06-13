"""Concrete image compression handlers.

Each handler is a single-responsibility class that compresses one image
format in-place while preserving the original file extension.
"""

import logging
from pathlib import Path

from PIL import Image

from compressors.image_handlers.base import BaseImageHandler
from config import DEFAULT_CONFIG

logger = logging.getLogger(__name__)


class JpegHandler(BaseImageHandler):
    """Compress JPEG images with configurable quality."""

    def compress(self, image_path: Path, quality: int) -> None:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            img.save(image_path, format="JPEG", quality=quality, optimize=True)

    @classmethod
    def supported_extensions(cls) -> set[str]:
        return {".jpg", ".jpeg"}


class PngHandler(BaseImageHandler):
    """Re-compress PNG images with maximum zlib compression."""

    def compress(self, image_path: Path, quality: int) -> None:
        with Image.open(image_path) as img:
            img.save(
                image_path,
                format="PNG",
                optimize=True,
                compress_level=DEFAULT_CONFIG.png_compress_level,
            )

    @classmethod
    def supported_extensions(cls) -> set[str]:
        return {".png"}


class WebpHandler(BaseImageHandler):
    """Compress WebP images with configurable quality."""

    def compress(self, image_path: Path, quality: int) -> None:
        with Image.open(image_path) as img:
            img.save(image_path, format="WEBP", quality=quality, optimize=True)

    @classmethod
    def supported_extensions(cls) -> set[str]:
        return {".webp"}


class TiffHandler(BaseImageHandler):
    """Re-compress TIFF images using lossless DEFLATE compression.

    Saves in native TIFF format to avoid extension/content mismatch
    that would corrupt DOCX internal references.
    """

    def compress(self, image_path: Path, quality: int) -> None:
        with Image.open(image_path) as img:
            img.save(image_path, format="TIFF", compression="tiff_deflate")

    @classmethod
    def supported_extensions(cls) -> set[str]:
        return {".tif", ".tiff"}


class GifHandler(BaseImageHandler):
    """Optimize static GIF images. Animated GIFs are skipped.

    Saves as GIF (not PNG) to preserve the original extension.
    """

    def compress(self, image_path: Path, quality: int) -> None:
        with Image.open(image_path) as img:
            if getattr(img, "is_animated", False):
                logger.debug("Skipping animated GIF: %s", image_path.name)
                return
            img.save(image_path, format="GIF", optimize=True)

    @classmethod
    def supported_extensions(cls) -> set[str]:
        return {".gif"}
