from krita import Krita, InfoObject, Selection
from enum import StrEnum
from PyQt5.QtGui import QColor

CLONEABLE_NODE_TYPES = {
    "paintlayer",
    "grouplayer",
    "filelayer",
    "filterlayer",
    "filllayer",
    "clonelayer",
    "vectorlayer",
}

class BlendingMode(StrEnum):
    Addition = 'add', # [sic!] it is not "addition"
    Multiply = 'multiply',
    Subtract = 'subtract',


def run():
    
    print("Chromatic Aberration: script starts")
    app = Krita.instance()
    currentDoc = app.activeDocument()
    if currentDoc is None:
        print("Chromatic Aberration: no active document")
        return None
    currentLayer = currentDoc.activeNode()
    if currentLayer is None:
        print("Chromatic Aberration: no active layer")
        return None

    if currentLayer.type() not in CLONEABLE_NODE_TYPES:
        print(f"Chromatic Aberration: Active node is not cloneable: {currentLayer.name()} ({currentLayer.type()})")
        return None

    chromaticAberrationGroupLayer = currentDoc.createGroupLayer("Chromatic Aberration")
    chromaticAberrationGroupLayer.setPassThroughMode(True)
    currentLayer.parentNode().addChildNode(chromaticAberrationGroupLayer, currentLayer)
    
    colorOneGroupLayer = currentDoc.createGroupLayer("Color 1")
    colorOneGroupLayer.setPassThroughMode(True)
    chromaticAberrationGroupLayer.addChildNode(colorOneGroupLayer, None)

    shiftedGroupLayer = currentDoc.createGroupLayer("Shifted")
    shiftedGroupLayer.setBlendingMode(BlendingMode.Addition)
    colorOneGroupLayer.addChildNode(shiftedGroupLayer, None)

    extractedColorGroupLayer = currentDoc.createGroupLayer("Extracted Color")
    shiftedGroupLayer.addChildNode(extractedColorGroupLayer, None)
    
    cloneOfInputLayer = currentDoc.createCloneLayer("Clone of Input", currentLayer)
    extractedColorGroupLayer.addChildNode(cloneOfInputLayer, None)

    fillLayerConfig = InfoObject()
    fillLayerConfig.setProperty("color", QColor(255, 0, 0, 255))
    fillLayerSelection = Selection()
    fillLayerSelection.select(0, 0, currentDoc.width(), currentDoc.height(), 255)
    fillLayer = currentDoc.createFillLayer("Fill Layer", "color", fillLayerConfig, fillLayerSelection)
    fillLayer.setBlendingMode(BlendingMode.Multiply)
    extractedColorGroupLayer.addChildNode(fillLayer, None)

    filterLayerFilter = app.filter("crosschannel")
    filterLayerSelection = Selection()
    filterLayerSelection.select(0, 0, currentDoc.width(), currentDoc.height(), 255)
    filterLayer = currentDoc.createFilterLayer("Cross-Channel RGB over Lightness", filterLayerFilter, filterLayerSelection)
    # For unknown reasons, setting the driver properties does not work if nTransfers has not been set previously,
    # and it does also not work if the filter has not already been applied to the layer.
    filterLayer.filter().configuration().setProperties({
        'activeCurve': -1,
        'curve0': '0,0.5;1,0.5;',
        'curve1': '0,0.5;1,0.5;',
        'curve2': '0,0.5;1,0.5;',
        'curve3': '0,0.5;1,0.5;',
        'curve4': '0,0;1,1;',
        'curve5': '0,0.5;1,0.5;',
        'curve6': '0,0.5;1,0.5;',
        'curve7': '0,0.5;1,0.5;',
        'nTransfers': 8
    })
    filterLayer.filter().configuration().setProperties({
        'driver0': 7,
        'driver1': 7,
        'driver2': 7,
        'driver3': 7,
        'driver4': 7,
        'driver5': 7,
        'driver6': 7,
        'driver7': 7,
    })
    extractedColorGroupLayer.addChildNode(filterLayer, None)
    
    transformMaskX = 3
    transformMaskY = 3
    transformMask = currentDoc.createTransformMask("Transform Mask")
    xml = f"""<!DOCTYPE transform_params>
<transform_params>
  <main id="tooltransformparams"/>
  <data mode="0">
    <free_transform>
      <transformedCenter type="pointf" x="{transformMaskX}" y="{transformMaskY}"/>
      <originalCenter type="pointf" x="0" y="0"/>
      <rotationCenterOffset type="pointf" x="0" y="0"/>
      <transformAroundRotationCenter value="0" type="value"/>
      <aX value="0" type="value"/>
      <aY value="0" type="value"/>
      <aZ value="0" type="value"/>
      <cameraPos z="1024" type="vector3d" x="0" y="0"/>
      <scaleX value="1" type="value"/>
      <scaleY value="1" type="value"/>
      <shearX value="0" type="value"/>
      <shearY value="0" type="value"/>
      <keepAspectRatio value="0" type="value"/>
      <flattenedPerspectiveTransform
        type="transform"
        m11="1" m12="0" m13="0"
        m21="0" m22="1" m23="0"
        m31="{transformMaskX}" m32="{transformMaskY}" m33="1"/>
      <filterId value="Bicubic" type="value"/>
      <boundsRotation value="0" type="value"/>
    </free_transform>
  </data>
</transform_params>"""
    transformMask.fromXML(xml)
    extractedColorGroupLayer.addChildNode(transformMask, None)
    
    cloneofExtractedColorLayer = currentDoc.createCloneLayer("Clone of Extracted Color", extractedColorGroupLayer)
    cloneofExtractedColorLayer.setBlendingMode(BlendingMode.Subtract)
    addChildAsBottommost(colorOneGroupLayer, cloneofExtractedColorLayer)
    
    currentDoc.refreshProjection()
    
    print("Chromatic Aberration: script finished successfully")
    
def runDebugLayer():
    doc = Krita.instance().activeDocument()
    node = doc.activeNode()
    print(node.type())
    print(node.blendingMode())
    
    if node.type() == 'transformmask':
        print(node.toXML())

def addChildAsBottommost(parent_node, child_node):
    children = parent_node.childNodes()

    # childNodes() order is bottommost -> topmost.
    # To make child_node bottommost, put it first.
    parent_node.setChildNodes([child_node] + children)