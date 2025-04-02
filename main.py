import re
from langchain.chat_models import init_chat_model
import streamlit as st
import os
import json

# Initialize session state variables
if "llm_response" not in st.session_state:
    st.session_state.llm_response = None
if "response_dict" not in st.session_state:
    st.session_state.response_dict = None
if "selected_answer" not in st.session_state:
    st.session_state.selected_answer = None

### Streamlit App ###
st.header("Math Exercise")
st.subheader("Generate Math Exercise for practice 🤖")

# Math topic selection
Math_topic = st.selectbox(
    "Choose a Math topic for today's Exercise:",
    ["LCM", "HCF", "Percentage", "Fractions", "Decimals", "Division", 
     "Multiples", "Long addition", "Long subtraction", "Long multiplication", "Long division"]
)

# Initialize the LLM model
try:
    os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
    llm = init_chat_model(
        "ft:gpt-4o-mini-2024-07-18:personal:my-math-llm-26th-1st:BFD9gRWW", 
        model_provider="openai"
    )
except Exception as e:
    st.error(f"Failed to initialize LLM: {str(e)}")
    st.stop()

# Generate question when button is clicked
if st.button(f"Generate {Math_topic} Math Problem"):
    messages = [
        {"role": "system", "content": "You are an AI tutor generating multiple-choice math questions with step-by-step explanations."},
        {"role": "user", "content": f"Generate a math question involving {Math_topic} for 6th grade with Challenge level moderate. Return the response in JSON format with these keys: Question, Choices (with A, B, C, D), Correct Answer, and Explanation."}
    ]
    
    try:
        st.session_state.llm_response = llm.invoke(messages)
# Clean response: Remove problematic control characters and ensure proper escaping
        raw_response = st.session_state.llm_response.content
        cleaned_response = re.sub(r'[\x00-\x1F]+', ' ', raw_response)  # Remove invalid control characters
        cleaned_response = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', cleaned_response)  # Properly escape backslashes

        try:
            st.session_state.response_dict = json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            st.error(f"Error parsing JSON: {str(e)}")
            st.stop()        
        # Display the Question
        st.subheader("Question:")
        st.write(st.session_state.response_dict["Question"])
        
    except Exception as e:
        st.error(f"Error generating question: {str(e)}")

# Show options if we have a question
if st.session_state.response_dict:
    options = [
        ("A", st.session_state.response_dict["Choices"]["A"]),
        ("B", st.session_state.response_dict["Choices"]["B"]),
        ("C", st.session_state.response_dict["Choices"]["C"]),
        ("D", st.session_state.response_dict["Choices"]["D"])
    ]
    
    # Create radio buttons with labels
    choice_key = st.radio(
        "Select an option:",
        options=[opt[0] for opt in options],
format_func=lambda x: f"{x}: {dict(options)[x]}"
        )
    
    if st.button("Submit Answer"):
        selected_answer = st.session_state.response_dict["Choices"][choice_key]
        st.write(f"✅ You selected: **{selected_answer}**")
        
        # Check if answer is correct
        correct_answer_key = st.session_state.response_dict["Correct Answer"]
        if choice_key == correct_answer_key:
            st.success("Correct! 🎉")
        else:
            st.error(f"Sorry, the correct answer is {correct_answer_key}: {st.session_state.response_dict['Choices'][correct_answer_key]}")
        
        # Show explanation
        st.subheader("Explanation:")
        explanation = st.session_state.response_dict["Explanation"]
        
        # First fix the completely broken LaTeX parts
        explanation = explanation.replace('frac{80{200', '(80/200)')
        explanation = explanation.replace(' imes', '×')
        explanation = explanation.replace(' ext{Percentage = ( ', 'Percentage = (')
        explanation = explanation.replace(' ight)', ')')
        explanation = explanation.replace('frac{Obtained Marks{Total Marks', '(Obtained Marks/Total Marks)')
        
        # Remove all remaining LaTeX artifacts
        explanation = re.sub(r'\\[a-zA-Z]+\{?', '', explanation)
        explanation = explanation.replace('{', '').replace('}', '')
        
        # Display the cleaned explanation
        st.markdown(explanation)
