"""실습 05 · Prompt 구성과 Chat Model 호출을 구분합니다."""

# 파일 경로 처리 기능 사용
# - Path : 파일 및 디렉터리 경로 관리
from pathlib import Path

# 명령행 인자 파싱 및 시스템 환경 제어 기능 사용
# - argparse : CLI 플래그(--offline 등) 처리
# - sys : 모듈 검색 경로 등록
import argparse
import sys

# 현재 파일 경로 기준 상위 루트 경로 등록
# - HERE : 현재 실습 파일 디렉터리
# - sys.path에 추가해 실행 위치와 무관하게 coursekit 모듈 로드 가능
HERE = Path(__file__).resolve().parent
# 어느 폴더에서 실행해도 이 역할 폴더의 coursekit을 사용합니다.
sys.path.insert(0, str(HERE.parents[1]))

# 실습 데이터 및 프롬프트·모델 구성 기능 사용
# - example_hit : 예시 검색 Hit 데이터 조회
# - load_hits : 전체 검색 Hit 데이터 목록 조회
from coursekit.data import example_hit, load_hits

# - make_prompt : 프롬프트 템플릿 생성
from coursekit.checkpoints import make_prompt

# - create_chat_model : 실제 Chat Model 객체 생성
from coursekit.llm import create_chat_model

# - fixture_chat_model, fixture_generation : 테스트용 고정 모델 및 장애 사례 생성
from coursekit.fixtures import fixture_chat_model, fixture_generation

# - execution_record, message_record : 실행 환경 및 응답 메시지 기록 형식 생성
from coursekit.reporting import execution_record, message_record

# - save_json, show_success : 결과 파일 저장 및 완료 메시지 출력
from coursekit.io import save_json, show_success

"""Prompt 입력 딕셔너리 생성, Prompt-Chat Model 순차 호출, 입력 누락·타임아웃 장애 관찰 및 결과 리포트 저장을 수행하는 모듈"""


# 프롬프트 입력 딕셔너리 생성 함수
# - question과 context 문자열을 프롬프트 템플릿 키에 맞춰 매핑
def make_inputs(question: str, context: str) -> dict:
    """입력: 질문·근거 문자열 / 출력: question, context 두 Key를 가진 dict."""
    # BEGIN D26-05-A01
    # TODO D26-05-A01: 질문과 Context를 각각 question·context Key로 묶어 반환합니다.
    # 힌트: Dictionary의 두 Key 이름은 Prompt의 변수 이름과 같아야 합니다.
    # 완료 후 아래 NotImplementedError를 제거하고 반환값을 확인하세요.

    # question과 context 키를 담은 딕셔너리 반환
    return {"question": question, "context": context}
    # raise NotImplementedError("D26-05-A01 TODO 미완성")
    # END D26-05-A01


# Prompt 및 Chat Model 순차 실행 함수
# - 입력 dict를 Prompt에 전달해 ChatPromptValue 생성
# - 생성된 prompt_value를 Chat Model에 전달해 AIMessage 생성 후 튜플로 반환
def invoke_pair(prompt, chat_model, inputs: dict):
    """dict → ChatPromptValue → AIMessage. 반환: (prompt_value, message)."""
    # BEGIN D26-05-A02
    # TODO D26-05-A02: Prompt를 먼저 실행하고 그 반환값을 Chat Model에 전달한 뒤 두 반환값을 함께 반환합니다.
    # 힌트: 첫 invoke의 반환값이 둘째 invoke의 입력입니다. 반환 순서는 (prompt_value, message)입니다.
    # 완료 후 아래 NotImplementedError를 제거하고 반환값을 확인하세요.

    # Prompt 실행으로 ChatPromptValue 생성
    prompt_value = prompt.invoke(inputs)
    # Chat Model 실행으로 응답 메시지 생성
    message = chat_model.invoke(prompt_value)
    # 두 단계 결과값 순서대로 반환
    return prompt_value, message
    # raise NotImplementedError("D26-05-A02 TODO 미완성")
    # END D26-05-A02


# context 누락 오류 관찰 함수
# - context 키가 빠진 입력으로 Prompt를 호출해 KeyError 발생 여부 확인
# - 프롬프트 단계 실패 및 모델 미호출 상태를 기록하여 반환
def inspect_missing_context(prompt) -> dict:
    """의도적으로 빠진 입력을 검사합니다. 모델 API는 이 함수에 등장하지 않습니다."""
    # BEGIN D26-05-A03
    # TODO D26-05-A03: context Key를 뺀 입력을 Prompt에 전달하여 발생한 KeyError의 단계를 기록합니다.
    # 힌트: try/except KeyError를 사용합니다. 이 함수에서는 Chat Model을 호출하지 않습니다.
    # 완료 후 아래 NotImplementedError를 제거하고 반환값을 확인하세요.

    try:
        # context 키 누락 입력으로 Prompt 호출 시도
        prompt.invoke({"question": "15분 늦으면 어떻게 기록되나요?"})
    # KeyError 발생 시 프롬프트 입력 단계 실패 기록 반환
    except KeyError:
        return {
            "stage": "prompt_input",
            "exception_type": "KeyError",
            "model_invoked": False,
        }
    # KeyError 미발생 시 단언 오류 발생
    raise AssertionError("context가 없는 입력은 Prompt 단계에서 실패해야 합니다.")
    # raise NotImplementedError("D26-05-A03 TODO 미완성")
    # END D26-05-A03


