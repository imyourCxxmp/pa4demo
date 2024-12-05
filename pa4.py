import streamlit as st
import pandas as pd
import re
import openai

user_api_key = st.sidebar.text_input("OpenAI API key")
client = openai.OpenAI(api_key=user_api_key)

prompt = """Act as an english exam writer who want undergraduate student to develop their reading comprehension skills.
1.Your task is generating reading comprehension exam from keyword provided by user.
2.You have to fact check and prove with 2-3 sources before using the information.
3.The article should be 300-500 words , vocabulary should be B2-C1 following the CEFR level and grammar must correct and no error.
4.The article must contains linking words, 2 or more type of conjunction and provide additional contents which relate to the topic if avaliable.
5.You must provide all link lead to references you took information form at the end of the article every time to respect the author.
6.The exam should be 10 questions with 4 multiple choice that very difficult, complex and challenging that require deeper comprehension and interpretation skills.
question should be in this structure:
Question\n
A)\n
B)\n
C)\n
D)\n
Thus, Question and Choice Shouldn't Place In The Same Line.
7.Then, you have to provide the answer key and description with proper reasons for every questions. 
title must be on 'Answer Key'. Also, the answer key should be in list of dictionaries. 
It will be 2 column: Answer and Explanation as this structure:
answer_key = [ {'Answer': '', 'Explanation': ""},
    ...........
    {'Answer': '', 'Explanation': ""} ]
Because I will use this data for st.dataframe.
"""

st.title('Reading exam generator')
st.markdown('Hello, I will generate reading exam from your keyword texted in input. The article will be about 300-400 words, Difficulty is B2-C1 level follwing CEFR and questions will be 10.')
user_input = st.text_input('text your keyword here', 'ex. Wicked')

if st.button('Click'):
    messages_so_far = [
        {"role": "system", "content": prompt},
        {'role': 'user', 'content': user_input},
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_so_far,
        temperature=1.2
    )
    answer = response.choices[0].message.content
    st.write(answer.split("answer_key = ")[0].strip())
    answer_string = answer.split("answer_key = ")[1].strip()
    pattern = r"\{'Answer':\s*'([A-D])',\s*'Explanation':\s*\"(.*?)\"\}"
    matches = re.findall(pattern, answer_string)
    answer_key = [{'Answer': answer, 'Explanation': explanation} for answer, explanation in matches]
    answer_df = pd.DataFrame(answer_key)
    answer_df.index = ['1', '2', '3','4', '5', '6','7', '8', '9','10']
    st.dataframe(answer_df)