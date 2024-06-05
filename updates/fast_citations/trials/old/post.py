from flask import Flask, request, jsonify

app = Flask(__name__)

from combine_all_1 import main

def generate_response(choice, path, query):
    answer, citations = main(choice, path, query)
    return {"answer": answer, "citations": citations}

@app.post('/input-for-citation')
def take_input():
    request_data = request.get_json()
    choice = request_data.get("choice")
    path = request_data.get("path")
    query = request_data.get("query")
    
    if not all([choice, path, query]):
        return jsonify({"error": "Missing data in request"}), 400
    
    response = generate_response(choice, path, query)
    return jsonify(response), 201

if __name__ == "__main__":
    app.run(debug=True)
