"""Main application window — pure presentation layer.

This module is responsible ONLY for:
- Building and laying out widgets
- Handling user events (button clicks, file dialogs)
- Displaying results from the service layer

It does NOT contain any compression logic, validation, or path management.
"""

from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from config import DEFAULT_CONFIG
from services.compression_service import CompressionService


class CompressorWindow(QMainWindow):
    """PyQt5 GUI for selecting and compressing PDF / DOCX files.

    Parameters
    ----------
    service:
        The ``CompressionService`` instance that handles all compression
        orchestration.  Injected for testability and decoupling.
    """

    def __init__(self, service: CompressionService | None = None) -> None:
        super().__init__()
        self._service = service or CompressionService()

        self.setWindowTitle(DEFAULT_CONFIG.window_title)
        self.setMinimumSize(DEFAULT_CONFIG.window_min_width, DEFAULT_CONFIG.window_min_height)

        # Set window icon (title bar + taskbar).
        icon_path = Path(__file__).resolve().parent.parent / "icon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self._selected_files: list[str] = []
        self._output_folder = Path.home()

        # Build the file-dialog filter from live registry data.
        ext_list = " ".join(f"*{e}" for e in sorted(self._service.supported_extensions()))
        self._dialog_filter = f"Documents ({ext_list})"

        self._build_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # --- File management buttons ---
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add Files")
        add_btn.clicked.connect(self._on_add_files)
        remove_btn = QPushButton("Remove Selected")
        remove_btn.clicked.connect(self._on_remove_selected)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(remove_btn)
        layout.addLayout(btn_layout)

        # --- File list ---
        self._file_list = QListWidget()
        layout.addWidget(self._file_list)

        # --- Output folder row ---
        out_layout = QHBoxLayout()
        self._output_label = QLabel(str(self._output_folder))
        self._output_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        browse_btn = QPushButton("Choose Output Folder")
        browse_btn.clicked.connect(self._on_select_output_folder)
        out_layout.addWidget(QLabel("Output folder:"))
        out_layout.addWidget(self._output_label, stretch=1)
        out_layout.addWidget(browse_btn)
        layout.addLayout(out_layout)

        # --- Quality spinner ---
        qual_layout = QHBoxLayout()
        qual_layout.addWidget(QLabel("JPEG quality (DOCX images):"))
        self._quality_spin = QSpinBox()
        self._quality_spin.setRange(DEFAULT_CONFIG.image_quality_min, DEFAULT_CONFIG.image_quality_max)
        self._quality_spin.setValue(DEFAULT_CONFIG.gui_default_quality)
        qual_layout.addWidget(self._quality_spin)
        qual_layout.addStretch()
        layout.addLayout(qual_layout)

        # --- Compress button ---
        compress_btn = QPushButton("Compress Selected Files")
        compress_btn.clicked.connect(self._on_compress)
        layout.addWidget(compress_btn)

        # --- Status bar ---
        self._status = QLabel("Ready.")
        layout.addWidget(self._status)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_add_files(self) -> None:
        selected, _ = QFileDialog.getOpenFileNames(
            self, "Select Files", "", self._dialog_filter
        )
        if not selected:
            return

        supported = self._service.supported_extensions()
        for file_path in selected:
            path = Path(file_path)
            if path.suffix.lower() not in supported:
                continue
            if file_path not in self._selected_files:
                self._selected_files.append(file_path)
                self._file_list.addItem(QListWidgetItem(file_path))

        self._status.setText(f"{len(self._selected_files)} file(s) ready for compression.")

    def _on_remove_selected(self) -> None:
        for item in self._file_list.selectedItems():
            file_path = item.text()
            self._selected_files.remove(file_path)
            self._file_list.takeItem(self._file_list.row(item))
        self._status.setText(f"{len(self._selected_files)} file(s) remaining.")

    def _on_select_output_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(
            self, "Select Output Folder", str(self._output_folder)
        )
        if folder:
            self._output_folder = Path(folder)
            self._output_label.setText(str(self._output_folder))
            self._status.setText("Output folder selected.")

    def _on_compress(self) -> None:
        if not self._selected_files:
            QMessageBox.warning(
                self, "No files selected",
                "Please add PDF or DOCX files to compress.",
            )
            return

        quality = self._quality_spin.value()

        # Delegate entirely to the service layer.
        batch = self._service.compress_batch(
            self._selected_files, self._output_folder, quality
        )

        # Present results.
        if batch.has_errors:
            error_lines = "\n".join(
                f"{r.input_path.name}: {r.error}" for r in batch.errors
            )
            self._status.setText("Compression completed with warnings.")
            QMessageBox.warning(
                self, "Compression completed",
                f"Some files could not be compressed:\n{error_lines}",
            )
        else:
            self._status.setText("Compression completed successfully.")
            QMessageBox.information(
                self, "Done",
                f"Compressed {batch.success_count} file(s) into {self._output_folder}.",
            )
