def get_city_code(city_name: str) -> str:
    """
    Chuyển đổi tên thành phố sang mã code (Mẫu cho Lab)
    """
    mapping = {
        "hồ chí minh": "SGN",
        "hcm": "SGN",
        "hà nội": "HAN",
        "hn": "HAN",
        "đà nẵng": "DAD"
    }
    # Làm sạch chuỗi: viết thường và bỏ khoảng trắng thừa
    city_clean = city_name.lower().strip()
    return mapping.get(city_clean, "UNKNOWN")

def get_showtimes(movie_name: str, location: str):
    """
    Tra cứu lịch chiếu phim thực tế.
    """
    # Giả lập dữ liệu trả về từ hệ thống rạp
    if "zootopia" in movie_name.lower():
        return f"Lịch chiếu {movie_name} tại {location}: 19:00 rạp CGV Liberty, 20:30 rạp CGV Vivo City."
    return "Xin lỗi, phim này hiện không có suất chiếu."

def book_ticket(movie_name: str, theater: str, time: str, quantity: int):
    """
    Đặt vé xem phim sau khi đã chọn được suất chiếu.
    """
    return f"THÀNH CÔNG: Đã đặt {quantity} vé phim {movie_name} tại {theater} lúc {time}. Mã đặt vé: VIN-123456."

# Danh sách để OpenAI hiểu các công cụ này (Sẽ dùng ở Phase 3)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_showtimes",
            "description": "Lấy danh sách giờ chiếu phim và tên rạp tại một thành phố",
            "parameters": {
                "type": "object",
                "properties": {
                    "movie_name": {"type": "string"},
                    "location": {"type": "string"}
                },
                "required": ["movie_name", "location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_ticket",
            "description": "Thực hiện đặt vé xem phim",
            "parameters": {
                "type": "object",
                "properties": {
                    "movie_name": {"type": "string"},
                    "theater": {"type": "string"},
                    "time": {"type": "string"},
                    "quantity": {"type": "integer"}
                },
                "required": ["movie_name", "theater", "time", "quantity"]
            }
        }
    }
]