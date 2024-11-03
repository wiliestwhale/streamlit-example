import json
from helper_functions import llm

filepath = './data/cpf_full_withdrawal_rules.json'
with open(filepath, 'r') as file:
    json_string = file.read()
    dict_of_contribution_rates = json.loads(json_string)

def is_prompt_relevant(user_message):
    delimiter = "####"

    system_message = f"""
    You will be provided with queries from Singapore citizens related to CPF (Central GProvident Fund) withdrawals. \
    The query will be enclosed in
    the pair of {delimiter}.
    Decide if the query is relevant to CPF withdrawals.

    Respond with 'Relevant' or 'Irrelevant' only
    """
    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_message}{delimiter}"},
    ]
    return llm.get_completion_by_messages(messages) == 'Relevant'

def generate_response(user_message):
    delimiter = "####"

    system_message = f"""
    You will be provided with queries from Singapore citizens related to CPF (Central Provident Fund) withdrawals. \
    The query will be enclosed in
    the pair of {delimiter}.

    Follow these steps to answer the queries.

    Step 1: If the user is asking about CPF unconditional withdrawals, \
    understand the relevant rule(s) from the following list.
    Relevant rules are shown in the json data below:
    {dict_of_contribution_rates}

    Step 2: Use the information about the CPF withdrawal rules to \
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


def process_usecase2_message(user_input):
    print(f"-------USER INPUT---------: {user_input}")
    if is_prompt_relevant(user_input):
        reply = generate_response(user_input)
        #reply = reply.replace("'", "\"")
        print(f"------RELEVANT REPLY------------: {reply}")
        return json.loads(reply)
    else:
        return json.loads('''
                          {"response":"😕 I can only respond to queries related to CPF withdrawals. Please rephrase your query so that is related to CPF withdrawals."}
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