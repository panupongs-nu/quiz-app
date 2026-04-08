# Project Logbook: ITPE Practice Quiz App

This document tracks the major features, bug fixes, and architectural improvements made to the `quiz-app` project.

## 1. Data Processing & Parsing
- **Whitespace Preservation**: Updated Python generators (`generate_quiz_jsonl.py`, `generate_51_100.py`) to stop collapsing newlines and multiple spaces. This ensures text-based tables and code blocks from OCR maintain their alignment.
- **Media Detection Refinement**: Tuned keywords to prevent `[Data]` or `[Program]` blocks from triggering unnecessary image displays, relying instead on clean Markdown rendering.
- **Specific Question Fixes**: Created `fix_specific_q.py` to manually correct complex questions (e.g., 2025A-Q1, Q3, Q6, Q8, Q72, Q97) where raw OCR failed to capture table structures or choice relationships.
- **Numbered Categories**: Standardized all `major_category` metadata to include official numbering (e.g., "1. Corporate and legal affairs") following the `ITPE_BOK.md` specification.
- **Unified ID Format**: Standardized all question IDs to the `Q-XXX` zero-padded format (e.g., `2025A-Q-001`) to ensure correct alphabetical and numeric sorting in the database and UI.
- **File Splitting**: Created `split_jsonl.py` to divide large 100-question files into smaller 20-question chunks (e.g., `part01.jsonl`, `part02.jsonl`) to optimize the upload process and prevent timeouts.

## 2. Frontend Rendering Engine
- **Markdown Support**: Integrated `react-markdown` and `remark-gfm` to render structured tables, bold text, and lists within question text, choices, and explanations.
- **LaTeX/Math Support**: Integrated `remark-math` and `rehype-katex` along with KaTeX CSS to render mathematical symbols and equations correctly (e.g., binary notation $1011_2$, fractions $\frac{1}{216}$).
- **Monospace Alignment**: Applied a system-level monospace font to `pre-wrap` content in `index.css` to ensure that raw text tables from OCR remain perfectly aligned.
- **Dynamic Choice Shuffling**: Refactored the quiz engine to shuffle choice content while dynamically re-assigning "A, B, C, D" labels. This ensures the UX is consistent even when the underlying data is randomized.

## 3. Image & Diagram Strategy
- **Advanced Smart Cropping**: Upgraded `image_utils.py` with an algorithm that uses horizontal "ink" projection and Canny edge complexity analysis to automatically distinguish diagrams from blocks of text.
- **Header/Footer Ignoring**: The cropping algorithm now automatically ignores the top and bottom 10% of pages to avoid capturing exam headers and page numbers.
- **Manual Overrides**: Added a coordinate-based manual override system for specific questions that require precise diagram framing.
- **Firebase Storage Integration**: Shifted from storing large Base64 strings in Firestore to a high-performance Storage strategy. Images are uploaded to Firebase Storage, and only the resulting Download URL is stored in the database.

## 4. Admin Panel Enhancements
- **Question Explorer**: Added a searchable table to browse all questions in the database.
- **Advanced Filtering**: Implemented filters for **Exam Source** (Year) and **Major Category**.
- **Live Preview**: Added an "Eye" button to view exactly how a question will appear to students, including diagrams and math.
- **Database Management**: 
    - Added a **"Clear All Data"** button for easy database resets.
    - Added a **"Clear before upload"** toggle to prevent duplicate or stale data.
- **Manual CRUD**: Added features to **Add New** questions and **Edit** existing ones directly through a rich-text modal.
- **Data Portability**: Added an **Export** button to save filtered question sets back into `.jsonl` format.
- **Performance**: Optimized the bulk upload process with **Parallel Image Processing** and a real-time **Progress Bar**.

## 5. UI/UX Improvements
- **Quiz Setup**: Added a **"Select All / Deselect All"** toggle for category selection.
- **Layout**: Expanded the Admin panel to a `max-w-5xl` layout to better accommodate data management tasks.
- **Feedback**: Refined the result display to show the currently assigned shuffled letter (A, B, C, or D) next to the correct answer for clarity.

---
## 6. Phase 4 - High-Fidelity Diagrams & Zero-Cost Migration (2026-04-07)

#### **Technical Challenges**
- **CORS Violations:** Attempting to upload diagrams to Firebase Storage from the browser triggered CORS blocks.
- **Billing Restrictions:** Standard "Spark" (free) plan has strict region requirements for storage buckets. Manual bucket creation was blocked by a disabled billing account status.
- **Firestore Size Limits:** Initial concern about 1MB document limit for Base64 embedding.

#### **Key Improvements & Decisions**
- **Smart Crop v2:** Implemented vertical ink profiling and Canny edge complexity analysis to isolate diagrams automatically.
- **Zero-Cost, Zero-CORS Migration:**
    - Abandoned Firebase Storage for diagram hosting due to billing/CORS friction.
    - Transitioned to **Base64-only strategy**: Diagrams are now embedded directly in Firestore documents.
    - Verified that typical ITPE diagrams (100-200KB) fit well within Firestore's 1MB limit.
- **Chunked Upload Strategy:**
    - Modified `split_jsonl.py` to create 20-question chunks.
    - Reduced Admin batch size to 10 for better stability with larger Base64 payloads.
    - Successfully verified near-instant upload speeds for 20-question chunks.

#### **Current Status**
- **2025A & 2025S Exams:** Fully processed, categorized, and diagrams extracted.
- **Deployment:** Live at `itpe-practice.web.app` with full Base64 support.
- **Admin UI:** Robust CRUD and bulk upload functionality verified.
