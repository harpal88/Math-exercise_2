#from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain import LLMChain
#from langchain import PromptTemplate

from langchain.chat_models import init_chat_model
import streamlit as st
import os

#Need to Check if these are required
from typing import Optional, Dict
#from pydantic import BaseModel, Field
from typing_extensions import Annotated, TypedDict

# Importing API Key 
os.environ['GOOGLE_API_KEY'] = st.secrets['GOOGLE_API_KEY']
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

#Initiation the LLM Model 
llm = init_chat_model("gpt-4o-mini", model_provider="openai")

# TypedDict
class Joke(TypedDict):
    """Math problem for Grade 6th student"""

    Question: Annotated[str, ..., "Simple Math question on persentage problem"]

    #Answers: Annotated[str, ..., "Provide 4 answer in MCQ"]
    #Answers: Annotated[list[str, str],...,"Provide 4 answer in MCQ"] Working
    A: Annotated[str,..., "Provide Option A answer"]
    B: Annotated[str,..., "Provide Option B Answer"]
    C: Annotated[str,..., "Provide Option C Answer"]
    D: Annotated[str,..., "Provide Option D Answer"]
    #Explanation: Annotated[str, ..., "Explain the answer"
    Correct_Ans: Annotated[str,...,"Answer amound A, B, C, D"]
    Explanation: Annotated[str, ..., "Explain the answer in Kids frindly and easy way"]
    #rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]

structured_llm = llm.with_structured_output(Joke)

#llm_response = structured_llm.invoke("Provide a math percentage Problem")


### Streamlit ###

st.header(" Math Exercise ")
st.subheader(" Generate Math Exercise for practice 🤖 ")

Math_topic = st.selectbox("Choose a Math topic for today's Exercise : ", ["Percentage", "LCM", "HCF"])
st.write("You selected:", Math_topic)

#============================

# Initialize session state variables if they don't exist
if "llm_response" not in st.session_state:
    st.session_state.llm_response = None
if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None

# Generate question when button is clicked
if st.button("Generate"):
    st.session_state.llm_response = structured_llm.invoke("Provide a math percentage Problem")

# Display the question and answer choices if a question has been generated
if st.session_state.llm_response:
    llm_response = st.session_state.llm_response  # Retrieve stored response
    st.write(llm_response["Question"])

    # Define answer choices
    options = [
        f"A) {llm_response['A']}",
        f"B) {llm_response['B']}",
        f"C) {llm_response['C']}",
        f"D) {llm_response['D']}"
    ]

    # Store answer selection in session state using key
    st.session_state.selected_answer = st.radio(
        "Select one option:", options, index=None, key="answer_radio"
    )

# Submit answer button
#st.write(st.session_state.selected_answer)
#st.write(st.session_state.llm_response['Correct_Ans'])
#st.write(llm_response['Correct_Ans'])
#st.write(st.session_state.answer_radio.split(")")[0])

if st.button("Submit Answer"):
    if not st.session_state.llm_response:
        st.warning("⚠️ Please generate a question first!")
    elif st.session_state.selected_answer is None:
        st.warning("⚠️ Please select an option before submitting.")
    elif st.session_state.answer_radio.split(")")[0] == llm_response['Correct_Ans']:
         st.success(f"✅ Correct! You selected: {st.session_state.selected_answer}")
    else:
        st.error(f"❌ Incorrect! The correct answer is {st.session_state.llm_response['Correct_Ans']}.")









"""
if st.button("Generate Question"):
    llm_response = structured_llm.invoke("Provide a math percentage Problem")
    st.write(llm_response["Question"])

    options = [
        f"A) {llm_response['A']}",
        f"B) {llm_response['B']}",
        f"C) {llm_response['C']}",
        f"D) {llm_response['D']}"
    ]
        
    #answer = st.radio("Select one option:", options, index=None)
    st.session_state.answer = st.radio("Select one option:", options, index=None)
# Button to submit the answer
if st.button("Submit Answer"):
    if not st.session_state.llm_response:
        st.warning("⚠️ Please generate a question first!")
    elif not st.session_state.answer:
        st.warning("⚠️ Please select an option before submitting.")
    elif st.session_state.answer == f"{st.session_state.llm_response['Correct_Ans']}":
        st.success(f"✅ Correct! You selected: {st.session_state.answer}")
    else:
        st.error(f"❌ Incorrect! The correct answer is {st.session_state.llm_response['Correct_Ans']}.")
""" 

"""
if st.button("Submit Answer"):
    if answer==llm_response["Correct_Ans"]:
        st.success(f"✅ You selected: {answer}")
    else:
        st.warning("⚠️ Please select an option before submitting.")
"""
