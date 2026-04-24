# Krita Plugin: Chromatic Aberration

## What it does

[Chromatic Aberration](https://en.wikipedia.org/wiki/Chromatic_aberration) is an (usually unintended) effect caused by different colors of light focus on slightly different points. a camera lens, telescope, or eyeglasses lens may create colored fringes around high-contrast edges.

This plugin allows to simulate this effect.

## You may not need it!

This plugin allows you to create Chromatic Aberration effects in any color.

If you want to create an chromatic aberration effect using only red, blue and/or green, there is a much simpler way, and you may not need this plugin at all.

- Create a clone-layer, with of your input-layer (or group) as source: Right-click on your input-layer -> Add -> Add Clone Layer.
- Set the clone-layer's blending mode to "Copy Red", "Copy Blue" or "Copy Green"
- Move the clone-layer using the "Move a Layer" tool (hotkey: T)

## Installation
- Copy the file `ChromaticAberration.desktop` and the directory `ChromaticAberration` into the `pykrita` folder in your Krita resource folder. You can find your Krita resource folder by clicking `Setting` -> `Manage Resources` -> `Open Resource Folder`.
- After copying the file, restart Krita
- Open your Krita settings by clicking `Settings` -> `Configure Krita`. Click the Category `Python Plugin Manager`.
- You should see an entry called `Chromatic Aberration`. Activate it by clicking the checkbox left of the name.
- If you do not see it, check that you copied the files to the correct location.

## Usage
- Select a paint or group layer of your choice.
- In the menu, click `Tools` -> `Scripts` -> `Chromatic Aberration`.
- This will create a layer-group called `Chromatic Aberration`, with a number of sub-groups and layers.
- You can ignore most of them, only two are relevant for configuration:
  - `Chromatic Aberration` -> `Color 1` -> `Shifted` -> `Extracted Color` -> `Transform Mask`
    - Use this to move or transform the Chromatic Aberration effect.
    - Use the "Move a Layer" (hotkey: T) or the "Transform a Layer" (hotkey: Ctrl+T) tool.
  - `Chromatic Aberration` -> `Color 1` -> `Shifted` -> `Extracted Color` -> `Fill Layer`
    - Use this to set the color of the Chromatic Aberration.
    - `Right-click` -> `Properties` -> `Color`. 
- To add a second color, simply duplicate the "Color 1" Group, and adjust position and color as described above.

## TODO
- Add docker with the ability to pre-select one or more colors and offsets