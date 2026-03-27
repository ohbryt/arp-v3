
=== DartLab 활용 M&A 스크리닝 코드 ===

# 설치
pip install dartlab

# 한국 기업 스크리닝
from dartlab import Company

# 스크리닝할 기업 리스트 (코드)
KR_CODES = [
    "299660",  # 씨티씨엔씨
    "086900",  # 휴마론
    "058110",  # 제ougou아이엔지
    "348370",  # 시지바이오
    "271940",  # 레고켐바이오
    "334890",  # 에이비드
    "328130",  # 신테카바이오
    "053800",  # 제테마
    "041530",  # 보령제약
]

def screen_company(code):
    c = Company(code)
    
    # 재무제표 추출
    bs = c.balance_sheet
    is_ = c.income_statement
    cf = c.cash_flow
    
    # valuation 지표
    try:
        revenue = is_["revenue"].iloc[-1]
        rd_expense = is_["research_and_development"].iloc[-1]
        rd_ratio = rd_expense / revenue if revenue else 0
    except:
        revenue = rd_ratio = 0
    
    return {
        "code": code,
        "revenue": revenue,
        "rd_ratio": rd_ratio,
        "sections": c.sections,
        "segments": c.segments,
    }

# 미국 기업 (EDGAR)
US_CODES = ["EL", "COTY", "LRLCY", "LGND", "REGN", "CUTR"]
for code in US_CODES:
    try:
        c = Company(code)  # 자동 EDGAR 인식
        print(f"{code}: {c.sections.shape}")
    except Exception as e:
        print(f"{code}: {e}")
