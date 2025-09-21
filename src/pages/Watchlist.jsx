import { useEffect, useState } from 'react';
import StockCard from '../components/watchlist/StockCard';
import { fetchWatchlist } from '../api';

const defaultTickers = ['AAPL', 'TSLA', 'NVDA', 'MSFT', 'GOOGL', 'AMZN'];

const Watchlist = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetchWatchlist(defaultTickers);
        setData(res || []);
      } catch (err) {
        console.error(err);
        setError('Could not load watchlist data.');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">AI-Powered Watchlist</h1>
        <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md transition-colors">
          + Add Stock
        </button>
      </div>

      {loading && <div className="text-gray-400">Loading watchlist...</div>}
      {error && <div className="text-red-400">{error}</div>}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {data.map((stock) => (
          <StockCard key={stock.ticker} name={stock.ticker} ticker={stock.ticker} price={stock.price} change={stock.change} percentage={`${stock.change_percent ?? ''}%`} isPositive={(stock.change ?? 0) >= 0} insight={stock.ai_insight ?? ''} />
        ))}
      </div>
    </div>
  );
};

export default Watchlist;
