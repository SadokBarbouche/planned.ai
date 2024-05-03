from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from mlx_lm import generate, load
from langchain.vectorstores.chroma import Chroma
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from rag.rag import get_best_destination
from langchain_community.embeddings import SentenceTransformerEmbeddings
app = Flask(__name__)

embeddings = SentenceTransformerEmbeddings()
model, tokenizer = load("SadokBarbouche/planned.AI-gemma-2b-it-quantized")

def choose_right_db(user_destination):
    db = Chroma(
        persist_directory=f"db/qa_it_{user_destination}_dataset",
        embedding_function=embeddings
    )
    return db

def get_places_to_visit(user_destination, user_preferences):
    user_preferences = user_preferences.split('\n')
    db = choose_right_db(user_destination)
    for user_preference in user_preferences:
        places_with_locations = get_best_destination(user_preference, db)
        
    return [(p,l) for (p,l) in places_with_locations]


def format_prompt(locations):
    return f"""Given these locations:
{locations}
Generate a good and coherent way to spend the dayduring a trip.
Your plan should follow this format:
Day Plan:
Morning: [Activity]
Mid-Morning: [Activity]
Midday: [Activity]
Afternoon: [Activity]
Evening: [Activity]
Night: [Activity]

Activities can include:
- Exploring [Location]
- Trying local cuisine at [Restaurant]
- Visiting [Landmark]
- Enjoying [Recreational Activity] at [Park/Beach]
- Relaxing with [Activity] at [Spa/Hotel]
- Participating in [Event/Activity] at [Venue]
- Shopping at [Market/Mall]
- Taking a guided tour of [Attraction]
- Engaging in outdoor activities like [Activity] at [Outdoor Location]
- Experiencing cultural immersion at [Museum/Cultural Site]
- Enjoying scenic views at [Scenic Spot]

Feel free to customize the activities based on your preferences and interests.
"""


def invoke(prompt):
    response = generate( model=model, tokenizer=tokenizer, prompt=format_prompt(prompt),verbose=False, max_tokens=1000)    
    return response


@app.route('/plan', methods=['POST'])
def ask():
    preferences = request.json.get('preferences')
    destination = request.json.get('destination')
    places_to_visit = get_places_to_visit(preferences, destination)
    response = invoke(places_to_visit)
    print(response)
    return jsonify({"plan": response})


if __name__ =='__main__':
    app.run(port=3000)
    # dst = "kairouan"
    # pref = """"Having a good cafe in haffuz
    # Visiting museums in haffuz
    # Visiting historical places in haffuz
    # Eating traditional food in haffuz
    # """
    # ans = [get_places_to_visit(dst, p) for p in pref.split('\n')]
    # print(ans)
    # print(invoke(ans))    
