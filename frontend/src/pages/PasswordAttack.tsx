import { useState, useRef, useEffect } from 'react';
import { Lock, Unlock, Play, RefreshCw, AlertCircle, Activity, AlertTriangle, Terminal } from 'lucide-react';
import axios from 'axios';

const PasswordAttack = () => {
    const [targetHash, setTargetHash] = useState('');
    const [attackType, setAttackType] = useState('dictionary');
    const [hashType, setHashType] = useState('md5');
    const [maxLength, setMaxLength] = useState(4);
    const [mask, setMask] = useState('?l?l?l?d?d');
    const [useRules, setUseRules] = useState(false);
    const [isRunning, setIsRunning] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [error, setError] = useState('');
    const [logs, setLogs] = useState<string[]>([]);
    const logsIntervalRef = useRef<any>(null);
    const logsBottomRef = useRef<HTMLDivElement>(null);

    // Auto-scroll logs
    useEffect(() => {
        if (logsBottomRef.current) {
            logsBottomRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [logs]);

    const startSimulationLog = () => {
        setLogs([]);
        if (logsIntervalRef.current) clearInterval(logsIntervalRef.current);

        logsIntervalRef.current = setInterval(() => {
            const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
            const randomString = Array.from({ length: 8 + Math.floor(Math.random() * 8) }, () => chars[Math.floor(Math.random() * chars.length)]).join('');
            const method = attackType === 'dictionary' ? 'DICT_CHECK' : (attackType === 'mask' ? 'MASK_MATCH' : 'BRUTE_FORCE');
            const newLog = `[${new Date().toLocaleTimeString().split(' ')[0]}] ${method} :: ${randomString} ... [FAILED]`;

            setLogs(prev => {
                const newLogs = [...prev, newLog];
                if (newLogs.length > 20) return newLogs.slice(newLogs.length - 20); // Keep last 20
                return newLogs;
            });
        }, 50); // Fast updates
    };

    const stopSimulationLog = (success: boolean, password?: string) => {
        if (logsIntervalRef.current) clearInterval(logsIntervalRef.current);
        if (success && password) {
            setLogs(prev => [...prev, `[${new Date().toLocaleTimeString().split(' ')[0]}] CRACK_SUCCESS :: ${password} ... [MATCH FOUND!]`]);
        } else {
            setLogs(prev => [...prev, `[${new Date().toLocaleTimeString().split(' ')[0]}] PROCESS_END :: Timeout or Exhausted.`]);
        }
    };

    const runAttack = async () => {
        if (!targetHash) {
            setError("Please enter a target hash.");
            return;
        }
        setIsRunning(true);
        setError('');
        setResult(null);
        startSimulationLog();

        // Educational warning for Brute Force
        if (attackType === 'bruteforce') {
            const combinations = Math.pow(62, maxLength); // Alphanumeric
            // Python backend approx 100k hashes/sec (optimistically)
            const seconds = combinations / 100000;
            if (seconds > 60) {
                console.log(`Estimated time: ${seconds} seconds`);
            }
        }

        try {
            const response = await axios.post('http://localhost:8000/api/password/attack', {
                target_hash: targetHash,
                hash_type: hashType,
                attack_type: attackType,
                max_length: maxLength,
                mask: mask,
                use_rules: useRules,
                hints: {
                    name: (document.getElementById('hint-name') as HTMLInputElement)?.value || '',
                    year: (document.getElementById('hint-year') as HTMLInputElement)?.value || '',
                    company: (document.getElementById('hint-company') as HTMLInputElement)?.value || ''
                }
            });
            setResult(response.data);
            stopSimulationLog(response.data.cracked, response.data.password);
        } catch (err) {
            setError("Attack failed or backend unreachable.");
            stopSimulationLog(false);
            console.error(err);
        } finally {
            setIsRunning(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-8">
            <div className="text-center space-y-2">
                <h1 className="text-3xl font-bold text-white">Password Attack Simulator</h1>
                <p className="text-gray-400">Test password strength against various cracking algorithms.</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Configuration Panel */}
                <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 shadow-xl">
                    <h2 className="text-xl font-semibold text-cyan-400 mb-6 flex items-center">
                        <Lock className="mr-2" size={20} /> Configuration
                    </h2>

                    <div className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-400 mb-1">Target Hash</label>
                            <input
                                type="text"
                                value={targetHash}
                                onChange={(e) => setTargetHash(e.target.value)}
                                className="w-full bg-gray-900 border border-gray-600 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-cyan-500 focus:border-transparent outline-none transition-all placeholder-gray-600 font-mono text-sm"
                                placeholder="Paste MD5/SHA256/Bcrypt hash..."
                            />
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-400 mb-1">Hash Type</label>
                                <select
                                    value={hashType}
                                    onChange={(e) => setHashType(e.target.value)}
                                    className="w-full bg-gray-900 border border-gray-600 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-cyan-500 outline-none"
                                >
                                    <option value="md5">MD5</option>
                                    <option value="sha256">SHA-256</option>
                                    <option value="bcrypt">Bcrypt</option>
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-400 mb-1">Attack Method</label>
                                <select
                                    value={attackType}
                                    onChange={(e) => setAttackType(e.target.value)}
                                    className="w-full bg-gray-900 border border-gray-600 rounded-lg px-4 py-2 text-white focus:ring-2 focus:ring-cyan-500 outline-none"
                                >
                                    <option value="dictionary">Dictionary Attack</option>
                                    <option value="mask">Mask Attack (Hashcat)</option>
                                    <option value="bruteforce">Brute Force</option>
                                    <option value="ai_guided">AI-Guided Guessing</option>
                                </select>
                            </div>
                        </div>

                        {attackType === 'dictionary' && (
                            <div className="bg-gray-900/50 p-4 rounded-lg border border-gray-700">
                                <label className="flex items-center space-x-3 cursor-pointer">
                                    <input
                                        type="checkbox"
                                        checked={useRules}
                                        onChange={(e) => setUseRules(e.target.checked)}
                                        className="form-checkbox h-5 w-5 text-cyan-600 rounded border-gray-300 focus:ring-cyan-500"
                                    />
                                    <span className="text-gray-300 text-sm">Enable Rule-Based Mutations</span>
                                </label>
                                <p className="text-xs text-gray-500 mt-2 ml-8">
                                    Applies rules like Best64 (Append numbers, capitalization, leet speak) to each dictionary word.
                                </p>
                            </div>
                        )}

                        {attackType === 'mask' && (
                            <div className="bg-gray-900/50 p-4 rounded-lg border border-gray-700 space-y-2">
                                <label className="block text-sm font-medium text-gray-400">Mask Pattern</label>
                                <input
                                    type="text"
                                    value={mask}
                                    onChange={(e) => setMask(e.target.value)}
                                    className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-2 text-white font-mono text-sm focus:ring-1 focus:ring-cyan-500 outline-none"
                                    placeholder="?u?l?l?l?d?d"
                                />
                                <div className="grid grid-cols-2 gap-2 text-xs text-gray-500 font-mono mt-1">
                                    <div>?l = a-z</div>
                                    <div>?u = A-Z</div>
                                    <div>?d = 0-9</div>
                                    <div>?s = special</div>
                                    <div>?a = all</div>
                                </div>
                                <p className="text-xs text-cyan-400 mt-2">
                                    Example: <strong>?u?l?l?l?d?d</strong> matches "Pass12"
                                </p>
                            </div>
                        )}

                        {attackType === 'bruteforce' && (
                            <div className="bg-gray-900/50 p-4 rounded-lg border border-gray-700">
                                <label className="block text-sm font-medium text-gray-400 mb-2">Max Length (Brute Force)</label>
                                <div className="flex items-center space-x-4">
                                    <input
                                        type="range"
                                        min="1"
                                        max="6"
                                        value={maxLength}
                                        onChange={(e) => setMaxLength(parseInt(e.target.value))}
                                        className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer"
                                    />
                                    <span className="text-white font-mono font-bold">{maxLength} chars</span>
                                </div>
                                <div className="mt-2 text-xs text-gray-400">
                                    <p>Combinations: <span className="text-cyan-400">{Math.pow(62, maxLength).toLocaleString()}</span></p>
                                    <p>Est. Time (Backend): <span className={Math.pow(62, maxLength) / 100000 > 60 ? "text-red-400" : "text-green-400"}>
                                        {(() => {
                                            const sec = Math.pow(62, maxLength) / 100000;
                                            if (sec < 60) return "< 1 minute";
                                            if (sec < 3600) return `~${Math.ceil(sec / 60)} minutes`;
                                            if (sec < 86400) return `~${(sec / 3600).toFixed(1)} hours`;
                                            return `~${(sec / 86400).toFixed(1)} days`;
                                        })()}
                                    </span></p>
                                </div>
                                <p className="text-xs text-gray-500 mt-2">
                                    <AlertTriangle size={12} className="inline mr-1" />
                                    Real "decryption" requires checking every combination.
                                    Trying to "decrypt" 8 chars would take ~60 years on this laptop.
                                </p>
                            </div>
                        )}

                        {attackType === 'ai_guided' && (
                            <div className="bg-gray-900/50 p-4 rounded-lg border border-gray-700 space-y-4">
                                <h3 className="text-sm font-medium text-cyan-400 flex items-center">
                                    <Activity size={16} className="mr-2" /> Target Information (Hints)
                                </h3>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-xs text-gray-500 mb-1">Name / Keyword</label>
                                        <input
                                            type="text"
                                            className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-1.5 text-white text-sm focus:ring-1 focus:ring-cyan-500 outline-none"
                                            placeholder="e.g. Alice"
                                            id="hint-name"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-xs text-gray-500 mb-1">Birth Year / Number</label>
                                        <input
                                            type="text"
                                            className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-1.5 text-white text-sm focus:ring-1 focus:ring-cyan-500 outline-none"
                                            placeholder="e.g. 1990"
                                            id="hint-year"
                                        />
                                    </div>
                                    <div className="col-span-2">
                                        <label className="block text-xs text-gray-500 mb-1">Company / Pet</label>
                                        <input
                                            type="text"
                                            className="w-full bg-gray-800 border border-gray-600 rounded px-3 py-1.5 text-white text-sm focus:ring-1 focus:ring-cyan-500 outline-none"
                                            placeholder="e.g. Google"
                                            id="hint-company"
                                        />
                                    </div>
                                </div>
                                <p className="text-xs text-gray-500">
                                    AI will generate smart variations (Leet speak, appendages) based on this info.
                                </p>
                            </div>
                        )}

                        <button
                            onClick={runAttack}
                            disabled={isRunning}
                            className={`w-full mt-4 py-3 rounded-lg font-bold flex items-center justify-center transition-all ${isRunning
                                ? 'bg-gray-600 cursor-not-allowed text-gray-400'
                                : 'bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 hover:to-red-400 text-white shadow-lg hover:shadow-red-500/30'
                                }`}
                        >
                            {isRunning ? (
                                <RefreshCw className="animate-spin mr-2" size={20} />
                            ) : (
                                <Play className="mr-2" size={20} />
                            )}
                            {isRunning ? 'Cracking in Progress...' : 'Launch Attack'}
                        </button>

                        {error && (
                            <div className="p-3 bg-red-900/30 border border-red-800 text-red-300 rounded-lg text-sm flex items-start">
                                <AlertCircle className="mr-2 mt-0.5 flex-shrink-0" size={16} />
                                {error}
                            </div>
                        )}
                    </div>
                </div>

                {/* Results Panel */}
                <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 shadow-xl flex flex-col">
                    <h2 className="text-xl font-semibold text-cyan-400 mb-6 flex items-center">
                        <Unlock className="mr-2" size={20} /> Results Analysis
                    </h2>

                    {result ? (
                        <div className="space-y-6 flex-1">
                            <div className={`p-4 rounded-lg flex items-center ${result.cracked ? 'bg-green-900/20 border border-green-800' : (result.password === "TIMEOUT" ? 'bg-yellow-900/20 border border-yellow-800' : 'bg-red-900/20 border border-red-800')}`}>
                                {result.cracked ? (
                                    <div className="flex items-center space-x-4">
                                        <div className={`p-2 rounded-full ${result.risk_severity === 'Critical' ? 'bg-red-600' : result.risk_severity === 'High' ? 'bg-orange-500' : 'bg-yellow-500'}`}>
                                            <Unlock size={24} className="text-white" />
                                        </div>
                                        <div>
                                            <p className={`text-sm uppercase tracking-wider font-bold ${result.risk_severity === 'Critical' ? 'text-red-400' : result.risk_severity === 'High' ? 'text-orange-400' : 'text-yellow-400'}`}>Password Cracked ({result.risk_severity} Risk)</p>
                                            <p className="text-2xl font-mono text-white mt-1">{result.password}</p>
                                        </div>
                                    </div>
                                ) : result.password === "TIMEOUT" ? (
                                    <div className="flex items-center space-x-4">
                                        <div className="p-2 bg-yellow-600 rounded-full">
                                            <Activity size={24} className="text-white" />
                                        </div>
                                        <div>
                                            <p className="text-sm text-yellow-500 uppercase tracking-wider font-bold">Time Limit Exceeded</p>
                                            <p className="text-sm text-gray-300 mt-1 max-w-sm">
                                                Search space too large for CPU. Mask <strong>{mask}</strong> has millions of combinations.
                                            </p>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="flex items-center space-x-4">
                                        <div className="p-2 bg-red-500 rounded-full">
                                            <Lock size={24} className="text-white" />
                                        </div>
                                        <div>
                                            <p className="text-sm text-red-400 uppercase tracking-wider font-bold">Failed to Crack</p>
                                            <p className="text-sm text-gray-400 mt-1">Try a different method or longer timeframe.</p>
                                        </div>
                                    </div>
                                )}
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="bg-gray-900/50 p-4 rounded-lg">
                                    <p className="text-gray-500 text-xs uppercase">Time Taken</p>
                                    <p className="text-xl font-mono text-white">{result.time_taken.toFixed(4)}s</p>
                                </div>
                                <div className="bg-gray-900/50 p-4 rounded-lg">
                                    <p className="text-gray-500 text-xs uppercase">Attempts</p>
                                    <p className="text-xl font-mono text-white">{result.attempts.toLocaleString()}</p>
                                </div>
                            </div>

                            <div className="mt-4">
                                <h4 className="text-gray-400 text-sm mb-2">Security Recommendation</h4>
                                <p className="text-sm text-gray-300 bg-gray-900 p-3 rounded border-l-4 border-cyan-500">
                                    {result.cracked
                                        ? "This password is extremely weak. It was found in a common dictionary or cracked instantly. Recommend immediate change to a passphrase."
                                        : "Password appears resistant to this specific attack vector. Try running AI-guided guessing for advanced analysis."}
                                </p>
                            </div>
                        </div>
                    ) : (
                        <div className="flex-1 flex flex-col items-center justify-center text-gray-600 space-y-4 min-h-[200px]">
                            <Activity size={48} className="opacity-20" />
                            <p>Awaiting simulation data...</p>
                        </div>
                    )}

                    {/* Matrix Terminal Log */}
                    <div className="mt-6 bg-black rounded-lg p-4 font-mono text-xs h-48 overflow-hidden border border-gray-700 shadow-inner relative">
                        <div className="absolute top-2 right-2 text-green-500 opacity-50 flex items-center">
                            <Terminal size={14} className="mr-1" /> TERMINAL
                        </div>
                        <div className="overflow-y-auto h-full space-y-1 scrollbar-hide">
                            {logs.map((log, i) => (
                                <div key={i} className={`${log.includes('MATCH FOUND') ? 'text-green-400 font-bold text-sm' : 'text-green-800/80'}`}>
                                    {log}
                                </div>
                            ))}
                            <div ref={logsBottomRef} />
                        </div>
                        {isRunning && (
                            <div className="absolute bottom-2 right-4 text-green-500 animate-pulse text-xs">
                                PROCESSING...
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PasswordAttack;
