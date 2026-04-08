# Skill: High-Fidelity Visual Exam Extraction

This playbook details the process for adding new IT Passport Examinations to the quiz database using our "Visual-First" coordinate-based engine.

## Prerequisites
- **System:** `poppler-utils` installed.
- **Python:** `pdf2image`, `pillow`, `opendataloader-pdf` installed.
- **Source Files:** Question PDF and Answer PDF in `data/raw_exams/`.

## The Workflow

### 1. Structure Analysis
Analyze the PDF structure to find coordinates for every line of text and diagram.
```bash
opendataloader-pdf data/raw_exams/YYYYX_IP_Questions.pdf -o opendataloader_test/YYYYX -f json
```

### 2. High-DPI Page Rendering
Convert PDF pages to 150 DPI JPEG images. This DPI is the optimized balance between readability and file size (~22MB per 100 questions).
```bash
python pipeline/utils/pdf_to_images.py data/raw_exams/YYYYX_IP_Questions.pdf data/intermediate/pages/YYYYX 150
```

### 3. Answer Key Normalization
Extract and format the answers into a standardized `Q{n} {ans}` format.
```bash
pdftotext data/raw_exams/YYYYX_IP_Answers.pdf docs/YYYYX_IP_Answers_OCR.txt
```
*Note: Ensure the file contains 100 lines formatted like `Q1 a`.*

### 4. Coordinate-Based JSONL Generation
Generate the final database. Our v2 engine uses Y-coordinates to strictly separate Question blocks from Choice blocks and avoids footer/page number bleeding.
```bash
python pipeline/extractors/generate_jsonl_v2.py \
  --year YYYYX \
  --json opendataloader_test/YYYYX/YYYYX_IP_Questions.json \
  --answers docs/YYYYX_IP_Answers_OCR.txt \
  --pages_dir data/intermediate/pages/YYYYX \
  --output data/processed_jsonl/YYYYX_IP_Questions.jsonl
```

### 5. Finalize: Categorize and Split
Assign ITPE categories based on question numbers and chunk into 20-question files for Firebase optimization.
1. Update `pipeline/processors/apply_categories_v2.py` with the new file path.
2. Update `pipeline/processors/split_jsonl.py` with the new file path.
3. Run both scripts.

## Quality Control Checklist
- [ ] **No Footer Bleeding:** Check questions at the bottom of pages (e.g., Q25, Q50) to ensure page numbers aren't in the crop.
- [ ] **Mutual Exclusivity:** Ensure "Question" part doesn't contain choice letters and "Choices" part doesn't contain question text.
- [ ] **File Size:** Final JSONL should be ~20-25MB for 100 questions.
- [ ] **Categories:** Verify that questions 1-9 are marked as "7. Basic Theory," etc.
