import streamlit as st
import openai
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from helper_functions import llm

from utility import check_password
from logics.usecase1_handler import process_usecase1_message
from logics.usecase2_handler import process_usecase2_message

def draw_chart (reponse_data):
    if 'charts' in response_data:
        for chart in response_data['charts']:
            data = chart.get('data')
            title = chart.get('title', 'Chart')
            x_label = chart.get('x_label', 'X-axis')
            y_label = chart.get('y_label', 'Y-axis')
            
            if data:
                fig, ax = plt.subplots(figsize=(8,5))
                #plt.figure(figsize=(8, 5))
                
                if isinstance(data, dict):
                    # Plotting if data is a dictionary
                    ax.bar(data.keys(), data.values())
                elif isinstance(data, list):
                    try:
                        # Ensure data contains pairs of (x, y)
                        if all(isinstance(item, (list, tuple)) and len(item) == 2 for item in data):
                            x_vals, y_vals = zip(*data)
                            ax.bar(x_vals, y_vals)
                        else:
                            raise ValueError("List data is not in the format [(x1, y1), (x2, y2), ...].")
                    except ValueError as e:
                        print(f"Error: {e}")
                        continue
                else:
                    print("Data format not supported for chart plotting.")
                    continue
                
                ax.set_title(title)
                ax.set_xlabel(x_label)
                ax.set_ylabel(y_label)

                st.pyplot(fig)
                #plt.show()
            else:
                print("No data available for the chart.")

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

st.set_page_config(
    layout="centered",
    page_title="My Project Type C - Capstone Assignment: Building an Interactive LLM-Powered Solution"
)

# Sidebar navigation
st.sidebar.title("AI Champions Bootcamp - Capstone Project - Navigation")
menu = st.sidebar.radio("Go to", ["About Us", "Methodology","CPF Contributions AI", "CPF Withdrawals AI"])

if menu == "CPF Contributions AI":
    st.title("CPF Contributions AI")

    st.subheader("Step 1. Hello! Tell me about your:")
    citizenship = st.selectbox("Citizenship status", ["Singapore Citizen/3rd year Permanent Resident and above", "1st year Permanent Resident", "2nd year Permanent Resident"])
    age = st.number_input("Age", min_value=16, max_value=100, value=30)
    employment_type = st.selectbox("Employment type", ["Full-time", "Part-time", "Self-employed"])
    salary = st.number_input("Ordinary Wages (SGD)", min_value=0, step=500, value=3000)
    salary_aw = st.number_input("Additional Wages (SGD)", min_value=0, step=500, value=0)
    with st.expander("What are Ordinary Wages and Additional Wages?"):
        '''
        For wages to be classified as Ordinary Wages for the month, it must satisfy both conditions below:

        * The wages are due or granted wholly or exclusively in respect of an employee’s employment during that month; and

        * The wages for that month are payable by 14th of the following month.

        For example, monthly salary.

        Wages which are not classified as Ordinary Wages will be Additional Wages for the month.

        For example, annual performance bonus.
        '''

    st.subheader("Step 2. Ask me anything related to CPF Contributions:")
    '''
    * I am updated on the latest CPF Contribution Rates from 1 Jan 2024.

    * I will attempt to illustrate with charts where relevant, e.g. for queries such as "_Show me my accruals in CPF contributions over the next 10 years_".

    * However, I may refuse to answer questions not related to CPF Contribution Rates.'''
    form = st.form(key="form")
   
    user_prompt = form.text_area("Enter your query here", height=200, value="Show me my accruals in CPF contributions over the next 10 years.")

    if form.form_submit_button("Submit"):
        response_data = process_usecase1_message(f'My citizenship is {citizenship}. I am a {employment_type} employee, aged {age}, with ordinary wages of {salary} and additional wages of {salary_aw}. {user_prompt}') # <--- This calls the helper function that we have created 🆕
        st.write(response_data['response']) 

        # Extract data for charts if available
        try:
            draw_chart(response_data)
        finally:
            print ('')

        

elif menu == "CPF Withdrawals AI":
    st.title("CPF Withdrawals AI")

    st.subheader("Step 1. Hello! Tell me about your:")
    age = st.number_input("Age", min_value=16, max_value=100, value=60)
    cpf_balance = st.number_input("Current CPF balance (SGD)", min_value=0, step=1000, value=300000)

    st.subheader("Step 2. Ask me anything related to CPF Withdrawals:")
    '''
    * I am updated on the latest CPF Unconditional Withdrawal Rules.

    * I will attempt to illustrate with charts where relevant, e.g. for queries such as "_Show me withdrawal amounts and future payouts over next 10 years_".

    * However, I may refuse to answer questions not related to CPF Withdrawals.'''
    form = st.form(key="form")
   
    user_prompt = form.text_area("Enter your query here", height=200, value="Show me withdrawal amounts and future payouts over next 10 years.")

    if form.form_submit_button("Submit"):
        response_data = process_usecase2_message(f'I am aged {age}, with current CPF balance of {cpf_balance} in SGD. {user_prompt}') # <--- This calls the helper function that we have created 🆕
        st.write(response_data['response']) 

        # Extract data for charts if available
        try:
            draw_chart(response_data)
        finally:
            print ('')

