# 실습 07 · 원문 대조 기록

- 선택한 수준: 심화 (07_validation Advanced)
- 실행한 파일: C:\workspace\2026-11-23\mentee\03_advanced\07_validation\outputs\validation_report.json (실행 스크립트: Day26 실습 07 심화)
- 실제 실행한 범위: 고정 입력 Validation / DB·Embedding·LLM 미실행 (mode: "offline", db: false, embedding: false, llm: false)

## 공통 확인

1. Context에 들어간 ID와 허용 ID는 각각 무엇인가요?
    - Context에 들어간 ID: 201 (단일 항목 [201] attendance_v2.md#sec-1이 Context 블록에 포함됨)
    - 허용 ID (included_ids): [201] (실제 Context에 포함된 Document의 metadata["citation_id"]로부터 추출한 집합 {201} 기준)
2. normal 답변의 숫자·조건·예외를 지지하는 원문 문장을 그대로 적고 위치를 밝히세요.
    - 원문 위치: attendance_v2.md#sec-1 (Context 헤더 [201] attendance_v2.md#sec-1 기준)
    - 원문 문장: 수업 시작 후 15분까지 입실하면 지각으로 기록합니다. 15분을 초과하면 결석으로 기록합니다. 단, 사전 승인을 받은 경우에는 운영실에 확인합니다.
    - 대조 요약:
        - 숫자·조건: 15분까지 입실 시 지각, 15분 초과 시 결석이라는 기준과 normal 답변("일반 기준으로 15분까지는 지각입니다...")이 일치합니다.
        - 예외: 단, 사전 승인을 받은 경우에는 운영실에 확인합니다.라는 예외 조건이 답변의 "사전 승인을 받았다면 운영실에 확인합니다."와 부합합니다.
3. unknown_source는 어떤 단계에서 거절됐나요? 검색 후보에만 있던 ID도 허용해도 되나요?
    - 거절 단계 및 사유: receive_bundle 검증 단계에서 거절(rejected)되었으며, 오류 코드는 answer_validation_error입니다. 허용 출처 ID 집합({201})에 없는 999를 인용했기 때문입니다.
    - 검색 후보 ID 허용 여부: 허용하면 안 됩니다. 검색 후보(hits / load_hits)에는 있었더라도 실제 build_context를 거쳐 모델 Context에 포함되지 않은 ID를 허용하면, 모델이 보지 못한 문서를 인용했다고 간주하거나 출처 추적 계약(provided_ids)이 어긋날 수 있습니다. 허용 ID는 반드시 실제 Context에 들어간 문서 기준으로만 구성해야 합니다.
4. insufficient_context가 시스템 오류와 다른 이유를 적으세요.
    - insufficient_context는 모델 호출 및 스키마 파싱/검증이 정상적으로 완료된 상태에서, 제공된 Context 안에 질문에 답할 근거가 없음을 모델이 명시적 상태(status: "insufficient_context")와 정해진 문구("제공된 지식으로는 답할 수 없습니다.")로 정확히 보고한 정상적인 안전 동작(accepted)입니다.
    - 반면 시스템 오류(output_parsing_error, answer_validation_error, generation_not_completed 등)는 출력 형식 파싱 실패, 스키마/출처 제약 위반, 또는 생성 미완료 등 파이프라인·계약·실행 단계의 결함이나 예외 상황을 뜻합니다.

## 선택한 수준의 추가 확인

- 응용: 문자열 ID와 중복 ID의 실패 지점은 어떻게 다른가요?
- 심화: incomplete와 insufficient_context를 비교하세요. wrong_claim이 기계 검사를 통과해도 원문과 맞지 않는 부분을 적으세요.
    - incomplete vs insufficient_context 비교:
        - incomplete (rejected, generation_not_completed): 응답 생성 자체가 온전히 완료되지 못한 수신·완료 상태 이상입니다. 기계 검증 단계에서 거부되며 정상 답변으로 수용되지 않습니다.
        - insufficient_context (accepted, status: "insufficient_context"): 생성은 정상 완료되었고, 주어진 자료에 해당 정보(예: 과제 마감 날짜)가 없음을 규약대로 반환한 정상 판정 상태입니다.
    - wrong_claim이 원문과 맞지 않는 부분:
        - wrong_claim은 status: "answered"이고 source_ids: [201]이 허용 집합 {201} 내에 존재하므로 스키마와 출처 ID 기계 검사는 통과(accepted)합니다.
        - 그러나 답변 내용이 "사전 승인과 무관하게 20분까지는 지각입니다."로 되어 있어, 원문(attendance_v2.md#sec-1)의 15분 지각 / 15분 초과 결석 기준(16~20분은 지각이 아니라 결석)과 사전 승인 시 운영실 확인 예외 모두와 정면으로 배치됩니다. 따라서 기계 검사(accepted)와 별도로 human_review_required: true에 따른 원문 의미 대조에서 부적합(원문 불일치)으로 판정해야 합니다.

자동 검사 통과 여부와 원문 대조 결과를 별도로 기록합니다.
