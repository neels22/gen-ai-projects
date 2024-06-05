from flask import Flask, request, jsonify
import os
from generate_embed_response import DocumentProcessor


app = Flask(__name__)
process = DocumentProcessor() 



# Define a folder to store uploaded files (you can customize this)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




def executing_main(choice,path):

    process.main(choice,path)

def generate_response(query):

    reponse_of_query = process.human_query_response(query)
    return {"response":reponse_of_query}





@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if file and file.filename.endswith('.pdf'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
      

        executing_main(1,filepath)
        return jsonify({'message': 'File successfully uploaded and embeddings generated'}), 200
    else:
        return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400


@app.post('/query-response')
def response_generator():
    request_query = request.get_json()

    query = request_query.get("query")
    if not query:
        return jsonify({"error":"missing query in request"}),400
    
    
    query_response = generate_response(query)
    if not query_response:
        return jsonify({"error": "no response generated"}), 500

    return jsonify(query_response),201





if __name__ == '__main__':
    app.run(debug=True)
