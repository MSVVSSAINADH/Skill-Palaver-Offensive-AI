import React, { useState } from 'react';
import { FileText, CheckCircle, AlertTriangle, Download } from 'lucide-react';
import axios from 'axios';
import { toPng } from 'html-to-image';
import { jsPDF } from 'jspdf';

const Report = () => {
    const [report, setReport] = useState<any>(null);
    const reportRef = React.useRef<HTMLDivElement>(null);

    const generateReport = async () => {
        try {
            // Fetch real session stats
            const statsResponse = await axios.get('http://localhost:8000/api/stats/');
            const realStats = statsResponse.data;

            const reportRequest = {
                user_name: "Lab User (Session)",
                simulations_run: realStats.simulations_run,
                phishing_clicks: realStats.phishing_campaigns, // Maps to 'phishing_campaigns' for now
                weak_passwords_count: realStats.weak_passwords
            };

            const response = await axios.post('http://localhost:8000/api/awareness/generate', reportRequest);
            setReport(response.data);
        } catch (error) {
            console.error("Failed to generate report", error);
        }
    };

    const handleDownloadPDF = async () => {
        console.log("Download initiated");
        if (!reportRef.current) {
            console.error("Report reference is null");
            return;
        }

        try {
            console.log("Starting html-to-image capture...");
            const imgData = await toPng(reportRef.current, {
                cacheBust: true,
                pixelRatio: 2,
                backgroundColor: '#1f2937' // Match bg-gray-800
            });
            console.log("Image captured successfully");

            const pdf = new jsPDF({
                orientation: 'portrait',
                unit: 'px',
                format: [reportRef.current.offsetWidth * 2, reportRef.current.offsetHeight * 2] // Scale for pixel ratio
            });

            const imgProps = pdf.getImageProperties(imgData);
            const pdfWidth = pdf.internal.pageSize.getWidth();
            const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

            pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
            pdf.save(`security_profile_${report.user_name.replace(/\s+/g, '_')}.pdf`);
            console.log("PDF saved");
        } catch (error) {
            console.error("Failed to generate PDF", error);
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-8">
            <div className="text-center space-y-2">
                <h1 className="text-3xl font-bold text-white">Awareness Training Report</h1>
                <p className="text-gray-400">Review your performance and personalized recommendations.</p>
            </div>

            {!report ? (
                <div className="bg-gray-800 rounded-xl p-12 border border-gray-700 text-center">
                    <FileText size={64} className="mx-auto text-gray-600 mb-6" />
                    <h2 className="text-xl font-bold text-white mb-2">Ready to generate report?</h2>
                    <p className="text-gray-400 mb-6">Based on your recent simulation activity.</p>
                    <button
                        onClick={generateReport}
                        className="px-8 py-3 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg font-bold transition-colors shadow-lg shadow-cyan-500/20"
                    >
                        Generate Security Profile
                    </button>
                </div>
            ) : (
                <div ref={reportRef} className="bg-gray-800 rounded-xl p-8 border border-gray-700 animation-fade-in">
                    <div className="flex justify-between items-start mb-8 border-b border-gray-700 pb-6">
                        <div>
                            <h2 className="text-2xl font-bold text-white mb-1">Security Profile: {report.user_name}</h2>
                            <p className="text-gray-400">Generated on {new Date().toLocaleDateString()}</p>
                        </div>
                        <div className="text-right">
                            <div className="text-sm text-gray-400 mb-1">Overall Score</div>
                            <div className={`text-4xl font-bold ${report.security_score > 80 ? 'text-green-500' : 'text-yellow-500'}`}>
                                {report.security_score}/100
                            </div>
                        </div>
                    </div>

                    <div className="space-y-6">
                        <h3 className="text-xl font-bold text-cyan-400">Recommendations</h3>
                        {report.recommendations.map((rec: any, index: number) => (
                            <div key={index} className="bg-gray-900 p-6 rounded-lg border border-gray-600 flex items-start">
                                {rec.risk === 'Low' ? (
                                    <CheckCircle className="text-green-500 mt-1 flex-shrink-0 mr-4" />
                                ) : (
                                    <AlertTriangle className={`mt-1 flex-shrink-0 mr-4 ${rec.risk === 'High' ? 'text-red-500' : 'text-yellow-500'}`} />
                                )}
                                <div>
                                    <div className="flex items-center mb-1">
                                        <h4 className="font-bold text-white mr-3">{rec.topic}</h4>
                                        <span className={`text-xs px-2 py-0.5 rounded ${rec.risk === 'High' ? 'bg-red-900/50 text-red-300' :
                                            rec.risk === 'Medium' ? 'bg-yellow-900/50 text-yellow-300' : 'bg-green-900/50 text-green-300'
                                            }`}>
                                            {rec.risk} Risk
                                        </span>
                                    </div>
                                    <p className="text-gray-400">{rec.advice}</p>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="mt-8 pt-6 border-t border-gray-700 flex justify-end">
                        <button
                            onClick={handleDownloadPDF}
                            className="flex items-center text-cyan-400 hover:text-cyan-300 font-medium"
                        >
                            <Download size={18} className="mr-2" /> Download PDF Report
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Report;
