"""Custom exception hierarchy for the file compressor application."""


class CompressionError(Exception):
    """Base exception for all compression-related failures."""


class UnsupportedFileTypeError(CompressionError):
    """Raised when the input file's extension is not supported."""

    def __init__(self, extension: str) -> None:
        self.extension = extension
        super().__init__(f"Unsupported file type: {extension}")


class InputFileError(CompressionError):
    """Raised when the input file does not exist or is not a regular file."""

    def __init__(self, path, reason: str = "not found") -> None:
        self.path = path
        super().__init__(f"Input file {reason}: {path}")


class OutputPathError(CompressionError):
    """Raised when the output path is invalid (e.g. same as input)."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ImageCompressionError(CompressionError):
    """Non-fatal error raised when a single image inside a document
    could not be compressed. The overall compression can still proceed."""

    def __init__(self, image_name: str, reason: str) -> None:
        self.image_name = image_name
        super().__init__(f"Failed to compress image {image_name}: {reason}")
