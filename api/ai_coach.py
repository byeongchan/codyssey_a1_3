import os

from fastapi import FastAPI
from pydantic import BaseModel
from google import genai

app = FastAPI()

class CoachRequest(BaseModel):
    question: str

@app.post("/")
def ask_coach(request: CoachRequest):
    if not request.question.strip():
        return {
            "success": False,
            "message": "질문을 입력해주세요."
        }

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return {
            "success": False,
            "message": "Gemini API 키가 설정되지 않았습니다."
        }

    try:

        client = genai.Client(
            api_key=api_key
        )

        prompt = f"""


    당신은 친절하고 전문적인 AI 학습 코치입니다.

    학생이 공부하면서 궁금한 내용을 질문하면
    학생의 학습을 도와주는 방식으로 답변해주세요.

    답변 원칙:

    1. 어려운 개념은 쉽게 설명해주세요.
    2. 필요한 경우 간단한 예시를 들어주세요.
    3. 핵심 내용을 단계적으로 설명해주세요.
    4. 다음에 공부하면 좋은 내용도 알려주세요.
    5. 너무 길지 않고 이해하기 쉽게 작성해주세요.
    6. 답변은 한국어로 작성해주세요.

    학생의 질문:

    {request.question}
    """


        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt
        )

        return {
            "success": True,
            "answer": response.text
        }

    except Exception as error:

        print("Gemini API ERROR:", error)

        return {
            "success": False,
            "message": "AI 코치 답변을 생성하지 못했습니다."
        }
