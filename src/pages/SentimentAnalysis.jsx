import NewsCard from '../components/news/NewsCard';

const sentimentData = [
    { source: 'Reuters', time: '2 hours ago', title: 'Tech Giants Report Strong Q3 Earnings Beat Expectations', aiSummary: 'Revenue ↑ 12%. AI investments paying off, cloud growth accelerating at 15% YoY. Market confidence remains high with strong forward guidance.', sentiment: 'positive' },
    { source: 'Bloomberg', time: '4 hours ago', title: 'Federal Reserve Maintains Current Interest Rate Policy', aiSummary: 'Policy unchanged, watching inflation data closely. Gradual approach expected through 2024. Market reaction muted.', sentiment: 'neutral' },
    { source: 'CNBC', time: '6 hours ago', title: 'Energy Sector Faces New Environmental Regulations', aiSummary: 'New policies ↓ 5% sector performance, compliance costs rising. Traditional energy companies reassessing strategies.', sentiment: 'negative' },
    { source: 'WSJ', time: '8 hours ago', title: 'Healthcare Breakthrough Drives Biotech Rally', aiSummary: 'FDA approvals ↑ 8%, biotech rally continues. Pharmaceutical partnerships expanding, innovation pipeline strong.', sentiment: 'positive' },
    { source: 'MarketWatch', time: '12 hours ago', title: 'Cryptocurrency Market Shows Mixed Signals', aiSummary: 'Bitcoin stable, altcoins volatile. Regulatory clarity improving but adoption pace varies. Institutional interest remains steady.', sentiment: 'neutral' },
    { source: 'Financial Times', time: '1 day ago', title: 'Emerging Markets Show Resilience Amid Global Uncertainty', aiSummary: 'EM currencies stabilizing, commodity demand strong. Infrastructure investments driving growth in developing economies.', sentiment: 'positive' },
];

const SentimentAnalysis = () => {
    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold">News Sentiment Analysis</h1>
                <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md transition-colors">
                    🔄 Refresh
                </button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {sentimentData.map((item, index) => (
                    <NewsCard key={index} {...item} isSentimentLayout={true} />
                ))}
            </div>
        </div>
    );
}

export default SentimentAnalysis;
