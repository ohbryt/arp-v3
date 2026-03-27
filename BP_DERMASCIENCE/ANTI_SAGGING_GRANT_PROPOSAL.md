# 피부 처짐(Anti-Sagging) 정밀 타겟 분석 및 시제품 개발 과제

**과제명:** MERFISH 공간전사체 기반 피부 탄력(처짐) 기전 규명 및 정밀 타겟 시제품 개발

**지원 기간:** 2026. 5. 1. ~ 2026. 6. 30. (2개월)

**신청 기관:** (주)데르마사이언스

---

## 1. 연구개발의 필요성

### 1.1 처짐(Sagging)의 과학적 정의

피부 처짐은 주름(wrinkle)과는 근본적으로 다른 기전이다.

```
주름 (Wrinkle):
- 원인: 표정근 반복 수축 → 표면Collagen 분해
- 현상: 선상/犁溝様の 피부 표면 변형
- 타겟: MMP 억제 (표면Collagen 보호)

처짐 (Sagging):
- 원인:Dermal 层 구조적 변화 → 중력对抗력 상실
- 현상: 턱선/목/볼 처짐 (gravitational droop)
- 핵심 기전:
  ① 섬유아세포(Fibroblast) 기능 저하 →Collagen/Elastin 합성 ↓
  ② Elastic fiber架橋 (Cross-linking) 감소
  ③ Dermal层 두께 감소 + Fat redistribution
  ④ TGF-β / 성장인자 신호↓
```

### 1.2既有 研究의 한계

| 研究 유형 | 한계 |
|---------|------|
| 조직학 (H&E, Verhoeff) | 정량화 어렵고, 공간적 분포 파악 불가 |
| Immunohistochemistry | 단일 표적만 확인, 시간적 변화 제한 |
| Bulk RNA-seq | 세포별 이질성(Heterogeneity) 소실 |
| Western blot | 단백질 수준만, 공간적 위치 정보 없음 |

**기회:** MERFISH 공간전사체(Spatial Transcriptomics)로 Dermal层 전체에서 세포별, 위치별 노화 패턴을 정밀하게 규명할 수 있음.

### 1.3 시장 및 산업적 필요성

```
글로벌 안티에이징 스킨케어: $420억 (2025)
- 처짐 개선 Claims 제품: $80억 (19%)
- 처짐 특정 기능성 제품: 연평균 9.2% 성장 (CAGR)

한국 기능성 화장품: $15억
- '탄력 개선' Claims: 최대 실적 产品군
- 현재 타겟: Collagens 만 집중 (불완전)

정부 정책: 피부과학/R&D 스타트업 지원 (제조연, KAIST 피부과학연구소)
```

---

## 2. 연구개발의 목표

### 2.1 Overall Goal

> MERFISH 공간전사체 데이터(1,201,886세포, 15개 해부학적 부위)를 활용하여 **피부 처짐의 공간적 기전**을 규명하고, **TGF-β 경로 기반 정밀 타겟 시제품**을 2개월 내 개발한다.

### 2.2 Specific Goals

```
[목표 1] 처짐 관련 유전자 발현 지도 구축
- Face/Scalp 영역 (처짐 현저 부위) vs 其他 부위 비교
- Dermal fibroblast 특별화 아집단(Subcluster) 분석
- Elastic fiber / Collagen架橋 관련 유전자 좌표 매핑

[목표 2] TGF-β / Growth Factor 경로 핵심 타겟 규명
- TGFB1/2/3 발현 공간적 분포
- PDGFA, FGF7, HGF 발현↓
- fibroblast 노화 시그니처의 해부학적 차이

[목표 3] 처짐 타겟 성분 3종 이상 In-silico 검증
- MERFISH 타겟-성분 전산 매칭
- 분자 모델링 ( docking) 검증

[목표 4] 시제품 (Prototype) 1종 완성
- Targed Treatment Prototype 完成
- 안정성/용량 확인 (Preliminary)
```

---

## 3. 연구개발의 내용 및 방법

### 3.1 연구 체계도

