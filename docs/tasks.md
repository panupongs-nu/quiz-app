# ITPE Quiz Web Application - Implementation Plan

## Objective
Build and deploy a web-based quiz application for ~120 students to practice IT Passport Examination questions. The app will be hosted on Firebase Free Tier, using Firestore for data and Google Auth for student logins.

## Tech Stack
- **Frontend:** React (Vite) or Vanilla JS + Tailwind CSS (for fast, responsive UI).
- **Backend/Database:** Firebase Firestore.
- **Authentication:** Firebase Auth (Google Provider).
- **Hosting:** Firebase Hosting.

## Firestore Data Schema (Proposed)
- `questions` (collection):
  - `id`: string (e.g., "2025S-Q1")
  - `content`: map (text, choices, has_media, media array)
  - `metadata`: map (topic, major_category, source, page)
  - `feedback`: map (correct_answer, explanation)
- `users` (collection):
  - `uid`: string (doc id)
  - `email`: string
  - `isAdmin`: boolean
  - `last_activity`: timestamp
- `results` (collection):
  - `userId`: reference
  - `timestamp`: timestamp
  - `score`: number
  - `total`: number
  - `topics`: array

---

## Task List

### Phase 1: Infrastructure & Setup
- [ ] Initialize Firebase Project in Console.
- [ ] Create `firebase.js` config and initialize SDK.
- [ ] Set up Firestore Security Rules (Public read for questions, Auth-only for results).
- [ ] Configure Google Auth in Firebase Console.

### Phase 2: Data Seeding (Local Script)
- [ ] Write a node/python script to parse `2025S_IP_Questions.jsonl` and `2025A_IP_Questions.jsonl`.
- [ ] Bulk upload questions to Firestore (to get the app started).

### Phase 3: Student Frontend (Core Quiz)
- [ ] **Login Screen:** Implement Google Login button.
- [ ] **Selection Screen:** 
    - Fetch unique topics from Firestore.
    - Let user select topics and number of questions (e.g., 10, 20, All).
- [ ] **Quiz Interface:**
    - Fetch random documents based on selected topics.
    - Show question text, diagram (image), and choices.
    - Handle selection and state.
- [ ] **Feedback/Results:**
    - Show score.
    - Save result to Firestore `results` collection.

### Phase 4: Admin Dashboard
- [ ] **Admin Check:** Logic to hide/show admin button based on user email.
- [ ] **JSONL Uploader:** 
    - File input for `.jsonl` files.
    - Frontend parser to read file line by line.
    - Bulk write to Firestore `questions` collection.
- [ ] **Question Management:** Basic list of questions with delete/edit option.

### Phase 5: Polish & Deployment
- [ ] Add Tailwind CSS for professional look.
- [ ] Implement "Explanation" display after each question or at the end.
- [ ] Deploy to Firebase Hosting.

---

## Finalized Requirements
1. **Authentication:** Google Login restricted to **@nu.ac.th** domain.
2. **Security:** Firestore rules to enforce **@nu.ac.th** domain-level access control.
3. **Admin Access:** Controlled via a specific admin email within the allowed domain.
3. **Quiz Flow:** One question at a time (Stepper UI).
4. **Admin Dashboard:** Drag-and-drop JSONL file uploader to bulk-add questions.
5. **Feedback Timing:** Immediate (show correct answer and explanation immediately after student selects an option).
6. **Data Seeding:** Automated script to upload current `2025S` and `2025A` questions.

---

## Task List
... (rest of the list) ...
