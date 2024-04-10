from dotenv import load_dotenv
from gemini_pro import load_gemini_pro_model
import warnings
import pandas as pd
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os
import pathlib

warnings.filterwarnings('ignore')

load_dotenv()
chat_model = load_gemini_pro_model()


def generate_answers(template, data_directory='../data/cities', output_directory='../finetuning/it_datasets'):
    """
    Generate descriptions based on a template for each dataset in the specified data directory.

    Args:
        template (str): The template for generating descriptions.
        data_directory (str): The directory containing city datasets.
        output_directory (str): The directory to save the generated descriptions.

    Returns:
        None
    """
    for dataset in os.listdir(data_directory):
        if pathlib.Path(f'{output_directory}/it_{dataset}').is_file():
            print(f"Already done: {dataset}")
            continue
        df = pd.read_excel(f'{data_directory}/{dataset}')
        df["instruction"] = ""
        for i, row in df.iterrows():
            try:
                parsed_data = {column: content for column, content in row.items()}
                formatted_data = '\n'.join(
                    [f"{column} : {content}" for column, content in parsed_data.items() if content])

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

                df.at[i, "instruction"] = output["place_description"]
                if i % 10 == 0:
                    print(f'Instruction n:{i + 1} : {output["place_description"]}')
            except Exception as e:
                print(f"Error occurred at index {i}: {e}")
                continue

        df.to_excel(f"{output_directory}/it_{dataset}")


def generate_questions(data_directory='../finetuning/it_datasets/'):
    for dataset in os.listdir(data_directory):
        if ''.join(os.listdir(data_directory)).count(dataset) > 1 or dataset == "concatenated_dfs.xlsx":
            print(f"Already done: qa_{dataset}")
            continue
        df = pd.read_excel(f"{data_directory}/{dataset}")
        print(dataset)
        df["question"] = ""
        for i in range(len(df)):
            prompt = PromptTemplate(
                input_variables=["place_desc"],
                template="The theme of my application is trip planning. Generate a question whose answer is contained in"
                         "the following description:\n'{place_desc}'\n. Make the question about the location mentioning"
                         "what makes this place special in the question."
            )
            try:
                chain = LLMChain(
                    llm=chat_model,
                    prompt=prompt,
                    output_key="question"
                )

                output = chain({
                    'place_desc': df["instruction"][i]
                })

                df.at[i, "question"] = output["question"]
                if i % 10 == 0:
                    print(f'Question n:{i + 1} : {output["question"]}')
                    print(f'Instruction n:{i + 1} : {df["instruction"][i]}')
            except Exception as e:
                print(f"Error occurred at index {i}: {e}")
                continue

        df.to_excel(f"../finetuning/it_datasets/qa_{dataset}")
