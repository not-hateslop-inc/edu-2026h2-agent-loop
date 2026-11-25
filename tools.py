import json
import datetime

EQUIPMENT = {"HS-NB14": {"stock": 12, "dept": "운영·기획부"}, "HS-MN27": {"stock": 30, "dept": "운영·기획부"}}

def get_today() -> str:
    return datetime.date.today().isoformat()

def get_equipment(model: str) -> str:
    info = EQUIPMENT.get(model.upper())
    if info is None:
        return json.dumps({"error": "등록되지 않은 모델"}, ensure_ascii=False)
    return json.dumps({"model": model.upper(), **info}, ensure_ascii=False)

def flaky_search(query: str) -> str:
    """재시도 실습용: 처음 두 번은 실패한다."""
    flaky_search.calls = getattr(flaky_search, "calls", 0) + 1
    if flaky_search.calls <= 2:
        raise TimeoutError("자료실 검색 응답 없음")
    return f"'{query}' 관련 문서 2건: SEC-04, EQ-03"

TOOLS = {
    "get_today": {"fn": get_today, "schema": {"type": "function", "function": {
        "name": "get_today", "description": "오늘 날짜(YYYY-MM-DD)", "parameters": {"type": "object", "properties": {}}}}},
    "get_equipment": {"fn": get_equipment, "schema": {"type": "function", "function": {
        "name": "get_equipment", "description": "사내 장비 모델명(예: HS-NB14)으로 보유 수량과 담당 부서를 조회",
        "parameters": {"type": "object", "properties": {"model": {"type": "string"}}, "required": ["model"]}}}},
    "flaky_search": {"fn": flaky_search, "schema": {"type": "function", "function": {
        "name": "flaky_search", "description": "사내 자료실 검색",
        "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}}},
}
