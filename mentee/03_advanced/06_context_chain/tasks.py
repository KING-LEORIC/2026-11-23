"""실습 06 · Context·출처를 보관하고 Runnable Chain을 실행합니다."""

# 파일 경로 처리 기능 사용
# - Path : 파일 및 디렉터리 경로 관리
from pathlib import Path

# 명령행 인자 파싱 및 시스템 환경 제어 기능 사용
# - argparse : CLI 플래그(--offline 등) 처리
# - sys : 모듈 검색 경로 등록
import argparse
import sys

# 현재 실습 디렉터리 및 상위 루트 경로 등록
# - HERE : 현재 스크립트 위치
# - sys.path에 추가하여 실행 위치와 무관하게 coursekit 모듈 로드 가능
HERE = Path(__file__).resolve().parent
# 어느 폴더에서 실행해도 이 역할 폴더의 coursekit을 사용합니다.
sys.path.insert(0, str(HERE.parents[1]))

# 검색 Hit 데이터 로더 사용
# - load_hits : 평가용 Hit 목록 조회
from coursekit.data import load_hits

# Context 빌더, 프롬프트 및 구조화 출력 스키마 사용
# - hits_to_documents : Hit 목록을 Document 목록으로 변환
# - build_context : 항목 수 및 문자 상한 기준 Context 문자열·포함 문서 구성
# - make_prompt : 프롬프트 템플릿 생성
# - WireAnswer : 구조화 출력 스키마 정의
from coursekit.checkpoints import (
    hits_to_documents,
    build_context,
    make_prompt,
    WireAnswer,
)

# Chat Model 생성 및 오프라인 픽스처 기능 사용
# - create_chat_model : 실제 Chat Model 객체 생성
# - fixture_generation : 오프라인 테스트용 고정 bundle 생성
from coursekit.llm import create_chat_model
from coursekit.fixtures import fixture_generation

# 리포트 레코드 포맷터 및 파일 입출력 기능 사용
# - execution_record, bundle_record : 실행 환경 및 구조화 bundle 기록 포맷 생성
# - save_json, show_success : 결과 JSON 저장 및 완료 출력
from coursekit.reporting import execution_record, bundle_record
from coursekit.io import save_json, show_success

"""Document 기반 Context 조립, Runnable Chain 실행, 중복·길이 경계 및 빈 Context 스킵 동작을 관찰·기록하는 모듈"""


# Context 및 프롬프트 입력 구성 함수
# - build_context로 선택된 문서 기반 Context 문자열과 포함 문서 목록 생성
# - 실제 포함된 문서의 citation_id 목록과 question/context 입력 dict 반환
def prepare_context(documents, question: str, max_items=2, max_chars=600) -> dict:
    """Document 목록 → Context·포함 문서·포함 ID·Prompt 입력. 원문은 바꾸지 않습니다."""
    # BEGIN D26-06-A01
    # TODO D26-06-A01: build_context로 Context와 포함 문서를 얻고, 포함 ID 및 Prompt 입력을 함께 반환합니다.
    # 힌트: 반환 Key는 context, included_docs, provided_ids, inputs입니다. ID는 included_docs에서만 모읍니다.
    # 완료 후 아래 NotImplementedError를 제거하고 반환값을 확인하세요.

    # 최대 개수 및 문자 상한 적용하여 Context와 포함 문서 구성
    context, included_docs = build_context(
        documents, max_items=max_items, max_chars=max_chars
    )
    # 실제 포함된 문서들에서만 citation_id 수집
    provided_ids = [doc.metadata["citation_id"] for doc in included_docs]
    # Context, 포함 문서, ID 목록 및 프롬프트 입력 dict 반환
    return {
        "context": context,
        "included_docs": included_docs,
        "provided_ids": provided_ids,
        "inputs": {"question": question, "context": context},
    }
    # raise NotImplementedError("D26-06-A01 TODO 미완성")
    # END D26-06-A01


# Runnable Chain 실행 함수
# - 공백 제외 Context가 비어 있으면 모델 호출 없이 None 반환
# - 유효 Context에서는 prompt | structured_model 체인 구성 후 invoke 실행
def run_generation(prompt, structured_model, inputs: dict):
    """Prompt → Structured Model의 bundle. bundle 검증·승인은 다음 실습입니다."""
    # BEGIN D26-06-A02
    # TODO D26-06-A02: 빈 Context에서는 None을 반환하고, 나머지는 Prompt와 Structured Model을 연결하여 bundle을 받습니다.
    # 힌트: 빈 문자열을 먼저 확인하여 모델 호출 전에 반환합니다. 정상 Context에서는 |와 invoke를 사용합니다.
    # 완료 후 아래 NotImplementedError를 제거하고 반환값을 확인하세요.

    # Context 비어 있음 여부 확인 후 조기 반환
    if not inputs["context"].strip():
        return None
    # 프롬프트와 구조화 모델 파이프 연결 및 실행
    generation = prompt | structured_model
    return generation.invoke(inputs)
    # raise NotImplementedError("D26-06-A02 TODO 미완성")
    # END D26-06-A02


