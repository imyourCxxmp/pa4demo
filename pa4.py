import streamlit as st
import pandas as pd
import json
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
It will be 3 column: No. , Answer and Explanation as this structure:
answer_key = [  
    {'No.': '1', 'Answer': '', 'Explanation': ""},
    {'No.': '2', 'Answer': '', 'Explanation': ""},
    {'No.': '3', 'Answer': '', 'Explanation': ""},
    ...........
    {'No.': '10', 'Answer': '', 'Explanation': ""},
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

    answer_key = [
    {'No.': 1, 'Answer': 'B', 'Explanation': "The article emphasizes that individuals make resolutions to reflect and set goals for self-improvement."},
    {'No.': 2, 'Answer': 'C', 'Explanation': "It states that around 40-45% of Americans typically create New Year resolutions."},
    {'No.': 3, 'Answer': 'C', 'Explanation': "Health and fitness goals are highlighted as the most common types of resolutions."},
    {'No.': 4, 'Answer': 'C', 'Explanation': "The failure to maintain resolutions is attributed to poor planning and lack of motivation."},
    {'No.': 5, 'Answer': 'C', 'Explanation': "Tracking progress through journaling or apps is suggested to help maintain resolutions."},
    {'No.': 6, 'Answer': 'B', 'Explanation': "Friends and family are described as providing support and encouragement in adhering to resolutions."},
    {'No.': 7, 'Answer': 'B', 'Explanation': "Critically analyzing reasons for past failures is suggested as valuable for setting future resolutions."},
    {'No.': 8, 'Answer': 'D', 'Explanation': "The article points out that resolutions should be specific to be effective."},
    {'No.': 9, 'Answer': 'B', 'Explanation': "The study indicates that most individuals abandon their resolutions by February."},
    {'No.': 10, 'Answer': 'B', 'Explanation': "Self-reflection helps individuals identify what strategies were effective or ineffective in their past resolutions."}
]
    answer_df = pd.DataFrame(answer_key)
    st.dataframe(answer_df)