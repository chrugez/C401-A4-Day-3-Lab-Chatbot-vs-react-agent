import os
from dotenv import load_dotenv

# Import các thành phần từ src
from src.core.llm_provider import LLMProvider
from src.agent.agent import ReActAgent
# Giả sử bạn có file movie_tools.py định nghĩa các hàm này
from src.tools.movie_tools import get_city_code, get_showtimes 
from src.core.openai_provider import OpenAIProvider

load_dotenv()

def main():
    # 1. Khởi tạo Model (Sửa model_name theo Key bạn có)
    llm = OpenAIProvider(model_name="gpt-5.4-mini") 

    # 2. Định nghĩa danh sách Tools để truyền vào Agent
    # Lưu ý: key 'func' phải trỏ trực tiếp đến tên hàm
    tools = [
        {
            "name": "get_city_code",
            "description": "Chuyển tên thành phố sang mã sân bay (Ví dụ: Hồ Chí Minh -> SGN)",
            "func": get_city_code
        },
        {
            "name": "get_showtimes",
            "description": "Tra cứu lịch chiếu phim dựa trên mã thành phố",
            "func": get_showtimes
        }
    ]

    # 3. Khởi tạo Agent
    agent = ReActAgent(llm=llm, tools=tools, max_steps=5)

    # 4. Chạy thử
    user_query = "Đặt 2 vé phim Zootopia 2 tại HCM tối nay"
    print(f"🚀 User: {user_query}")
    
    result = agent.run(user_query)
    
    print("\n" + "="*50)
    print(f"FINAL RESULT: {result}")
    print("="*50)

if __name__ == "__main__":
    main()