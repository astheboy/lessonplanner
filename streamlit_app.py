import streamlit as st
import openai
import os

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_lesson_plan(subject, achievement_standard, lesson_topic):
    prompt = f"""
당신은 초등학교 교사를 위한 개념 기반 수업 설계 도우미입니다. 다음 정보를 바탕으로 수업 설계를 해주세요:

교과목: {subject}
성취기준: {achievement_standard}
수업 주제: {lesson_topic}

다음 항목들을 포함해 주세요:
1. 핵심 아이디어 (2-3개)
2. 핵심 개념 (3-5개)
3. 핵심 질문 (2-3개)
4. 수업 활동 운영 계획 (3-5개 활동)
5. 평가 루브릭:
   - 이 수업 활동을 위한 3-4개의 평가 요소를 제시하세요.
   - 각 평가 요소에 대해 상중하 3단계의 평가 관점을 제시하세요.
   - 각 평가 관점은 '~함'으로 끝나는 명사형 어미체로 작성하세요.
   - 예시 형식:
     평가요소1: 
     - 상: ~하게 수행함
     - 중: ~하게 수행함
     - 하: ~하게 수행함

각 항목에 대해 간결하고 명확하게 설명해 주세요.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates lesson plans for elementary school teachers."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        n=1,
        temperature=0.7,
    )

    return response.choices[0].message['content'].strip()

def main():
    st.title("개념 기반 수업 설계 도구")

    subject = st.text_input("교과목")
    achievement_standard = st.text_input("성취기준")
    lesson_topic = st.text_input("수업 주제")

    if st.button("수업 설계 생성"):
        if subject and achievement_standard and lesson_topic:
            with st.spinner("수업 설계 생성 중..."):
                lesson_plan = generate_lesson_plan(subject, achievement_standard, lesson_topic)

            sections = lesson_plan.split("\n\n")
            
            st.subheader("핵심 아이디어")
            st.write(sections[0])

            st.subheader("핵심 개념")
            st.write(sections[1])

            st.subheader("핵심 질문")
            st.write(sections[2])

            st.subheader("수업 활동 운영 계획")
            st.write(sections[3])

            st.subheader("평가 루브릭")
            st.write(sections[4])
        else:
            st.warning("모든 필드를 입력해주세요.")

if __name__ == "__main__":
    main()
