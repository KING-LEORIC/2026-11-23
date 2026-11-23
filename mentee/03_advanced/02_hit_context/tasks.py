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

"""검색 Hit 후보를 포맷팅하고 상위 항목을 선택하여 모델 입력용 Context 문자열과 허용 인용 ID 목록을 생성하는 모듈"""


# 단일 Hit 문자열 블록 포맷팅 함수
# - citation_id, source_locator, body 필드를 추출해 '[ID] 위치\n본문' 형태로 조합
def format_hit(hit: dict) -> str:
    """Hit 한 건의 ID·위치·본문을 한 문자열 블록으로 반환합니다."""
    # BEGIN D26-02-A01
    # TODO D26-02-A01: [ID] 원문위치, 줄바꿈, 본문 순서로 한 블록을 만듭니다.
    # 힌트: citation_id·source_locator·body를 읽어 f-string으로 연결합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.

    # 출처 ID, 위치 정보, 본문 추출
    citation_id = hit["citation_id"]
    locator = hit["source_locator"]
    body = hit["body"]
    # 헤더 라인과 본문을 개행으로 연결한 문자열 반환
    return f"[{citation_id}] {locator}\n{body}"
    # raise NotImplementedError("D26-02-A01 TODO 미완성")
    # END D26-02-A01


# 상위 Hit 목록 선택 함수
# - 기존 순서를 유지한 채 앞에서부터 최대 max_items건까지 슬라이싱
def select_hits(hits: list[dict], max_items: int = 2) -> list[dict]:
    """입력 순서를 유지해 앞의 최대 max_items건만 고릅니다."""
    # BEGIN D26-02-A02
    # TODO D26-02-A02: 입력 순서대로 앞의 최대 max_items건을 선택합니다.
    # 힌트: 목록 슬라이스를 사용합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.

    # 최대 개수 제한 슬라이스 반환
    return hits[:max_items]
    # raise NotImplementedError("D26-02-A02 TODO 미완성")
    # END D26-02-A02


# Context 문자열 및 포함 citation_id 동시 생성 함수
# - select_hits로 선별된 후보만을 대상으로 포맷팅 블록과 ID 목록 구성
# - 빈 줄('\n\n') 구분자로 블록을 결합한 Context와 included_ids 튜플 반환
def make_context(hits: list[dict], max_items: int = 2) -> tuple[str, list[int]]:
    """선택한 목록에서 Context와 포함 ID를 동시에 만듭니다."""
    # BEGIN D26-02-A03
    # TODO D26-02-A03: 선택 결과를 문자열로 연결하고 같은 Hit의 citation_id 목록을 반환합니다.
    # 힌트: 본문과 ID 수집을 같은 for 반복문 안에 둡니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.

    # 최대 개수 기준 후보 선별
    selected = select_hits(hits, max_items)
    # 포맷팅 블록 및 인용 ID 누적 리스트 초기화
    blocks = []
    included_ids = []
    # 선별된 각 Hit의 문자열 블록과 citation_id 수집
    for hit in selected:
        blocks.append(format_hit(hit))
        included_ids.append(hit["citation_id"])
    # 블록 결합 Context 문자열과 포함 ID 리스트 반환
    return "\n\n".join(blocks), included_ids
    # raise NotImplementedError("D26-02-A03 TODO 미완성")
    # END D26-02-A03


# 빈 입력과 단건 입력 출력 비교 함수
# - 빈 Hit 리스트 입력 시 빈 문자열 및 빈 ID 목록 생성 확인
# - 단일 Hit 입력 시 생성되는 Context 및 ID 목록과 나란히 구성
def compare_empty_and_one(hit: dict) -> dict:
    """빈 목록과 한 건의 출력 차이를 나란히 기록합니다."""
    # BEGIN D26-02-A04
    # TODO D26-02-A04: 빈 목록과 한 건을 각각 호출해 두 결과를 저장합니다.
    # 힌트: 빈 경우도 make_context를 실제 호출하여 확인하세요.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.

    # 빈 입력 및 단일 입력 기준 Context·ID 쌍 생성
    empty_context, empty_ids = make_context([])
    one_context, one_ids = make_context([hit])
    # 두 케이스 비교 딕셔너리 반환
    return {
        "empty": {"context": empty_context, "included_ids": empty_ids},
        "one": {"context": one_context, "included_ids": one_ids},
    }
    # raise NotImplementedError("D26-02-A04 TODO 미완성")
    # END D26-02-A04


# 프로그램 진입 함수
# - 예시 Hit 기반 Context 및 포함 ID 생성 후 리포트 구성
# - 문자 수 및 빈/단건 비교 결과 추가 후 hit_context.json 저장 및 완료 알림 출력
def main():
    # 예시 Hit 조회 및 Context 생성
    hit = example_hit()
    context, included_ids = make_context([hit])
    # 실행 기록 및 Context 메타데이터 리포트 구성
    report = {
        "execution": execution_record("local_python"),
        "context": context,
        "included_ids": included_ids,
        "input_source": "lecture_fixture",
        "character_count": len(context),
    }
    # 빈 입력과 단일 입력 비교 결과 기록
    report["comparison"] = compare_empty_and_one(hit)
    # 결과 JSON 저장 및 완료 메시지 출력
    path = save_json(HERE, "hit_context.json", report)
    show_success("02 심화", path)


# 스크립트 직접 실행 시 메인 진입점 호출
if __name__ == "__main__":
    main()

"""
검색 후보 Hit의 출처 ID·로케이터·본문을 일관된 텍스트 블록으로 변환하고, 실제 Context에 포함된 후보만 허용 출처 ID로 동기화하도록 구현하였다.
또한 빈 입력과 단일 입력의 경계 동작을 비교 기록함으로써, LLM 프롬프트 구성 이전 단계에서 Context 품질과 출처 추적의 정합성을 확보하였다.
"""
