#!/usr/bin/env python
"""Main entry point for the SA application"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from sa.ui.app import main  # noqa: E402

if __name__ == "__main__":
    main()
