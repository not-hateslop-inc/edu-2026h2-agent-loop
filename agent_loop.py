import json
import sys
import uuid
from dotenv import load_dotenv
from openai import OpenAI
from tools import TOOLS
from tracing import Trace

load_dotenv()
client = OpenAI(timeout=30)

MAX_STEPS = 6          # 모델 호출 최대 횟수
MAX_RETRIES = 2        # Tool 하나당 재시도
SYSTEM = "헤이트슬롭 사내 업무 도우미다. 필요한 경우에만 도구를 쓰고, 모르면 모른다고 한다."


def call_tool(name, args, trace, step):
    if name not in TOOLS:
        return f"오류: 없는 도구 {name}"
    for attempt in range(MAX_RETRIES + 1):
        try:
            out = TOOLS[name]["fn"](**args)
            trace.log(step, "tool", name=name, args=args, attempt=attempt, ok=True, result=str(out)[:200])
            return out
        except Exception as e:  # noqa: BLE001 - 실습: 모든 Tool 오류를 모델에게 돌려준다
            trace.log(step, "tool", name=name, args=args, attempt=attempt, ok=False, error=str(e))
    return f"오류: {name} 도구가 {MAX_RETRIES + 1}번 실패했습니다"


def run(question: str) -> str:
    trace = Trace(uuid.uuid4().hex[:8])
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]
    seen = set()
    for step in range(MAX_STEPS):
        msg = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, tools=[t["schema"] for t in TOOLS.values()]
        ).choices[0].message
        messages.append(msg)
        trace.log(step, "llm", content=msg.content, tool_calls=[tc.function.name for tc in msg.tool_calls or []])
        if not msg.tool_calls:                                   # 종료 조건 1: 더 부를 Tool이 없음
            trace.log(step, "end", reason="answer")
            return msg.content
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments or "{}")
            key = (tc.function.name, json.dumps(args, sort_keys=True))
            if key in seen:                                      # 종료 조건 2: 같은 호출 반복
                trace.log(step, "end", reason="repeat", call=key)
                return "같은 작업을 반복하고 있어 멈췄습니다. 담당자에게 문의해 주세요."
            seen.add(key)
            out = call_tool(tc.function.name, args, trace, step)
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": str(out)})
    trace.log(MAX_STEPS, "end", reason="max_steps")             # 종료 조건 3: 최대 단계
    return "최대 단계에 도달해 멈췄습니다."


if __name__ == "__main__":
    print(run(" ".join(sys.argv[1:]) or "HS-NB14 노트북 몇 대 있어?"))
