from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import LLMChain
from langchain import PromptTemplate

import streamlit as st
import os
import re
import json

os.environ['GOOGLE_API_KEY'] = st.secrets['GOOGLE_API_KEY']

def extract_qa_explanation(response):
    """
    Extracts question, answer, and explanation from an LLM response using regex.

    Args:
        response (str): The LLM response text.

    Returns:
        tuple: A tuple containing the question, answer, and explanation (or None if not found).
    """

    # Define regex patterns for question, answer, and explanation sections
    question_pattern = r"Questions Begin:(.*?)Questions End:"
    choice_pattern = r"choice Begin:(.*?)choice End:"
    answer_pattern = r"Answer Begin:(.*?)Answer End:"
    explanation_pattern = r"Explanation Begin:(.*?)Explanation End:"
    
    # Search for patterns in the response
    question_match = re.search(question_pattern, response, re.DOTALL)
    choice_match = re.search(choice_pattern, response, re.DOTALL)
    answer_match = re.search(answer_pattern, response, re.DOTALL)
    explanation_match = re.search(explanation_pattern, response, re.DOTALL)

    # Extract and clean the matched sections
    question = question_match.group(1).strip() if question_match else None
    #choice_str = choice_match.group(1).strip() if choice_match else None
    choice = choice_match.group(1).strip() if choice_match else None
    answer = answer_match.group(1).strip() if answer_match else None
    explanation = explanation_match.group(1).strip() if explanation_match else None

    print(f"Variable choice = {choice}  {type(choice)}")
    #Convert the choice string to Dict
    #choice = dict(choice)
    
    return question, choice, answer, explanation

# Initializing Google Gemini AI Model 
gemini_model = ChatGoogleGenerativeAI(model = "gemini-1.5-flash-latest")


# Defining Math Prompt Template 
Math_template ="""
'Can you generate one Math problem for grade 6th student on math topic {Math_topic} with multiple choise answer and also provide answer with explanation'

Format e.g.: 

Questions Begin:
Find the least common multiple (LCM) of 12 and 18.
Questions End:

choice Begin:
{('a', 6), ('b', 36), ('c', 72), ('d', 216)}
choice End:

Answer Begin:
(b) 36 
Answer End:

Explanation Begin:
There are two main ways to find the LCM of 12 and 18:

Method 1: Listing Multiples
List the multiples of 12: 12, 24, 36, 48, 60, ... List the multiples of 18: 18, 36, 54, 72, ...
The smallest number that appears in both lists is 36. Therefore, the LCM of 12 and 18 is 36.

Method 2: Prime Factorization
Find the prime factorization of each number: 12 = 2 x 2 x 3 = 2² x 3 18 = 2 x 3 x 3 = 2 x 3²
Identify the highest power of each prime factor present in either factorization: The highest power of 2 is 2² = 4 The highest power of 3 is 3² = 9
Multiply these highest powers together: 2² x 3² = 4 x 9 = 36
Therefore, the LCM of 12 and 18 is 36. 
Explanation End:


Questions Begin:
Sarah bought a bicycle that was originally priced at $250. She received a 15% discount. How much did Sarah pay for the bicycle?
Questions End:

choice Begin:
{('a', 186.50), ('b', 184), ('c', 37.50), ('d', 216)}
choice End:

Answer Begin: a) $187.50 Answer End:

Explanation Begin::
To find the discount amount, calculate 15% of $250:
15% of 250 = (15/100)∗250 = $37.50
This means the discount was $37.50. To find the final price Sarah paid, subtract the discount from the original price:
250−37.50 = $187.50
Therefore, Sarah paid $187.50 for the bicycle. 
Explanation End:
"""
# Defining Math Prompt with Prompt Template 
Math_prompt = PromptTemplate(template = Math_template, input_variables =['Math_topic'])

#Create LLM Chain using theprompt template and Model
Math_chain = Math_prompt | gemini_model


### Streamlit ###
# Web Page Header and Subheader 
st.header(" Math Exercise ")
st.subheader(" Generate Math Exercise for practice 🤖 ")

# Getting Input from user for Math topic
Math_topic = st.selectbox("Choose a topic for the tweet:", ["Percentage", "LCM", "HCF"])
st.write("You selected:", Math_topic)

Math_Q = None
response = None

#if st.button("Generate"):
Math_Q = Math_chain.invoke({"Math_topic" : Math_topic})
response = Math_Q.content
#print(f"##################\n\n Resond from LLM is \n\n {response} \n\n\n ##################")

# Extracting Question, Answer and explanation 
question, choice, answer, explanation = extract_qa_explanation(response)

# Now you can use the extracted question, answer, and explanation variables
#st.write("##################################")
#st.write("Question:", question)
st.write("##################################")
st.write("choice:", choice)
st.write(f"Type of Chice Veriable : {type(choice)}")
st.write("##################################")
choice_1 = json.loads(choice)
st.write("choice_1):", choice_1)
st.write(f"Type of Chice_1 Veriable : {type(choice_1)}")

#st.write("##################################")
#st.write("Answer:", answer)
#st.write("##################################")
#st.write("Explanation:", explanation)
