# iPAS AI應用規劃師（初級）模擬試題

AI 自編模擬試題（非官方），逐題詳解版 PDF。

- `mock/R{回}-S{科目}.txt`：題目原稿（格式：`## 題號 | 題型 | 答案`，選項、`解說：`）
- `mock/parse_mock.py`：格式檢查（題號、選項、情境題 ≥15、陷阱題 ≥10、答案序列）
- `mock/lenstat.py`、`mock/cuecheck.py`：檢查「正解是否為最長選項」與正解長度排名分布
- `mock/build_mock_inline.py`：產生 PDF，用法 `python3 mock/build_mock_inline.py ipas_mock 5,6 ipas_mock/out`
- `mock/v1_backup/`：第 4～6 回加難前的原稿
- `out/`：第 5、6 回進階版 PDF

產生 PDF 需在 `fonts/` 放入 `NotoTC-Regular.ttf`、`NotoTC-Bold.ttf`（Noto Sans TC 靜態字重，未納入版本控制）。

## set3：情境陷阱百題（不含計算題）

- `set3/S1.txt`、`set3/S2.txt`：兩科各 50 題（格式同 `mock/`，可用 `parse_mock.parse()` 解析）
- `set3/draft_S*.txt`：原稿（正解一律寫在 A），`set3/build.py` 依預排答案序列重排選項，並把考點行的 `@sub:`／`@cat:` 換成參考檔中實際存在的題號
- `set3/simcheck.py`：與官方歷屆、R1～R6、必考百題（含備份）的相似度比對
- `set3/web/build_web.py`：產生 `set3/web/data.json` 與 `set3/web/ipas_exam_set3.html`

## pred_v3：考前預測百題 第 3 版（不含計算題）

- `pred_v3/S1.txt`、`pred_v3/S2.txt`：兩科各 50 題（可用 `parse_mock.validate()` 驗證）
- `pred_v3/draft_S*.txt`：原稿（正解一律寫在 A）；`pred_v3/build.py` 依預排答案序列重排選項，並把 `@sub:`／`@cat:` 換成參考檔中實際存在的題號
- `pred_v3/simcheck.py`：與官方歷屆、R1～R6、必考百題（含備份）、set3 的相似度比對；`pred_v3/kw.py`：用關鍵字查舊題是否已用過同一角度；`pred_v3/abscheck.py`：檢查絕對用語與「因為／所以」在正解與錯誤選項中的比例
- `pred_v3/web/build_web.py`：產生 `pred_v3/web/data.json` 與 `pred_v3/web/ipas_pred_v3.html`（另補 `[hidden]{display:none}`，修正範本交卷前出現空白結果框的問題）

## s1_two：科目一 情境陷阱百題（兩回，不含計算題）

- `s1_two/R1.txt`、`s1_two/R2.txt`：科目一第一回、第二回各 50 題（可用 `parse_mock.validate()` 驗證）
- `s1_two/draft_R*.txt`：原稿（正解一律寫在 A）；`s1_two/build.py` 依預排答案序列重排選項並換入 `@sub:`／`@cat:` 的實際題號
- `s1_two/simcheck.py`：與官方 400 題、R1～R6、必考百題（含兩個備份）、set3、pred_v3 及兩回互比的相似度；`s1_two/near.py`：列出概念最接近的舊題，人工檢查切入角度；`s1_two/lenrank.py`、`s1_two/cues.py`：正解長度排名與絕對用語、「因為／所以」檢查
- `s1_two/web/build_web.py`：產生 `s1_two/web/data.json` 與 `s1_two/web/ipas_s1_two.html`（分頁為第一回、第二回）
