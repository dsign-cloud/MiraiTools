# Mirai Exporter

## Overview
**Mirai Exporter** is a Blender add-on designed to simplify the export of 3D models to the Mirai platform. It offers tools to organize collections, set up materials, configure UV mappings, and generate raycast and room screenshots, all while optimizing the export process for GLB files.

## Features
- **Collection Organization**: Ensures proper collection setup for `rooms` and `raycast` objects.
- **Material Management**: Automatically creates and assigns materials, including specialized opacity and raycast materials.
- **Screenshot Capture**: Captures screenshots in both room and raycast views with specific overlay configurations.
- **GLB Export**: Exports the scene in GLB format, optimized for use in MiraiTwin.

## Installation
1. Clone or download this repository.
2. In Blender, go to **`Edit > Preferences > Add-ons > Install…`**.
3. Select the downloaded `mirai_exporter_v2.py` file.
4. Enable the add-on in the Blender add-ons list.

## Usage
1. Open your project in Blender.
2. Set up your scene with the required collections(this happen:
   - `rooms`: For room objects.
   - `raycast`: For raycast objects.
3. Go to `View3D > Add > Mesh > New Object` to access the Mirai Exporter panel.
4. Use the available buttons to configure and export your scene:
   - **Apply Modifiers**: Apply modifiers to selected objects.
   - **Center Origins**: Centers the origins of selected objects.
   - **UV Reset Rooms**: Resets UVs for objects in the `rooms` collection.
   - **Export**: Exports the scene in GLB format.

## Requirements
- **Blender** version 4.2.0 or higher.
- **Python** libraries: `numpy`

## Credits
Developed by:
- Amadeo Delgado Casado
- Long H B
- Minh Nguyen

