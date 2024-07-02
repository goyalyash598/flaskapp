from PyPDF2 import PdfReader, PdfWriter
from pre_processing import *
from database import *
from PIL import Image
import pytesseract
import pdfplumber
import os

def ocr_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            image = page.to_image()
            page_text = pytesseract.image_to_string(image.original, lang='hin')
            text += page_text + "\n\n"  # Add some spacing between pages
            # print(f"Extracted text from page {i + 1}:\n", page_text)
            # print("\n" + "="*80 + "\n")  # Separator for better readability
    return text

def process_request(pdf_file, language, m, question_type, input_type, bloom, num_questions, prompt, question_level, text_input, same_file):
    model = model_selection(m)

    if input_type == "PDF":
        if same_file:
            combined_text = get_data()
            print("Same file found, getting data from buffer")
        else:    
            if language == "Hindi":
                combined_text = ocr_from_pdf(pdf_file)
                save_data_to_db(combined_text)
            else:
                combined_text = handle_pdf_file(pdf_file, language, m, model)
                save_data_to_db(combined_text)
            
        # combined_text = get_data()
        if combined_text:
            questions = generate_questions(model, m, combined_text, prompt, question_type, question_level, bloom, language, num_questions)
            # latex_text = pypandoc.convert_text(questions, 'latex', format='markdown')
            # with open("questions.txt", "w", encoding='utf-8') as f:
            #     f.write(latex_text)
        
            result = save_questions_to_db(questions, question_type,bloom)
            return result
        
    elif input_type == "Text" and text_input:
        combined_text = text_input
        print(combined_text)
        save_data_to_db(combined_text)
        combined_text = get_data()
        if combined_text:
                questions = generate_questions(model, m, combined_text, prompt, question_type, question_level, bloom, language, num_questions)
                print(questions)
        else:
            pass
        
        
        result = save_questions_to_db(questions, question_type, bloom)
        return result
    # else:
    #     pass
    #     # st.error("Please upload a PDF file or enter text, and enter a prompt.")
    #     combined_text = None