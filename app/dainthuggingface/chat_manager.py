import json
from app.dainthuggingface.base_service import get_llm, get_weather
from app.dainthuggingface.memory import MemoryStore

class ChatManager:
    def __init__(self):
        self.memory = MemoryStore()
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Lấy thông tin thời tiết tại một địa điểm.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "Tên thành phố hoặc địa điểm."
                            },
                            "unit": {
                                "type": "string",
                                "enum": ["C", "F"],
                                "description": "Đơn vị nhiệt độ."
                            }
                        },
                        "required": ["location"]
                    }
                }
            }
        ]

    def add_to_history(self, role, content):
        self.memory.add_message(role, content)

    def build_messages(self, user_input):

        similar_memories = self.memory.query(user_input, k=10)

        if similar_memories:

            memory_block = "\n".join(
                f"- {m}" for m in similar_memories
            )

            system_prompt = (
                "Bạn là trợ lý AI.\n"
                "Dưới đây là các đoạn hội thoại liên quan trước đây:\n"
                f"{memory_block}"
            )
        else:
            system_prompt = "Bạn là trợ lý AI."

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ]

    def chat(self, user_input):

        self.add_to_history("user", user_input)

        messages = self.build_messages(user_input)

        llm = get_llm()


        response = llm.create_chat_completion(
            messages=messages,
            # tools=self.tools,
            # tool_choice="auto",
            max_tokens=300
        )

        msg = response["choices"][0]["message"]

        if "tool_calls" in msg:
            call = msg["tool_calls"][0]
            fn = call["function"]["name"]
            args = json.loads(call["function"]["arguments"])

            if fn == "get_weather":
                result = get_weather(**args)
                self.add_to_history("assistant", str(result))
                return result

        assistant_reply = msg.get("content", "").strip()

        self.add_to_history("assistant", assistant_reply)

        return assistant_reply