import { useState } from 'react';
import { Mail, Send, AlertTriangle, ShieldCheck, User, MessageSquare, Play, X, Check, ThumbsUp, ThumbsDown } from 'lucide-react';
import axios from 'axios';

const PhishingSim = () => {
    // Mode: 'generator' or 'training'
    const [mode, setMode] = useState('training');

    // Generator State
    const [persona, setPersona] = useState('hr');
    const [tone, setTone] = useState('urgent');
    const [emailContent, setEmailContent] = useState<any>(null);
    const [analysis, setAnalysis] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    // Training State
    const [trainingEmail, setTrainingEmail] = useState<any>(null);
    const [trainingFeedback, setTrainingFeedback] = useState<any>(null);
    const [score, setScore] = useState({ correct: 0, total: 0 });

    // --- Generator Logic ---
    const generateEmail = async () => {
        setLoading(true);
        setAnalysis(null);
        try {
            const response = await axios.post('http://localhost:8000/api/social/generate', {
                persona,
                tone
            });
            setEmailContent(response.data);
        } catch (error) {
            console.error("Error generating email", error);
        } finally {
            setLoading(false);
        }
    };

    const analyzeEmail = async () => {
        if (!emailContent) return;
        try {
            const response = await axios.post('http://localhost:8000/api/social/analyze', {
                content: emailContent.content
            });
            setAnalysis(response.data);
        } catch (error) {
            console.error("Analysis failed", error);
        }
    };

    // --- Training Logic ---
    const loadTrainingEmail = async () => {
        setLoading(true);
        setTrainingFeedback(null);
        setTrainingEmail(null);
        try {
            const response = await axios.get('http://localhost:8000/api/social/email/simulation');
            setTrainingEmail(response.data);
        } catch (error) {
            console.error("Error loading training email", error);
        } finally {
            setLoading(false);
        }
    };

    const handleDecision = (choice: 'phishing' | 'safe') => {
        if (!trainingEmail) return;

        const isActuallyPhishing = trainingEmail.type === 'phishing';
        const isCorrect = (choice === 'phishing' && isActuallyPhishing) || (choice === 'safe' && !isActuallyPhishing);

        setScore(prev => ({
            correct: prev.correct + (isCorrect ? 1 : 0),
            total: prev.total + 1
        }));

        setTrainingFeedback({
            correct: isCorrect,
            message: isCorrect ? "Correct! You identified the email correctly." : "Incorrect. Review the indicators below.",
            reason: trainingEmail.reason
        });
    };

    return (
        <div className="max-w-6xl mx-auto space-y-8 min-h-[calc(100vh-140px)] flex flex-col">
            <div className="text-center space-y-2">
                <h1 className="text-3xl font-bold text-white">Social Engineering Simulator</h1>
                <p className="text-gray-400">Master the art of detecting deception.</p>

                <div className="flex justify-center mt-4 bg-gray-800 inline-flex rounded-lg p-1 border border-gray-700">
                    <button
                        onClick={() => setMode('training')}
                        className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${mode === 'training' ? 'bg-cyan-600 text-white' : 'text-gray-400 hover:text-white'}`}
                    >
                        <Play size={16} className="inline mr-2" /> Training Mode
                    </button>
                    <button
                        onClick={() => setMode('generator')}
                        className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${mode === 'generator' ? 'bg-purple-600 text-white' : 'text-gray-400 hover:text-white'}`}
                    >
                        <AlertTriangle size={16} className="inline mr-2" /> Generator Mode
                    </button>
                </div>
            </div>

            {mode === 'training' ? (
                // --- TRAINING MODE ---
                <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div className="md:col-span-2 space-y-6">
                        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 min-h-[400px] flex flex-col">
                            <div className="flex justify-between items-center mb-4">
                                <h2 className="text-xl font-bold text-cyan-400 flex items-center">
                                    <Mail className="mr-2" /> Inbox Item
                                </h2>
                                <div className="text-sm text-gray-400">
                                    Score: <span className="text-cyan-400 font-bold">{score.correct}</span> / {score.total}
                                </div>
                            </div>

                            {trainingEmail ? (
                                <div className="flex-1 bg-gray-900 p-6 rounded-lg border border-gray-600 font-mono text-sm whitespace-pre-wrap text-gray-300 shadow-inner">
                                    {trainingEmail.content}
                                </div>
                            ) : (
                                <div className="flex-1 flex flex-col items-center justify-center text-gray-600 border border-gray-700 border-dashed rounded-lg">
                                    <ShieldCheck size={48} className="opacity-20 mb-2" />
                                    <p>Ready to test your skills?</p>
                                    <button
                                        onClick={loadTrainingEmail}
                                        disabled={loading}
                                        className="mt-4 px-6 py-2 bg-cyan-600 text-white rounded-lg hover:bg-cyan-500 transition-colors"
                                    >
                                        {loading ? 'Loading...' : 'Start Next Scenario'}
                                    </button>
                                </div>
                            )}
                        </div>

                        {trainingEmail && !trainingFeedback && (
                            <div className="grid grid-cols-2 gap-4">
                                <button
                                    onClick={() => handleDecision('safe')}
                                    className="py-4 bg-green-600/20 border border-green-600/50 text-green-400 rounded-xl hover:bg-green-600/30 transition-all font-bold flex items-center justify-center group"
                                >
                                    <ThumbsUp className="mr-2 group-hover:scale-110 transition-transform" /> Legit / Safe
                                </button>
                                <button
                                    onClick={() => handleDecision('phishing')}
                                    className="py-4 bg-red-600/20 border border-red-600/50 text-red-400 rounded-xl hover:bg-red-600/30 transition-all font-bold flex items-center justify-center group"
                                >
                                    <ThumbsDown className="mr-2 group-hover:scale-110 transition-transform" /> Phishing Attempt
                                </button>
                            </div>
                        )}

                        {trainingFeedback && (
                            <div className={`p-6 rounded-xl border ${trainingFeedback.correct ? 'bg-green-900/30 border-green-800' : 'bg-red-900/30 border-red-800'} animate-fade-in`}>
                                <div className="flex items-center mb-2">
                                    {trainingFeedback.correct ? (
                                        <Check className="text-green-400 mr-2" size={24} />
                                    ) : (
                                        <X className="text-red-400 mr-2" size={24} />
                                    )}
                                    <h3 className={`text-lg font-bold ${trainingFeedback.correct ? 'text-green-400' : 'text-red-400'}`}>
                                        {trainingFeedback.message}
                                    </h3>
                                </div>
                                <p className="text-gray-300 ml-8 mb-4">{trainingFeedback.reason}</p>
                                <button
                                    onClick={loadTrainingEmail}
                                    className="ml-8 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg text-sm transition-colors"
                                >
                                    Next Email &rarr;
                                </button>
                            </div>
                        )}
                    </div>

                    <div className="space-y-6">
                        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                            <h3 className="text-lg font-bold text-white mb-4">Training Stats</h3>
                            <div className="space-y-4">
                                <div className="flex justify-between items-center text-sm">
                                    <span className="text-gray-400">Accuracy</span>
                                    <span className="text-white font-bold">{score.total > 0 ? Math.round((score.correct / score.total) * 100) : 0}%</span>
                                </div>
                                <div className="w-full bg-gray-700 rounded-full h-2">
                                    <div
                                        className="bg-cyan-500 h-2 rounded-full transition-all duration-500"
                                        style={{ width: `${score.total > 0 ? (score.correct / score.total) * 100 : 0}%` }}
                                    ></div>
                                </div>
                                <p className="text-xs text-center text-gray-500 mt-2">
                                    Identify mixed bag of safe and malicious emails to improve your detection rate.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            ) : (
                // --- GENERATOR MODE (Legacy) ---
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {/* Configuration */}
                    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
                        <h2 className="text-xl font-bold text-purple-400 mb-6 flex items-center">
                            <User className="mr-2" /> Campaign Configuration
                        </h2>

                        <div className="space-y-4">
                            <div>
                                <label className="block text-sm text-gray-400 mb-1">Target Persona</label>
                                <select
                                    value={persona}
                                    onChange={(e) => setPersona(e.target.value)}
                                    className="w-full bg-gray-900 border border-gray-600 rounded-lg p-3 text-white focus:ring-2 focus:ring-purple-500 outline-none"
                                >
                                    <option value="hr">HR Department</option>
                                    <option value="finance">Finance Team</option>
                                    <option value="it">IT Support</option>
                                </select>
                            </div>

                            <div>
                                <label className="block text-sm text-gray-400 mb-1">Emotional Tone</label>
                                <select
                                    value={tone}
                                    onChange={(e) => setTone(e.target.value)}
                                    className="w-full bg-gray-900 border border-gray-600 rounded-lg p-3 text-white focus:ring-2 focus:ring-purple-500 outline-none"
                                >
                                    <option value="urgent">Urgency / Fear</option>
                                    <option value="friendly">Friendly / Curiosity</option>
                                    <option value="authority">Authority / Compliance</option>
                                </select>
                            </div>

                            <button
                                onClick={generateEmail}
                                disabled={loading}
                                className="w-full py-3 bg-gradient-to-r from-purple-600 to-indigo-600 rounded-lg font-bold text-white hover:from-purple-500 hover:to-indigo-500 transition-all flex items-center justify-center"
                            >
                                {loading ? 'Generating AI Content...' : (
                                    <><Send size={18} className="mr-2" /> Generate Campaign</>
                                )}
                            </button>
                        </div>
                    </div>

                    {/* Email Preview */}
                    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 flex flex-col">
                        <h2 className="text-xl font-bold text-purple-400 mb-6 flex items-center">
                            <Mail className="mr-2" /> Email Preview
                        </h2>

                        {emailContent ? (
                            <div className="flex-1 space-y-4">
                                <div className="bg-gray-900 p-4 rounded-lg border border-gray-600 font-mono text-sm whitespace-pre-wrap text-gray-300">
                                    {emailContent.content}
                                </div>

                                <div className="flex space-x-4">
                                    <button
                                        onClick={analyzeEmail}
                                        className="flex-1 py-2 bg-yellow-600/20 text-yellow-500 border border-yellow-600/50 rounded-lg hover:bg-yellow-600/30 transition-colors flex items-center justify-center"
                                    >
                                        <ShieldCheck size={18} className="mr-2" /> Analyze for Indicators
                                    </button>
                                </div>
                            </div>
                        ) : (
                            <div className="flex-1 flex flex-col items-center justify-center text-gray-600 min-h-[200px]">
                                <MessageSquare size={48} className="opacity-20 mb-2" />
                                <p>Generate a campaign to view email draft.</p>
                            </div>
                        )}

                        {/* Analysis Results */}
                        {analysis && (
                            <div className="mt-4 bg-gray-900 rounded-xl p-4 border border-gray-700 animation-fade-in">
                                <h2 className="text-lg font-bold text-yellow-400 mb-2 flex items-center">
                                    <AlertTriangle className="mr-2" size={18} /> Security Analysis
                                </h2>
                                <p className={`text-2xl font-bold ${analysis.rating === 'High Risk' ? 'text-red-500' : 'text-yellow-500'}`}>
                                    {analysis.rating} ({analysis.score}/100)
                                </p>
                                <ul className="mt-2 space-y-1">
                                    {analysis.indicators.map((ind: string, i: number) => (
                                        <li key={i} className="text-xs text-red-400 flex items-center">
                                            <span className="w-1.5 h-1.5 bg-red-500 rounded-full mr-2" /> {ind}
                                        </li>
                                    ))}
                                </ul>
                                {analysis.feedback && analysis.feedback.length > 0 && (
                                    <div className="mt-4 border-t border-gray-700 pt-3">
                                        <h3 className="text-sm font-bold text-gray-300 mb-2">Awareness Feedback</h3>
                                        <ul className="space-y-2">
                                            {analysis.feedback.map((fb: string, i: number) => (
                                                <li key={i} className="text-xs text-gray-400 bg-gray-800 p-2 rounded border border-gray-700 border-l-2 border-l-cyan-500">
                                                    {fb}
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default PhishingSim;
