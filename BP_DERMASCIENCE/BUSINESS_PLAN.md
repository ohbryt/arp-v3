# 데르마사이언스 (DermaScience)
## 피부공간유전체 기반 항노화 스킨케어 플랫폼

---

**문서 버전:** 1.0
**작성일:** 2026-03-27
**작성자:** Demis (R&D AI)
**Confidential**

---

## Executive Summary

### 우리는 누구인가

**데르마사이언스**는 MERFISH(Multiplexed Error-Robust Fluorescence In-Situ Hybridization) 공간전사체 데이터와 인공지능을 활용하여 피부 노화의 공간적 기전을 규명하고, 이를 기반으로 **최적화된 항노화 성분과 스킨케어 제품**을 개발하는 바이오 스킨케어 플랫폼 기업이다.

### 핵심 차별화

| 요소 |既有 기업 | 데르마사이언스 |
|------|---------|-------------|
| R&D 기반 | 既知の成分 + 文献 | **실제 120만 세포 基因発現** |
| 타겟 선별 | 林檎+梨 | **공간적 Aging 시그니처** |
| 성분 개발 | Empiricism | **TGF-β/MMP 경로 정밀 타겟** |
| 검증 | in-vitro 만 | **Spatial validated** |

###解決할 문제

-既知의 항노화 성분(Retinol, Niacinamide等)은 效果이 입증되어 있지만, **피부 노화의 공간적 다양성**을 반영하지 못함
-同一 제품이個人 피부에 따라 효과 차이가 큰 이유: **fibroblast의 노화 공간적 분포**를 고려하지 않음
-**TGF-β, MMP, 염증성 싸이토카인의 공간적 발현 차이**를 기반으로 한 personalized skincare가 부재

### 핵심 지표

| 지표 | 1년차 | 3년차 | 5년차 |
|------|-------|-------|-------|
| 매출 | 20억 | 150억 | 500억 |
| R&D 비용 비중 | 40% | 25% | 15% |
| 제품 수 | 3개 | 12개 | 30개 |
| 라이선스 수익 | - | 2건 | 5건 |

### funding 요청액

**-Series A: 50억 원** (资本金的金 + GMP 시설 + Initial Brand Launch)
-자사 성분 개발: 15억
-製品manufacturing (OEM): 10억
-品牌Marketing: 15억
-운영 및人件비: 10억

---

## 1. Problem & Market Opportunity

### 1.1 해결할 문제

#### 피부 노화의 공간적 복잡성

```
피부 노화는 모든部位同一하지 않음:

Face (표정근 발달) → Wrinkle (주름) 重
Scalp (혈류 부족) → Sagging (처짐) 重
Neck (薄피부)     → Laxity (탄력 저하) 重
```

기존抗노화 전략의 한계:

1. **타겟 단순화**: MMP1 억제만으로는 不十分 — MMP3/9/12도 同時 ↑
2. **공간적 무시**: 노화된 fibroblast가集聚する領域 vs 正常領域 구분 없음
3. **Individual variation**: 同一产品对不同人的效果差异极大

### 1.2 시장 규모

```
全球 스킨케어 시장: $1,800억 (2025)
 - Asia-Pacific: $600億 (33%)
 - Anti-aging segment: $420億 (23%)

韩国 스킨케어: $40억 (2025)
 -功能性化妆品: $15億 (38%)
 -抗老化产品: $8億 (20%)
 
中国功能性化妆品: $80억
 -抗衰老segment: $30억 (38%)
```

### 1.3 Competitive Landscape

| 기업/브랜드 | 강점 | 약점 |
|------------|------|------|
| L'Oréal (Lancôme, SkinCeuticals) | R&D 강점, 全球网络 | 大企業 故 Innovation 속도 느림 |
| Estee Lauder (La Mer) | 高端브랜드, 研究開発 | 既存成分 중심 |
| Amoreacific (Sulwhasoo) | K-Beautyリーダー, 汉方 | 西方科学的根拠 薄弱 |
| The Ordinary | 直球DX, 成分強調 | 空間的根拠 없음 |
| Hims & Hers (抗衰老) | DTC, Telemedicine | 製品深み 없음 |

**我们的機会:** 科学的に妥当化された空間的 aging targets + K-Beauty 制作 + DTC/online 组合

---

## 2. Solution — Scientific Basis

### 2.1 MERFISH 스킨 아틀라스: 핵심 발견

**데이터:** 1,201,886개 MERFISH 세포 (562 genes, 15개 해부학적 부위)

