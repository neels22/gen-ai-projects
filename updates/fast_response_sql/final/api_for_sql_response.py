from flask import Flask, request, jsonify


from sql_response import main 

app = Flask(__name__)


def generate_response(query):
    answer= main(query)
    return answer



@app.post('/input-to-sql-chain')
def take_input():
    request_data = request.get_json()
   
    query = request_data.get("query")
    
    if not all([query]):
        return jsonify({"error": "Missing data in request"}), 400
    
    response = generate_response(query)
    return jsonify(response), 201



if __name__ == "__main__":
    app.run(debug=True)
