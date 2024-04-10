from dataset_generation import generate_answers, generate_questions

if __name__ == "__main__":
    template = """
    If you're in {city} and looking for something fun to do, check out {name} located at {address}. 
    This top-rated destination is perfect for {main_category} lovers and offers a range of {categories} to choose from. 
    With a rating of {rating}, it's a must-visit spot. It's open during these hours: {workday_timing}, but closed on {
    closed_on}. To get there, use these GPS coordinates: {latitude}, {longitude}. For more details, visit their website 
    at {website} or call them at {phone}.
    """
    generate_answers(template)
    generate_questions()
