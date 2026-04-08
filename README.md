# ITPE Quiz Ecosystem

This repository is a monorepo containing the full ecosystem for ITPE (Information Technology Professional Examination) preparation.

## Project Structure

- **`/apps`**: High-level applications.
  - **`quiz-app`**: A React + TypeScript + Firebase web application for students to practice exams.
- **`/pipeline`**: Python-based data processing engine.
  - **`extractors`**: 
    - `generate_jsonl_v2.py`: Visual-first generator (crops questions/choices as images).
  - **`processors`**: 
    - `apply_categories_v2.py`: Maps questions to official ITPE syllabus categories.
  - **`utils`**: 
    - `pdf_to_images.py`: High-DPI PDF-to-JPG conversion.
- **`/data`** (Git Ignored): Storage for raw and processed exam data.
  - **`raw_exams`**: Original ITPE PDF booklets.
  - **`processed_jsonl`**: Structured JSONL files containing question images and metadata.
  - **`intermediate`**: Temporary image crops, page renders, and templates.
- **`/docs`**: Documentation, syllabus, BOK (Body of Knowledge), and logs.

## Getting Started

### Prerequisites
- Node.js (for the quiz-app)
- Python 3.10+ (for the pipeline)
- Firebase Account (for database/hosting)

### Running the App
```bash
cd apps/quiz-app
npm install
npm run dev
```

### Running the Pipeline
Check the documentation in `/docs` for detailed instructions on how to process new exam PDFs.
