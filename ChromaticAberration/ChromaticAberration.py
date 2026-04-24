from krita import Extension, Krita
import importlib
import traceback

from . import ChromaticAberrationCore


class ChromaticAberrationExtension(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction(
            "chromatic_aberration",
            "Chromatic Aberration",
            "tools/scripts"
        )
        action.triggered.connect(self.run)

        # actionDebugLayer = window.createAction(
        #     "chromatic_aberration_debug_layer",
        #     "Chromatic Aberration: Debug Layer",
        #     "tools/scripts"
        # )
        # actionDebugLayer.triggered.connect(self.runDebugLayer)

    def run(self):
        try:
            importlib.reload(ChromaticAberrationCore)
            ChromaticAberrationCore.run()
        except Exception:
            traceback.print_exc()

    def runDebugLayer(self):
        try:
            importlib.reload(ChromaticAberrationCore)
            ChromaticAberrationCore.runDebugLayer()
        except Exception:
            traceback.print_exc()

app = Krita.instance()
extension = ChromaticAberrationExtension(parent=app)
app.addExtension(extension)