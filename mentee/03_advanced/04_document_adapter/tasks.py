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

# LangChain 문서 객체 및 CLI 인자 파싱 기능 사용
# - Document : 본문(page_content)과 메타데이터(metadata)를 담는 표준 문서 객체
# - argparse : 명령행 옵션 파싱
from langchain_core.documents import Document
import argparse

"""검색 Hit 딕셔너리에서 출처 메타데이터를 추출하여 LangChain Document 객체로 변환하고, 경계 케이스와 보존 무결성을 검증하는 모듈"""


# Hit 메타데이터 추출 함수
# - 보존 대상 6개 키(citation_id, chunk_id, doc_id, source_version, source_locator, category) 정의
# - 각 키에 대응하는 값을 원본 Hit에서 그대로 추출해 딕셔너리로 반환
def metadata_of(hit: dict) -> dict:
    """본문과 분리해서 여섯 Metadata 필드를 그대로 반환합니다."""
    # BEGIN D26-04-A01
    # TODO D26-04-A01: 보존할 여섯 Key를 정하고 입력의 값을 그대로 반환합니다.
    # 힌트: citation_id·chunk_id·doc_id·source_version·source_locator·category입니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.

    # 보존할 여섯 개 메타데이터 키 정의
    keys = (
        "citation_id",
        "chunk_id",
        "doc_id",
        "source_version",
        "source_locator",
        "category",
    )
    # 지정 키 기준 원본 값 그대로 매핑 반환
    return {key: hit[key] for key in keys}
    # raise NotImplementedError("D26-04-A01 TODO 미완성")
    # END D26-04-A01


# 단일 Hit LangChain Document 변환 함수
# - 원본 본문(body)을 page_content로 유지
# - metadata_of 결과를 metadata로 주입하여 Document 생성
def to_document(hit: dict) -> Document:
    """원문 본문을 그대로 두고 출처 Metadata와 함께 Document를 생성합니다."""
    # BEGIN D26-04-A02
    # TODO D26-04-A02: 본문과 metadata_of의 결과로 Document를 생성합니다.
    # 힌트: hit의 body는 수정하지 않습니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.

    # 본문과 추출 메타데이터를 담은 Document 인스턴스 반환
    return Document(page_content=hit["body"], metadata=metadata_of(hit))
    # raise NotImplementedError("D26-04-A02 TODO 미완성")
    # END D26-04-A02


# Hit 목록 일괄 Document 변환 함수
# - 입력 Hit 순서를 유지하며 각 항목을 Document로 변환해 리스트에 누적
def hits_to_documents(hits: list[dict]) -> list[Document]:
    """같은 순서의 Document 목록을 반환합니다."""
    # BEGIN D26-04-A03
    # TODO D26-04-A03: 입력 Hit들을 순서대로 변환합니다.
    # 힌트: to_document를 호출해 빈 목록부터 차례로 채웁니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.

    # 변환된 Document 저장 리스트 초기화
    documents = []
    # 입력 Hit 순회 및 순차 변환
    for hit in hits:
        documents.append(to_document(hit))
    # 변환된 Document 목록 반환
    return documents
    # raise NotImplementedError("D26-04-A03 TODO 미완성")
    # END D26-04-A03


# 경계 조건 검증 함수
# - 빈 Hit 목록 입력 시 빈 Document 목록 반환 확인
# - 복사본에서 source_locator 제거 후 변환 시 KeyError 발생 및 누락 키명 추출
def inspect_boundary_cases(hit: dict) -> dict:
    """교육용 복사본으로 빈 입력과 원문 위치 누락을 대조합니다."""
    # BEGIN D26-04-A04
    # TODO D26-04-A04: 빈 목록과 source_locator가 없는 복사본을 비교합니다.
    # 힌트: dict(hit)로 복사하고 KeyError의 누락 Key를 기록합니다.
    # 함수의 docstring·README·expected/EXPECTED.md에서 입력과 완료 조건을 확인하세요.
    # 구현 후 아래 NotImplementedError를 제거하세요. 정답은 이 아래에 숨겨져 있지 않습니다.

    # 빈 목록 변환 결과 확인
    empty = hits_to_documents([])
    # 원본 보호용 딕셔너리 복사 및 source_locator 키 제거
    incomplete = dict(hit)
    incomplete.pop("source_locator")
    try:
        # 필수 키 누락 항목 변환 시도
        hits_to_documents([incomplete])
    # KeyError 발생 시 누락된 키 문자열 추출
    except KeyError as exc:
        missing_key = str(exc.args[0])
    # 예외 미발생 시 단언 오류 발생
    else:
        raise AssertionError("필수 source_locator 누락을 감지하지 못했습니다.")
    # 빈 입력 건수 및 누락 키 정보 반환
    return {"empty_count": len(empty), "missing_key": missing_key}
    # raise NotImplementedError("D26-04-A04 TODO 미완성")
    # END D26-04-A04


