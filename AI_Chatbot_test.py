
import streamlit as st
import openai

# API 호출 함수
def askGPT(messages):
    # API 키를 안전하게 관리하는 방식으로 설정 (여기서는 Streamlit secrets 사용)
    apikey = st.secrets["openai"]["apikey"]  # 환경변수나 Streamlit secrets에서 가져오기
    openai.api_key = apikey
    
    # GPT-4o-mini 모델로 채팅 생성
    client = openai.OpenAI(api_key=apikey)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    return response.choices[0].message.content

# 메인 함수
def main():
    st.title('AI Chatbot Test용')
    st.header('※주의. 개인용 유료 API key 사용 중')    
    st.markdown('---')


    # 세션 상태에 메시지 리스트 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]
    
    # 이전 메시지를 화면에 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 사용자 입력
    prompt = st.chat_input("채팅을 입력하세요")
    if prompt:
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # GPT 응답
        with st.chat_message("assistant"):
            response = askGPT(st.session_state.messages)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        # 디버그를 위해 세션 상태 출력
        print(st.session_state.messages)

# 프로그램 실행
if __name__ == "__main__":
    main()
