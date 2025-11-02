# PDF Image Retrieval

## Overview
This Python package extracts images from PDFs, stores them in AWS S3, and retrieves relevant images based on keyword extraction.

## Features
- Extract images from PDFs automatically
- Upload images to AWS S3 for storage
- Extract keywords from PDFs using NLP
- Train on PDFs to improve retrieval accuracy
- Search and retrieve images based on keywords
- Open-source & developer-friendly

## Installation
Install the package from PyPI:
```python
pip install pdf-image-retrieval
```
Or install directly from GitHub:
```python
pip install git+https://github.com/aryadhandhukiya/pdf-image-retrieval.git
```
## Usage
Extracting Images from a PDF and Storing in S3
```python
from pdf_image_retrieval import PdfImageExtractor

# Initialize extractor
extractor = PdfImageExtractor(pdf_path="sample.pdf", s3_bucket="my-bucket")

# Extract images and store them in S3
extractor.extract_and_upload()
```

Retrieving Relevant Images Based on a Query
```python
from pdf_image_retrieval import PdfImageRetriever

# Initialize retriever
retriever = PdfImageRetriever(s3_bucket="my-bucket")

# Search for images based on keywords
images = retriever.search_images("machine learning diagram")

# Print retrieved image URLs
for img in images:
    print(img)
```

## Configuration
Set up AWS credentials via environment variables:
```python
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="your-region"
```

## Contributing
We welcome contributions! Here's how you can help:

1. Fork the repo and create a new branch.

2. Make your changes and commit them.

3. Open a pull request with a description of your changes.

To set up for development:
```python
git clone https://github.com/aryandhandhukiya/pdf-image-retrieval.git
cd pdf-image-retrieval
pip install -r requirements.txt
```
