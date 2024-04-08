from dotenv import load_dotenv
from gemini_pro import load_gemini_pro_model
import warnings
import pandas as pd
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

warnings.filterwarnings('ignore')

load_dotenv()
chat_model = load_gemini_pro_model()

df = pd.read_excel("../preprocessing/preprocessed_data/Data with geolocation.xlsx")

template = """If you're in {city} and looking for something fun to do, check out {name} located at {address}. 
This top-rated destination is perfect for {main_category} lovers and offers a range of {categories} to choose from. 
With a rating of {rating}, it's a must-visit spot. It's open during these hours: {workday_timing}, but closed on {
closed_on}. To get there, use these GPS coordinates: {latitude}, {longitude}. For more details, visit their website 
at {website} or call them at {phone}."""

df["instruction"] = ""

for i in range(len(df)):
    row = df.iloc[i]
    parsed_data = {}
    for column, content in row.items():
        parsed_data[column] = content
    formatted_data = '\n'.join([f"{column} : {content}" for column, content in parsed_data.items()])

    prompt = PromptTemplate(
        input_variables=["place_info", "template"],
        template="Given this template: \n{template}\nTry generate something like it (not exactly) related to the "
                 "place with the following details:\n{place_info}\n. Any field containing nan , [] , "
                 "None or equivalent term shouldn't be mentioned."
    )

    chain = LLMChain(
        llm=chat_model,
        prompt=prompt,
        output_key="place_description"
    )

    output = chain({
        "template": template,
        'place_info': formatted_data
    })

    df["instruction"][i] = output["place_description"]
    if i % 10 == 0:
        print(f'Instruction n:{i+1} : {output["place_description"]}')

df.to_excel("it-dataset.xlsx")