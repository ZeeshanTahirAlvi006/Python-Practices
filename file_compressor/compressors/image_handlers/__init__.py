"""Image handler strategies for compressing individual image formats."""

from compressors.image_handlers.base import BaseImageHandler
from compressors.image_handlers.registry import (
    ImageHandlerRegistry,
    create_default_image_registry,
)

__all__ = [
    "BaseImageHandler",
    "ImageHandlerRegistry",
    "create_default_image_registry",
]
