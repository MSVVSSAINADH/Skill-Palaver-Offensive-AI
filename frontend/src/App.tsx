import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { useState } from 'react';
import Dashboard from './pages/Dashboard';
import PasswordAttack from './pages/PasswordAttack';
import PhishingSim from './pages/PhishingSim';
import ChatPhishing from './pages/ChatPhishing';
import Report from './pages/Report';
import { Menu, Shield, Lock, Users, BarChart, MessageSquare } from 'lucide-react';

function App() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <Router>
      <div className="flex h-screen bg-gray-900 text-white font-sans antialiased selection:bg-cyan-500 selection:text-white">
        {/* Sidebar */}
        <aside className={`fixed inset-y-0 left-0 z-50 w-64 bg-gray-800 border-r border-gray-700 transition-transform transform ${isOpen ? 'translate-x-0' : '-translate-x-full'} md:translate-x-0 md:static md:inset-0`}>
          <div className="flex items-center justify-between p-4 border-b border-gray-700">
            <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-blue-500 truncate">
              CyberSim Platform
            </h1>
            <button onClick={() => setIsOpen(false)} className="md:hidden text-gray-400 hover:text-white">
              ✕
            </button>
          </div>
          <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
            <NavLink to="/" icon={<Shield size={20} />} label="Dashboard" />
            <NavLink to="/password-attack" icon={<Lock size={20} />} label="Password Attack" />
            <NavLink to="/phishing-sim" icon={<Users size={20} />} label="Social Engineering" />
            <NavLink to="/chat-phishing" icon={<MessageSquare size={20} />} label="Chat Phishing" />
            <NavLink to="/report" icon={<BarChart size={20} />} label="Awareness Report" />
          </nav>
          <div className="p-4 border-t border-gray-700 text-xs text-center text-gray-500">
            v1.0.0 Alpha • Lab Environment Only
          </div>
        </aside>

        {/* content */}
        <div className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
          <div className="w-full bg-red-900/90 text-red-100 text-center py-1.5 text-xs font-bold tracking-widest uppercase border-b border-red-700 z-50">
            ⚠️ FOR SECURITY TRAINING PURPOSES ONLY. RED-TEAM SIMULATOR ENVIRONMENT. ⚠️
          </div>
          <header className="md:hidden flex items-center p-4 bg-gray-800 border-b border-gray-700">
            <button onClick={() => setIsOpen(true)} className="text-gray-400 hover:text-white mr-4">
              <Menu size={24} />
            </button>
            <span className="font-bold">CyberSim Platform</span>
          </header>
          <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-950 p-6">
            <div className="max-w-7xl mx-auto">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/password-attack" element={<PasswordAttack />} />
                <Route path="/phishing-sim" element={<PhishingSim />} />
                <Route path="/chat-phishing" element={<ChatPhishing />} />
                <Route path="/report" element={<Report />} />
              </Routes>
            </div>
          </main>
        </div>
      </div>
    </Router>
  );
}

function NavLink({ to, icon, label }: { to: string; icon: React.ReactNode; label: string }) {
  return (
    <Link to={to} className="flex items-center px-4 py-3 text-gray-300 rounded-lg hover:bg-gray-700/50 hover:text-cyan-400 transition-colors group">
      <span className="mr-3 text-gray-400 group-hover:text-cyan-400">{icon}</span>
      <span className="font-medium">{label}</span>
    </Link>
  );
}

export default App;
