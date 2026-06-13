"""Desktop launcher for File Compressor.

This .pyw file is executed by pythonw.exe (no console window).
It sets the working directory to the project root so all relative
imports resolve correctly, then delegates to main().
"""

import os
import sys

# Ensure the working directory is the project folder,
# regardless of where the shortcut launches from.
project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_dir)
sys.path.insert(0, project_dir)

from main import main

main()
