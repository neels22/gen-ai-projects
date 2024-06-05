from flask import Flask, request, jsonify
from combine_all_1_copy import DocumentProcessor



app = Flask(__name__)
process = DocumentProcessor() 



def executing_main(choice,path):

    process.main(choice,path)


def generate_response(query):

    reponse_of_query = process.human_query_response(query)
    return {"response":reponse_of_query}


@app.post('/generate-embeddings-for-data')
def embeddings_generator():
    request_data=request.get_json()

    choice = request_data.get("choice")
    path=request_data.get("path")

    if not all([choice, path]):
        return jsonify({"error": "Missing data in request"}), 400
    
    executing_main(choice,path)
    return jsonify({"message": "Embeddings generated successfully"}), 200 
    


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




if __name__ == "__main__":
    app.run(debug=True)
