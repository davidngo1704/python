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
        similar_memories = self.memory.query(user_input, k=3)

        print("daint similar_memories:", similar_memories)

        if similar_memories:
            memory_block = "\n".join(f"- {m}" for m in similar_memories)
            system_prompt = (
                "Bạn là trợ lý AI. "
                "Dưới đây là những ký ức liên quan từ quá khứ:\n"
                f"{memory_block}"
            )
        else:
            system_prompt = "Bạn là trợ lý AI. Không có ký ức nào liên quan."

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ]

    def chat(self, user_input):
        messages = self.build_messages(user_input)

        llm = get_llm()

        print("daint messages input:", messages)

        response = llm.create_chat_completion(
            messages=messages,
            # tools=self.tools,
            # tool_choice="auto",
            max_tokens=300
        )

        msg = response["choices"][0]["message"]

        print("daint LLM response:", msg)

        # Handle function calling
        if "tool_calls" in msg:
            call = msg["tool_calls"][0]
            fn = call["function"]["name"]
            args = json.loads(call["function"]["arguments"])

            if fn == "get_weather":
                result = get_weather(**args)
                self.add_to_history("assistant", str(result))
                return result

        # Normal reply
        assistant_reply = msg.get("content", "").strip()

        # if assistant_reply == "":
        #     print("Empty content, retrying with text-only mode…")
        #     retry = llm.create_chat_completion(
        #         messages=messages + [{"role": "system", "content": "Hãy trả lời bằng văn bản."}],
        #         max_tokens=300
        #     )
        #     assistant_reply = retry["choices"][0]["message"]["content"]

        self.add_to_history("assistant", assistant_reply)

        return assistant_reply