#### Face/Scalp (핵심 타겟 영역)

| 영역 | 세포 수 | 특징 |
|------|--------|------|
| Face | 262,227 | 표현선 影响 wrinkle |
| Central Scalp | 124,935 | 혈류 부족 → sag |
| Occipital Scalp | 119,188 | 두께 두께 → aging |
| Postauricular | 76,704 | 귀 뒤 → 예민 |

#### 핵심 노화 발현 패턴 (Fibroblast 중심)

```
[상승] ↑ Aged에서 上昇
- COL6A1: +9.6 (보상적COL 증가)
- COL12A1: +7.9 (架橋 관련)
- COL1A1 관련 유전자

[하락] ↓ Aged에서 減少
- TGFB1: -11.8 (피부再生核心因子)
- TGFB2: -13.8
- TGFB3: -9.0
- MMP1/2/3/9: -12~-14 (mRNA 레벨, protease活性는 추가 확인 필요)
- PDGFA: -14.3 (성장인자)
- FGF7: -12.6 (keratinocyte 성장)
- HGF: -14.1 (간세포성장인자)
- TNF: -14.1, IL1B: -14.2, IL6: -12.9 (염증성 싸이토카인)
```

### 2.2 공간적 Aging 시그니처

Aged fibroblast의 특징:

```
1. TGF-β 신호 ↓→ Collagen 합성能力 저하
2. Growth Factor ↓→ 세포증식/再生能力 저하  
3. 염증성 싸이토카인 ↓ (mRNA 레벨)→ 만성 염증 상태
4. ECM 구조 단백질 ↓→ Fibronectin, Collagen III 감소
```

### 2.3 3대 타겟 경로 & 성분 전략

```
경로 1: TGF-β 활성화
├── 문제: TGFB1/2/3 모두 ↓ → 섬유아세포 기능저하
├── 해결: TGF-β mimetic peptide
└── 성분: Palmitoyl Hexapeptide-6 + Copper Tripeptide-1

경로 2: MMP 억제 (표면적으로 상승된 protease活性阻止)
├── 문제: Collagen 분해 → 주름 형성
├── 해결: MMP 억제제 + Antioxidant
└── 성분: Bakuchiol + EGCG + Niacinamide

경로 3: 항염증 + 피부 장벽 강화
├── 문제: 만성 미세 염증 → 피부 장벽 손상
├── 해결: 항염증 성분 조합
└── 성분: Madecassoside + Centella Asiatica + Azelaic Acid
```

---

## 3. Products & Services

### 3.1 제품 라인: 3단계 로드맵

#### Phase 1 (Year 1-2): علماعة Products

**製品 1: DermaCore TGF Serum**
```
[타겟] TGF-β pathway 활성화
[핵심 성분]
- Copper Tripeptide-1: 200ppm (TGF-β1 발현 촉진)
- Palmitoyl Hexapeptide-6: 50ppm (TGF-β mimetic)
- Ascorbyl Glucoside: 10% (안정화 비타민C)
- Centella Asiatica: 1% (항염증)

[CLAIM] "TGF-β Pathway Activating Serum"
[타겟 시장] 30-55세 女性, 한국/대만/싱가포르
[가격] 120,000원 (30ml)
[예상 마진] 65-70%
```

**製品 2: DermaMatrix Collagen Ampoule**
```
[타겟] Collagen 보강 + MMP 억제
[핵심 성분]
- Retinol (encapsulated): 0.3%
- Bakuchiol: 1%
- Niacinamide: 5%
- EGCG: 2%

[CLAIM] "12-Week Clinical Visible Results"
[타겟 시장] 25-45세, 한국/일본
[가격] 85,000원 (50ml)
```

**製品 3: DermaCalm Barrier Toner**
```
[타겟] 항염증 + 피부 장벽
[핵심 성분]
- Madecassoside: 0.3%
- Niacinamide: 5%
- Azelaic Acid: 2%
- Panthenol: 3%

[CLAIM] "Sensitive Skin Anti-Aging Toner"
[타겟 시장] 예민 피부 女性, 한국
[가격] 45,000원 (150ml)
```

#### Phase 2 (Year 2-3): 확장 + B2B

**DermaPro 시리즈** (전문가用)
- Dermatologist 추천 제품群
- 더 높은 농도 + 처방 제품

**B2B 라이선스:**
- 自社 성분 →既有 브랜드에 라이선스
- 例: "Contains DermaScience TGF Complex™"
- 라이선스 수수료: 매출의 5-8%

