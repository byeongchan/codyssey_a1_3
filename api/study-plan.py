import json
import os

from http.server import BaseHTTPRequestHandler

from google import genai


class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        try:
            # 요청 데이터 읽기
            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            body = self.rfile.read(content_length)

            data = json.loads(body)


            # 입력값 가져오기
            subject = data.get("subject", "").strip()
            level = data.get("level", "").strip()
            goal = data.get("goal", "").strip()
            duration = data.get("duration", "").strip()
            daily_time = data.get("daily_time", "").strip()


            # 필수값 확인
            if not subject:
                self.send_error_response(
                    400,
                    "공부할 분야를 입력해주세요."
                )
                return

            if not level:
                self.send_error_response(
                    400,
                    "현재 수준을 입력해주세요."
                )
                return

            if not goal:
                self.send_error_response(
                    400,
                    "학습 목표를 입력해주세요."
                )
                return

            if not duration:
                self.send_error_response(
                    400,
                    "학습 기간을 입력해주세요."
                )
                return

            if not daily_time:
                self.send_error_response(
                    400,
                    "하루 학습 시간을 입력해주세요."
                )
                return


            # Gemini API 클라이언트
            client = genai.Client(
                api_key=os.environ.get("GEMINI_API_KEY")
            )


            # Gemini에게 전달할 프롬프트
            prompt = f"""
당신은 전문적인 AI 학습 코치입니다.

사용자의 학습 정보를 바탕으로
현실적으로 실천할 수 있는 맞춤형 학습 계획을 만들어주세요.

[사용자 정보]

공부 분야:
{subject}

현재 수준:
{level}

학습 목표:
{goal}

학습 기간:
{duration}

하루 학습 시간:
{daily_time}


다음 내용을 포함해주세요.

1. 전체 학습 방향
2. 주차별 학습 계획
3. 각 주차의 핵심 학습 내용
4. 실습 또는 복습 방법
5. 학습자가 주의해야 할 점

사용자가 실제로 실행할 수 있는 수준으로
현실적인 계획을 작성해주세요.

너무 많은 내용을 한꺼번에 요구하지 마세요.

답변은 한국어로 작성해주세요.
"""


            # Gemini API 호출
            response = client.models.generate_content(
                model="gemini-3.7-flash",
                contents=prompt
            )


            # Gemini 결과
            result = response.text


            # 성공 응답
            self.send_json_response(
                200,
                {
                    "success": True,
                    "plan": result
                }
            )


        except Exception as error:

            print("Gemini API ERROR:", error)

            self.send_json_response(
                500,
                {
                    "success": False,
                    "message":
                        "AI 학습 계획을 생성하지 못했습니다."
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


    def send_error_response(self, status_code, message):

        self.send_json_response(
            status_code,
            {
                "success": False,
                "message": message
            }
        )