"""Centralized configuration for the file compressor application."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CompressionConfig:
    """Immutable configuration for compression settings."""

    # Image quality for lossy formats (JPEG, WebP) inside DOCX files.
    default_image_quality: int = 70

    # GUI quality spinner bounds.
    image_quality_min: int = 40
    image_quality_max: int = 95
    gui_default_quality: int = 75

    # PNG-specific: zlib compression level (0 = none, 9 = max).
    png_compress_level: int = 9

    # GUI window defaults.
    window_title: str = "PDF & Word File Compressor"
    window_min_width: int = 640
    window_min_height: int = 440

    # File dialog filter string.
    file_dialog_filter: str = "Documents (*.pdf *.docx)"


# Singleton default configuration used throughout the application.
DEFAULT_CONFIG = CompressionConfig()
