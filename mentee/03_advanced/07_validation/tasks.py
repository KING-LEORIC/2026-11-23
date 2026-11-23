"""Day26 실습 7 · 심화. 실행 위치와 무관하게 현재 역할 폴더를 사용합니다."""

# 파일 경로 처리 기능 사용
# - Path : 파일 및 디렉터리 경로 관리
from pathlib import Path

# 파이썬 실행 환경 제어 기능 사용
# - sys : 모듈 검색 경로 등록
import sys

# 현재 스크립트 및 역할 루트 경로 등록
# - ROLE_ROOT : 상위 2단계 디렉터리를 역할 루트로 지정
# - sys.path에 추가해 실행 위치와 무관하게 coursekit 모듈 로드 가능
HERE = Path(__file__).resolve().parent
ROLE_ROOT = HERE.parents[1]
sys.path.insert(0, str(ROLE_ROOT))

# 결과 파일 저장 및 완료 출력 기능 사용
# - save_json : 검증 리포트 JSON 저장
# - show_success : 실행 완료 메시지 출력
from coursekit.io import save_json, show_success

# 예시 검색 Hit 로더 사용
# - example_hit : 기준 단일 Hit 데이터 조회
from coursekit.data import example_hit

# 컨텍스트 구성, 상수, 예외 및 번들 수신 검증 함수 사용
# - hits_to_documents : Hit 목록을 Document 목록으로 변환
# - build_context : Context 문자열 및 포함 Document 목록 생성
# - NO_ANSWER : 정보 부족 시 표준 미답변 문구 상수
# - RagServiceError : RAG 검증/서비스 계층 커스텀 예외
# - receive_bundle : 모델 출력 번들 수신 및 스키마·출처 검증
from coursekit.checkpoints import (
    hits_to_documents,
    build_context,
    NO_ANSWER,
    RagServiceError,
    receive_bundle,
)

# 테스트용 고정 번들 생성기 사용
# - fixture_bundle : 검증 시나리오별 고정 응답 번들 구성
from coursekit.fixtures import fixture_bundle

# 실행 환경 메타데이터 기록기 사용
# - execution_record : 실행 모드 기록 딕셔너리 생성
from coursekit.reporting import execution_record

"""공통·타입/중복·수신상태/근거불일치 검증 시나리오 구성, 허용 출처 ID 집합 추출 및 번들 수용·거부 검증 리포트 생성 모듈"""


# 공통 검증 사례 생성 함수
# - 정상 답변(answered), 정보 부족(insufficient_context), 미등록 출처 ID(999) 시나리오 구성
# - 각 사례를 fixture_bundle로 감싸 테스트 케이스 목록 반환
def common_cases():
    """의도적으로 만든 세 입력입니다. 실제 모델의 응답 로그가 아닙니다."""
    # 정상 인용 포함 답변 데이터 정의
    answered = {
        "status": "answered",
        "answer": "일반 기준으로 15분까지는 지각입니다. 사전 승인을 받았다면 운영실에 확인합니다.",
        "source_ids": [201],
        "missing_information": "",
    }
    # 근거 부족 상태 및 미답변 데이터 정의
    insufficient = {
        "status": "insufficient_context",
        "answer": NO_ANSWER,
        "source_ids": [],
        "missing_information": "정확한 과제 마감 날짜가 자료에 없습니다.",
    }
    # 허용 범위에 없는 출처 ID(999) 포함 데이터 정의
    unknown = {**answered, "source_ids": [999]}
    # 세 가지 공통 테스트 케이스 반환
    return [
        {"name": "normal", "bundle": fixture_bundle(answered)},
        {"name": "insufficient", "bundle": fixture_bundle(insufficient)},
        {"name": "unknown_source", "bundle": fixture_bundle(unknown)},
    ]


