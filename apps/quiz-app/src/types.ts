export interface Media {
  type: string;
  label: string;
  base64: string;
  url?: string;
}

export interface Question {
  id: string;
  metadata: {
    topic: string;
    major_category: string;
    source: string;
    page: number;
  };
  content: {
    question_text: string;
    choices: Record<string, string>;
    shuffledChoices?: [string, string][];
    has_media: boolean;
    media: Media[];
  };
  feedback: {
    correct_answer: string;
    explanation: string;
  };
}

export interface QuizResult {
  userId: string;
  userName: string;
  timestamp: any;
  score: number;
  total: number;
  topics: string[];
}
