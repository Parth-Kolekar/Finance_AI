import React from 'react';
import Card from '../components/shared/Card';
import Tag from '../components/shared/Tag';
import { LuBrainCircuit } from 'react-icons/lu';

const marketData = [
  { name: 'S&P 500', value: '4,891.23', change: '+42.75', percentage: '+0.88%', isPositive: true },
  { name: 'NASDAQ', value: '17,425.68', change: '+215.92', percentage: '+1.25%', isPositive: true },
  { name: 'Dow Jones', value: '38,109.43', change: '-118.27', percentage: '-0.31%', isPositive: false },
  { name: 'NIFTY 50', value: '25,145.10', change: '+238.45', percentage: '+0.96%', isPositive: true },
];

const recentAnalysisData = [
    { sector: 'Tech Sector', sentiment: 'BULLISH', summary: 'AI investments driving growth in major tech companies', isPositive: true },
    { sector: 'Energy Sector', sentiment: 'BEARISH', summary: 'New environmental policies impacting sector performance', isPositive: false },
];

const Dashboard = () => {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-xl font-semibold mb-4">Market Overview</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {marketData.map((item) => (
            <Card key={item.name}>
              <div className="flex justify-between items-center text-gray-400 text-sm">
                <span>{item.name}</span>
                <span className="font-mono bg-gray-800 px-2 py-0.5 rounded text-xs">{item.name.split(' ')[0]}</span>
              </div>
              <p className="text-3xl font-semibold my-2 text-white">{item.value}</p>
              <div className={`text-sm font-medium ${item.isPositive ? 'text-green-500' : 'text-red-500'}`}>
                <span>{item.change}</span>
                <span className="ml-1">({item.percentage})</span>
              </div>
            </Card>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
            <Card>
                <h3 className="text-lg font-semibold mb-2">Quick AI Insights</h3>
                <p className="text-sm text-gray-400 mb-4">Ask about market trends, stock analysis, or any financial questions.</p>
                <div className="flex items-start gap-4">
                    <div className="bg-purple-500 p-2 rounded-full"><LuBrainCircuit size={20} /></div>
                    <div className="bg-[#0D1117] p-3 rounded-lg flex-1">
                        <p className="text-sm">Hi! I'm your AI financial assistant.</p>
                    </div>
                </div>
            </Card>
            <Card>
                <h3 className="text-lg font-semibold">Market Trend Analysis</h3>
                <p className="text-sm text-gray-400 mt-2">All-powered technical analysis will be displayed here.</p>
            </Card>
        </div>

        <div className="lg:col-span-1">
            <Card>
                <h3 className="text-lg font-semibold mb-4">Recent Analysis</h3>
                <div className="space-y-4">
                    {recentAnalysisData.map(item => (
                        <div key={item.sector}>
                            <div className="flex justify-between items-center mb-1">
                                <h4 className="font-medium text-gray-300">{item.sector}</h4>
                                <Tag type={item.isPositive ? 'positive' : 'negative'}>{item.sentiment}</Tag>
                            </div>
                            <p className="text-sm text-gray-400">{item.summary}</p>
                        </div>
                    ))}
                </div>
            </Card>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
