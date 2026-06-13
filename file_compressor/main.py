"""Entry point for the File Compressor application."""

import logging
import sys

from PyQt5.QtWidgets import QApplication

from services.compression_service import CompressionService
from ui.main_window import CompressorWindow

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


def main() -> None:
    app = QApplication(sys.argv)

    service = CompressionService()
    window = CompressorWindow(service=service)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