elif menu == "About Us":
    '''
    # About Us
    Hello there. This is William Lau from the GovTech Digital Governance Group. 
    
    This is my submission of the capstone project (Type C) for the inaugural GovTech AI Champions Bootamp. 
    
    Many thanks to Nick and team for preparing and conducting the course. It was tough but I'm glad I went through it.
    
    GenAI is earth-shakingly powerful and ushers some brave new world. Which is ultimately better for everyone, I sincerely hope.
    
    There is much to explore and get better at.

    ## Project Scope

    The domain area that I've focused on for the capstone project is:
   
    * __Understanding CPF (Central Provident Fund) Policies__

    ## Objectives

    Objectives for the two use cases implemented are:

    1. __CPF Contribution AI__
    
       * Use GenAI with charts to help enhance understanding of citizen users of their CPF contributions based on their citizenship status, age, employment status and wages.
    -----

    2. __CPF Withdrawal AI__
    
       * Use GenAI with charts to help enhance understanding of citizen users of CPF withdrawals based on their age and the total CPF savings accumulated.

    ## Data Sources

   Key data sources for the two use cases implemented are:

    1. __CPF Contribution AI__
    
       * CPF Contribution Rates from 1 Jan 2024 (converted to JSON)
         * https://www.cpf.gov.sg/content/dam/web/employer/employer-obligations/documents/CPF_contribution_rates_from_1_Jan_2024.pdf

    -----

    2. __CPF Withdrawal AI__

        * CPF Withdrawl Rules (converted to JSON)
          * https://www.cpf.gov.sg/content/dam/web/member/faq/retirement-income/documents/withdrawal-rules-table.pdf

    ## Features

    Both use cases share the following common features:
    * Citizen users is first asked to enter relevant details in a form which is included into the prompt to enhance context.

    * Application will first check if user query is relevant to the topic at hand before responding.

    * Application outputs in Markdown format which improves presentation.

    * Application will also attempt to dynamically generate and plot charts to illustrate if relevant to the query. 
        
    '''
  

elif menu == "Methodology":
    """
    # Methodology

    ## Implementation Details

    This is a basic web application bulit using Streamlit, and deployed on the Streamlit Community Cloud.

    Core libraries include ```openai``` and ```matplotlib```

    It uses OpenAI API in various functions to provide natural language processing.
  
    Prompts are revised/extended and crafted from the base code used as part of the AI Champions Bootcamp, to use GenAI to:
    
    1. Verify relevance of query

    2. Determine relevant grouping of query. This technique is used for CPF Contribution AI due to the size of the data file. 
     
    3. Filter, programmatically, larger body of information based on that grouping to a smaller set in order to include into context which is then used to help answer the query. 

    4. Generate datapoints if relevant to enhance understanding of the citizen user, that is compatible to ```matplotlib``` 

    5. Structure and format whole response into a JSON dictionary string which can then be programmed to:

        a) Write answer back to the user

        b) Visualise the data for the user

    Chatbots also helped build the application. ChatGPT was used to: 
    
    1. Provide ideas
    
    2. Rapidly provide the wireframe/skeleton for the application

    4. Explain Python libraries, functions and concepts

    5. Explain exception that the application threw, which helped debugging. 

    4. Code out 'workable' functions, which shortened development time. E.g. Function to handle charting with ```matplotlib``` of datapoints dynamically generated in the OpenAI response would have been very hard to come out with.

    ## Data flows

    1. Data downloaded from CPF in PDF or image were piped to a multimodal LLM to transform to JSON strings representing Python dictionaries.

    2. The JSON strings are sample-reviewed (human-in-the-loop,so to speak) for basic integrity (I'm not a CPF expert), cleaned up and saved as JSON files. 

    3. The program logic can then load the JSON files, to then 'down-filter' or better contextualise the data based on user inputs.
     
    4. This allowed selected, more contextualised, higher quality (in my lay judgment) data to be fed into the system-side message for building the final prompt to answer the query.

    ## Flowcharts illustrating process flow for each usecase
    
    """
    st.image("./flowcharts.png")

# Footer
with st.expander("__IMPORTANT NOTICE__"):
    '''
    This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

    __Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.__

    Always consult with qualified professionals for accurate and personalized advice.
    '''

