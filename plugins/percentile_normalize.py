"""Percentile normalize — clip to a percentile window and rescale to [0, 1].

Pure NumPy (no optional dependencies). Useful for taming outliers before
display or downstream analysis.
"""

import numpy as np

from imswitch.improcess.processors.base import Processor
from imswitch.improcess.model.array_result import ArrayProcessingResult


class PercentileNormalizeProcessor(Processor):
    name = "Percentile normalize"
    id = "example.percentile-normalize"
    category = "User"
    kinds = ("image",)

    @property
    def applies_to(self):
        return lambda result: getattr(result.data, "ndim", 0) >= 2

    def make_param_widget(self, parent):
        from qtpy import QtWidgets

        widget = QtWidgets.QWidget(parent)
        layout = QtWidgets.QFormLayout(widget)

        low_spin = QtWidgets.QDoubleSpinBox()
        low_spin.setRange(0.0, 100.0)
        low_spin.setValue(1.0)
        low_spin.setSuffix(" %")
        layout.addRow("Low percentile:", low_spin)

        high_spin = QtWidgets.QDoubleSpinBox()
        high_spin.setRange(0.0, 100.0)
        high_spin.setValue(99.0)
        high_spin.setSuffix(" %")
        layout.addRow("High percentile:", high_spin)

        widget.get_values = lambda: {
            "low": float(low_spin.value()),
            "high": float(high_spin.value()),
        }
        return widget

    def apply(self, result, params):
        low = float(params.get("low", 1.0))
        high = float(params.get("high", 99.0))
        if high <= low:
            raise ValueError("High percentile must be greater than low percentile")

        data = np.asarray(result.data, dtype=np.float32)
        finite = data[np.isfinite(data)]
        lo = float(np.percentile(finite, low)) if finite.size else 0.0
        hi = float(np.percentile(finite, high)) if finite.size else 1.0
        span = hi - lo if hi > lo else 1.0
        normalized = np.clip((data - lo) / span, 0.0, 1.0)

        return ArrayProcessingResult(
            name=f"{result.name} (norm {low:g}-{high:g}%)",
            data=normalized,
            axis_labels=list(result.axis_labels),
            axis_scales=list(getattr(result, "axis_scales", None) or []) or None,
            scale_unit=getattr(result, "scale_unit", "px"),
            display_levels=(0.0, 1.0),
        )
