import streamlit as st
import pandas as pd
import re
import openai

user_api_key = st.sidebar.text_input("OpenAI API key")
client = openai.OpenAI(api_key=user_api_key)
prompt = """Act as an english exam writer who want undergraduate student to develop their reading comprehension skills.
1.Your task is generating reading comprehension exam from keyword provided by user.
2.You have to fact check and prove before using the information.
3.The article should be 300-400 words , vocabulary should be B2-C1 following the CEFR level and grammar must correct and no error.
4.The exam should be 10 questions with 4 multiple choice that complex and challenging that require deeper comprehension and interpretation skills.
question should be in this structure:
Question\n
A)\n 
B)\n 
C)\n 
D)\n
5.Then, you have to provide the answer key and description with proper reasons for every questions. 
title must be on 'Answer Key'. Also, the answer key should be in list of dictionaries. 
It will be 2 column: Answer and Explanation as this structure:
answer_key = [ {'Answer': '', 'Explanation': ""},
    {'Answer': '', 'Explanation': ""},
    ...........
    {'Answer': '', 'Explanation': ""},
    ]
Because I will use this data to st.dataframe.
"""

st.title('Reading exam generator')
st.markdown('AI ช่วยแต่งข้อสอบพาร์ต Reading เพียงแค่เขียน keyword ที่ต้องการ \n Article จะมีความยาว 300-400 คำ ความยากระดับ B2-C1 และมีข้อสอบทั้งหมด 10 ข้อ')
user_input = st.text_area('text your keyword here')

if st.button('Click'):
    messages_so_far = [
        {"role": "system", "content": prompt},
        {'role': 'user', 'content': user_input},
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_so_far,
        temperature=1.1
    )
    st.markdown('**AI response:**')
    answer = response.choices[0].message.content
    st.write(answer.split("answer_key = ")[0].strip())

    answer_string = answer.split("answer_key = ")[1].strip()
    pattern = r"\{'Answer':\s*'([A-D])',\s*'Explanation':\s*\"(.*?)\"\}"
    matches = re.findall(pattern, answer_string)
    answer_key = [{'Answer': answer, 'Explanation': explanation} for answer, explanation in matches]
    answer_df = pd.DataFrame(answer_key)
    answer_df.index = ['1', '2', '3','4', '5', '6','7', '8', '9','10']
    st.dataframe(answer_df)