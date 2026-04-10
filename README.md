# Complaint Routing Chatbot

## 📌 Project Overview
This project is an intelligent conversational agent (Chatbot) designed to automate the intake, classification, and routing of consumer complaints. Instead of requiring users to fill out long, complex forms, the chatbot interacts with the consumer naturally to extract the required information (Product category, Sub-product, Issue) and determine the overall sentiment or risk of dispute.

## 🎯 Features
- **Conversational Intake:** Collects complaint details interactively.
- **Automated Classification:** Identifies the product category using ML/NLP text classification behind the scenes.
- **Dispute Prediction:** Estimates the likelihood that a user will dispute the resolution based on their tone and historical data.
- **Seamless Handoff:** Routes the processed structured data to the appropriate internal department.

## 📁 Repository Structure
```
project-root/
│
├── data/                  # Data directory
│   ├── raw/               # Unprocessed, unstructured data and conversation logs
│   └── processed/         # Cleaned data ready for model training/analytics
│
├── src/                   # Main application source code
│   ├── models/            # ML and NLP models for classification
│   ├── bot/               # Chatbot logic and dialogue state management
│   ├── api/               # API endpoints (e.g., FastAPI integrations)
│   └── main.py            # Entry point to run the chatbot server
│
├── docs/                  # Documentation
│   ├── HLD.md             # High-Level Design (Architecture)
│   └── LLD.md             # Low-Level Design (Component details)
│
├── README.md              # Project documentation
├── requirements.txt       # Project dependencies
└── PROMPTS.md             # System prompts and templates for the LLM
```

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3.9+ installed and optionally a virtual environment set up.

### Installation
1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App
Start the main chatbot application server by executing:
```bash
python src/main.py
```