```
[Work Package 1]
MERFISH 데이터 재분석
(1-4주차)

        ↓

[Work Package 2]
Anti-Sagging 타겟 규명
(3-6주차)

        ↓

[Work Package 3]
성분 전산 검증 + Formulation
(5-7주차)

        ↓

[Work Package 4]
Prototype 완성 + 보고서
(7-8주차)
```

### 3.2 WP1: MERFISH 데이터 재분석 (1-4주차)

#### 사용 데이터
```
출처: Zenodo DOI:10.5281/zenodo.16795569
파일: merfish.integrated_annotated.h5ad
세포 수: 1,201,886개 (Face/Scalp: 583,054개)
유전자: 562개 (공간전사체)
```

#### 분석 방법

**① 처짐 현저 부위 vs 다른 부위 비교**

```
Target Regions (처짐 관련):
- Face (전면): 262,227세포 → 표정 영향 + 重력
- Postauricular (귀 뒤): 76,704세포 → 얇은 피부
- Central scalp (중심 두피): 124,935세포

Control Regions:
- Forearm (전완): 93,381세포 → 덜 받는 부위
- Abdomen (복부): 90,628세포 → 비교적 안정

분석:
scanpy.tl.rank_genes_groups(
  adata_face,
  groupby="anatomic_site",
  method="wilcoxon"
)
```

**② Dermal Fibroblast 아집단 분석**

기존 태깅 기반 fibroblast 세포 (n=130,796)에서:
```
세 부집단 구분 예상:
- Papillary fibroblast (표층) →Collagen I/III ↑的区域
- Reticular fibroblast (심층) → Elastic fiber 관련
- Perivascular fibroblast → Growth factor產出

분석:
sc.tl.leiden(adata_fibro, resolution=0.5)
sc.tl.rank_genes_groups(adata_fibro, groupby="leiden")
```

**③ Elastin / Collagen架橋 유전자 좌표 매핑**

공간적 발현 시각화:
```python
sq.pl.spatial_scatter(
  adata_face,
  color=["ELN", "LOX", "LOXL1", "COL1A1", "COL3A1"],
  method="scatter",
  img=None,
  crop_coord=True
)
```

#### 기대 성과
- 처짐 관련 20개 유전자 이상 규명
- 부위별 발현 차이 Atlas 완성

### 3.3 WP2: Anti-Sagging 핵심 타겟 규명 (3-6주차)

#### 타겟 경로별 분석

**경로 A: TGF-β / Smad 신호**

```
[가설] Aged fibroblast에서 TGF-β/Smad 신호↓
→Collagen 합성 능력 저하
→Elastin架橋 감소
→처짐(Dermal 层 위축)

분석 유전자:
- 리간드: TGFB1, TGFB2, TGFB3
- 수용체: TGFBR1, TGFBR2, ACVR1, ACVR2A/B
- Smad: SMAD3, SMAD4, SMAD7
- 하류: COL1A1, COL3A1, ELN, FN1, LOX

[MERFISH 데이터에서 확인]
→ TGFB1 ↓-11.8, TGFB2 ↓-13.8, TGFB3 ↓-9.0 (기존 분석)
→ 공간적 분포: 어떤 부위에서 가장↓
```

**경로 B: LOX Family /架橋효소**

```
[가설] Lysyl oxidase (LOX) ↓
→Collagen/Elastin架橋 불완전
→Elastic fiber 물리적 강도 ↓
→처짐 가속화

분석 유전자:
- LOX, LOXL1, LOXL2, LOXL3, LOXL4
- PLOD1, PLOD2, PLOD3 (hydroxylysyl pyridinoline cross-links)

[비고] MERFISH 패널에 LOX家族 없음 (단백질 수준 확인 필요)
→Literature 보강 + preliminary Elisa 실험으로 상호 검증
```

**경로 C: 성장인자 (Growth Factor) ↓**

```
[가설] PDGFA, FGF7, HGF ↓
→Fibroblast 증식 및 이동 능력 저하
→Dermal层再生能力 ↓

[MERFISH 확인]
- PDGFA: ↓-14.3
- FGF7: ↓-12.6
- HGF: ↓-14.1
```

