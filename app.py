from flask import Flask, request, jsonify, send_file
from pdfminer.high_level import extract_text as pdfminer_extract_text
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from googletrans import Translator  # For basic translation (accuracy might be an issue)
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from transformers import pipeline  # For more advanced translation (requires setup)
import os

app = Flask(__name__)
translator = Translator()
# If using a more advanced model like MarianMT:
# nlp = pipeline('translation', model='Helsinki-NLP/opus-mt-hi-en')

def extract_text_from_pdf(pdf_path):
    """Attempts to extract text directly from PDF, then uses OCR if needed."""
    try:
        text = pdfminer_extract_text(pdf_path)
        if text.strip():
            return text
        else:
            # Try OCR if direct extraction fails
            images = convert_from_path(pdf_path)
            ocr_text = ""
            for img in images:
                ocr_text += pytesseract.image_to_string(img, lang='hin+eng') # Assuming Hindi and English might both be present
            return ocr_text
    except Exception as e:
        print(f"Error extracting text: {e}")
        try:
            images = convert_from_path(pdf_path)
            ocr_text = ""
            for img in images:
                ocr_text += pytesseract.image_to_string(img, lang='hin+eng')
            return ocr_text
        except Exception as ocr_e:
            print(f"OCR Error: {ocr_e}")
            return ""

def translate_text(text, target_language='en'):
    """Translates text using googletrans (basic) or a more advanced model."""
    try:
        # Using googletrans:
        translation = translator.translate(text, dest=target_language)
        return translation.text
        # Using a more advanced model (MarianMT example):
        # result = nlp(text, max_length=512)
        # return result[0]['translation_text']
    except Exception as e:
        print(f"Translation error: {e}")
        return ""

def generate_summary(text, language='en'):
    """Generates a basic summary (you might need a more sophisticated approach)."""
    # This is a very basic example; consider using libraries like transformers for better summarization
    sentences = text.split('.')
    if len(sentences) > 2:
        return '. '.join(sentences[:2]) + '...'
    return text

def create_pdf(text):
    """Generates a PDF from the given text."""
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    textobject = p.beginText()
    textobject.setTextOrigin(30, 750)
    lines = text.split('\n')
    for line in lines:
        textobject.textLine(line)
    p.drawText(textobject)
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

@app.route('/process_pdf', methods=['POST'])
def process_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['pdf_file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and file.filename.endswith('.pdf'):
        temp_pdf_path = "temp.pdf"
        try:
            file.save(temp_pdf_path)
            hindi_text = extract_text_from_pdf(temp_pdf_path)
            english_text = translate_text(hindi_text, 'en')
            hindi_summary = generate_summary(hindi_text, 'hi')
            english_summary = generate_summary(english_text, 'en')
            return jsonify({
                'hindi_text': hindi_text,
                'english_text': english_text,
                'hindi_summary': hindi_summary,
                'english_summary': english_summary
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)
    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf_route():
    data = request.get_json()
    english_text = data.get('text')
    if english_text:
        pdf_buffer = create_pdf(english_text)
        return send_file(pdf_buffer, download_name='translated_document.pdf', as_attachment=True, mimetype='application/pdf')
    return jsonify({'error': 'No text provided for PDF generation'}), 400

if __name__ == '__main__':
    app.run(debug=True)