# Context 구성 조건 비교 함수
# - 기본 설정, 중복 문서 삽입, max_items=1 조건별 포함 citation_id 비교
# - LLM 호출 없이 build_context 선택 결과만 대조
def compare_contexts(documents) -> dict:
    """같은 목록에서 중복과 선택 개수를 각각 바꿉니다. LLM 호출은 없습니다."""
    # BEGIN D26-06-A03
    # TODO D26-06-A03: 기본·중복 청크 추가·max_items=1 조건을 각각 실행하여 포함 ID를 비교합니다.
    # 힌트: 세 조건에서 한 가지 설정만 바꿉니다. 모델은 호출하지 않고 build_context 결과만 비교합니다.

    # 첫 문서를 복제한 중복 포함 리스트 구성
    with_duplicate = [documents[0], documents[0], *documents[1:]] if documents else []
    # 세 가지 조건별 build_context 실행
    _, baseline = build_context(documents, max_items=2, max_chars=600)
    _, duplicated = build_context(with_duplicate, max_items=2, max_chars=600)
    _, one_document = build_context(documents, max_items=1, max_chars=600)
    # 각 조건별 포함 citation_id 목록 및 LLM 호출 수(0) 반환
    return {
        "baseline_ids": [doc.metadata["citation_id"] for doc in baseline],
        "duplicate_ids": [doc.metadata["citation_id"] for doc in duplicated],
        "one_document_ids": [doc.metadata["citation_id"] for doc in one_document],
        "llm_calls": 0,
    }
    # raise NotImplementedError("D26-06-A03 TODO 미완성")
    # END D26-06-A03


# 문자 상한 경계 비교 함수
# - 단일 문서 블록 전체 문자 길이 계산
# - 상한(길이 - 1)과 정확한 상한(길이)에서의 포함 Context 및 ID 비교
def inspect_boundary(document) -> dict:
    """문자 상한의 직전·정확한 경계 비교. Token 개수를 계산하는 함수가 아닙니다."""
    # BEGIN D26-06-A04
    # TODO D26-06-A04: 첫 Document 블록 길이보다 1자 작은 상한과 정확한 길이의 상한에서 포함 여부를 비교합니다.
    # 힌트: ID·위치·줄바꿈·본문을 포함한 블록 전체 길이를 계산합니다. 본문을 슬라이스로 자르지 않습니다.
    # 완료 후 아래 NotImplementedError를 제거하고 반환값을 확인하세요.

    # 메타데이터 및 전체 블록 문자열 구성·길이 계산
    meta = document.metadata
    block_text = (
        f"[{meta['citation_id']}] {meta['source_locator']}\n{document.page_content}"
    )
    size = len(block_text)
    # 상한 size - 1 및 size 조건에서 Context 생성 비교
    before_context, before_docs = build_context(
        [document], max_items=1, max_chars=size - 1
    )
    exact_context, exact_docs = build_context([document], max_items=1, max_chars=size)
    # 경계별 상한값, Context 문자열, 포함 ID 및 LLM 호출 수 반환
    return {
        "block_chars": size,
        "before_limit": size - 1,
        "exact_limit": size,
        "before_context": before_context,
        "before_ids": [doc.metadata["citation_id"] for doc in before_docs],
        "exact_context": exact_context,
        "exact_ids": [doc.metadata["citation_id"] for doc in exact_docs],
        "llm_calls": 0,
    }
    # raise NotImplementedError("D26-06-A04 TODO 미완성")
    # END D26-06-A04


