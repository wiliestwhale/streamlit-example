import json
from helper_functions import llm

contribution_rate_tables = ["CPF Contribution Rate Table from 1 January 2024 for Singapore Citizens or Singapore Permanent Residents (3rd year onwards)",
"CPF Contribution Rate Table from 1 January 2024 for Singapore Permanent Residents (SPR) during 1st year of SPR status under Graduated contribution rates (G/G)",
"CPF Contribution Rate Table from 1 January 2024 for Singapore Permanent Residents (SPR) during 2nd year of SPR status under Graduated contribution rates (G/G)",
"CPF Contribution Rate Table from 1 January 2024 for Singapore Permanent Residents (SPR) during 1st year of SPR status under Full Employer & Graduated Employee contribution rates (F/G)",
"CPF Contribution Rate Table from 1 January 2024 for Singapore Permanent Residents (SPR) during 2nd year of SPR status under Full Employer & Graduated Employee contribution rates (F/G)"]


# Load the JSON file
filepath = './data/cpf_contribution_rates.json'
with open(filepath, 'r') as file:
    json_string = file.read()
    dict_of_contribution_rates = json.loads(json_string)

def is_prompt_relevant(user_message):
    delimiter = "####"

    system_message = f"""
    You will be provided with queries from Singapore citizens related to CPF (Central Provident Fund) contributions. \
    The query will be enclosed in
    the pair of {delimiter}.
    Decide if the query is relevant to CPF contributions.

    Respond with 'Relevant' or 'Irrelevant' only
    """
    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]
    return llm.get_completion_by_messages(messages) == 'Relevant'

def identify_contribution_table(user_message):
    delimiter = "####"

    system_message = f"""

    You will be provided with queries from Singapore citizens related to CPF (Central Provident Fund) contributions. \
    The query will be enclosed in
    the pair of {delimiter}.


    Decide if the query is relevant to any specific contribution rate table
    in the Python list below.

    If there are any relevant contribution(s) found, output the value in a list.

    {contribution_rate_tables}

    If no relevant contribution rates are found, output an empty list.

    Ensure your response contains only the list or an empty list, \
    without any enclosing tags or delimiters.
    """
    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]

    response_str = llm.get_completion_by_messages(messages)
    response_str = response_str.replace("'", "\"")
    return json.loads(response_str)

def get_contribution_rates(target_desc):
    return dict_of_contribution_rates.get(target_desc)    




def generate_response_based_on_contribution_rates(user_message, product_details):
    delimiter = "####"

    system_message = f"""
    You will be provided with queries from Singapore citizens related to CPF (Central Provident Fund) contributions. \
    The query will be enclosed in
    the pair of {delimiter}.

    Follow these steps to answer the queries.

    Step 1: If the user is asking about CPF contribution rates, \
    understand the relevant rates(s) from the following list.
    Relevant rates are shown in the json data below:
    {product_details}

    Step 2: Use the information about the contribution rate to \
    generate the answer for the query.
    You must rely on the facts or information in the contribution rates.
    Your answer should be as detailed as possible and \
    include information that is useful for customer to better understand the contribution rates.

    Step 3: Answer the citizen in a friendly tone.
    Make sure the statements are factually accurate.
    Your answer should be comprehensive and informative to help the \
    the citizen to make their decision.

    Use Neural Linguistic Programming to construct your answer. Your answer must use markdown formatting and readable.
    
    
    """
    system_message = system_message + """
    Step 4:  output structured data in JSON format. Respond with JSON that contains the following structure:
    {
    "response": "<summary or text content>",
    "charts": [
        {
        "title": "<chart title>",
        "x_label": "<x-axis label>",
        "y_label": "<y-axis label>",
        "data": [
            ["<x1>", <y1>],
            ["<x2>", <y2>],
            ...
        ]
        }
    ]
    }

    Ensure that the response is valid JSON and formatted exactly as specified. Do not include any additional text or explanations outside of the JSON block. Here is an example output:

    {
    "response": "Here is your requested analysis.",
    "charts": [
        {
        "title": "Sales Overview",
        "x_label": "Month",
        "y_label": "Revenue ($)",
        "data": [
            ["January", 12000],
            ["February", 15000],
            ["March", 13000]
        ]
        }
    ]
    }
    """

    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]

    response_to_customer = llm.get_completion_by_messages(messages)
    #response_to_customer = response_to_customer.split(delimiter)[-1]
    return response_to_customer


def process_usecase1_message(user_input):
    print(f"-------USER INPUT---------: {user_input}")
    if is_prompt_relevant(user_input):
        table = identify_contribution_table(user_input)
        if(len(table)>0):
            rates = get_contribution_rates(table[0])
        reply = generate_response_based_on_contribution_rates(user_input, rates)
        #reply = reply.replace("'", "\"")
        print(f"------RELEVANT REPLY------------: {reply}")
        return json.loads(reply)
    else:
        return json.loads('''
                          {"response":"😕 I can only respond to queries related to CPF contribution rates. Please rephrase your query so that is related to CPF contribution rates."}
                          ''')

    # Process 1: If Courses are found, look them up
   # category_n_course_name = identify_category_and_courses(user_input)
  #  print("category_n_course_name : ", category_n_course_name)

    # Process 2: Get the Course Details
  #  course_details = get_course_details(category_n_course_name)

    # Process 3: Generate Response based on Course Details
  #  reply = generate_response_based_on_course_details(user_input, course_details)

    # Process 4: Append the response to the list of all messages
 #   return reply