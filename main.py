import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    Below is a snippet of code.
    Your goal is to:
    - Understand the code, and explain it in plain english.
    - Print the purpose of the code.
    - Find issues or bugs in the code.
    - Make suggestions for optimization.
    - Point out if there are any inefficiencies.
    - Make suggestions to improve the code.
    Your response should begin with the purpose followed by the explanation and then other details like optimizations, bugs, inefficiencies etc.
    Print the purpose with a title like this: 
    \nPURPOSE:
    \nEXPLANATION:
    \nISSUES/BUGS: 
    \nOPTIMIZATION:
    \nINEFFICIENCIES:

    When the action is 'Generate Unit test', you can omit everything else (ie. do not give any explanation or any other text besides the unit test code) and you should just write a correct unit test in the language specified.
    Below is the language, and action to be performed on the code:
    LANGUAGE: {language}
    ACTION: {action}
    CODE: {code}

    
    YOUR RESPONSE:
"""


template_unittest = """
    Below is a snippet of code.
    Your goal is to:
    - Understand the code and generate a unit test in the language specified.
    You should just write a correct unit test in the language specified.
    Below is the language, and action to be performed on the code:
    LANGUAGE: {language}
    ACTION: {action}
    CODE: {code}

    
    YOUR RESPONSE:
"""
prompt = PromptTemplate(
    input_variables=["language", "action","code"],
    template=template,
)

prompt_for_unit_test = PromptTemplate(
    input_variables=["language", "action","code"],
    template=template_unittest,
)
def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Review Code", page_icon=":robot:")
st.header("Review Code")

col1, col2 = st.columns(2)

with col1:
    st.markdown("A simple code review tool by Faeez Shaikh")

# with col2:
    # st.image(image='TweetScreenshot.png', width=500, caption='https://twitter.com/DannyRichman/status/1598254671591723008')

st.markdown("## Enter Your Code for review")

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2 = st.columns(2)
with col1:
    programming_language = st.selectbox(
        'Select the programming language for this snippet:',
        ('Java','Typescript with JSX syntax', 'Javascript','Python',))
    
with col2:
    requested_action = st.selectbox(
        'Select what action you would like to do:',
        ('Optimize','Explain','Find bugs','Generate Unit test'))

def get_text():
    input_text = st.text_area(label="Code input", label_visibility='collapsed', placeholder="Your Code...", key="code_input")
    return input_text

code_input = get_text()

# if len(code_input.split(" ")) > 700:
#     st.write("Please enter a shorter email. The maximum length is 700 words.")
#     st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.code_input = """function add(int a, int b) {
 return a-b;
}"""

st.markdown("### Your Code Explained:")

# def perform_submit_action():
    # print ("in submit")

if code_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    st.write({programming_language},{requested_action})

    if requested_action == 'Generate Unit test':
        prompt_for_unit_test = prompt_for_unit_test.format(language=programming_language, action=requested_action, code=code_input)
        ai_response = llm(prompt_for_unit_test)
        st.code(ai_response, language='{programming_language}', line_numbers=True)
    else:
        prompt_for_code_comments = prompt.format(language=programming_language, action=requested_action, code=code_input)
        ai_response = llm(prompt_for_code_comments)
        st.write(ai_response)

st.button("*See An Example*", type='secondary', help="Click to see an example of how code is reviewed.", on_click=update_text_with_example)


# col1, col2 = st.columns(2)
# with col1:
    
# with col2:
    # st.button("Submit", type="primary", disabled=False, use_container_width=True,on_click=perform_submit_action)



