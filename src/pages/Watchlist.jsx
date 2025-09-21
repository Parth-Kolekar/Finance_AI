import StockCard from '../components/watchlist/StockCard';

const watchlistData = [
  { name: 'Apple Inc.', ticker: 'AAPL', price: '189.25', change: '+4.42', percentage: '+2.39%', isPositive: true, insight: 'Strong iPhone 15 sales momentum. Services revenue growing steadily.' },
  { name: 'Tesla Inc.', ticker: 'TSLA', price: '242.15', change: '-4.61', percentage: '-1.87%', isPositive: false, insight: 'EV competition intensifying, but Cybertruck launch showing promise.' },
  { name: 'NVIDIA Corp.', ticker: 'NVDA', price: '478.92', change: '+16.34', percentage: '+3.54%', isPositive: true, insight: 'AI chip demand remains robust, datacenter growth accelerating.' },
  { name: 'Microsoft Corp.', ticker: 'MSFT', price: '378.85', change: '+4.62', percentage: '+1.23%', isPositive: true, insight: 'Azure growth strong. Copilot integration driving productivity gains.' },
  { name: 'Alphabet Inc.', ticker: 'GOOGL', price: '142.68', change: '+2.15', percentage: '+1.53%', isPositive: true, insight: 'Search dominance intact. Bard AI integration showing progress.' },
  { name: 'Amazon.com Inc.', ticker: 'AMZN', price: '156.42', change: '+1.89', percentage: '+1.22%', isPositive: true, insight: 'AWS growth stable, holiday season retail performance solid.' },
];

const Watchlist = () => {
  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">AI-Powered Watchlist</h1>
        <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md transition-colors">
          + Add Stock
        </button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {watchlistData.map((stock) => (
          <StockCard key={stock.ticker} {...stock} />
        ))}
      </div>
    </div>
  );
};

export default Watchlist;
