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
# - example_hit : 비교 검증용 단일 Hit 예시 조회
# - load_hits : 검색 후보 Hit 목록 조회
from coursekit.data import example_hit, load_hits

# 실행 기록 생성 기능 사용
# - execution_record : 실행 모드 메타데이터 레코드 생성
from coursekit.reporting import execution_record

"""RAG 파이프라인 5단계 처리 순서 정의, 출처·근거 필드 보존, 가상 출석 사례 조건 판정 및 비교 레코드 생성 모듈"""

# 입력·출력 설명은 제공됩니다. TODO에서는 올바른 처리 순서를 연결합니다.
# RAG 파이프라인 단계별 입·출력 명세 카드 정의
STAGE_CARDS = {
    "Generator": {"input": "모델 입력", "output": "생성된 답변"},
    "Prompt": {"input": "규칙·질문·Context", "output": "모델이 읽을 메시지"},
    "Retriever": {"input": "질문·검색 조건", "output": "관련 청크 후보"},
    "Validator · Source 연결": {
        "input": "생성 결과·허용 ID",
        "output": "검증 결과·원문 위치",
    },
    "Context Builder": {"input": "후보 목록", "output": "선택한 근거·포함 ID"},
}


# RAG 처리 단계 순서 반환 함수
# - 검색부터 컨텍스트 구성, 프롬프트 조합, 생성, 출처 검증까지의 파이프라인 순서 고정
def stage_order() -> list[str]:
    """STAGE_CARDS의 이름 다섯 개를 처리 순서대로 반환합니다."""
    # BEGIN D26-01-A01
    # TODO D26-01-A01: 다섯 단계의 처리 순서를 반환합니다.
    # 힌트: 검색과 생성 사이에 Context 선택과 Prompt 작성이 필요합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.

    # 파이프라인 처리 순서 리스트 반환
    return [
        "Retriever",
        "Context Builder",
        "Prompt",
        "Generator",
        "Validator · Source 연결",
    ]
    # raise NotImplementedError("D26-01-A01 TODO 미완성")
    # END D26-01-A01


# 출처 및 근거 필드 추출 함수
# - 입력 Hit에서 인용 ID, 문서 ID, 소스 버전, 위치 로케이터, 근거 본문 보존
def evidence_fields(hit: dict) -> dict:
    """출처와 근거 본문을 비교 기록에 넣을 공통 필드로 반환합니다."""
    # BEGIN D26-01-A02
    # TODO D26-01-A02: 입력 Hit의 출처와 본문 필드를 보존합니다.
    # 힌트: 숫자나 예외 문장을 새로 만들지 않습니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.

    # 공통 근거 포맷 딕셔너리 반환
    return {
        "citation_id": hit["citation_id"],
        "doc_id": hit["doc_id"],
        "source_version": hit["source_version"],
        "source_locator": hit["source_locator"],
        "evidence": hit["body"],
    }
    # raise NotImplementedError("D26-01-A02 TODO 미완성")
    # END D26-01-A02


# 가상 출석 사례 판정 함수
# - minutes 및 prior_approval 인자 타입·범위 유효성 검사
# - 사전 승인 예외, 0분 정시 예외, 15분 경계 기준 지각/결석 판정 수행
def attendance_judgment(minutes: int, prior_approval: bool = False) -> str:
    """강의의 가상 사례를 조건문으로 대조합니다. 실제 기관의 출석 판정기가 아닙니다."""
    # BEGIN D26-01-A03
    # TODO D26-01-A03: 15분 경계와 사전 승인 예외를 원문대로 구분합니다.
    # 힌트: 사전 승인이라면 운영실 확인, 그렇지 않은 1~15분은 지각, 15분 초과는 결석입니다. 0분은 비교 대상 밖으로 표시합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.

    # minutes 타입 및 음수 여부 검증
    # - bool 제외 순수 int 타입 및 0 이상 정수만 허용
    if type(minutes) is not int or minutes < 0:
        raise ValueError("minutes는 0 이상의 정수여야 합니다.")
    # prior_approval 불리언 타입 검증
    if type(prior_approval) is not bool:
        raise TypeError("prior_approval은 bool이어야 합니다.")
    # 사전 승인 여부 최우선 확인
    # - 승인 시 '운영실 확인' 반환
    if prior_approval:
        return "운영실 확인"
    # 0분 입실 비교 대상 제외 안내 반환
    if minutes == 0:
        return "정시 입실: 이 실습의 지각 비교 대상 아님"
    # 15분 이하 지각, 15분 초과 결석 판정 반환
    return "지각" if minutes <= 15 else "결석"
    # raise NotImplementedError("D26-01-A03 TODO 미완성")
    # END D26-01-A03


# 비교 사례 목록 생성 함수
# - (15분, 미승인), (20분, 미승인), (20분, 승인) 세 시나리오 순회
# - 각 사례별 판정 결과와 동일 근거 필드를 결합한 레코드 생성
def comparison(hit: dict) -> list[dict]:
    """15분·20분·사전 승인 20분의 세 사례를 같은 원문과 연결합니다."""
    # BEGIN D26-01-A04
    # TODO D26-01-A04: 15분·20분·사전 승인 20분 세 행에 판단과 동일 근거를 묶습니다.
    # 힌트: 앞의 두 함수를 호출하여 각 행을 작성하세요.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.

    # 검증 대상 케이스 정의 및 결과 행 리스트 초기화
    cases = [(15, False), (20, False), (20, True)]
    rows = []
    # 각 시나리오별 판정 수행 및 출처 정보 병합
    for minutes, approved in cases:
        rows.append(
            {
                "minutes": minutes,
                "prior_approval": approved,
                "judgment": attendance_judgment(minutes, approved),
                **evidence_fields(hit),
            }
        )
    # 구성된 비교 행 목록 반환
    return rows
    # raise NotImplementedError("D26-01-A04 TODO 미완성")
    # END D26-01-A04


# 프로그램 진입 함수
# - 개념 검토 실행 기록 및 파이프라인 단계 명세 구성
# - 예시 Hit 기반 비교 결과 생성 후 rag_flow.json 저장 및 완료 알림 출력
def main():
    # 최종 리포트 딕셔너리 구성
    report = {
        "execution": execution_record("concept_review"),
        "stages": [{"stage": name, **STAGE_CARDS[name]} for name in stage_order()],
        "cases": comparison(example_hit()),
        "observation": "원문의 조건을 Python 조건문으로 대조한 교육용 기록; LLM 호출 아님",
    }
    # 결과 JSON 저장 및 실행 완료 메시지 출력
    path = save_json(HERE, "rag_flow.json", report)
    show_success("01 Advanced", path)


# 스크립트 직접 실행 시 메인 진입점 호출
if __name__ == "__main__":
    main()

"""
RAG 파이프라인의 핵심 처리 단계 순서를 명확히 정의하고, 검색 Hit의 출처와 근거 본문을 훼손 없이 보존하도록 구현하였다.
가상 출석 사례에 대한 조건 분기 판정과 동일 근거 매핑을 결합함으로써, 
LLM 호출 이전 단계에서 규칙 대조와 출처 추적 흐름이 일관되게 작동하는 기반을 마련하였다.
"""
