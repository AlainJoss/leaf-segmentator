# Leaf Segmentator

Leaf Segmentator is an application developed with Streamlit, which allows to segment leaf images and translate the segmented area from pixels to square centimeters (cm²).

## Features and Usage

1. **Start Processing**: Click the "Start Processing" button to begin. This will remove older states and prepare the application for image upload.
2. **Upload Images**: Users can upload a zip file containing the images they want to segment.
3. **Image Manipulation**: Rotate the images so that the leaves are positioned upside-down and cut the stem. Crop any unused contours of the image that could interfere with the segmentation process.
4. **Segmentation**: Adjust the given parameters to segment the images.
5. **Image Selection**: For each image, select the best segmented version. If no version meets your requirements, select further processing.
6. **Further Processing**: Further process the images you selected for this task.
7. **Conversion**: Define the conversion rate (cm²/pixel) to compute the leaf areas.
8. **Report Generation**: Download the generated report.

## Important Notes

- The app was designed to segment images taken on a white background. If you wish to process other kinds of images, you must modify the backend of the app.
- Give the app time to execute your instructions to avoid crashes.
- If an error occurs, refresh the browser and start again.
- Avoid refreshing the browser if the app does not crash, as your progress will be lost.

## Setup and Installation

1. Clone the repository: Clone the application repository to your local machine using the following command in your terminal.

```bash
git clone <repository-url>
```

2. Navigate into the project directory:

```bash
cd <leaf-segmentator>
```

3. Install pipenv if not already installed:

```bash
pip install pipenv
```

4. Create a virtual environment and install the required packages using pipenv and the provided `requirements.txt` file:

```bash
pipenv install -r requirements.txt
```

5. Activate the pipenv shell:

```bash
pipenv shell
```

6. Run the application:

```bash
streamlit run overview.py
```