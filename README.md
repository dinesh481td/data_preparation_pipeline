# SuperAnnotate Automation Tool

## Overview

This Python script automates various tasks related to the SuperAnnotate platform, including downloading images and annotations, converting annotations to COCO format, replacing IDs, merging JSON files, and visualizing bounding boxes on images.

## Prerequisites

Before using this tool, ensure you have the following:

- Python 3.x installed on your system
- Required Python libraries specified in `requirements.txt` installed
- Access to the SuperAnnotate platform with an API key
- Necessary permissions to access projects on the SuperAnnotate platform

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone <repository_url>
    ```

2. Install the required Python dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up your SuperAnnotate API key:
   
   - Obtain your SuperAnnotate API key from the platform.
   - Replace `"api-key here"` with your actual API key in the `api_key` variable within `main.py`.

4. Ensure you have the necessary credentials and directories set up as per the script requirements.

## Usage

1. Run the `main.py` script:

    ```bash
    python main.py
    ```

2. Follow the prompts and instructions provided by the script.

## Directory Structure

- **jsons_superann**: Directory to store downloaded JSON files from SuperAnnotate.
- **coco_output_superann**: Directory to store COCO converted JSON files.
- **coco_final_jsons**: Directory to store final merged COCO JSON files.
- **merged_jsons**: Directory to store intermediate merged JSON files.
- **all_images**: Directory to store downloaded images.
- **ann_folder**: Directory to store annotated images with bounding boxes.

## Credits

- This project utilizes the SuperAnnotate API for data extraction and manipulation.
- Developed by [Your Name].

## License

This project is licensed under the [License Name] License - see the [LICENSE](LICENSE) file for details.
