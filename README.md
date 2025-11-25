# Leaf Disease Detection by Color Segmentation 
Automatic Detection System for "Black Rot" in Apple Trees

This project proposes a desktop software solution for the automatic detection of foliar diseases in apple trees, with a specific focus on Black Rot. The application employs image processing techniques and chromatic segmentation to provide a rapid diagnosis and an estimation of the infection severity.

Description

Precision agriculture requires fast and non-invasive methods for monitoring crop health. Traditional visual inspection methods are often subjective and time-consuming.

This project addresses the challenge of detecting diseases under variable lighting conditions (shadows, bright sunlight) by utilizing the CIELAB color space. The algorithm ignores the luminance component ($L^*$) and analyzes only the chromatic information ($a^*, b^*$), allowing for robust segmentation of the affected areas regardless of illumination.

Key Features

Image Loading: Support for standard image formats (.jpg, .png).

Automated Analysis: Segmentation of the image into three regions: Healthy Tissue, Disease (Black Rot), and Background.

Severity Calculation: Automatic estimation of the percentage of the affected leaf surface area.

Visualization: Graphical user interface displaying segmentation maps and statistical charts.

Intelligent Post-processing: Morphological filtering to remove noise and false detections.

Technologies Used

The project is developed in Python 3.x and utilizes the following libraries:

OpenCV (cv2): For image processing, color space conversions, and morphological operations.

NumPy: For mathematical calculations and matrix manipulation.

Tkinter: For the standard graphical user interface (GUI).

Pillow (PIL): For image manipulation within the interface.

Matplotlib: For generating statistical charts (Pie Charts).