# 고정 타임아웃 오류 관찰 함수
# - 장애 픽스처 모델에 입력을 전달해 TimeoutError 발생 여부 확인
# - 모델 호출 단계 실패 및 미실행·미수신 상태를 기록하여 반환
def inspect_timeout(failing_model, inputs: dict) -> dict:
    """제공된 고정 오류 사례만 관찰합니다. 실제 API 장애를 재현하지 않습니다."""
    # BEGIN D26-05-A04
    # TODO D26-05-A04: 고정 Timeout 사례를 실행하여 호출 실패라는 관찰 기록을 반환합니다.
    # 힌트: TimeoutError만 처리합니다. status=insufficient_context를 만들어 답변으로 바꾸지 않습니다.
    # 완료 후 아래 NotImplementedError를 제거하고 반환값을 확인하세요.

    try:
        # 고정 타임아웃 모델 호출 시도
        failing_model.invoke(inputs)
    # TimeoutError 발생 시 모델 호출 실패 관찰 기록 반환
    except TimeoutError:
        return {
            "stage": "model_call",
            "exception_type": "TimeoutError",
            "source_mode": "fixed_timeout_example",
            "llm_executed": False,
            "answer_received": False,
        }
    # TimeoutError 미발생 시 단언 오류 발생
    raise AssertionError("제공된 Timeout 예시는 TimeoutError를 발생시켜야 합니다.")
    # raise NotImplementedError("D26-05-A04 TODO 미완성")
    # END D26-05-A04


# 출처 헤더 포함 컨텍스트 문자열 생성 함수
# - citation_id, source_locator, body를 결합해 단일 컨텍스트 블록 구성
def context_of(hit: dict) -> str:
    """앞 장에서 배운 출처 포함 블록 형식입니다. 이번 실습의 제공 코드입니다."""
    return f"[{hit['citation_id']}] {hit['source_locator']}\n{hit['body']}"


# 프로그램 진입 함수
# - --offline 옵션 파싱 및 평가 대상 케이스 구성
# - context 누락 및 timeout 경계 사례 관찰
# - 오프라인 픽스처 또는 실제 Chat Model 실행 결과 수집 후 prompt_model.json 저장
def main():
    # 명령행 옵션(--offline) 파싱
    parser = argparse.ArgumentParser(description="Prompt → Chat Model 입력·출력 관찰")
    parser.add_argument(
        "--offline", action="store_true", help="고정 응답 예시만 사용; 실제 모델 미실행"
    )
    args = parser.parse_args()
    # 출석 및 과제 마감 검증 케이스 목록 구성
    attendance = example_hit()
    prompt = make_prompt()
    cases = [("attendance_15", "15분 늦으면 어떻게 기록되나요?", attendance)]
    assignment = next(hit for hit in load_hits() if hit["doc_id"] == "DOC-ASSIGN")
    cases.append(("assignment_deadline", "내 과제의 정확한 마감 날짜는?", assignment))
    # 모델 생성·호출 전에 로컬 TODO와 입력을 먼저 확인합니다.
    # 모델 생성 및 호출 전 케이스별 프롬프트 입력 사전 구성
    prepared = [
        (case_id, make_inputs(question, context_of(hit)), hit)
        for case_id, question, hit in cases
    ]
    # context 누락 및 timeout 오류 관찰 결과 수집
    observations = {}
    observations["missing_context"] = inspect_missing_context(prompt)
    observations["timeout_example"] = inspect_timeout(
        fixture_generation("timeout"), prepared[0][1]
    )
    # 기본 경로는 실제 모델입니다. 환경 문제가 있어도 자동으로 예시로 전환하지 않습니다.
    # 실행 모드(--offline 여부)에 따른 Chat Model 선택
    chat_model = fixture_chat_model() if args.offline else create_chat_model()
    # 각 케이스별 프롬프트 메시지, 응답 및 출처 근거 레코드 생성
    records = []
    for case_id, inputs, hit in prepared:
        prompt_value, message = invoke_pair(prompt, chat_model, inputs)
        records.append(
            {
                "case_id": case_id,
                "question": inputs["question"],
                "context": inputs["context"],
                "prompt_value_type": type(prompt_value).__name__,
                "prompt_messages": [
                    {"type": m.type, "content": m.content}
                    for m in prompt_value.to_messages()
                ],
                "response": message_record(message),
                "evidence": {
                    "citation_id": hit["citation_id"],
                    "doc_id": hit["doc_id"],
                    "source_locator": hit["source_locator"],
                    "body": hit["body"],
                },
                "human_evidence_review": "pending",
            }
        )
    # 최종 리포트 딕셔너리 조립
    result = {
        "exercise": "05_prompt_model",
        "execution": execution_record(
            "offline_fixture" if args.offline else "live", llm=not args.offline
        ),
        "real_model_calls": 0 if args.offline else len(records),
        "fixed_example_calls": len(records) if args.offline else 0,
        "observations": observations,
        "cases": records,
        "review_note": "문장·출처의 정답 여부는 자동 판정하지 않았습니다. reports/review.md에 원문 대조를 기록하세요.",
    }
    # 결과 JSON 저장, 완료 알림 및 실행 상태 요약 출력
    path = save_json(HERE, "prompt_model.json", result)
    show_success("05 Prompt·Chat Model 관찰 기록", path)
    print("실제 LLM 실행:", not args.offline, "| 원문 대조: 수강생 확인 필요")


# 스크립트 직접 실행 시 메인 진입점 호출
if __name__ == "__main__":
    main()

"""
Prompt 템플릿 실행(ChatPromptValue 생성)과 Chat Model 실행(AIMessage 생성)을 명확히 분리하여 입·출력 흐름을 관찰할 수 있도록 구현하였다.
필수 context 누락(KeyError)과 모델 타임아웃(TimeoutError) 같은 경계 장애를 사전에 격리 관찰하고, 오프라인 픽스처와 라이브 모델 경로를 명시적으로 구분함으로써 
후속 근거 대조 및 생성 검증 단계의 추적성과 안정성을 확보하였다.
"""
