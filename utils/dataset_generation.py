import random
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


def different_categories(dataset_path):
    """Filter categories based on rating > 3 and randomly choose one item per category.

    Args:
        dataset_path (str): The path to the dataset containing categories and ratings.

    Returns:
        dict: A dictionary where keys are categories and values are randomly chosen indices of items with rating > 3.
    """

    df_categories = pd.read_excel(dataset_path)
    categories_dict = {}
    for category in df_categories['main_category'].unique():
        category_indices = df_categories[
            (df_categories['main_category'] == category) & (df_categories['rating'] > 3)].index.tolist()
        if category_indices:
            chosen_index = random.choice(category_indices)
            categories_dict[category] = chosen_index
    return categories_dict


def clear_df(data_directory='../finetuning/it_datasets'):
    """Remove 'instruction' column from datasets in the specified directory.

    Args:
        data_directory (str): The directory containing datasets.

    Returns:
        None
    """
    for dataset in os.listdir(data_directory):
        if dataset.endswith('.xlsx') or dataset.endswith('.xls'):
            df = pd.read_excel(f'{data_directory}/{dataset}')
            if 'instruction' in df.columns:
                df = df.drop('instruction', axis=1)
                df.to_excel(f'{data_directory}/{dataset.split(".")[0]}_modified.xlsx', index=False)


def generate_answers(data_directory='../db/cities', output_directory='../finetuning/it_datasets'):
    """
    Generate descriptions based on a template for each dataset in the specified db directory.

    Args:
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
        print(f"Dataset being Processed : {dataset}")
        for i, row in df.iterrows():
            try:
                parsed_data = {column: content for column, content in row.items()}
                formatted_data = '\n'.join(
                    [f"{column} : {content}" for column, content in parsed_data.items() if content])

                prompt = PromptTemplate(
                    input_variables=["place_info"],
                    template="Generate a brief description about the place whose infos are :\n{place_info}. Focus on "
                             "what it offers, its geolocation (lon,lat)..."
                )

                chain = LLMChain(
                    llm=chat_model,
                    prompt=prompt,
                    output_key="place_description"
                )

                output = chain({
                    'place_info': formatted_data
                })

                df.at[i, "instruction"] = output["place_description"]
                if i % 10 == 0:
                    print(f'Instruction n:{i + 1} : {output["place_description"]}')
            except Exception as e:
                print(f"Error occurred at index {i}: {e}")
                continue

        df.to_excel(f"{output_directory}/it_{dataset}")


def generate_plans(data_directory='../finetuning/it_datasets/it_dataset'):
    """Generate plans for each dataset based on given locations.

    Args:
        data_directory (str): The directory containing datasets.

    Returns:
        None
    """
    plan_format = (
        "Day Plan:\n"
        "Morning: [Activity]\n"
        "Mid-Morning: [Activity]\n"
        "Midday: [Activity]\n"
        "Afternoon: [Activity]\n"
        "Evening: [Activity]\n"
        "Night: [Activity]\n"
        "\n"
        "Activities can include:\n"
        "- Exploring [Location]\n"
        "- Trying local cuisine at [Restaurant]\n"
        "- Visiting [Landmark]\n"
        "- Enjoying [Recreational Activity] at [Park/Beach]\n"
        "- Relaxing with [Activity] at [Spa/Hotel]\n"
        "- Participating in [Event/Activity] at [Venue]\n"
        "- Shopping at [Market/Mall]\n"
        "- Taking a guided tour of [Attraction]\n"
        "- Engaging in outdoor activities like [Activity] at [Outdoor Location]\n"
        "- Experiencing cultural immersion at [Museum/Cultural Site]\n"
        "- Enjoying scenic views at [Scenic Spot]\n"
        "\n"
        "Feel free to customize the activities based on your preferences and interests."
    )

    for dataset in os.listdir(data_directory):
        if ''.join(os.listdir(data_directory)).count(dataset) > 1 or dataset == "concatenated_dfs.xlsx":
            print(f"Already done: qa_{dataset}")
            continue
        # print(dataset)
        if dataset.startswith("concatenated"):
            continue
        df = pd.read_excel(f"{data_directory}/{dataset}")
        df["plan"] = ""
        for i in range(len(df)):
            prompt = PromptTemplate(
                input_variables=["choices", "format"],
                template=(
                    "Given these locations:\n"
                    "{choices}\n\n"
                    "Generate a good and coherent way to spend the day during a trip.\n"
                    "Your plan should follow this format:\n"
                    "{format}"
                )
            )
            try:
                chain = LLMChain(
                    llm=chat_model,
                    prompt=prompt,
                    output_key="plan"
                )
                categories_dict = different_categories(
                    f"{data_directory}/{dataset}")
                all_indices = list(categories_dict.values())
                output = chain({
                    'format': plan_format,
                    'choices': [df["instruction"][i] for i in all_indices]
                })
                df.at[i, "choices"] = ((
                                               "Given these locations:\n"
                                               + "\n".join(
                                           [df["instruction"][i] for i in all_indices])) + "\n\nGenerate a good and "
                                                                                           "coherent way to spend the "
                                                                                           "day"
                                                                                           "during a trip.\nYour plan "
                                                                                           "should follow this "
                                                                                           "format:\n"
                                                                                           f"{plan_format}"
                                       )

                df.at[i, "plan"] = output["plan"]
                if i % 10 == 0:
                    print(f'Question n:{i + 1} : {df["choices"][i]}')
                    print(f'Instruction n:{i + 1} : {df["plan"][i]}')
            except Exception as e:
                print(f"Error occurred at index {i}: {e}")
                continue

        df.to_excel(f"../finetuning/it_datasets/qa_dataset/qa_{dataset}")