# 허용 출처 citation_id 집합 추출 함수
# - 실제 Context에 포함된 Document 목록의 metadata에서 citation_id 수집
# - 중복 제거된 set[int] 형태로 반환
def allowed_source_ids(included_docs):
    """입력: 실제 Context에 포함된 Document 목록 / 출력: set[int]."""
    # BEGIN D26-07-A01
    # TODO D26-07-A01: included_docs의 metadata에서 citation_id를 모아 set으로 반환합니다.
    # 힌트: Document 목록을 순회하고 doc.metadata["citation_id"]를 읽으세요. 검색 후보 목록은 사용하지 않습니다.
    # 아래 NotImplementedError를 지우고 이 블록을 완성하세요.

    # 포함된 문서 메타데이터에서 citation_id 집합 구성 및 반환
    return {doc.metadata["citation_id"] for doc in included_docs}
    # raise NotImplementedError("D26-07-A01 TODO 미완성")
    # END D26-07-A01


# 개별 검증 케이스 실행 및 기록 함수
# - receive_bundle로 번들 유효성 및 허용 출처 ID 검증 수행
# - RagServiceError 발생 시 rejected 기록, 성공 시 accepted 및 사람 검토 필요 플래그 기록
def inspect_case(case, provided_ids):
    """검증 결과를 JSON으로 기록합니다. 원문 의미의 참/거짓은 자동 판정하지 않습니다."""
    # BEGIN D26-07-A02
    # TODO D26-07-A02: receive_bundle로 검사한 결과를 accepted/rejected 형식으로 기록합니다.
    # 힌트: 성공 시 KnowledgeAnswer.model_dump(), RagServiceError 시 str(exc)를 사용합니다. 반환 Key는 docstring 아래 호출부와 expected를 확인하세요.
    # 아래 NotImplementedError를 지우고 이 블록을 완성하세요.

    try:
        # 번들 검증 및 파싱된 응답 객체 획득
        answer = receive_bundle(case["bundle"], provided_ids)
    # 검증 실패 시 거부 상태 및 오류 메시지 기록 반환
    except RagServiceError as exc:
        return {
            "case": case["name"],
            "outcome": "rejected",
            "error": str(exc),
            "result": None,
            "human_review_required": False,
        }
    # 검증 통과 시 수용 상태, 딕셔너리 직렬화 결과 및 수동 원문 검토 필요 기록 반환
    return {
        "case": case["name"],
        "outcome": "accepted",
        "error": None,
        "result": answer.model_dump(),
        "human_review_required": True,
    }
    # raise NotImplementedError("D26-07-A02 TODO 미완성")
    # END D26-07-A02


# ID 자료형 및 중복 검증 사례 생성 함수
# - 문자열 ID(["201"]) 사례와 중복 정수 ID([201, 201]) 사례 구성
# - 나머지 답변 필드는 정상 예시와 동일하게 유지
def type_and_duplicate_cases():
    """같은 답변의 ID 자료형과 중복 여부만 바꾸어 검사 지점을 비교합니다."""
    # BEGIN D26-07-A03
    # TODO D26-07-A03: 정상 입력에서 ID만 문자열 또는 중복 정수로 바꾼 두 fixture_bundle 사례를 반환합니다.
    # 힌트: case 이름은 string_id와 duplicate_id입니다. 다른 네 필드는 정상 예시와 같게 유지하세요.
    # 아래 NotImplementedError를 지우고 이 블록을 완성하세요.

    # 기준 정상 응답 데이터 정의
    data = {
        "status": "answered",
        "answer": "15분까지는 지각입니다.",
        "source_ids": [201],
        "missing_information": "",
    }
    # 문자열 ID 및 중복 ID 검증용 두 케이스 반환
    return [
        {
            "name": "string_id",
            "bundle": fixture_bundle({**data, "source_ids": ["201"]}),
        },
        {
            "name": "duplicate_id",
            "bundle": fixture_bundle({**data, "source_ids": [201, 201]}),
        },
    ]
    # raise NotImplementedError("D26-07-A03 TODO 미완성")
    # END D26-07-A03