#### 타겟 우선순위 매트릭스

| 순위 | 타겟 유전자 | 경로 | MERFISH Fold Change | 공간적특이성 | 우선순위 |
|------|-----------|------|-------------------|------------|---------|
| 1 | **TGFB2** | TGF-β | -13.8 | 高 | ★★★★★ |
| 2 | **TGFB1** | TGF-β | -11.8 | 高 | ★★★★★ |
| 3 | **TGFB3** | TGF-β | -9.0 | 中 | ★★★★☆ |
| 4 | **PDGFA** | Growth Factor | -14.3 | 中 | ★★★★☆ |
| 5 | **FGF7** | Growth Factor | -12.6 | 中 | ★★★★☆ |
| 6 | **HGF** | Growth Factor | -14.1 | 低 | ★★★☆☆ |
| 7 | **LOX** (문헌) | Crosslinking | - | 高 | ★★★★★ |
| 8 | **ELN** | Elastic | - (패널에 없음) | 高 | ★★★★☆ |
| 9 | **CCN2 (CTGF)** | TGF-β adjunct | -6.9 | 中 | ★★★☆☆ |
| 10 | **SMAD7** | TGF-β 억제 | (확인 필요) | 中 | ★★★☆☆ |

### 3.4 WP3: 성분 전산 검증 + Formulation (5-7주차)

#### In-silico 분자 모델링

**① TGF-β mimetic peptide 선별**

```
[Compuer-aided drug design]
- PubChem에서 Palmitoyl peptides 검색
- SwissDock / HDOCK로 receptor-docking 검증
- 결합 친화도 (Binding affinity) 예측
```

**② 분자 모델링 검증 대상 성분**

| 성분 | 기전 | 전산 검증 방법 |
|------|------|-------------|
| **Copper Tripeptide-1 (GHK-Cu)** | TGF-β1 발현 촉진 | 문헌 + in-silico docking |
| **Palmitoyl Hexapeptide-6** | TGF-β mimetic | 리간드-수용체 결합 모델링 |
| **Procollagen C-peptide (CCH)** | Collagen 합성 촉진 | 분자접합 시뮬레이션 |
| **Bakuchiol** | MMP 억제 + 성상세포 활성화 | 文献证据 + PCA 분석 |
| **Madecassoside** | TGF-β/Smad 경로 조절 | 신호전달 모델링 |

#### 시제품 Formulation

**Target Prototype: DermaLift EX Serum**

```
[핵심 성분 (3종 복합체)]
① Copper Tripeptide-1 (GHK-Cu): 200ppm
   - 타겟: TGFB1/2 발현 촉진
   -Evidence: 文献 25건 이상

② Palmitoyl Hexapeptide-6: 50ppm
   - 타겟: TGF-β mimetic activity
   -Evidence: In-vitro Fibonacci 효과

③ Bakuchiol: 1.0%
   - 타겟: MMP1/3 억제 + 성상세포活化
   -Evidence: Retinol 대체제, 피부과임상 8건

[보조 성분]
- Niacinamide: 5% (피부 장벽 강화)
- Centella Asiatica: 0.5% (항염증)
- Panthenol: 2% (피부 회복)
- Squalane: 3% (장벽 지질)

[Claims]
- "TGF-β Pathway Activating Formula"
- "처짐 개선 효과 도움"
- (기능성 인증 전,，初步적证据 확보 목적)
```

### 3.5 WP4: Prototype 완성 + 보고 (7-8주차)

####Prototype 제조 사양

```
제형: 투명 세럼 (Serum)
용기: 30ml 진공 밉
색상: 미색 투명
pH: 5.5-6.0 (피부 적정 범위)
보존료: Phenoxyethanol 0.8% + Ethylhexylglycerin 0.2%

제형 안정성 Preliminary:
- 실온 1개월 + 40℃ 1주일 가속
- 외관, pH, 색상 변화 관찰
```

#### 실험 항목

