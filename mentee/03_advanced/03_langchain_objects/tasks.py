"""Day26 실습. 실행 위치와 관계없이 현재 역할 폴더의 지원 모듈을 사용합니다."""

# 파일 경로 처리 기능 사용
# - Path : 파일 및 디렉터리 경로 관리
from pathlib import Path

# 파이썬 실행 환경 제어 기능 사용
# - sys : 모듈 검색 경로 등록
import sys

# 현재 스크립트 위치 및 역할 루트 경로 계산
# - ROLE_ROOT : 상위 2단계 디렉터리를 역할 루트로 지정
# - sys.path에 추가하여 coursekit 패키지 임포트 지원
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))
# 입출력 및 완료 알림 기능 사용
# - save_json : 결과 리포트 JSON 저장
# - show_success : 실행 완료 메시지 출력
from coursekit.io import save_json, show_success

# 실습 샘플 데이터 로드 기능 사용
# - example_hit : 단일 Hit 예시 조회
# - load_hits : 검색 후보 Hit 목록 조회
from coursekit.data import example_hit, load_hits

# 실행 기록 생성 기능 사용
# - execution_record : 실행 환경 메타데이터 생성
from coursekit.reporting import execution_record

"""RAG 주요 구성요소(Document, Retriever, Prompt, Chat Model)의 입·출력 계약, 접근 방식(data vs invoke), 호출 오용 교정 및 Prompt 입력 구성을 다루는 모듈"""

# 구성요소별 입력 명세 딕셔너리 정의
# - Document, Retriever, Prompt, Chat Model의 입력 형태 명시
COMPONENT_INPUTS = {
    "Document": "page_content와 metadata를 담아 생성",
    "Retriever": "query·category·candidate_k가 있는 dict",
    "Prompt": "question·context가 있는 dict",
    "Chat Model": "ChatPromptValue 또는 메시지 목록",
}


# 구성요소별 출력 자료형 매핑 반환 함수
# - Document는 데이터 객체, Retriever는 list[Document], Prompt는 ChatPromptValue, Chat Model은 AIMessage로 구분
def component_outputs() -> dict[str, str]:
    """강의에서 다룬 네 구성요소의 출력 자료형을 대응시킵니다."""
    # BEGIN D26-03-A01
    # TODO D26-03-A01: 네 구성요소의 반환값을 구분해 dict로 반환합니다.
    # 힌트: Prompt는 ChatPromptValue, Chat Model은 AIMessage입니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.

    # 각 구성요소의 출력 타입 설명 딕셔너리 반환
    return {
        "Document": "본문·출처를 보관하는 데이터 객체",
        "Retriever": "list[Document]",
        "Prompt": "ChatPromptValue",
        "Chat Model": "AIMessage",
    }
    # raise NotImplementedError("D26-03-A01 TODO 미완성")
    # END D26-03-A01


# 구성요소 접근 유형 구분 함수
# - 단순 데이터 보관 객체(Document)와 invoke 실행 대상 구성요소 구분
def access_kinds() -> dict[str, str]:
    """데이터를 읽는 경우와 invoke로 작업을 실행하는 경우를 구분합니다."""
    # BEGIN D26-03-A02
    # TODO D26-03-A02: Document는 data, 실행 구성요소는 invoke로 표시합니다.
    # 힌트: 값 읽기와 실행을 구분합니다. 여기서는 실제 API 호출을 하지 않습니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.

    # 구성요소별 접근 방식(data 또는 invoke) 딕셔너리 반환
    return {
        "Document": "data",
        "Retriever": "invoke",
        "Prompt": "invoke",
        "Chat Model": "invoke",
    }
    # raise NotImplementedError("D26-03-A02 TODO 미완성")
    # END D26-03-A02


# Document 호출 오용 교정 정보 반환 함수
# - 잘못된 invoke 호출 예시와 올바른 본문 읽기·답변 생성 책임 명시
def repair_document_call() -> dict[str, str]:
    """Document.invoke로 답변을 얻는다는 설명을 올바른 읽기 표현으로 고칩니다."""
    # BEGIN D26-03-A03
    # TODO D26-03-A03: 잘못된 Document 호출과 올바른 본문 읽기·생성 역할을 기록합니다.
    # 힌트: doc.page_content로 값을 읽고 모델 생성은 Chat Model이 담당합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.

    # 오용 표현, 올바른 속성 접근, 데이터 및 생성 역할 명세 반환
    return {
        "incorrect": "doc.invoke(question)",
        "correct_read": "doc.page_content",
        "data_role": "본문과 Metadata를 보관",
        "generation_role": "Chat Model의 invoke",
    }
    # raise NotImplementedError("D26-03-A03 TODO 미완성")
    # END D26-03-A03


# Prompt 입력 딕셔너리 생성 함수
# - question과 context 문자열을 키로 갖는 딕셔너리 구성
def make_prompt_input(question: str, context: str) -> dict[str, str]:
    """Document 목록 대신 Prompt가 받을 두 문자열의 dict를 작성합니다."""
    # BEGIN D26-03-A04
    # TODO D26-03-A04: question과 context 문자열을 두 Key의 dict로 반환합니다.
    # 힌트: documents 목록을 그대로 전달하지 않습니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.

    # 질문 및 컨텍스트 문자열 딕셔너리 반환
    return {"question": question, "context": context}
    # raise NotImplementedError("D26-03-A04 TODO 미완성")
    # END D26-03-A04


# 프로그램 진입 함수
# - 구성요소별 입·출력 및 접근 유형 대응표 생성
# - Document 호출 교정 정보와 예시 Prompt 입력을 구성하여 object_contracts.json 저장 및 완료 출력
def main():
    # 구성요소 출력 및 접근 방식 조회
    outputs = component_outputs()
    access = access_kinds()
    # 실행 기록 및 구성요소 계약 대응표 리포트 구성
    report = {
        "execution": execution_record("concept_review"),
        "components": [
            {
                "component": name,
                "input": value,
                "output": outputs[name],
                "access": access[name],
            }
            for name, value in COMPONENT_INPUTS.items()
        ],
        "observation": "입력·출력 대응표; Prompt·모델 invoke는 실행하지 않음",
    }
    # Document 호출 교정 및 샘플 Prompt 입력 추가
    report["document_correction"] = repair_document_call()
    report["prompt_input"] = make_prompt_input(
        "15분 늦으면 어떻게 기록되나요?",
        "[201] attendance_v2.md#sec-1\n" + example_hit()["body"],
    )
    # 결과 JSON 저장 및 완료 메시지 출력
    path = save_json(HERE, "object_contracts.json", report)
    show_success("03 심화", path)


# 스크립트 직접 실행 시 메인 진입점 호출
if __name__ == "__main__":
    main()

"""
RAG 구성요소별 입력·출력 타입과 데이터 읽기(data) 및 실행(invoke) 책임을 명확히 구분하여 객체 계약 대응표를 구성하였다.
Document 객체에 대한 잘못된 invoke 호출 관점을 교정하고, 질문과 정제된 컨텍스트 문자열 기반의 Prompt 입력 구조를 정립함으로써 
구성요소 간 데이터 전달 경계와 역할 분리를 명확히 확립하였다.
"""
