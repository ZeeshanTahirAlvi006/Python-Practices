"""Registry that maps image file extensions to their compression handler."""

import logging
from pathlib import Path

from compressors.image_handlers.base import BaseImageHandler
from compressors.image_handlers.handlers import (
    GifHandler,
    JpegHandler,
    PngHandler,
    TiffHandler,
    WebpHandler,
)

logger = logging.getLogger(__name__)


class ImageHandlerRegistry:
    """Maps lowercase file extensions to ``BaseImageHandler`` instances.

    Usage::

        registry = create_default_image_registry()
        registry.compress_image(Path("photo.jpg"), quality=75)
    """

    def __init__(self) -> None:
        self._handlers: dict[str, BaseImageHandler] = {}

    def register(self, handler: BaseImageHandler) -> None:
        """Register a handler for all of its declared extensions."""
        for ext in handler.supported_extensions():
            self._handlers[ext.lower()] = handler

    def get_handler(self, extension: str) -> BaseImageHandler | None:
        """Return the handler for *extension*, or ``None`` if unsupported."""
        return self._handlers.get(extension.lower())

    def supported_extensions(self) -> set[str]:
        """Return every image extension that has a registered handler."""
        return set(self._handlers.keys())

    def compress_image(self, image_path: Path, quality: int) -> None:
        """Compress a single image in-place using the appropriate handler.

        If no handler is registered for the image's extension the file is
        left untouched and a debug message is logged.

        Raises
        ------
        Exception
            Re-raises any handler error after logging it so the caller can
            decide whether to treat it as fatal.
        """
        ext = image_path.suffix.lower()
        handler = self.get_handler(ext)

        if handler is None:
            logger.debug("No image handler for extension '%s', skipping: %s", ext, image_path.name)
            return

        try:
            handler.compress(image_path, quality)
        except Exception as exc:
            logger.warning("Failed to compress image %s: %s", image_path.name, exc)
            # Non-fatal: the DOCX can still be assembled with the original image.


def create_default_image_registry() -> ImageHandlerRegistry:
    """Create a registry pre-loaded with all built-in image handlers."""
    registry = ImageHandlerRegistry()
    registry.register(JpegHandler())
    registry.register(PngHandler())
    registry.register(WebpHandler())
    registry.register(TiffHandler())
    registry.register(GifHandler())
    return registry