# 프로그램 진입 함수
# - --offline 옵션 파싱 및 학사 카테고리 Hit → Document 변환
# - Context 준비, 중복/길이 경계 실험, 빈 Context 스킵 검증 및 Runnable Chain 실행
# - 실행 결과와 관찰 지표를 context_chain.json으로 저장
def main():
    # CLI 인자 파서 구성 및 --offline 플래그 파싱
    parser = argparse.ArgumentParser(
        description="Context → Prompt → Structured Model 관찰"
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="고정 bundle 예시만 사용; 실제 모델 미실행",
    )
    args = parser.parse_args()
    # 앞 실습의 미완성 코드에 의존하지 않는 제공된 Document 변환 Checkpoint입니다.
    # 학사 카테고리 Hit 필터링 및 Document 객체 변환
    academic_hits = [hit for hit in load_hits() if hit["category"] == "학사"]
    documents = hits_to_documents(academic_hits)
    # 검증 질의 설정 및 Context·프롬프트 입력 준비
    question = "15분 늦으면 어떻게 기록되나요?"
    prepared = prepare_context(documents, question)
    # Context 비교 및 문자 상한 경계 실험 결과 수집
    experiments = {}
    experiments["context_comparison"] = compare_contexts(documents)
    experiments["length_boundary"] = inspect_boundary(documents[0])
    # 프롬프트 템플릿 생성 및 실행 모드별 구조화 출력 모델 준비
    prompt = make_prompt()
    if args.offline:
        # 이 Runnable은 제공된 고정 bundle을 반환합니다. 실제 모델 실행은 아닙니다.
        # 오프라인 고정 bundle 반환 모델 사용
        structured_model = fixture_generation()
    else:
        # 라이브 모델 설정과 Schema를 준비하는 단계입니다. 아직 API를 호출하지 않습니다.
        # 라이브 Chat Model 및 WireAnswer 구조화 출력 래퍼 구성
        chat_model = create_chat_model()
        structured_model = chat_model.with_structured_output(
            WireAnswer, method="json_schema", strict=True, include_raw=True
        )
    # 준비된 입력으로 구조화 생성 체인 실행
    bundle = run_generation(prompt, structured_model, prepared["inputs"])
    # 빈 Context 확인은 실패해야 하는 로컬 Spy로 검사합니다. 유료 모델을 다시 호출하지 않습니다.
    # 빈 Context 호출 차단 확인용 로컬 스파이 Runnable 구성 및 실행
    from langchain_core.runnables import RunnableLambda

    def forbidden_call(_):
        # 빈 Context에서 모델이 호출될 경우 단언 오류 발생
        raise AssertionError("빈 Context에서 모델을 호출했습니다.")

    skipped = run_generation(
        prompt, RunnableLambda(forbidden_call), {"question": question, "context": ""}
    )
    # 빈 Context 스킵 여부 실험 결과 기록
    experiments["empty_context"] = {
        "generation_skipped": skipped is None,
        "llm_calls": 0,
    }
    # 정상 Context 생성 결과 존재 여부 검증 및 인용 ID 추출
    if bundle is None:
        raise AssertionError("이번 정상 예시의 Context는 비어 있지 않아야 합니다.")
    parsed = bundle.get("parsed")
    cited_ids = list(parsed.source_ids) if parsed is not None else []
    # 전체 관찰 리포트 딕셔너리 조립
    result = {
        "exercise": "06_context_chain",
        "execution": execution_record(
            "offline_fixture" if args.offline else "live", llm=not args.offline
        ),
        "real_model_calls": 0 if args.offline else 1,
        "context": prepared["context"],
        "included_ids": prepared["provided_ids"],
        "included_sources": [dict(doc.metadata) for doc in prepared["included_docs"]],
        "prompt_input": prepared["inputs"],
        "bundle": bundle_record(bundle),
        "observed_source_ids": cited_ids,
        "source_id_membership_only": None
        if parsed is None
        else set(cited_ids).issubset(prepared["provided_ids"]),
        "experiments": experiments,
        "human_evidence_review": "pending",
        "review_note": "bundle·포함 ID를 관찰한 기록입니다. 자료형·상태·출처의 승인 검사는 실습07에서 진행합니다.",
    }
    # 결과 JSON 저장, 완료 알림 및 콘솔 요약 출력
    path = save_json(HERE, "context_chain.json", result)
    show_success("06 Context·Runnable 관찰 기록", path)
    print("실제 LLM 실행:", not args.offline, "| 검증 승인 전 bundle 관찰")


# 스크립트 직접 실행 시 메인 진입점 호출
if __name__ == "__main__":
    main()

"""
문서 목록으로부터 Context 문자열과 포함 citation_id를 동기화 구성하고, 빈 Context 조기 스킵 및 Prompt-Structured Model Runnable 체인을 실행하도록 구현하였다.
중복 문서 삽입, max_items 변화, 문자 상한(N-1 vs N) 경계 조건과 빈 입력 차단 여부를 체계적으로 관찰함으로써, 
구조화 생성 단계 이전의 컨텍스트 제어와 인용 후보 추적의 신뢰성을 확보하였다.
"""