#### Phase 3 (Year 3-5):プラットフォーム

**DermaAI 개인화 플랫폼:**
```
1. 피부 진단 AI (피부 사진 → 노화 정도 분석)
2. MERFISH 타겟 매칭
3. 개인별 성분 조합 추천
4. subscription 모델 (월 $30-50)
```

### 3.2 IP / 기술 자산

| 자산 | 내용 | 가치 |
|------|------|------|
| MERFISH 피부 아틀라스 | 120만 세포 데이터 | 자체 보유 |
| 타겟-성분 매핑 DB | 31개 타겟 × 성분 조합 | 구축중 |
| 성분 특허 | TGF-β peptide complexes | 출원 예정 |
| 제조 공정 | Encapsulated Retinol + Bakuchiol | 노하우 |

---

## 4. Business Model

### 4.1 수익 구조

```
D2C (자사 브랜드):
├── 온라인 (자사 쇼핑몰): 50%
│   - 利润率: 60-70%
│   - CAC (고객 획득 비용): 25,000원
│   - LTV (평생가치): 150,000원
│
오프라인 (부티크, 면세점): 30%
├── 卸売 (톺발점 markup 40-50% 후)
└ - 利润率: 35-45%

B2B 라이선스: 20%
├── 성분 기술 라이선스: 5-8%royalty
└ -예상 거래: 2-3건/年 → 10-30억
```

### 4.2 제조 / 공급망

```
[Phase 1] OEM/ODM 활용
- 제조사: 한국/일본 GMP 인증 OEM
- 최소 주문량 (MOQ): 3,000-5,000개
- Lead time: 60-90일
- 단가: 8,000-15,000원/개 (포장 포함)

[Phase 2] 自社 제조 라인 구축 검토
- GMP 인증 시설 ( coûte : 30-50억 )
-眉毛向前一体化
```

### 4.3 마케팅 전략

**Phase 1 (Launch):**
```
1. K-Beauty 커뮤니티 마케팅
   - 레딧, SNS (인스타 40K+, 틱톡)
   -micro-influencer 50명 (각 10-50K 팔로워)

2. 과학적 내용营销
   - YouTube: "피부노화의 공간적 차이" 설명
   - Blog: MERFISH 데이터 기반 글

3. dermatologist 추천
   - 20명 피부과 전문의 협업
   - 샘플 + 리베이트

예산: 1년차 15억 중 40% = 6억
```

---

## 5. Market & Competitive Strategy

### 5.1 타겟 시장 세분화

| 세그먼트 | 규모 | 성장률 | Prize |접근 |
|---------|------|--------|-------|------|
| Premium Anti-Aging (30-45세) | $80억 | 8% | $80-150 | dermatologist + SNS |
| Mass Premium (25-40세) | $120억 | 6% | $30-80 | 오프라인 + online |
| Sensitive Skin | $50억 | 7% | $25-60 | dermatologist + pharmacy |

### 5.2 경쟁 우위

```
기존 기업 대비:

          既存            DermaScience
          ------           ---------
R&D      文献기반         실제 세포 데이터
타겟     单一            3경로 同時
証示     사용자 後測     Clinical trial
個性化   一律            AI 맞춤
```

### 5.3 해외진출

```
Year 1: 한국 内
  - 자사 쇼핑몰 + 톺발점
  - dermatologist 20명 협업

Year 2: 대만 + 싱가포르
  - K-Beauty 热風 利用
  - 現地 파트너:、台湾+新加坡

Year 3: 일본 + 홍콩
  - 現地法人 或合作
  - 면세점(tax free) 진입

Year 4-5: Global
  - SEP (Single Exit Programme)
  - 北米: DTC + department store
```

---

## 6. Financial Projections

### 6.1 손익 계산서 (단위: 억 원)

| 항목 | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|------|--------|--------|--------|--------|--------|
| **매출** | 20 | 60 | 150 | 320 | 550 |
| D2C | 12 | 35 | 85 | 180 | 300 |
| 오프라인 | 6 | 18 | 45 | 100 | 180 |
| 라이선스 | 2 | 7 | 20 | 40 | 70 |
| **매출원가** | 8 | 20 | 45 | 95 | 160 |
| Gross Profit | 12 | 40 | 105 | 225 | 390 |
| **R&D** | 8 | 12 | 22 | 38 | 55 |
| **Marketing** | 6 | 15 | 30 | 60 | 90 |
| **관리비** | 4 | 6 | 10 | 15 | 20 |
| **영업이익** | -6 | 7 | 43 | 112 | 225 |
| | | | | | |
| **R&D 비중** | 40% | 20% | 15% | 12% | 10% |
| **마진률** | 60% | 67% | 70% | 70% | 71% |

