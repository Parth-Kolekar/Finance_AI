import NewsCard from '../components/news/NewsCard';

const marketNewsData = [
    { source: 'Reuters', time: '1 hour ago', title: 'S&P 500 Hits New Record High on Tech Rally', summary: 'The S&P 500 reached a new all-time high today as technology stocks surged on strong earnings reports and optimistic AI outlook.', aiAnalysis: 'Tech sector momentum ↑ 3.2%, driven by cloud computing growth and AI investments. Market breadth expanding beyond mega-cap names.', sentiment: 'positive' },
    { source: 'Bloomberg', time: '3 hours ago', title: 'Fed Officials Signal Cautious Approach to Rate Cuts', summary: 'Federal Reserve officials indicated they will take a measured approach to potential interest rate reductions in 2024.', aiAnalysis: 'Policy stance remains data-dependent. Market expectations for rate cuts ↓ 25bps. Bond yields stable.', sentiment: 'neutral' },
    { source: 'CNBC', time: '5 hours ago', title: 'Healthcare Stocks Rally on FDA Approval Wave', summary: 'Healthcare and biotech stocks surged following several key FDA approvals and positive clinical trial results.', aiAnalysis: 'Healthcare sector ↑ 2.8%, biotech subsector leading gains. Drug approval pipeline robust for Q1 2024.', sentiment: 'positive' },
];

const MarketNews = () => {
    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold">Market News</h1>
                <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md transition-colors">
                    🔄 Refresh
                </button>
            </div>
            <div className="space-y-6">
                {marketNewsData.map((newsItem, index) => (
                    <NewsCard key={index} {...newsItem} />
                ))}
            </div>
        </div>
    );
};

export default MarketNews;