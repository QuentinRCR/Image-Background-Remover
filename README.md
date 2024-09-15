# Background Remover - README

## Overview

This Python project provides a simple GUI application that allows users to remove specific background colors from images and replace them with a new color, including the ability to adjust opacity. The app can handle image files (PNG, JPG, and JPEG) and allows users to select colors, adjust opacity, and fine-tune the removal based on a margin of tolerance.

## Prerequisites

Ensure you have the following Python libraries installed:

```bash
pip install numpy Pillow FreeSimpleGUI
```

## Usage Instructions

1. Run the script to launch the GUI.
1. Select the folder containing your images.
1. The list of images will appear on the left panel.
1. Select an image to preview it.
1. Adjust the following options:
    1. Opacity: Set the opacity level for the new background color (0 to 1).
    1. Color to Remove: Choose the background color to remove using a hex code.
    1. New Color: Choose the color to replace the background with, using a hex code.
    1. Margin: Set the margin of tolerance for color differences.
1. Click the Execute button to remove the background and preview the modified image.
1. The modified image will be saved in the same folder with -modified appended to the filename.

## Features

- **Folder Selection**: Choose a folder containing images.
- **Image List**: Automatically lists all PNG, JPG, and JPEG files in the selected folder.
- **Background Removal**: Allows users to select a color to remove from the image and replace it with a new color and opacity.
- **Adjustable Opacity and Margin**: Opacity and margin sliders let users control how much transparency and tolerance for color removal is applied.
- **Image Preview**: Displays both the original and modified images side by side in the GUI.