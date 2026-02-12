import React from 'react';
import { Shield, Lock, Users, AlertTriangle, Key, Activity, BarChart } from 'lucide-react';
import { Link } from 'react-router-dom';

import axios from 'axios';
import { useEffect, useState } from 'react';

const Dashboard = () => {
    const [stats, setStats] = useState({
        simulations_run: 0,
        weak_passwords: 0,
        phishing_campaigns: 0,
        threat_level: "None"
    });

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/stats/');
                setStats(response.data);
            } catch (error) {
                console.error("Failed to fetch stats", error);
            }
        };
        fetchStats();
        // Poll every 5 seconds for live updates
        const interval = setInterval(fetchStats, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="space-y-6">
            <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">
                Security Dashboard
            </h1>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <DashboardCard
                    title="Active Threat Level"
                    value={stats.threat_level}
                    icon={<Shield size={24} className="text-green-400" />}
                    description="Lab environment secure."
                    color="border-green-500/50 bg-green-900/10"
                />
                <DashboardCard
                    title="Simulations Run"
                    value={stats.simulations_run}
                    icon={<Activity size={24} className="text-blue-400" />}
                    description="Total attacks simulated."
                    color="border-blue-500/50 bg-blue-900/10"
                />
                <DashboardCard
                    title="Risk Score"
                    value={stats.weak_passwords > 0 ? "High" : "Low"}
                    icon={<AlertTriangle size={24} className="text-yellow-400" />}
                    description={`${stats.weak_passwords} weak passwords found.`}
                    color="border-yellow-500/50 bg-yellow-900/10"
                />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
                <ModuleCard
                    title="Password Attack Simulator"
                    description="Test password strength against dictionary, brute-force, and AI-guided attacks."
                    link="/password-attack"
                    icon={<Lock size={32} />}
                    color="from-red-500 to-orange-500"
                />
                <ModuleCard
                    title="Social Engineering"
                    description="Simulate phishing campaigns and analyze user awareness."
                    link="/phishing-sim"
                    icon={<Users size={32} />}
                    color="from-purple-500 to-pink-500"
                />
                <ModuleCard
                    title="Awareness & Training Report"
                    description="View your personalized security risk profile and learning recommendations."
                    link="/report"
                    icon={<BarChart size={32} />}
                    color="from-green-500 to-emerald-500"
                />
            </div>
        </div>
    );
};

const DashboardCard = ({ title, value, icon, description, color }: any) => (
    <div className={`p-6 rounded-xl border ${color} hover:shadow-lg transition-all`}>
        <div className="flex items-center justify-between mb-4">
            <h3 className="text-gray-400 font-medium">{title}</h3>
            {icon}
        </div>
        <div className="text-3xl font-bold text-white mb-1">{value}</div>
        <div className="text-sm text-gray-500">{description}</div>
    </div>
);

const ModuleCard = ({ title, description, link, icon, color }: any) => (
    <Link to={link} className="relative group overflow-hidden rounded-2xl bg-gray-800 border border-gray-700 hover:border-gray-600 transition-all p-8">
        <div className={`absolute inset-0 bg-gradient-to-r ${color} opacity-0 group-hover:opacity-10 transition-opacity`} />
        <div className="relative z-10 flex items-start space-x-4">
            <div className={`p-3 rounded-lg bg-gradient-to-br ${color} text-white shadow-lg`}>
                {icon}
            </div>
            <div>
                <h3 className="text-xl font-bold text-white mb-2 group-hover:text-cyan-400 transition-colors">{title}</h3>
                <p className="text-gray-400">{description}</p>
            </div>
        </div>
        <div className="absolute bottom-0 right-0 p-4 opacity-0 group-hover:opacity-100 transition-opacity transform translate-y-2 group-hover:translate-y-0">
            <span className="text-sm font-medium text-cyan-400">Launch Module →</span>
        </div>
    </Link>
);

export default Dashboard;
