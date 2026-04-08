import { useState, useEffect } from 'react'
import { auth, googleProvider, db } from './firebase'
import { signInWithPopup, signOut, onAuthStateChanged } from 'firebase/auth'
import type { User } from 'firebase/auth'
import { collection, getDocs, query, where, limit, addDoc, serverTimestamp } from 'firebase/firestore'
import type { Question, QuizResult } from './types'
import { LogOut, BookOpen, CheckCircle2, XCircle, ChevronRight, Trophy, LayoutDashboard } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'
import 'katex/dist/katex.min.css'
import Admin from './Admin'

type AppState = 'LOBBY' | 'SETUP' | 'QUIZ' | 'RESULT' | 'ADMIN';

function App() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [state, setState] = useState<AppState>('LOBBY')
  const [questions, setQuestions] = useState<Question[]>([])
  const [currentIdx, setCurrentIdx] = useState(0)
  const [score, setScore] = useState(0)
  const [selectedCats, setSelectedCategories] = useState<string[]>([])
  const [numQuestions, setNumQuestions] = useState(10)
  const [userAnswer, setUserAnswer] = useState<string | null>(null)
  const [showFeedback, setShowFeedback] = useState(false)
  const [allCats, setAllCats] = useState<string[]>([])

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (u) => {
      if (u) {
        if (u.email?.toLowerCase().endsWith('@nu.ac.th')) {
          setUser(u)
          setState('SETUP')
          fetchCategories()
        } else {
          alert('Access restricted to @nu.ac.th domain.')
          signOut(auth)
        }
      } else {
        setUser(null)
        setState('LOBBY')
      }
      setLoading(false)
    })
    return unsubscribe
  }, [])

  const fetchCategories = async () => {
    try {
      console.log("Fetching categories from Firestore...");
      const q = query(collection(db, "questions"), limit(1000));
      const snapshot = await getDocs(q);
      const categories = new Set<string>();
      
      snapshot.forEach(doc => {
        const data = doc.data();
        if (data.metadata && data.metadata.major_category) {
          categories.add(data.metadata.major_category);
        }
      });
      
      const categoryList = Array.from(categories).sort((a, b) => {
        return a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' });
      });
      console.log("Categories found:", categoryList);
      setAllCats(categoryList);
    } catch (error) {
      console.error("Error fetching categories:", error);
    }
  }

  const login = async () => {
    try {
      await signInWithPopup(auth, googleProvider)
    } catch (error) {
      console.error(error)
    }
  }

  const startQuiz = async () => {
    setLoading(true)
    try {
      console.log(`Starting quiz with ${numQuestions} questions. Categories:`, selectedCats);
      let fetched: Question[] = [];
      const qRef = collection(db, "questions");
      let q;
      
      if (selectedCats.length > 0) {
        q = query(qRef, where("metadata.major_category", "in", selectedCats.slice(0, 10)), limit(numQuestions * 3));
      } else {
        q = query(qRef, limit(numQuestions * 3));
      }
      
      const snapshot = await getDocs(q);
      snapshot.forEach(doc => fetched.push(doc.data() as Question));
      
      if (fetched.length === 0) {
        alert("No questions found for selected categories.");
        setLoading(false);
        return;
      }

      const shuffled = fetched
        .sort(() => 0.5 - Math.random())
        .slice(0, numQuestions)
        .map(q => ({
          ...q,
          content: {
            ...q.content,
            shuffledChoices: Object.entries(q.content.choices).sort(() => 0.5 - Math.random())
          }
        }));
      setQuestions(shuffled);
      setCurrentIdx(0);
      setScore(0);
      setUserAnswer(null);
      setShowFeedback(false);
      setState('QUIZ');
    } catch (error) {
      console.error("Error starting quiz:", error);
      alert("Failed to load questions.");
    } finally {
      setLoading(false);
    }
  }

  const handleAnswer = (letter: string) => {
    if (showFeedback) return;
    setUserAnswer(letter);
    setShowFeedback(true);
    if (letter === questions[currentIdx].feedback.correct_answer) {
      setScore(s => s + 1);
    }
  }

  const nextQuestion = () => {
    if (currentIdx + 1 < questions.length) {
      setCurrentIdx(i => i + 1);
      setUserAnswer(null);
      setShowFeedback(false);
    } else {
      saveResult();
      setState('RESULT');
    }
  }

  const saveResult = async () => {
    if (!user) return;
    const result: QuizResult = {
      userId: user.uid,
      userName: user.displayName || user.email || 'Unknown',
      timestamp: serverTimestamp(),
      score: score,
      total: questions.length,
      topics: selectedCats
    }
    await addDoc(collection(db, "results"), result);
  }

  if (loading) return <div className="flex items-center justify-center h-screen bg-gray-900 text-white">Loading...</div>

  return (
    <div className="min-h-screen bg-gray-100 text-gray-900 w-full flex flex-col">
      <header className="bg-white shadow-sm p-4 flex justify-between items-center sticky top-0 z-10">
        <div className="flex items-center gap-2 font-bold text-xl text-blue-600">
          <BookOpen size={28} />
          <span>ITPE Practice</span>
        </div>
        {user && (
          <div className="flex items-center gap-4">
            {user.email === 'panupongs@nu.ac.th' && (
              <button 
                onClick={() => setState('ADMIN')}
                className="text-gray-600 hover:text-blue-600 flex items-center gap-1 text-sm font-medium"
              >
                <LayoutDashboard size={18} />
                <span>Admin</span>
              </button>
            )}
            <div className="hidden sm:block text-right">
              <div className="text-sm font-semibold">{user.displayName}</div>
              <div className="text-xs text-gray-500">{user.email}</div>
            </div>
            <button onClick={() => signOut(auth)} className="p-2 rounded-full hover:bg-gray-100 text-gray-600">
              <LogOut size={20} />
            </button>
          </div>
        )}
      </header>

      <main className="flex-1 container mx-auto p-4 flex flex-col items-center justify-center">
        {state === 'LOBBY' && (
          <div className="bg-white p-8 rounded-2xl shadow-xl text-center max-w-md w-full">
            <div className="bg-blue-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6 text-blue-600">
              <BookOpen size={40} />
            </div>
            <h2 className="text-2xl font-bold mb-2">Welcome Students</h2>
            <p className="text-gray-600 mb-8">Sign in with your @nu.ac.th Google account to start practicing IT Passport Exam questions.</p>
            <button 
              onClick={login}
              className="w-full flex items-center justify-center gap-3 bg-white border-2 border-gray-200 p-3 rounded-xl font-semibold hover:bg-gray-50 transition-all shadow-sm"
            >
              <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" className="w-6" alt="Google" />
              <span>Sign in with Google</span>
            </button>
          </div>
        )}

        {state === 'SETUP' && (
          <div className="bg-white p-8 rounded-2xl shadow-lg w-full max-w-2xl">
            <h2 className="text-2xl font-bold mb-6">Quiz Configuration</h2>
            
            <div className="mb-6">
              <div className="flex justify-between items-center mb-2">
                <label className="block text-sm font-medium text-gray-700">Select Major Categories</label>
                <button 
                  onClick={() => {
                    if (selectedCats.length === allCats.length) setSelectedCategories([]);
                    else setSelectedCategories([...allCats]);
                  }}
                  className="text-xs font-bold text-blue-600 hover:text-blue-800 transition-colors bg-blue-50 px-2 py-1 rounded"
                >
                  {selectedCats.length === allCats.length ? 'Deselect All' : 'Select All'}
                </button>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-h-64 overflow-y-auto p-2 border rounded-lg">
                {allCats.length === 0 ? (
                  <div className="col-span-full py-8 text-center text-gray-400 italic text-sm">
                    No categories found. Please upload questions in Admin panel.
                  </div>
                ) : (
                  allCats.map(cat => (
                    <label key={cat} className="flex items-center gap-2 p-2 rounded hover:bg-gray-50 cursor-pointer border border-transparent has-[:checked]:border-blue-500 has-[:checked]:bg-blue-50">
                      <input 
                        type="checkbox" 
                        className="rounded text-blue-600 focus:ring-blue-500"
                        checked={selectedCats.includes(cat)}
                        onChange={(e) => {
                          if (e.target.checked) setSelectedCategories([...selectedCats, cat])
                          else setSelectedCategories(selectedCats.filter(c => c !== cat))
                        }}
                      />
                      <span className="text-sm">{cat}</span>
                    </label>
                  ))
                )}
              </div>
              <p className="text-xs text-gray-500 mt-2">Select one or more categories, or none for a mix from all {allCats.length}.</p>
            </div>

            <div className="mb-8">
              <label className="block text-sm font-medium text-gray-700 mb-2">Number of Questions: {numQuestions}</label>
              <input 
                type="range" min="5" max="50" step="5"
                value={numQuestions}
                onChange={(e) => setNumQuestions(parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
              <div className="flex justify-between text-xs text-gray-400 px-1 mt-1">
                <span>5</span><span>25</span><span>50</span>
              </div>
            </div>

            <button 
              onClick={startQuiz}
              className="w-full bg-blue-600 text-white p-4 rounded-xl font-bold hover:bg-blue-700 transition-colors shadow-md flex items-center justify-center gap-2"
            >
              <span>Start Practice Session</span>
              <ChevronRight size={20} />
            </button>
          </div>
        )}

        {state === 'QUIZ' && questions.length > 0 && (
          <div className="w-full max-w-3xl">
            <div className="mb-6">
              <div className="flex justify-between text-sm font-medium text-gray-500 mb-2">
                <span>Question {currentIdx + 1} of {questions.length}</span>
                <span>Score: {score}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${((currentIdx + 1) / questions.length) * 100}%` }}
                ></div>
              </div>
            </div>

            <div className="bg-white p-6 rounded-2xl shadow-lg mb-6">
              <div className="text-xs font-bold text-blue-500 uppercase tracking-wider mb-2">
                {questions[currentIdx].metadata.major_category}
              </div>
              <div className="text-lg font-medium leading-relaxed mb-6 markdown-content pre-wrap">
                <ReactMarkdown remarkPlugins={[remarkGfm, remarkMath]} rehypePlugins={[rehypeKatex]}>
                  {questions[currentIdx].content.question_text}
                </ReactMarkdown>
              </div>

              {questions[currentIdx].content.has_media && questions[currentIdx].content.media && questions[currentIdx].content.media.length > 0 && (
                <div className="space-y-6 mb-8">
                  {questions[currentIdx].content.media.map((m, idx) => (
                    <div key={idx} className="p-4 border rounded-2xl bg-gray-50 flex flex-col items-center">
                      <img 
                        src={m.url || m.base64} 
                        alt={m.label || "Visual"} 
                        className="max-w-full h-auto rounded shadow-sm"
                      />
                      {m.label && <p className="text-[10px] text-gray-400 mt-2 font-bold uppercase tracking-widest">{m.label}</p>}
                    </div>
                  ))}
                </div>
              )}

              <div className="space-y-3">
                {(questions[currentIdx].content.shuffledChoices || Object.entries(questions[currentIdx].content.choices)).map(([originalKey, text], index) => {
                  const displayLabel = String.fromCharCode(65 + index); // A, B, C, D
                  const isCorrect = originalKey === questions[currentIdx].feedback.correct_answer;
                  const isSelected = originalKey === userAnswer;
                  let bgClass = "bg-white border-gray-200 hover:border-blue-300 hover:bg-blue-50";
                  let icon = null;

                  if (showFeedback) {
                    if (isCorrect) {
                      bgClass = "bg-green-100 border-green-600 ring-2 ring-green-600 text-green-900";
                      icon = <CheckCircle2 className="text-green-600 fill-white" size={24} />;
                    } else if (isSelected) {
                      bgClass = "bg-red-100 border-red-600 ring-2 ring-red-600 text-red-900";
                      icon = <XCircle className="text-red-600 fill-white" size={24} />;
                    } else {
                      bgClass = "bg-gray-50 border-gray-200 opacity-50";
                    }
                  }

                  return (
                    <button
                      key={originalKey}
                      disabled={showFeedback}
                      onClick={() => handleAnswer(originalKey)}
                      className={`w-full text-left p-4 rounded-xl border-2 transition-all flex items-center justify-between ${bgClass}`}
                    >
                      <div className="flex gap-3 items-start">
                        <span className="font-bold text-blue-600 mt-0.5">{displayLabel})</span>
                        <div className="text-gray-700 markdown-content flex-1 pre-wrap">
                          <ReactMarkdown remarkPlugins={[remarkGfm, remarkMath]} rehypePlugins={[rehypeKatex]}>
                            {text}
                          </ReactMarkdown>
                        </div>
                      </div>
                      {icon}
                    </button>
                  )
                })}
              </div>

              {/* Feedback Overlay Section */}
              {showFeedback && userAnswer && (
                <div className="mt-8 space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                  {/* High-Impact Feedback Banner */}
                  <div 
                    className="p-6 rounded-3xl flex items-center justify-between shadow-2xl border-4 border-white/20 text-white"
                    style={{ backgroundColor: userAnswer === questions[currentIdx].feedback.correct_answer ? '#16a34a' : '#dc2626' }}
                  >
                    <div className="flex items-center gap-5">
                      <div className="bg-white/30 p-4 rounded-2xl backdrop-blur-md shadow-inner">
                        {userAnswer === questions[currentIdx].feedback.correct_answer 
                          ? <CheckCircle2 size={40} className="stroke-[3px] animate-bounce" /> 
                          : <XCircle size={40} className="stroke-[3px] animate-pulse" />
                        }
                      </div>
                      <div>
                        <h3 className="text-3xl font-black uppercase tracking-tighter leading-none mb-1">
                          {userAnswer === questions[currentIdx].feedback.correct_answer ? 'Brilliant!' : 'Not Quite!'}
                        </h3>
                        <p className="text-white/90 font-bold text-lg">
                          Correct Answer: <span className="underline decoration-wavy underline-offset-4 bg-white/20 px-2 py-0.5 rounded ml-1">
                            {(() => {
                              const shuffled = questions[currentIdx].content.shuffledChoices || Object.entries(questions[currentIdx].content.choices);
                              const correctIdx = shuffled.findIndex(([key]) => key === questions[currentIdx].feedback.correct_answer);
                              return String.fromCharCode(65 + correctIdx);
                            })()}
                          </span>
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Rationale Deep-Dive Card */}
                  <div className="bg-white border-2 border-gray-100 rounded-[2.5rem] p-10 shadow-xl relative overflow-hidden group">
                    <div className={`absolute top-0 left-0 w-3 h-full ${
                      userAnswer === questions[currentIdx].feedback.correct_answer ? 'bg-green-500' : 'bg-red-500'
                    }`}></div>
                    <div className="flex items-center gap-3 mb-6">
                      <div className="p-2 bg-blue-50 text-blue-600 rounded-xl">
                        <BookOpen size={20} />
                      </div>
                      <h4 className="font-black text-gray-900 uppercase tracking-[0.2em] text-sm">
                        Concept Rationale
                      </h4>
                    </div>
                    <div className="text-gray-700 text-lg leading-relaxed markdown-content prose max-w-none">
                      <ReactMarkdown remarkPlugins={[remarkGfm, remarkMath]} rehypePlugins={[rehypeKatex]}>
                        {questions[currentIdx].feedback.explanation}
                      </ReactMarkdown>
                    </div>
                  </div>

                  <button 
                    onClick={nextQuestion}
                    className="w-full mt-4 bg-gray-900 text-white p-6 rounded-[2rem] font-black text-xl hover:bg-black transition-all flex items-center justify-center gap-4 shadow-2xl hover:shadow-black/40 hover:-translate-y-2 active:translate-y-0"
                  >
                    <span className="uppercase tracking-widest">
                      {currentIdx + 1 === questions.length ? 'Finalize Practice' : 'Continue Mission'}
                    </span>
                    <ChevronRight size={28} />
                  </button>
                </div>
              )}
            </div>
          </div>
        )}

        {state === 'RESULT' && (
          <div className="bg-white p-8 rounded-3xl shadow-xl text-center w-full max-w-md">
            <div className="bg-yellow-100 w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6 text-yellow-600">
              <Trophy size={48} />
            </div>
            <h2 className="text-3xl font-bold mb-2">Quiz Complete!</h2>
            <div className="bg-gray-50 rounded-2xl p-6 mb-8">
              <div className="text-5xl font-black text-blue-600 mb-2">{score} / {questions.length}</div>
              <div className="text-sm font-medium text-gray-400 uppercase tracking-widest">Final Score</div>
            </div>
            <button 
              onClick={() => setState('SETUP')}
              className="w-full bg-blue-600 text-white p-4 rounded-xl font-bold hover:bg-blue-700 transition-colors shadow-md"
            >
              Practice Again
            </button>
          </div>
        )}

        {state === 'ADMIN' && (
          <div className="w-full max-w-5xl">
            <Admin 
              onBack={() => setState('SETUP')} 
              onUploadSuccess={fetchCategories}
            />
          </div>
        )}
      </main>
    </div>
  )
}

export default App
