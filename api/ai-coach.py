import json
import os

from http.server import BaseHTTPRequestHandler
from google import genai

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            body = self.rfile.read(content_length)
            data = json.loads(body)

            question = data.get("question", "").strip()

            if not question:
                self.send_json_response(
                    400,
                    {
                        "success": False,
                        "message": "질문을 입력해주세요."
                    }
                )
                return

            api_key = os.environ.get("GEMINI_API_KEY")

            if not api_key:
                self.send_json_response(
                    500,
                    {
                        "success": False,
                        "message": "Gemini API 키가 설정되지 않았습니다."
                    }
                )
                return

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

    {question}
    """


            response = client.models.generate_content(
                model="gemini-3.7-flash",
                contents=prompt
            )

            answer = response.text

            self.send_json_response(
                200,
                {
                    "success": True,
                    "answer": answer
                }
            )

        except Exception as error:
            print("Gemini API ERROR:", error)

            self.send_json_response(
                500,
                {
                    "success": False,
                    "message": "AI 코치 답변을 생성하지 못했습니다."
                }
            )

    def send_json_response(self, status_code, data):
        response = json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(status_code)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(response))
        )

        self.end_headers()

        self.wfile.write(response)