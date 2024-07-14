import os
import requests
import json
import PyPDF2
from fpdf import FPDF
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def split_into_chunks(text, chunk_size=5000):
    """
    Splits the input text into manageable chunks, each not exceeding the chunk_size.
    """
    chunks = []
    while text:
        if len(text) > chunk_size:
            # Find the last newline character within the chunk size
            split_index = text.rfind('\n', 0, chunk_size)
            if split_index == -1:  # No newline character found; fallback to chunk_size
                split_index = chunk_size
            chunks.append(text[:split_index])
            text = text[split_index:]
        else:
            chunks.append(text)
            break
    return chunks

def summarize_text(text):
    openai_api_key = os.getenv('OPENAI_API_KEY')
    """
    Summarizes text using OpenAI's API.
    """
    prompt = (f"""
    Summarize the following text:

    {text}

    """)
    api_url = 'https://api.openai.com/v1/chat/completions'
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {openai_api_key}'}
    data = {
        'model': 'gpt-4',
        'messages': [{"role": "user", "content": prompt}],
        'temperature': 0.7
    }
    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        print("Error from Open AI")
        return None

def read_pdf(file_path):
    """
    Reads a PDF file and extracts its text.
    """
    pdf_text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            pdf_text += page.extract_text()
    return pdf_text

def write_pdf(file_path, summaries):
    """
    Writes summaries to a PDF file.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for summary in summaries:
        pdf.multi_cell(0, 10, summary)
        pdf.ln()

    pdf.output(file_path)

def main():
    # Load the PDF file
    input_file_name = os.getenv('INPUT_PDF_FILE_NAME')

    pdf_text = read_pdf(input_file_name)

    chunks = split_into_chunks(pdf_text)
    summarized_chunks = []

    for chunk in chunks:
        summarized_chunk = summarize_text(chunk)
        if summarized_chunk:
            summarized_chunks.append(summarized_chunk)
        else:
            print("Error summarizing chunk")
            summarized_chunks.append(chunk)  # Fallback to original chunk in case of error

    # Write the summarized content to a new PDF file
    output_file_name = os.getenv('OUTPUT_PDF_FILE_NAME')
    write_pdf(output_file_name, summarized_chunks)

if __name__ == '__main__':
    main()
