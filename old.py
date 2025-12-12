#import subprocess

#subprocess.run(['python', 'HuggingFace/main.py'])

# from app.dainthuggingface.ultis import call_llm_function

# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "get_weather",
#             "description": "Lấy thông tin thời tiết tại một địa điểm.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "location": {
#                         "type": "string",
#                         "description": "Tên thành phố hoặc địa điểm."
#                     },
#                     "unit": {
#                         "type": "string",
#                         "enum": ["C", "F"],
#                         "description": "Đơn vị nhiệt độ."
#                     }
#                 },
#                 "required": ["location"]
#             }
#         }
#     }
# ]


# result = call_llm_function(
#     system_prompt="You are a helpful assistant.",
#     user_input="Thời tiết ở Hà Nội thế nào?",
#     functions=tools  # truyền tools vào
# )


# print("Final LLM Output:", result)

from app.dainthuggingface.chat_manager import ChatManager

chat = ChatManager()

print(chat.chat("Hello, bạn còn nhớ tôi không?"))
