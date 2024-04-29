from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from mlx_lm import generate, load
# Initialize Flask app
app = Flask(__name__)


model, tokenizer = load("SadokBarbouche/planned.AI-gemma-2b-it-quantized")

def invoke(prompt):
    response = generate( model=model, tokenizer=tokenizer, prompt=prompt,verbose=False, max_tokens=1000)    
    # print("salem")
    return response


@app.route('/ask', methods=['POST'])
def ask():
    prompt = request.json.get('prompt')
    # print(prompt)
    response = invoke(prompt)
    print(response)
    return jsonify({"answer": response})


if __name__ =='__main__':
    app.run(port=3000)

