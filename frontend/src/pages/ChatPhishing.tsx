import React, { useState, useEffect, useRef } from 'react';
import { MessageCircle, Send, Shield, AlertTriangle, User, RefreshCw } from 'lucide-react';
import axios from 'axios';

const ChatPhishing = () => {
    const [scenario, setScenario] = useState('it_support');
    const [messages, setMessages] = useState<any[]>([]);
    const [script, setScript] = useState<any[]>([]);
    const [completed, setCompleted] = useState(false);
    const [currentStep, setCurrentStep] = useState(0);
    const [typing, setTyping] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, typing]);

    const startSimulation = async () => {
        setMessages([]);
        setCompleted(false);
        setCurrentStep(0);
        try {
            const response = await axios.post('http://localhost:8000/api/social/chat/generate', {
                scenario
            });
            setScript(response.data.script);
            // Kick off the first message
            processStep(response.data.script, 0);
        } catch (error) {
            console.error("Failed to load script", error);
        }
    };

    const processStep = (currentScript: any[], stepIndex: number) => {
        if (stepIndex >= currentScript.length) return;

        const step = currentScript[stepIndex];

        if (step.sender === 'bot') {
            setTyping(true);
            setTimeout(() => {
                setTyping(false);
                setMessages(prev => [...prev, { ...step, id: Date.now() }]);

                if (step.end) {
                    setCompleted(true);
                } else if (stepIndex + 1 < currentScript.length) {
                    const nextStep = currentScript[stepIndex + 1];
                    if (nextStep.sender === 'bot') {
                        processStep(currentScript, stepIndex + 1);
                    } else {
                        // Wait for user input
                        setCurrentStep(stepIndex + 1);
                    }
                }
            }, step.delay || 1000);
        }
    };

    const handleOptionClick = (option: any) => {
        // Add user message
        setMessages(prev => [...prev, { sender: 'user', text: option.label, id: Date.now() }]);

        // Find next step based on 'next' ID or just next index
        const nextStepId = option.next;
        const nextIndex = script.findIndex(s => s.id === nextStepId);

        if (nextIndex !== -1) {
            processStep(script, nextIndex);
        }
    };

    return (
        <div className="max-w-4xl mx-auto h-[calc(100vh-140px)] flex flex-col">
            <div className="text-center space-y-2 mb-6">
                <h1 className="text-3xl font-bold text-white flex justify-center items-center">
                    <MessageCircle className="mr-3" /> Chat Phishing Simulator
                </h1>
                <p className="text-gray-400">Can you spot the manipulation in a conversation?</p>
            </div>

            <div className="flex-1 bg-gray-900 rounded-2xl border border-gray-700 shadow-2xl overflow-hidden flex flex-col md:flex-row">
                {/* Sidebar Configuration */}
                <div className="w-full md:w-64 bg-gray-800 p-6 border-r border-gray-700 flex flex-col">
                    <h2 className="text-lg font-bold text-cyan-400 mb-4">Configuration</h2>

                    <div className="mb-6">
                        <label className="block text-sm text-gray-400 mb-2">Scenario</label>
                        <select
                            value={scenario}
                            onChange={(e) => setScenario(e.target.value)}
                            className="w-full bg-gray-900 border border-gray-600 rounded-lg p-2 text-white text-sm focus:ring-2 focus:ring-cyan-500 outline-none"
                        >
                            <option value="it_support">IT Support Scam (Randomized)</option>
                            <option value="prize">Prize/Lottery Scam (Randomized)</option>
                            <option value="ceo_fraud">CEO/Executive Fraud</option>
                        </select>
                    </div>

                    <button
                        onClick={startSimulation}
                        className="w-full py-2 bg-gradient-to-r from-cyan-600 to-blue-600 rounded-lg font-bold text-white hover:opacity-90 transition-opacity flex items-center justify-center mt-auto"
                    >
                        <RefreshCw size={18} className="mr-2" /> Restart Chat
                    </button>
                </div>

                {/* Chat Area */}
                <div className="flex-1 flex flex-col bg-gray-950 relative">
                    {/* Header */}
                    <div className="p-4 bg-gray-900 border-b border-gray-800 flex items-center">
                        <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center mr-3">
                            <User size={20} className="text-gray-400" />
                        </div>
                        <div>
                            <h3 className="text-white font-bold">
                                {scenario === 'it_support' && 'IT Support (Verified)'}
                                {scenario === 'prize' && 'Prize Notification'}
                                {scenario === 'ceo_fraud' && 'CEO - John Doe'}
                            </h3>
                            <p className="text-xs text-green-500 flex items-center">
                                <span className="w-2 h-2 bg-green-500 rounded-full mr-1 animate-pulse"></span> Online
                            </p>
                        </div>
                    </div>

                    {/* Messages */}
                    <div className="flex-1 overflow-y-auto p-4 space-y-4">
                        {messages.length === 0 && !typing && (
                            <div className="flex flex-col items-center justify-center h-full text-gray-600">
                                <MessageCircle size={48} className="opacity-20 mb-2" />
                                <p>Start a simulation to verify your skills.</p>
                            </div>
                        )}

                        {messages.map((msg, idx) => (
                            <div key={msg.id || idx} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[80%] p-3 rounded-2xl ${msg.sender === 'user'
                                    ? 'bg-cyan-600 text-white rounded-br-none'
                                    : 'bg-gray-800 text-gray-200 rounded-bl-none'
                                    }`}>
                                    <p className="text-sm">{msg.text}</p>
                                </div>
                            </div>
                        ))}

                        {typing && (
                            <div className="flex justify-start">
                                <div className="bg-gray-800 p-3 rounded-2xl rounded-bl-none flex space-x-1">
                                    <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></span>
                                    <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-100"></span>
                                    <span className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-200"></span>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Interaction Area */}
                    <div className="p-4 bg-gray-900 border-t border-gray-800">
                        {completed ? (
                            <div className={`p-4 rounded-lg text-center ${messages[messages.length - 1]?.success ? 'bg-red-900/30 text-red-400 border border-red-800' : 'bg-green-900/30 text-green-400 border border-green-800'}`}>
                                {messages[messages.length - 1]?.success ? (
                                    <>
                                        <AlertTriangle className="mx-auto mb-2" />
                                        <p className="font-bold">You were Phished!</p>
                                        <p className="text-sm">Always verify through official channels before sharing codes.</p>
                                    </>
                                ) : (
                                    <>
                                        <Shield className="mx-auto mb-2" />
                                        <p className="font-bold">Good Catch!</p>
                                        <p className="text-sm">You successfully identified the social engineering attempt.</p>
                                    </>
                                )}
                            </div>
                        ) : (
                            script[currentStep]?.sender === 'user_options' && (
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                    {script[currentStep].options.map((opt: any, idx: number) => (
                                        <button
                                            key={idx}
                                            onClick={() => handleOptionClick(opt)}
                                            className="p-3 bg-gray-800 hover:bg-gray-700 text-cyan-400 text-sm font-medium rounded-lg border border-gray-700 transition-colors text-left"
                                        >
                                            {opt.label}
                                        </button>
                                    ))}
                                </div>
                            )
                        )}

                        {!completed && script[currentStep]?.sender !== 'user_options' && (
                            <div className="text-center text-xs text-gray-600">
                                Waiting for reply...
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatPhishing;