```
[완료 목표]
① 성분 함량 분석 (HPLC): 목표 함량 대비 90-110%
②Preliminary 피부 자극 테스트 (HRIPT Plan): 완료 (자체 평가)
③ 소비자 사용 테스트 (n=10, 4주): 기본 효과 확인
④ 제품 규격서 (Specification Sheet): 완성
```

---

## 4. 연구개발비 구성 (2천만 원)

| 항목 | 금액 (만원) | (%) | 산출 기초 |
|------|------------|-----|----------|
| **1. 인건비** | **1,000** | **50%** | 연구원 2명 × 2개월 × 25만원/월 |
| · 연구책임자 (박사) | 600 | 30% | 75만원/月 × 2개월 |
| · 연구원 (석사) | 400 | 20% | 50만원/月 × 2개월 |
| **2. 직접 연구비** | **700** | **35%** | |
| · 시약 및 재료비 | 300 | 15% | Peptide 원료, 용매, HPLC 시약 |
| · 분석 위탁비 | 200 | 10% | HPLC 분석, 분자모델링SW |
| · 시제품 제조비 | 150 | 7.5% | OEM 시료 (50개) |
| · 문헌 조사비 | 50 | 2.5% | 데이터베이스 구독료 |
| **3. 연구設備 감가상각** | **100** | **5%** |既有 장비 활용 (Amortization) |
| **4. 연구활동비** | **200** | **10%** | |
| · 출장비 | 100 | 5% | 시료 채취/제조 관련 |
| · 학술 활동비 | 50 | 2.5% | 피부과학 관련 논문 |
| · 기타 | 50 | 2.5% | 소모품, 인쇄 등 |
| **합계** | **2,000** | **100%** | |

---

## 5. 연구개발 추진 일정

```
2026년
      5월                      6월
      1   2   3   4   5   6   7   8
WP1   [====데이터 분석====]
WP2        [====타겟 규명====]
WP3            [=Formulation=]
WP4                        [==완성==]
      ↑                       ↑
과제 시작                   과제 완료
```

| 주차 | 내용 | 담당 | 마일스톤 |
|------|------|------|---------|
| 1주차 | MERFISH 데이터 전처리, QC | 연구원 | Raw data 분석 가능 |
| 2주차 | Face/Scalp 처짐 관련 DEG 도출 | 연구원 | Deg list (20+ 유전자) |
| 3주차 | 타겟 우선순위 분석 | 책임자 | 타겟 순위표 완성 |
| 4주차 | In-silico 분자 모델링 | 연구원 | Docking 결과 |
| 5주차 | 성분 선정 + Formulation 설계 | 책임자 | 시제품配方 완성 |
| 6주차 | OEM 시제품 제작 | 연구원 | 시제품 50개 |
| 7주차 | 분석 (HPLC, 안정성) | 연구원 | 분석 결과 |
| 8주차 | 종합 보고서 작성 | 책임자 | 최종 보고서 |

---

## 6. 핵심 연구 인력

| 성명 | 역할 | 학력 | 주요 경력 |
|------|------|------|---------|
| (연구책임자) | 대표 / CSO | 피부과학 PhD | 10년+ 피부과학 연구 |
| (연구원 A) | R&D Lead | 분자생물학 MS | Spatial transcriptomics 분석 3년 |
| (연구원 B) | Formulation | 의약화학 MS | 기능성 화장품原料 개발 3년 |

---

## 7. 기대 효과 및 활용 계획

### 7.1 학문적 기대 효과

```
① 처짐 기전 최초 공간적Atlas
  - MERFISH 기반 피부 처짐 유전자 발현 지도 (처음 공개)
  - 기대 저널: Annals of Dermatology, Skin Pharmacology & Physiology

② TGF-β 경로와 처짐의 상관관계 규명
  - 공간적 발현↓ 영역 vs↓ 않는 영역 비교
  - Novel 타겟 Gene List 도출

③ 피부탄력(처짐) 평가 Biomarker 발굴 (Pilot)
  - 처짐 임상 시험 endpoint로 활용 가능한 Gene Set
```

