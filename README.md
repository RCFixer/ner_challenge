# FSC Data Extraction with NER

A project for parsing and analyzing data using a Named Entity Recognition (NER) model. The system can extract structured information from text data and includes tools for training custom NER models.

## Features

- **Data Extraction**: Parse and analyze data using a pre-trained NER model
- **Dataset Generation**: Create training datasets for custom NER models
- **Model Training**: Train your own NER models on custom data

## Installation

### For Production Use (Model Inference Only)

If you only need to use the pre-trained model for data extraction:
```bash
pip install -r requirements_without_train.txt
```

### For Development (Including Model Training)

If you plan to train models or work with the full pipeline:
```bash
pip install -r requirements_with_train.txt
```

## Getting the Pre-trained Model

1. Download the pre-trained model from Google Drive: https://drive.google.com/file/d/1-q4pzKODh1GOENiY9A-u6o1_EKDXBx5U/view?usp=sharing
2. Extract the `result_model` folder from the downloaded ZIP archive
3. Place the `result_model` folder in the project root directory

Your project structure should look like:
```
project-root/
├── extract_FSC_data.py
├── generate_dataset.py
├── train_model.py
├── result_model/          # Extracted model files
├── requirements_with_train.txt
└── requirements_without_train.txt
```

## Usage

### Extracting Data with NER Model

Run the main extraction script to parse and analyze data:
```bash
pip install -r requirements_without_train.txt
python extract_FSC_data.py
```

### Generating Training Dataset

To create a dataset for training a new NER model:
```bash
python generate_dataset.py
```

### Training a Custom NER Model

To train your own NER model on custom data:
```bash
pip install -r requirements_with_train.txt
python train_model.py
```

## Project Structure

- `extract_FSC_data.py` - Main script for data extraction and analysis using the NER model
- `generate_dataset.py` - Generates training datasets for NER model development
- `train_model.py` - Handles the training process for custom NER models
- `requirements_with_train.txt` - Full dependencies including training libraries
- `requirements_without_train.txt` - Minimal dependencies for model inference only
- `result_model/` - Pre-trained NER model directory (not included, must be downloaded)

## Requirements

See `requirements_with_train.txt` or `requirements_without_train.txt` depending on your use case.

