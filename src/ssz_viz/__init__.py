"""
SSZ Visualization Module

Modular plotting functions for SSZ metric analysis.

© 2025 Carmen Wrede & Lino Casu
"""

__version__ = "1.0.0"

from .plot_time_dilation import plot_time_dilation, gif_time_dilation
from .plot_metric_a import plot_metric_a, gif_metric_a
from .plot_curvature import plot_curvature, curvature_proxy
from .plot_comparison import plot_ssz_vs_gr

__all__ = [
    "plot_time_dilation",
    "gif_time_dilation",
    "plot_metric_a",
    "gif_metric_a",
    "plot_curvature",
    "curvature_proxy",
    "plot_ssz_vs_gr",
]
