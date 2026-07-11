"""Median filter — edge-preserving denoise (drop-in ImProcess plugin)."""

from imswitch.improcess.processors.base import Processor
from imswitch.improcess.model.array_result import ArrayProcessingResult


class MedianFilterProcessor(Processor):
    name = "Median filter"
    id = "example.median-filter"
    category = "User"
    kinds = ("image",)

    @property
    def applies_to(self):
        return lambda result: getattr(result.data, "ndim", 0) >= 2

    def make_param_widget(self, parent):
        from qtpy import QtWidgets

        widget = QtWidgets.QWidget(parent)
        layout = QtWidgets.QFormLayout(widget)

        size_spin = QtWidgets.QSpinBox()
        size_spin.setRange(2, 99)
        size_spin.setValue(3)
        size_spin.setSuffix(" px")
        layout.addRow("Kernel size:", size_spin)

        widget.get_values = lambda: {"size": int(size_spin.value())}
        return widget

    def apply(self, result, params):
        size = int(params.get("size", 3))
        try:
            from scipy.ndimage import median_filter
        except Exception as exc:  # pragma: no cover
            raise RuntimeError("Median filter requires scipy") from exc

        data = result.data
        # Filter only the trailing (Y, X) plane so stacks filter per-plane.
        footprint = [1] * (data.ndim - 2) + [size, size]
        filtered = median_filter(data, size=footprint)

        return ArrayProcessingResult(
            name=f"{result.name} (median {size})",
            data=filtered,
            axis_labels=list(result.axis_labels),
            axis_scales=list(getattr(result, "axis_scales", None) or []) or None,
            scale_unit=getattr(result, "scale_unit", "px"),
        )
