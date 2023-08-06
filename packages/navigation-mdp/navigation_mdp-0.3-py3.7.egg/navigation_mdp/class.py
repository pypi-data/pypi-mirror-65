import numpy as np
"""
Is
"""
class XYClassDistribution:

    def __init__(self, layout, marker_to_class_id):
        self.layout = layout
        self.marker_to_class_id = marker_to_class_id
        self.class_layout = self._create_layout(self.layout)

    def _create_layout(self, layout):
        class_layout = []
        for line in layout:
            class_layout.append([])
            for sym in line:
                class_layout[-1].append(self.marker_to_class_id[sym])
        return class_layout

    def __call__(self):
        return np.asarray(self.class_layout)