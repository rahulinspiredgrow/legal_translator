# Legal Translator (Hindi to English)

This project provides a web interface for users to upload PDF documents (containing both direct text and scanned text requiring OCR), translate the content from Hindi to English, and generate a PDF of the translated text. It also displays basic summaries of both the original Hindi text and the translated English text.

**Disclaimer:** Please note that achieving 99.9999% accuracy in legal translation through automated means is extremely challenging due to the nuances of legal language. This tool aims to provide a useful translation but should not be relied upon for critical legal decisions without human review.

## Features

* **PDF Upload:** Users can upload PDF files through a simple web interface.
* **Text Extraction:** Attempts to extract text directly from the PDF. If that fails, it uses OCR (Optical Character Recognition) to extract text from images within the PDF.
* **Hindi to English Translation:** Translates the extracted Hindi text into English using the `googletrans` library.
* **Basic Summarization:** Generates rudimentary summaries of both the original Hindi and the translated English text.
* **PDF Generation:** Allows users to download the translated English text as a PDF file.
* **Web Interface:** Built using HTML for the frontend and Flask (Python) for the backend.
* **Deployment Ready (Render):** The project structure and necessary files are included for easy deployment on Render.

## Project Structure
