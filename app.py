from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from process import process_request
from database import store_in_api,clear_data
from io import BytesIO


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
last_uploaded_filename = ""
same_file = False

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file and file.filename:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200
    return jsonify({'error': 'No file provided'}), 400


@app.route('/generate', methods=['POST'])
def generate():
    clear_data()
    global last_uploaded_filename
    global same_file

    model = request.form.get('model')
    pdfLang = request.form.get('pdfLang')
    questionType = request.form.get('questionType')
    inputType = request.form.get('inputType')
    bloomType = request.form.get('bloomType')
    numberQuestions = request.form.get('numberQuestions')
    questionLevel = request.form.get('questionLevel')
    prompt = request.form.get('prompt')
    print(f"Question Type:  {questionType}")
    
    textInput = ""
    file = None
    filepath = None  
    if 'textInput' in request.form:
        textInput = request.form.get('textInput')
        print("Text Input received: ", textInput)

    response_data = {}
    if 'file' in request.files:
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if filename == last_uploaded_filename:
                same_file = True

            else:
                same_file = False
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename) 
                file.save(filepath)

  
    questions_and_answers = process_request(filepath, pdfLang, model, questionType, inputType, bloomType, numberQuestions, prompt, questionLevel, textInput, same_file)
    
    if("textInput" == inputType):
        last_uploaded_filename = filename
    return jsonify(questions_and_answers), 200




@app.route("/store_api", methods=['POST'])
def handleKeys():
    keys = request.json.get('keys')
    if keys:
        response = store_in_api(keys)
        print(response)
        if response==[]:
            return "DNS error"
        for i in response:
            if(i!=200):
                return str(i)
        return "200"
    else:
        return  "Select some Questions"
        
if __name__ == '__main__':
    app.run(debug=True)