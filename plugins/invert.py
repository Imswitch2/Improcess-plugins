"""Invert intensities — the minimal ImProcess drop-in analysis plugin."""

from imswitch.improcess.processors.base import Processor
from imswitch.improcess.model.array_result import ArrayProcessingResult


class InvertProcessor(Processor):
    name = "Invert"
    id = "example.invert"
    category = "User"
    kinds = ("image",)

    @property
    def applies_to(self):
        return lambda result: getattr(result.data, "ndim", 0) >= 2

    def make_param_widget(self, parent):
        from qtpy import QtWidgets

        widget = QtWidgets.QWidget(parent)
        widget.get_values = lambda: {}
        return widget

    def apply(self, result, params):
        data = result.data
        return ArrayProcessingResult(
            name=f"{result.name} (inverted)",
            data=data.max() - data,
            axis_labels=list(result.axis_labels),
            axis_scales=list(getattr(result, "axis_scales", None) or []) or None,
            scale_unit=getattr(result, "scale_unit", "px"),
        )
