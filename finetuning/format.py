import pandas as pd


def format_prompt(system_prompt: str, question: str) -> str:
    "Format the question to the format of the dataset we fine-tuned to."
    return """<bos><start_of_turn>user
## Instructions
{}
## User
{}<end_of_turn>
<start_of_turn>model
""".format(
        system_prompt, question
    )


system_prompt = """Below is an instruction that describes a task. Write a response that appropriately completes the request.
As a diligent SOC Analyst, your responsibility is to proficiently interpret db logs. Your job is to interpret the given logs:"""


def generate_prompt(row: pd.Series, system_prompt: str = system_prompt) -> str:
    "Format to Gemma's chat template"
    return """<bos><start_of_turn>user
## Instructions
{}
## User
{}<end_of_turn>
<start_of_turn>model
{}<end_of_turn><eos>""".format(system_prompt, row["question"], row["instruction"])


def train_valid_test_split(df: pd.DataFrame):
    df["text"] = df.apply(generate_prompt, axis=1)
    data = df.sample(frac=1, random_state=42)
    train, valid, test = data[:int(len(df) * 0.9)], data[int(len(df) * 0.9):int(len(df) * 0.95)], data[int(len(df) * 0.95):]
    train[["text"]].to_json("db/train.jsonl", orient="records", lines=True, force_ascii=False)
    valid[["text"]].to_json("db/valid.jsonl", orient="records", lines=True, force_ascii=False)
    test[["text"]].to_json("db/test.jsonl", orient="records", lines=True, force_ascii=False)
    return train, valid, test
