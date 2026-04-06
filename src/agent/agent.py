import os
import sys
import re
from typing import List, Dict, Any, Optional
from src.core.llm_provider import LLMProvider
from src.telemetry.logger import logger

class ReActAgent:
    """
    SKELETON: A ReAct-style Agent that follows the Thought-Action-Observation loop.
    Students should implement the core loop logic and tool execution.
    """
    
    def __init__(self, llm: LLMProvider, tools: List[Dict[str, Any]], max_steps: int = 5):
        self.llm = llm
        self.tools = tools
        self.max_steps = max_steps
        self.history = []

    def get_system_prompt(self) -> str:
        tool_descriptions = "\n".join([f"- {t['name']}: {t['description']}" for t in self.tools])
        
        return f"""
        Bạn là một trợ lý đặt vé xem phim thông minh. Nhiệm vụ của bạn là giúp người dùng tra cứu lịch chiếu và đặt vé.
        Bạn có quyền truy cập vào các công cụ sau:
        {tool_descriptions}

        QUY TRÌNH BẮT BUỘC (ReAct):
        1. Thought: Suy nghĩ về những gì bạn cần làm tiếp theo để trả lời câu hỏi.
        2. Action: Chọn một công cụ từ danh sách trên và viết theo định dạng: tool_name(arguments). 
           Sau khi viết Action, bạn phải DỪNG LẠI và không được viết thêm gì nữa.
        3. Observation: Bạn sẽ nhận được kết quả từ hệ thống (đừng tự bịa ra phần này).
        4. Lặp lại Thought/Action nếu cần thiết cho đến khi có đủ thông tin.
        5. Final Answer: Đưa ra câu trả lời cuối cùng cho người dùng dựa trên các Observation thu được.

        LƯU Ý QUAN TRỌNG:
        - Chỉ sử dụng các công cụ được cung cấp.
        - Nếu người dùng cung cấp tên thành phố như "HCM", hãy dùng công cụ để đổi sang mã chuẩn trước.
        - Tuyệt đối KHÔNG tự tạo ra kết quả Observation giả.

        Hãy bắt đầu!
        """

    def run(self, user_input: str) -> str:
        logger.log_event("AGENT_START", {"input": user_input, "model": self.llm.model_name})
        self.history = [f"Question: {user_input}"]
        steps = 0

        while steps < self.max_steps:
            current_prompt = "\n".join(self.history)
            
            # 1. Gọi LLM
            response = self.llm.generate(current_prompt, system_prompt=self.get_system_prompt())
            
            # --- SỬA TẠI ĐÂY ---
            # Nếu response là Dictionary (như log bạn gửi), ta lấy ['content']
            # Nếu response đã là string sẵn rồi, thì giữ nguyên.
            if isinstance(response, dict):
                result = response.get('content', "")
            else:
                result = response if response is not None else ""
            # --------------------

            print(f"\n--- STEP {steps + 1} ---\n{result}")
            self.history.append(result)

            # 2. Kiểm tra Final Answer TRƯỚC (Để thoát ngay nếu xong)
            if "Final Answer:" in result:
                final_answer = result.split("Final Answer:")[-1].strip()
                logger.log_event("AGENT_END", {"steps": steps + 1})
                return final_answer

            # 3. Parse Action
            action_match = re.search(r"Action:\s*(\w+)\((.*)\)", result)
            
            if action_match:
                tool_name = action_match.group(1)
                tool_args = action_match.group(2)
                
                # 4. Thực thi Tool
                observation = self._execute_tool(tool_name, tool_args)
                obs_message = f"Observation: {observation}"
                print(f"[TOOL RESULT]: {obs_message}")
                self.history.append(obs_message)
            else:
                # Chỉ báo lỗi nếu không tìm thấy cả Action lẫn Final Answer
                error_msg = "Observation: Invalid format. Please use 'Action: tool_name(args)' or 'Final Answer: answer'."
                self.history.append(error_msg)
            
            steps += 1
            
        logger.log_event("AGENT_END", {"steps": steps})
        return "I'm sorry, I couldn't finish the task within the maximum steps."

    def _execute_tool(self, tool_name: str, args: str) -> str:
        clean_args = args.strip().strip('"').strip("'")
        
        for tool in self.tools:
            if tool['name'] == tool_name:
                # Thực thi hàm được lưu trong key 'func' của dictionary tool
                try:
                    return tool['func'](clean_args)
                except Exception as e:
                    return f"Error executing tool: {str(e)}"
                    
        return f"Tool {tool_name} not found."
