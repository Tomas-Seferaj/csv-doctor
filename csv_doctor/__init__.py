"""csv-doctor: find and fix common problems in messy CSV files."""
from .core import diagnose, clean, Report

__all__ = ["diagnose", "clean", "Report"]
__version__ = "1.0.0"
