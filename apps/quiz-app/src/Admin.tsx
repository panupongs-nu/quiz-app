import { useState, useEffect } from 'react'
import { db, auth } from './firebase'
import { collection, doc, writeBatch, query, limit, getDocs, deleteDoc } from 'firebase/firestore'
import type { Question } from './types'
import { Upload, ChevronLeft, Database, CheckCircle, AlertCircle, Search, Trash2, Eye, X, Plus, Download, Edit2 } from 'lucide-react'
import { setDoc } from 'firebase/firestore'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import remarkMath from 'remark-math'
import rehypeKatex from 'rehype-katex'
import 'katex/dist/katex.min.css'

interface AdminProps {
  onBack: () => void;
  onUploadSuccess?: () => void;
}

export default function Admin({ onBack, onUploadSuccess }: AdminProps) {
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState<{ type: 'success' | 'error', msg: string } | null>(null);
  const [stats, setStats] = useState({ total: 0, categories: [] as string[], sources: [] as string[] });
  const [explorerQuestions, setExplorerQuestions] = useState<Question[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [sourceFilter, setSourceFilter] = useState("All");
  const [categoryFilter, setCategoryFilter] = useState("All");
  const [viewingQuestion, setViewingQuestion] = useState<Question | null>(null);
  const [clearBeforeUpload, setClearBeforeUpload] = useState(false);
  const [uploadProgress, setUploadProgress] = useState({ current: 0, total: 0 });
  const [isEditing, setIsEditing] = useState(false);
  const [formQuestion, setFormQuestion] = useState<Partial<Question>>({
    content: { question_text: "", choices: { a: "", b: "", c: "", d: "" }, has_media: false, media: [] },
    metadata: { topic: "", major_category: "", source: "", page: 0 },
    feedback: { correct_answer: "a", explanation: "" }
  });

  const handleExport = () => {
    const jsonl = filteredQuestions.map(q => JSON.stringify(q)).join('\n');
    const blob = new Blob([jsonl], { type: 'application/x-jsonlines' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `exported_questions_${new Date().toISOString().split('T')[0]}.jsonl`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleSave = async () => {
    if (!formQuestion.id) {
      alert("Question ID is required");
      return;
    }
    try {
      setUploading(true);
      await setDoc(doc(db, "questions", formQuestion.id), formQuestion);
      setStatus({ type: 'success', msg: `Question ${formQuestion.id} saved successfully.` });
      setIsEditing(false);
      loadStats();
    } catch (err) {
      console.error("Save error:", err);
      setStatus({ type: 'error', msg: "Failed to save question." });
    } finally {
      setUploading(false);
    }
  };

  useEffect(() => {
    console.log("viewingQuestion changed:", viewingQuestion?.id);
  }, [viewingQuestion]);

  const loadStats = async () => {
    try {
      console.log("Admin: Fetching database stats...");
      const q = query(collection(db, "questions"), limit(1000));
      const snapshot = await getDocs(q);
      const fetched: Question[] = [];
      const categories = new Set<string>();
      const sources = new Set<string>();
      
      snapshot.forEach(doc => {
        const data = doc.data() as Question;
        fetched.push(data);
        if (data.metadata?.major_category) categories.add(data.metadata.major_category);
        if (data.metadata?.source) sources.add(data.metadata.source);
      });
      
      setStats({
        total: snapshot.size,
        categories: Array.from(categories).sort((a, b) => a.localeCompare(b, undefined, { numeric: true })),
        sources: Array.from(sources).sort()
      });
      setExplorerQuestions(fetched);
    } catch (err) {
      console.error("Admin: Error loading stats:", err);
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm(`Are you sure you want to delete question ${id}?`)) return;
    
    try {
      await deleteDoc(doc(db, "questions", id));
      setStatus({ type: 'success', msg: `Question ${id} deleted.` });
      loadStats();
    } catch (err) {
      console.error("Delete error:", err);
      alert("Failed to delete question.");
    }
  };

  useEffect(() => {
    loadStats();
  }, []);

  const filteredQuestions = explorerQuestions.filter(q => {
    const matchesSearch = q.id.toLowerCase().includes(searchQuery.toLowerCase()) || 
                         q.content.question_text.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         q.metadata.topic.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesSource = sourceFilter === "All" || q.metadata.source === sourceFilter;
    const matchesCategory = categoryFilter === "All" || q.metadata.major_category === categoryFilter;
    
    return matchesSearch && matchesSource && matchesCategory;
  });

  if (auth.currentUser?.email !== 'panupongs@nu.ac.th') {
    return (
      <div className="bg-white p-8 rounded-2xl shadow-lg w-full text-center">
        <AlertCircle size={48} className="mx-auto text-red-500 mb-4" />
        <h2 className="text-xl font-bold">Access Denied</h2>
        <p className="text-gray-500 mt-2">You do not have permission to access this page.</p>
        <button onClick={onBack} className="mt-6 text-blue-600 font-semibold">Go Back</button>
      </div>
    );
  }

  const clearDatabase = async () => {
    try {
      console.log("Admin: Clearing database...");
      const q = query(collection(db, "questions"), limit(500));
      let snapshot = await getDocs(q);
      
      while (!snapshot.empty) {
        const batch = writeBatch(db);
        snapshot.docs.forEach((doc) => {
          batch.delete(doc.ref);
        });
        await batch.commit();
        console.log(`Deleted ${snapshot.size} documents...`);
        snapshot = await getDocs(q);
      }
      return true;
    } catch (err) {
      console.error("Error clearing database:", err);
      return false;
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    setUploading(true);
    setStatus(null);
    setUploadProgress({ current: 0, total: 0 });

    if (clearBeforeUpload) {
      const cleared = await clearDatabase();
      if (!cleared) {
        setStatus({ type: 'error', msg: 'Failed to clear database before upload.' });
        setUploading(false);
        return;
      }
    }

    let totalUploaded = 0;

    try {
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const text = await file.text();
        const lines = text.split('\n').filter(l => l.trim() !== '');
        
        setUploadProgress(prev => ({ ...prev, total: prev.total + lines.length }));

        const questions: Question[] = lines.map((line, index) => {
          try {
            return JSON.parse(line);
          } catch (err) {
            throw new Error(`Error parsing line ${index + 1} in file ${file.name}`);
          }
        });
        
        await bulkUpload(questions);
        totalUploaded += questions.length;
      }
      setStatus({ type: 'success', msg: `Successfully uploaded ${totalUploaded} questions from ${files.length} file(s).` });
      loadStats();
      if (onUploadSuccess) onUploadSuccess();
    } catch (err: any) {
      console.error(err);
      let errorMsg = err.message || 'Failed to upload JSONL file.';
      if (err.code === 'permission-denied') {
        errorMsg = "Database Permission Denied. Please ensure your Firestore Rules are deployed and you are using @nu.ac.th email.";
      }
      setStatus({ type: 'error', msg: errorMsg });
    } finally {
      setUploading(false);
      // Reset input
      e.target.value = '';
    }
  };

  const bulkUpload = async (questions: Question[]) => {
    console.log(`Starting upload of ${questions.length} questions (Base64 Mode)...`);
    const batchSize = 10; // Smaller batch size because documents are now larger with Base64
    
    for (let i = 0; i < questions.length; i += batchSize) {
      try {
        const chunk = questions.slice(i, i + batchSize);
        const batch = writeBatch(db);
        
        chunk.forEach(q => {
          const qRef = doc(collection(db, "questions"), q.id);
          // Ensure we're not sending empty Base64 if we have a URL, 
          // but for new uploads, we just keep the Base64 as is.
          batch.set(qRef, q);
        });
        
        await batch.commit();
        setUploadProgress(prev => ({ ...prev, current: i + chunk.length }));
        console.log(`Batch ${Math.floor(i/batchSize) + 1} completed.`);
      } catch (err: any) {
        console.error(`Error uploading batch at index ${i}:`, err);
        throw err;
      }
    }
  };

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg w-full">
      <button 
        onClick={onBack}
        className="flex items-center gap-1 text-gray-500 hover:text-blue-600 mb-6 transition-colors"
      >
        <ChevronLeft size={20} />
        <span>Back to Dashboard</span>
      </button>

      <div className="flex justify-between items-start mb-8">
        <div>
          <h2 className="text-2xl font-bold mb-2 flex items-center gap-2">
            <Database className="text-blue-600" />
            <span>Question Management</span>
          </h2>
          <p className="text-gray-500 text-sm">Upload JSONL files to update the practice database.</p>
        </div>
        <div className="text-right">
          <div className="text-xs font-bold text-gray-400 uppercase tracking-widest">Admin User</div>
          <div className="text-sm font-medium text-blue-600">{auth.currentUser?.email}</div>
        </div>
      </div>

      <div className="flex items-center gap-4 mb-8">
        <label className="flex items-center gap-2 cursor-pointer bg-gray-100 px-4 py-3 rounded-xl hover:bg-gray-200 transition-colors">
          <input 
            type="checkbox" 
            checked={clearBeforeUpload}
            onChange={(e) => setClearBeforeUpload(e.target.checked)}
            className="w-4 h-4 text-blue-600 rounded"
          />
          <span className="text-sm font-medium text-gray-700">Clear database before upload</span>
        </label>
        
        <button 
          onClick={async () => {
            if (window.confirm("CRITICAL: Are you sure you want to delete ALL questions?")) {
              setUploading(true);
              await clearDatabase();
              await loadStats();
              setUploading(false);
              setStatus({ type: 'success', msg: 'Database cleared completely.' });
            }
          }}
          disabled={uploading}
          className="flex items-center gap-2 px-4 py-3 rounded-xl bg-red-50 text-red-600 hover:bg-red-100 transition-colors text-sm font-medium"
        >
          <Trash2 size={18} />
          <span>Clear All Data</span>
        </button>
      </div>

      <div className="border-2 border-dashed border-gray-200 rounded-2xl p-8 text-center hover:border-blue-400 transition-colors bg-gray-50 relative mb-8">
        <input 
          type="file" 
          accept=".jsonl"
          multiple
          onChange={handleFileUpload}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          disabled={uploading}
        />
        <div className="flex flex-col items-center">
          <div className="bg-white p-4 rounded-full shadow-sm mb-4 text-blue-600">
            <Upload size={32} />
          </div>
          <p className="font-semibold text-gray-700">
            {uploading ? 'Processing & Uploading...' : 'Click or Drag JSONL file to upload'}
          </p>
          <p className="text-xs text-gray-400 mt-1">Accepts .jsonl files</p>
          
          {uploading && uploadProgress.total > 0 && (
            <div className="w-full max-w-xs mt-6">
              <div className="flex justify-between text-xs text-gray-500 mb-1 font-medium">
                <span>Uploading Questions...</span>
                <span>{Math.round((uploadProgress.current / uploadProgress.total) * 100)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300" 
                  style={{ width: `${(uploadProgress.current / uploadProgress.total) * 100}%` }}
                ></div>
              </div>
              <p className="text-[10px] text-gray-400 mt-2">
                {uploadProgress.current} of {uploadProgress.total} questions processed
              </p>
            </div>
          )}
        </div>
      </div>

      {status && (
        <div className={`mt-6 p-4 rounded-xl flex items-center gap-3 ${status.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
          {status.type === 'success' ? <CheckCircle size={20} /> : <AlertCircle size={20} />}
          <span className="text-sm font-medium">{status.msg}</span>
        </div>
      )}

      <div className="mt-12 pt-8 border-t border-gray-100">
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-bold text-gray-800">Database Live Stats</h3>
          <button 
            onClick={loadStats}
            className="text-xs bg-gray-100 hover:bg-gray-200 text-gray-600 px-3 py-1 rounded-lg font-semibold transition-colors"
          >
            Refresh Stats
          </button>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
          <div className="bg-blue-50 p-4 rounded-xl border border-blue-100">
            <div className="text-3xl font-bold text-blue-600">{stats.total}</div>
            <div className="text-xs text-blue-500 uppercase tracking-widest font-semibold">Total Questions</div>
          </div>
          <div className="bg-purple-50 p-4 rounded-xl border border-purple-100">
            <div className="text-3xl font-bold text-purple-600">{stats.categories.length}</div>
            <div className="text-xs text-purple-500 uppercase tracking-widest font-semibold">Major Categories</div>
          </div>
        </div>

        <div className="bg-gray-50 p-6 rounded-2xl border border-gray-100">
          <h4 className="text-sm font-bold text-gray-700 mb-3 uppercase tracking-wider">Category Distribution</h4>
          <div className="flex flex-wrap gap-2">
            {stats.categories.length === 0 ? (
              <span className="text-gray-400 italic text-sm">No categories detected yet.</span>
            ) : (
              stats.categories.map(c => (
                <span key={c} className="px-3 py-1 bg-white border border-gray-200 rounded-full text-xs font-medium text-gray-600 shadow-sm">
                  {c}
                </span>
              ))
            )}
          </div>
        </div>
      </div>

      <div className="mt-12 pt-8 border-t border-gray-100">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <h3 className="font-bold text-gray-800 flex items-center gap-2 text-xl">
            <Search size={24} className="text-gray-400" />
            <span>Question Explorer</span>
          </h3>
          <div className="flex gap-2">
            <button 
              onClick={() => {
                setFormQuestion({
                  id: `NEW-${Date.now()}`,
                  content: { question_text: "", choices: { a: "", b: "", c: "", d: "" }, has_media: false, media: [] },
                  metadata: { topic: "General", major_category: "10. Other (Categorization Pending)", source: "Manual Add", page: 0 },
                  feedback: { correct_answer: "a", explanation: "" }
                });
                setIsEditing(true);
              }}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors text-sm font-bold shadow-sm"
            >
              <Plus size={18} />
              <span>Add New</span>
            </button>
            <button 
              onClick={handleExport}
              className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-colors text-sm font-bold shadow-sm"
            >
              <Download size={18} />
              <span>Export {filteredQuestions.length} Items</span>
            </button>
          </div>
        </div>
        
        <div className="flex flex-col md:flex-row gap-4 mb-4">
          <div className="flex-1 relative">
            <input 
              type="text"
              placeholder="Search by ID, text, or topic..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
            />
            <Search className="absolute left-3 top-2.5 text-gray-400" size={18} />
          </div>
          
          <select 
            value={sourceFilter}
            onChange={(e) => setSourceFilter(e.target.value)}
            className="px-4 py-2 border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 bg-white text-sm"
          >
            <option value="All">All Sources</option>
            {stats.sources.map(s => <option key={s} value={s}>{s}</option>)}
          </select>

          <select 
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="px-4 py-2 border border-gray-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 bg-white text-sm"
          >
            <option value="All">All Categories</option>
            {stats.categories.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </div>

        <div className="bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-sm">
          <div className="max-h-[500px] overflow-y-auto">
            <table className="w-full text-left border-collapse">
              <thead className="bg-gray-50 sticky top-0 z-10 shadow-sm">
                <tr>
                  <th className="px-4 py-3 text-xs font-bold text-gray-500 uppercase tracking-widest">ID</th>
                  <th className="px-4 py-3 text-xs font-bold text-gray-500 uppercase tracking-widest">Snippet</th>
                  <th className="px-4 py-3 text-xs font-bold text-gray-500 uppercase tracking-widest">Category</th>
                  <th className="px-4 py-3 text-xs font-bold text-gray-500 uppercase tracking-widest text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {filteredQuestions.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="px-4 py-8 text-center text-gray-400 italic text-sm">
                      No questions found.
                    </td>
                  </tr>
                ) : (
                  filteredQuestions.map(q => (
                    <tr key={q.id} className="hover:bg-gray-50 transition-colors group">
                      <td className="px-4 py-3 text-sm font-mono text-blue-600 whitespace-nowrap">{q.id}</td>
                      <td className="px-4 py-3 text-sm text-gray-600 max-w-[150px] truncate">{q.content.question_text}</td>
                      <td className="px-4 py-3 text-sm text-gray-500 truncate max-w-[120px]">{q.metadata.major_category}</td>
                      <td className="px-4 py-3 text-right flex justify-end gap-1">
                        <button 
                          onClick={() => setViewingQuestion(q)}
                          className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all cursor-pointer"
                          title="View Question"
                        >
                          <Eye size={18} />
                        </button>
                        <button 
                          onClick={() => {
                            setFormQuestion(q);
                            setIsEditing(true);
                          }}
                          className="p-2 text-gray-400 hover:text-purple-600 hover:bg-purple-50 rounded-lg transition-all cursor-pointer"
                          title="Edit Question"
                        >
                          <Edit2 size={18} />
                        </button>
                        <button 
                          onClick={() => handleDelete(q.id)}
                          className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all"
                          title="Delete Question"
                        >
                          <Trash2 size={18} />
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {isEditing && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, zIndex: 9999, backgroundColor: 'rgba(0,0,0,0.75)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '1rem', backdropFilter: 'blur(4px)' }}>
          <div className="bg-white rounded-3xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">
            <div className="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50">
              <h3 className="text-xl font-bold text-gray-800">
                {formQuestion.id ? `Edit Question: ${formQuestion.id}` : 'Add New Question'}
              </h3>
              <button onClick={() => setIsEditing(false)} className="p-2 hover:bg-gray-200 rounded-full text-gray-500">
                <X size={24} />
              </button>
            </div>
            
            <div className="p-8 overflow-y-auto flex-1 grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Left Column: Metadata */}
              <div className="space-y-4">
                <h4 className="font-bold text-gray-700 uppercase tracking-widest text-xs border-b pb-2">Information</h4>
                
                <div>
                  <label className="block text-xs font-bold text-gray-500 mb-1">Question ID</label>
                  <input 
                    type="text" 
                    value={formQuestion.id || ""} 
                    onChange={e => setFormQuestion({...formQuestion, id: e.target.value})}
                    className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-gray-500 mb-1">Topic</label>
                    <input 
                      type="text" 
                      value={formQuestion.metadata?.topic || ""} 
                      onChange={e => setFormQuestion({...formQuestion, metadata: {...formQuestion.metadata!, topic: e.target.value}})}
                      className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-gray-500 mb-1">Page</label>
                    <input 
                      type="number" 
                      value={formQuestion.metadata?.page || 0} 
                      onChange={e => setFormQuestion({...formQuestion, metadata: {...formQuestion.metadata!, page: parseInt(e.target.value)}})}
                      className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-gray-500 mb-1">Major Category</label>
                  <select 
                    value={formQuestion.metadata?.major_category || ""} 
                    onChange={e => setFormQuestion({...formQuestion, metadata: {...formQuestion.metadata!, major_category: e.target.value}})}
                    className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none"
                  >
                    {stats.categories.map(c => <option key={c} value={c}>{c}</option>)}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-gray-500 mb-1">Exam Source</label>
                  <input 
                    type="text" 
                    value={formQuestion.metadata?.source || ""} 
                    onChange={e => setFormQuestion({...formQuestion, metadata: {...formQuestion.metadata!, source: e.target.value}})}
                    className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none"
                  />
                </div>

                <div className="pt-4 space-y-4">
                  <h4 className="font-bold text-gray-700 uppercase tracking-widest text-xs border-b pb-2">Feedback</h4>
                  <div>
                    <label className="block text-xs font-bold text-gray-500 mb-1">Correct Answer</label>
                    <div className="flex gap-4">
                      {['a', 'b', 'c', 'd'].map(l => (
                        <label key={l} className="flex items-center gap-2 cursor-pointer">
                          <input 
                            type="radio" 
                            name="correct" 
                            checked={formQuestion.feedback?.correct_answer === l}
                            onChange={() => setFormQuestion({...formQuestion, feedback: {...formQuestion.feedback!, correct_answer: l}})}
                            className="w-4 h-4 text-blue-600"
                          />
                          <span className="font-bold uppercase text-gray-700">{l}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-gray-500 mb-1">Explanation</label>
                    <textarea 
                      rows={4}
                      value={formQuestion.feedback?.explanation || ""} 
                      onChange={e => setFormQuestion({...formQuestion, feedback: {...formQuestion.feedback!, explanation: e.target.value}})}
                      className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none resize-none"
                    />
                  </div>
                </div>
              </div>

              {/* Right Column: Content */}
              <div className="space-y-4">
                <h4 className="font-bold text-gray-700 uppercase tracking-widest text-xs border-b pb-2">Content</h4>
                
                <div>
                  <label className="block text-xs font-bold text-gray-500 mb-1">Question Text (Markdown supported)</label>
                  <textarea 
                    rows={6}
                    value={formQuestion.content?.question_text || ""} 
                    onChange={e => setFormQuestion({...formQuestion, content: {...formQuestion.content!, question_text: e.target.value}})}
                    className="w-full p-3 bg-gray-50 border border-gray-200 rounded-xl outline-none font-mono text-sm"
                  />
                </div>

                <div className="space-y-3">
                  <label className="block text-xs font-bold text-gray-500 mb-1 text-center">Choices</label>
                  {['a', 'b', 'c', 'd'].map(l => (
                    <div key={l} className="flex gap-3 items-center">
                      <span className="font-bold text-blue-600 uppercase">{l})</span>
                      <textarea 
                        rows={2}
                        value={formQuestion.content?.choices[l] || ""} 
                        onChange={e => {
                          const newChoices = {...formQuestion.content!.choices, [l]: e.target.value};
                          setFormQuestion({...formQuestion, content: {...formQuestion.content!, choices: newChoices}});
                        }}
                        className="flex-1 p-2 bg-gray-50 border border-gray-100 rounded-lg outline-none text-sm"
                      />
                    </div>
                  ))}
                </div>
              </div>
            </div>
            
            <div className="p-6 border-t border-gray-100 bg-gray-50 flex justify-end gap-3">
              <button 
                onClick={() => setIsEditing(false)}
                className="px-6 py-2 bg-white border border-gray-200 text-gray-600 rounded-xl font-bold hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button 
                onClick={handleSave}
                disabled={uploading}
                className="px-8 py-2 bg-blue-600 text-white rounded-xl font-bold hover:bg-blue-700 transition-colors shadow-md shadow-blue-200 disabled:opacity-50"
              >
                {uploading ? 'Saving...' : 'Save Question'}
              </button>
            </div>
          </div>
        </div>
      )}

      {viewingQuestion && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, zIndex: 9999, backgroundColor: 'rgba(0,0,0,0.75)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '1rem', backdropFilter: 'blur(4px)' }}>
          <div className="bg-white rounded-3xl shadow-2xl w-full max-w-3xl max-h-[90vh] overflow-hidden flex flex-col">
            <div className="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50">
              <div>
                <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
                  <span className="text-blue-600">{viewingQuestion.id}</span>
                </h3>
                <div className="flex gap-2 mt-1">
                  <span className="text-xs font-semibold px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full">{viewingQuestion.metadata.source}</span>
                  <span className="text-xs font-semibold px-2 py-0.5 bg-purple-100 text-purple-700 rounded-full">{viewingQuestion.metadata.major_category}</span>
                </div>
              </div>
              <button 
                onClick={() => setViewingQuestion(null)}
                className="p-2 hover:bg-gray-200 rounded-full text-gray-500 transition-colors"
              >
                <X size={24} />
              </button>
            </div>
            
            <div className="p-8 overflow-y-auto flex-1">
              <div className="mb-8">
                <h4 className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3">Question Text</h4>
                <div className="text-lg text-gray-800 leading-relaxed markdown-content pre-wrap">
                  <ReactMarkdown remarkPlugins={[remarkGfm, remarkMath]} rehypePlugins={[rehypeKatex]}>
                    {viewingQuestion.content.question_text}
                  </ReactMarkdown>
                </div>
              </div>

              {viewingQuestion.content.has_media && viewingQuestion.content.media && viewingQuestion.content.media.length > 0 && (
                <div className="space-y-6 mb-8">
                  {viewingQuestion.content.media.map((m, idx) => (
                    <div key={idx} className="p-4 border rounded-2xl bg-gray-50 flex flex-col items-center">
                      <img 
                        src={m.url || m.base64} 
                        alt={m.label || "Visual"} 
                        className="max-w-full h-auto rounded-lg shadow-sm"
                      />
                      <p className="text-xs text-gray-400 mt-2 italic font-bold uppercase tracking-widest">{m.label || `Visual ${idx+1}`}</p>
                    </div>
                  ))}
                </div>
              )}

              <div className="mb-8">
                <h4 className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3">Choices</h4>
                <div className="grid gap-3">
                  {Object.entries(viewingQuestion.content.choices)
                    .sort(([a], [b]) => a.localeCompare(b))
                    .map(([letter, text]) => (
                    <div 
                      key={letter}
                      className={`p-4 rounded-xl border-2 flex gap-3 items-start ${
                        letter === viewingQuestion.feedback.correct_answer 
                          ? 'border-green-500 bg-green-50' 
                          : 'border-gray-100 bg-white'
                      }`}
                    >
                      <span className={`font-bold ${letter === viewingQuestion.feedback.correct_answer ? 'text-green-600' : 'text-blue-600'}`}>
                        {letter.toUpperCase()})
                      </span>
                      <div className="markdown-content pre-wrap flex-1 text-gray-700">
                        <ReactMarkdown remarkPlugins={[remarkGfm, remarkMath]} rehypePlugins={[rehypeKatex]}>
                          {text}
                        </ReactMarkdown>
                      </div>
                      {letter === viewingQuestion.feedback.correct_answer && (
                        <CheckCircle className="text-green-600 flex-shrink-0" size={20} />
                      )}
                    </div>
                  ))}
                </div>
              </div>

              <div className="p-6 bg-blue-50 border-l-4 border-blue-500 rounded-r-2xl">
                <h4 className="font-bold text-blue-800 mb-2">Feedback & Explanation</h4>
                <div className="text-blue-700 leading-relaxed markdown-content pre-wrap">
                  <ReactMarkdown remarkPlugins={[remarkGfm, remarkMath]} rehypePlugins={[rehypeKatex]}>
                    {viewingQuestion.feedback.explanation}
                  </ReactMarkdown>
                </div>
              </div>
            </div>
            
            <div className="p-6 border-t border-gray-100 bg-gray-50 flex justify-end">
              <button 
                onClick={() => setViewingQuestion(null)}
                className="px-6 py-2 bg-gray-900 text-white rounded-xl font-bold hover:bg-black transition-colors"
              >
                Close Preview
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
