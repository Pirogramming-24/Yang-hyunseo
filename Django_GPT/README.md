# 나만의 AI 사이트 (Django)

---
## 사용 모델 (3개 이상)

<!--
### 1. facebook/nllb-200-distilled-600M
-**태스크**: Translation (번역)
-**저는 노란색을 아주 좋아해요.**
-**I love yellow.**
- 실행 화면 예시:
-->
<img width="1382" height="1451" alt="스크린샷 2026-01-23 오전 1 25 19" src="https://github.com/user-attachments/assets/8371dfbe-3edb-4c1a-8bc7-c4f69b0b6991" />

<!--
### 2. distilgpt2
-**태스크**: Generation (텍스트 생성)
-**how is coffee bad for health?**
-**how is coffee bad for health? You can see that when you drink caffeine, it’s very likely to cause inflammation and constipation. But if the amount of wate....**
- 실행 화면 예시:
-->
<img width="1382" height="1451" alt="스크린샷 2026-01-23 오전 1 28 21" src="https://github.com/user-attachments/assets/0d5f48d5-3dc3-4beb-8559-6915be50181a" />


<!--
### 3. distilbert-base-uncased-finetuned-sst-2-english
-**태스크**: Sentiment Analysis (감정 분석)
-**I am so sad..**
-**NEGATIVE (1.00)**
- 실행 화면 예시:
-->
<img width="1382" height="1451" alt="스크린샷 2026-01-23 오전 1 26 26" src="https://github.com/user-attachments/assets/f4d7c979-2994-4d5d-8bfa-5cab4e0faa3f" />


---
## 로그인 제한(Access Control)

- 비로그인 사용자는**1개 탭만 사용 가능**
- 제한 탭 접근 시**“로그인 후 이용해주세요” alert 후 로그인 페이지로 이동**
- 로그인 성공 시**원래 페이지로 복귀(next)**

---
## 구현 체크리스트

- [ ✅ ] 탭 3개 이상 + 각 탭 별 URL 분리
- [ ✅ ] 각 탭: 입력 → 실행 → 결과 출력
- [ ✅ ] 에러 처리: 모델 호출 실패 시 사용자에게 메시지 표시
- [ ✅ ] 로딩 표시(최소한 “처리 중…” 텍스트라도)
- [ ✅ ] 요청 히스토리 5개
- [ ✅ ]`.env` 사용 (토큰/API Key 노출 금지)
- [ ✅ ]`README.md`에 모델 정보/사용 예시/실행 방법 작성 후 GitHub push

### 로그인 제한 체크
- [ ✅ ] 비로그인 사용자는 1개 탭만 접근 가능
- [ ✅ ] 제한 탭 접근 시 alert 후 로그인 페이지로 redirect
- [ ✅ ] 로그인 성공 시 원래 페이지로 복귀(next)