# 메타데이터 보존 검증 관찰 함수
# - 필수 6개 키 집합 일치 여부 및 각 필드 값 동일 여부 검사
def metadata_is_preserved(hit: dict, metadata: dict) -> bool:
    """제공된 관찰 함수: 여섯 필드가 모두 있고 각 값이 같은지 확인합니다."""
    # 필수 보존 메타데이터 키 집합 정의
    required = {
        "citation_id",
        "chunk_id",
        "doc_id",
        "source_version",
        "source_locator",
        "category",
    }
    # 일부 필드만 복사한 결과를 '보존 완료'로 표시하지 않도록 Key 집합부터 확인합니다.
    # 키 집합 완전 일치 및 모든 키의 원본 값 동일성 검사
    return set(metadata) == required and all(
        metadata[key] == hit[key] for key in required
    )


# 프로그램 진입 함수
# - CLI 인자(--live-db, --question, --category, --candidate-k) 파싱
# - 실행 모드에 따른 Hit 데이터 수집 및 LangChain Document 변환
# - 본문/메타데이터 보존 비교 및 경계 케이스 점검 후 document_adapter.json 저장
def main():
    # 명령행 인자 파서 구성 및 인자 파싱
    # - --live-db 플래그, 질의 문구, 카테고리 선택지, 후보 개수 설정
    parser = argparse.ArgumentParser(description="Hit → 실제 LangChain Document 변환")
    parser.add_argument(
        "--live-db",
        action="store_true",
        help="실제 E5·PostgreSQL 검색 결과를 입력으로 사용",
    )
    parser.add_argument("--question", default="15분 늦으면 어떻게 기록되나요?")
    parser.add_argument("--category", default="학사", choices=["학사", "시설", "지원"])
    parser.add_argument("--candidate-k", type=int, default=3)
    args = parser.parse_args()
    # --live-db 옵션 여부에 따른 입력 Hit 획득 분기
    if args.live_db:
        # --live-db를 선택한 경우에만 실제 모델·DB 준비 함수를 불러옵니다.
        # 라이브 DB 및 E5 검색 함수 로드 및 검색 실행
        from coursekit.live import make_search_hits

        search_hits = make_search_hits()
        hits = search_hits(args.question, args.category, k=args.candidate_k)
        mode, input_source = "live_db", "E5_PostgreSQL"
    else:
        # 로컬 고정 픽스처 기반 단일 Hit 구성
        hits = [example_hit()]
        mode, input_source = "local_adapter", "lecture_fixture"
    # Hit 목록을 LangChain Document 목록으로 변환
    documents = hits_to_documents(hits)
    # 원본 Hit와 변환 Document 간 보존 상태 비교 목록 구성
    comparisons = []
    for hit, doc in zip(hits, documents):
        # 각 문서별 인용 ID, 본문/메타데이터 보존 여부, ID 타입 및 내용 기록
        comparisons.append(
            {
                "citation_id": doc.metadata["citation_id"],
                "body_preserved": doc.page_content == hit["body"],
                "metadata_preserved": metadata_is_preserved(hit, doc.metadata),
                "citation_id_type": type(doc.metadata["citation_id"]).__name__,
                "page_content": doc.page_content,
                "metadata": doc.metadata,
            }
        )
    # 최종 리포트 딕셔너리 조립
    report = {
        "execution": execution_record(mode, db=args.live_db, embedding=args.live_db),
        "input_source": input_source,
        "input_count": len(hits),
        "document_count": len(documents),
        "documents": comparisons,
    }
    # 경계 케이스 점검 결과 추가
    report["fixture_boundary_checks"] = inspect_boundary_cases(example_hit())
    # 결과 JSON 저장 및 완료 메시지 출력
    path = save_json(HERE, "document_adapter.json", report)
    show_success("04 심화", path)


# 스크립트 직접 실행 시 메인 진입점 호출
if __name__ == "__main__":
    main()

"""
검색 Hit의 원문 본문과 여섯 가지 출처 메타데이터 필드를 손실 없이 LangChain Document 객체로 변환하는 어댑터를 구현하였다.
빈 입력 및 필수 메타데이터 누락에 대한 경계 검증과 본문·메타데이터 보존 여부 확인 로직을 결합하여, 
후속 프롬프트 구성 및 출처 검증 단계로 넘어가는 문서 객체의 신뢰성과 일관성을 확보하였다.
"""