# 수신 완료 상태 및 의미적 근거 불일치 검증 사례 생성 함수
# - status="incomplete" 수신 미완료 사례 구성
# - 유효 ID(201)를 인용하지만 원문과 다른 주장("20분까지 지각")을 담은 wrong_claim 사례 구성
def receipt_and_grounding_cases():
    """수신 미완료와 의미 오류를 서로 다른 사례로 만듭니다."""
    # BEGIN D26-07-A04
    # TODO D26-07-A04: incomplete 완료 상태 사례와 올바른 ID의 잘못된 주장 사례를 반환합니다.
    # 힌트: case 이름은 incomplete와 wrong_claim입니다. 후자는 20분까지 지각이라고 주장하도록 하되 ID는 201입니다.
    # 아래 NotImplementedError를 지우고 이 블록을 완성하세요.

    # 기준 응답 데이터 및 원문 불일치 주장 데이터 정의
    data = {
        "status": "answered",
        "answer": "15분까지는 지각입니다.",
        "source_ids": [201],
        "missing_information": "",
    }
    wrong = {**data, "answer": "사전 승인과 무관하게 20분까지는 지각입니다."}
    # incomplete 및 wrong_claim 두 테스트 케이스 반환
    return [
        {"name": "incomplete", "bundle": fixture_bundle(data, status="incomplete")},
        {"name": "wrong_claim", "bundle": fixture_bundle(wrong)},
    ]
    # raise NotImplementedError("D26-07-A04 TODO 미완성")
    # END D26-07-A04


# 검증 시나리오 통합 실행 함수
# - 예시 Hit 기반 Document 및 Context 생성 후 허용 출처 ID 산출
# - 전체 검증 케이스를 순회 검사하여 리포트 딕셔너리 반환
def run():
    # 단일 예시 Hit 변환 및 Context·허용 ID 집합 생성
    documents = hits_to_documents([example_hit()])
    context, included_docs = build_context(documents)
    provided_ids = allowed_source_ids(included_docs)
    # 전체 검증 케이스 결합 및 결과 리포트 구성
    cases = common_cases() + type_and_duplicate_cases() + receipt_and_grounding_cases()
    return {
        "source_mode": "validation_fixtures",
        "execution": execution_record("offline"),
        "context": context,
        "included_ids": sorted(provided_ids),
        "cases": [inspect_case(case, provided_ids) for case in cases],
        "grounding_review": "reports/review.md에서 숫자·조건·예외와 원문 위치를 직접 대조합니다.",
    }


# 프로그램 진입 함수
# - 검증 실행 후 validation_report.json 저장 및 완료 알림 출력
# - 케이스별 판정 결과와 원문 대조 안내 문구 출력
def main():
    # 검증 실행 및 결과 파일 저장
    report = run()
    path = save_json(HERE, "validation_report.json", report)
    show_success("07 · 고정 입력 검증표 (모델·DB 미실행)", path)
    # 케이스별 검증 판정 요약 출력
    for row in report["cases"]:
        print(row["case"], row["outcome"], row["error"])
    # 기계 검사 통과와 원문 대조 완료의 구분 안내 출력
    print(
        "accepted는 기계 검사를 통과했다는 뜻입니다. 원문 대조를 마쳐야 학습이 완료됩니다."
    )


# 스크립트 직접 실행 시 메인 진입점 호출
if __name__ == "__main__":
    main()

"""
허용 출처 ID 집합을 실제 Context 포함 문서에서만 추출하도록 구성하고, 정상·미답변·미등록ID·타입오류·중복ID·수신미완료·근거불일치 등 
다양한 경계 시나리오에 대해 receive_bundle 기반 수용/거부 검증을 체계적으로 수행하도록 구현하였다.
이를 통해 스키마·출처·수신 상태의 기계적 검증과 원문 의미 대조(human review)의 책임을 명확히 분리하여 
최종 생성 응답의 신뢰성 검증 체계를 완성하였다.
"""