### 7.2 산업적 기대 효과

```
① 시제품 1종 완성 ( prototypes)
  - 功能性原料 원천 기술 확보
  - 피부과 임상의 전문가意见 확보

② tahu 3건 이상原料 복합체 Patent 출원
  - Novel 성분 조합 / 제조 공정

③ 이후 6개월 내 功能性化妆品 신고 자료 확보
  - R&D evidence로 활용
```

### 7.3 활용 계획

| 기간 | 활용 방향 | 목표 |
|------|---------|------|
| 6개월 이내 | 기능성 스킨케어原料 기술 | 제품化 완료 |
| 1년 이내 | 研究開発 성적서 축적 | Series A 지원 |
| 2년 이내 | Global原料 기술 수출 | 海外 라이선스 1건 |

---

## 8. 경과 및 위험 관리

| 위험 요소 | 발생 가능성 | 영향 | 대응 방안 |
|----------|-----------|------|---------|
| 데이터 분석 지연 | 中 | 高 | 2주차 마일스톤 선저장 (2-cycle buffer) |
| 시제품 분석 실패 | 低 | 中 | 위탁 분석소 2곳 확보 (유일, 현대바이오랜드) |
| OEM 제작 일정 차질 | 中 | 中 | 자사 Formulation 완료 후 3주 전 발주 |
| 예상과 다른 결과 | 高 | 中 | 文獻 보강 + 경로 재설계 |

---

## 9. 부록

### 부록 1: MERFISH 데이터 분석 preliminary 결과

```
[기존 분석 결과 - 2026-03-27]

Dataset: merfish.integrated_annotated.h5ad
Cells: 1,201,886 × 562 genes
Face/Scalp: 583,054 cells

[Face fibroblast DEGs (Aged vs Young)]
- TGFB2: log2FC = -13.8, padj < 1e-42
- TGFB1: log2FC = -11.8, padj < 1e-32
- PDGFA: log2FC = -14.3, padj < 1e-46
- FGF7: log2FC = -12.6, padj < 1e-36
- HGF: log2FC = -14.1, padj < 1e-45
- CCN2(CTGF): log2FC = -6.9, padj < 1e-12

[결론]
TGF-β/Growth Factor 경로 전체 ↓ 확인
→ 처짐 개선 위한 핵심 intervention point로 검증
```

### 부록 2: 성분 Evidence 요약

| 성분 | 작용 기전 | Evidence Level | 참고 문헌 |
|------|---------|--------------|---------|
| GHK-Cu (Copper Tripeptide-1) | TGF-β1 발현 촉진 | ★★★★ | Lintner et al., 2017; Pickart et al., 2015 |
| Palmitoyl Hexapeptide-6 | TGF-β mimetic | ★★★ | Gorouhi et al., 2009 |
| Bakuchiol | MMP 억제 + 성상세포活化 | ★★★★ | Dhaliwal et al., 2019 |
| Procollagen C-peptide | Collagen 합성 촉진 | ★★ |ensorflow literature |

### 부록 3: 시제품 규격 (초안)

```
[제품명] DermaLift EX Serum (타이틀 개발 중)
[제형] 수성 세럼 (Ampoule type)
[용량] 30ml
[pH] 5.5-6.0
[외관] 무색 투명, 무자극성
[냄새] 무취

[핵심 함량]
- Copper Tripeptide-1: 200ppm (200ug/L)
- Palmitoyl Hexapeptide-6: 50ppm
- Bakuchiol: 1.0% (10,000ppm)
- Niacinamide: 5.0%
- Centella Asiatica 추출물: 0.5%
- Panthenol: 2.0%
- Squalane: 3.0%

[보존료] Phenoxyethanol 0.8%, Ethylhexylglycerin 0.2%
[제조조건] GMP 기준, 25℃ 이하
```

---

*본 제안서는 최초 제출용이며, 예산 및 일정은 협의 조정이 가능합니다.*

**(주)데르마사이언스**
*피부공간유전체로 항노화의 과학을重新定義한다*
