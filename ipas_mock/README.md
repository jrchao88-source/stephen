# iPAS AI應用規劃師（初級）模擬試題

AI 自編模擬試題（非官方），逐題詳解版 PDF。

- `mock/R{回}-S{科目}.txt`：題目原稿（格式：`## 題號 | 題型 | 答案`，選項、`解說：`）
- `mock/parse_mock.py`：格式檢查（題號、選項、情境題 ≥15、陷阱題 ≥10、答案序列）
- `mock/lenstat.py`、`mock/cuecheck.py`：檢查「正解是否為最長選項」與正解長度排名分布
- `mock/build_mock_inline.py`：產生 PDF，用法 `python3 mock/build_mock_inline.py ipas_mock 5,6 ipas_mock/out`
- `mock/v1_backup/`：第 4～6 回加難前的原稿；`mock/v2_backup/`：第 5、6 回調整選項長度前的原稿
- `out/`：第 5、6 回進階版 PDF

產生 PDF 需在 `fonts/` 放入 `NotoTC-Regular.ttf`、`NotoTC-Bold.ttf`（Noto Sans TC 靜態字重，未納入版本控制）。

## set3：情境陷阱百題（不含計算題）

- `set3/S1.txt`、`set3/S2.txt`：兩科各 50 題（格式同 `mock/`，可用 `parse_mock.parse()` 解析）
- `set3/draft_S*.txt`：原稿（正解一律寫在 A），`set3/build.py` 依預排答案序列重排選項，並把考點行的 `@sub:`／`@cat:` 換成參考檔中實際存在的題號；`set3/edits/` 為選項長度調整紀錄
- `set3/simcheck.py`：與官方歷屆、R1～R6、必考百題（含備份）的相似度比對
- `set3/web/build_web.py`：產生 `set3/web/data.json` 與 `set3/web/ipas_exam_set3.html`
