# Web Scraping Pipeline with ZenML

This project demonstrates a web scraping pipeline using ZenML to extract article content from URLs, process the data, and save the results.

## Features

- Extracts article titles, publication dates, and content from URLs
- Uses ZenML for pipeline orchestration
- Saves extracted data to JSON files
- Modular and extensible design

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Setting Up ZenML

1. Initialize ZenML:

   ```bash
   zenml init
   ```

2. Create a new ZenML stack (or use the default):
   ```bash
   zenml stack register local -m local -o local -a default --set
   ```

## Running the Pipeline

1. Run the pipeline with the default URLs:

   ```bash
   python pipeline.py
   ```

2. To use custom URLs, modify the `urls` list in the `if __name__ == "__main__":` block in `pipeline.py`.

## Project Structure

- `pipeline.py`: Contains the ZenML pipeline and steps for web scraping
- `main.py`: Original script (kept for reference)
- `requirements.txt`: Project dependencies

## Customization

You can modify the extraction logic in the `extract_article` function in `pipeline.py` to handle different website structures.

## License

This project is open source and available under the [MIT License](LICENSE).