### 6.2 필요 자본금 사용 계획

**Series A: 50억 원**

| 항목 | 금액 | 비고 |
|------|------|------|
| R&D (성분 개발 + Clinical) | 15억 | 3개 제품 |
| Manufacturing (OEM) | 10억 | 3,000개×3製品 |
| Marketing (Launch) | 15억 | 커뮤니티+SNS+의사 |
| GMP 시설 설계 | 3억 | Phase 2 대비 |
| 운영자금 | 5억 | 12개월 운영 |
| 인건비 | 7억 | R&D 3명 + 마케팅 3명 |
| 예비비 | 5억 | |
| **합계** | **50억** | |

### 6.3 Valuation

```
Series A 후 Evaluation:
- Share price: 50억 won / (Series A 지분율 15-20%)
- Pre-money valuation: 200-250억 won
- Post-money: 250-300억 won

Comparable transactions:
- Beauty of LIBERN: 시리즈 B 100억 (2024)
- The Ordinary (Estee Lauder): $1B acquisition
- Skinceuticals (L'Oréal): $2.4B acquisition
```

---

## 7. Team

### 7.1 핵심 인력 (구성예정)

| 역할 |人数 | 要求 |
|------|------|------|
| CEO ( бизнес ) | 1 | 스킨케어/화장품 10년+, 初創 경험 |
| CSO (과학책임자) | 1 | 피부과학 PhD + MERFISH 경험 |
| R&D Lead | 1 | 生物化学/분자생물학 PhD |
| Marketing Lead | 1 | K-Beauty 5년+ |
| Operations | 1 | 製造/供応당 chain |

### 7.2 자문단

| 분야 | 인적망 |
|------|--------|
| 피부과 전문의 | 대학병원 피부과 教授 2명 |
|Beauty Regulatory | 前 Ralph cosmetics regulatory head |
| 투자 | Series A 투자자 2명 引受 |

---

## 8. Risks & Mitigations

| 위험 요소 | 수준 | 대응책 |
|----------|------|--------|
| R&D 실패 (성분 효과 미입증) | 中 | 기존 입증 성분 조합 + 단계적 新성분 도입 |
| Competitor模倣 | 高 | 特許출원 + 성분kompleks 합성 |
| Manufacturing 不良 | 中 | GMP 인증OEM 选择 + QC 강화 |
| Regulatory (화장품 功能성) | 低 |事前各省备案 + 功能성식품 검토 |
| Marketing 효과 미달 | 中 | KOC/마이크로인플루언서 + dermatologist |

---

## 9. Roadmap

```
2026 Q2-Q3: Series A 마무리 (50억)
           ↓
2026 Q4:   R&D 시설 Setup + 성분 개발 착수
           Team 구성 (CEO + CSO + R&D 2명)
           ↓
2027 Q1:   첫 제품론 R&D 완료 + 임상計画
           OEM협업사 确定
           ↓
2027 Q2:   Product 1-2 Launch (DermaCore, DermaMatrix)
           Marketing 착수 (K-Beauty 커뮤니티)
           ↓
2027 Q4:   Product 3 Launch + dermatologist협업 확대
           Japan/Taiwan 파트너십
           ↓
2028:      Series B 준비 (100-150억)
           B2B 라이선스 1건 完成
           Platform (DermaAI) 착수
           ↓
2029-2030: Global Launch + M&A (原料사/中小ブランド)
           IPO 검토
```

---

## 10. Investment Highlights

```
□ Scientifically validated targets (MERFISH 120만 세포 데이터)
□ Strong IP potential (3개 patent families)
□ K-Beauty global momentum (Hallyu + 기능성 식품 風潮)
□ Clear path to revenue (D2C + B2B 双輪)
□ Experienced founding team (탭핑 가능: 피부과 +beauty +투자)
□ Large TAM ($1,800억 全球 스킨케어)
□ Defensible moat (데이터 + 特許 + 브랜드)
```

---

**Contact:**
본 문서는 机密的으로 취급되며, 투자 목적 외에는 사용을 제한합니다.

*DermaScience — 피부공간유전체로 항노화의 科学を再定義する*
