# summarize-pdf-by-gpt

summarize-pdf-by-gpt is a Python script that reads a PDF file, splits it into manageable chunks, summarizes each chunk using OpenAI's GPT model, and writes the summarized content into a new PDF file.

## Features

- Reads text from PDF files
- Splits the text into chunks to manage large content
- Summarizes each chunk using OpenAI API
- Writes the summaries into a new PDF file

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/SummarizePdfByGPT.git
cd summarize-pdf-by-gpt
```
## Install Dependencies
Install the required Python dependencies by running:
```
pip3 install -r requirements.txt
```

## Environment Variables
**Create a new .env file and copy the content from .env.example (don’t forget to add your own OPENAI_API_KEY and pdf filenames INPUT_PDF_FILE_NAME and OUTPUT_PDF_FILE_NAME)**

## Running the Application
To start the server, run the following command from the root of your project directory:
```
python3 summarize_pdf.py
```
