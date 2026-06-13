"""Compression service — orchestration layer.

This module is the single entry point for all compression operations.
It owns input validation, output path generation, error aggregation,
and result reporting.  The UI layer should depend only on this service.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from compressors.registry import CompressorRegistry, create_default_registry
from config import DEFAULT_CONFIG
from exceptions import InputFileError, OutputPathError

logger = logging.getLogger(__name__)


@dataclass
class CompressionResult:
    """Outcome of a single file compression attempt."""

    input_path: Path
    output_path: Path
    success: bool
    error: str | None = None


@dataclass
class BatchResult:
    """Aggregated outcome of compressing multiple files."""

    results: list[CompressionResult] = field(default_factory=list)

    @property
    def success_count(self) -> int:
        return sum(1 for r in self.results if r.success)

    @property
    def error_count(self) -> int:
        return sum(1 for r in self.results if not r.success)

    @property
    def errors(self) -> list[CompressionResult]:
        return [r for r in self.results if not r.success]

    @property
    def has_errors(self) -> bool:
        return self.error_count > 0


class CompressionService:
    """High-level orchestration for file compression.

    Parameters
    ----------
    registry:
        A ``CompressorRegistry`` mapping extensions to compressors.
        If *None*, the default registry with DOCX + PDF support is used.
    """

    def __init__(self, registry: CompressorRegistry | None = None) -> None:
        self._registry = registry or create_default_registry()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def supported_extensions(self) -> set[str]:
        """Return every file extension this service can compress."""
        return self._registry.supported_extensions()

    def compress_file(
        self,
        input_path: Path,
        output_path: Path,
        image_quality: int = DEFAULT_CONFIG.default_image_quality,
    ) -> CompressionResult:
        """Compress a single file.

        Validates inputs, resolves the correct compressor via the registry,
        and returns a ``CompressionResult`` (never raises on user errors).
        """
        input_path = Path(input_path)
        output_path = Path(output_path)

        try:
            self._validate(input_path, output_path)
            compressor = self._registry.get_compressor(input_path.suffix.lower())
            compressor.compress(input_path, output_path, image_quality)
            return CompressionResult(input_path, output_path, success=True)

        except Exception as exc:
            logger.error("Compression failed for %s: %s", input_path.name, exc)
            return CompressionResult(input_path, output_path, success=False, error=str(exc))

    def compress_batch(
        self,
        file_paths: list[str | Path],
        output_folder: Path,
        image_quality: int = DEFAULT_CONFIG.default_image_quality,
    ) -> BatchResult:
        """Compress a list of files into *output_folder*.

        Creates the output folder if it does not exist. Generates unique
        output filenames to avoid overwriting existing files.
        """
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)

        batch = BatchResult()
        for raw_path in file_paths:
            input_path = Path(raw_path)
            output_path = self.make_unique_output_path(input_path, output_folder)
            result = self.compress_file(input_path, output_path, image_quality)
            batch.results.append(result)

        return batch

    # ------------------------------------------------------------------
    # Output path helpers
    # ------------------------------------------------------------------

    @staticmethod
    def make_unique_output_path(input_path: Path, output_folder: Path) -> Path:
        """Generate a non-colliding output path inside *output_folder*.

        Strategy:
        1. Use the original filename.
        2. If it exists, append ``_compressed``.
        3. If that also exists, append ``_compressed_N`` (N = 2, 3, …).
        """
        candidate = output_folder / input_path.name
        if not candidate.exists():
            return candidate

        stem = input_path.stem
        suffix = input_path.suffix
        candidate = output_folder / f"{stem}_compressed{suffix}"
        if not candidate.exists():
            return candidate

        counter = 2
        while True:
            candidate = output_folder / f"{stem}_compressed_{counter}{suffix}"
            if not candidate.exists():
                return candidate
            counter += 1

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    @staticmethod
    def _validate(input_path: Path, output_path: Path) -> None:
        """Raise on invalid inputs."""
        if not input_path.exists():
            raise InputFileError(input_path, reason="not found")
        if not input_path.is_file():
            raise InputFileError(input_path, reason="is not a file")
        if input_path.resolve() == output_path.resolve():
            raise OutputPathError("Output path must be different from the input path.")
