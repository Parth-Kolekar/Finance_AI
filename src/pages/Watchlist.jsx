import { useEffect, useState } from 'react';
import StockCard from '../components/watchlist/StockCard';
import AddStockModal from '../components/watchlist/AddStockModal';
import { fetchWatchlist } from '../api';

const WATCHLIST_STORAGE_KEY = 'financeai_watchlist';
const WATCHLIST_CACHE_KEY = 'financeai_watchlist_cache';
const defaultTickers = ['AAPL', 'TSLA', 'NVDA', 'MSFT', 'GOOGL', 'AMZN'];

const getInitialTickers = () => {
  try {
    const storedTickers = sessionStorage.getItem(WATCHLIST_STORAGE_KEY);
    const parsed = storedTickers ? JSON.parse(storedTickers) : defaultTickers;
    return Array.isArray(parsed) && parsed.length ? parsed : defaultTickers;
  } catch (error) {
    console.error('Failed to parse watchlist from sessionStorage', error);
    return defaultTickers;
  }
};

const getCachedWatchlistData = (tickers) => {
  try {
    const key = `${WATCHLIST_CACHE_KEY}:${tickers.join(',')}`;
    const storedData = sessionStorage.getItem(key);
    if (!storedData) return null;

    const parsed = JSON.parse(storedData);
    return Array.isArray(parsed) ? parsed : null;
  } catch (error) {
    console.error('Failed to read cached watchlist data', error);
    return null;
  }
};

const setCachedWatchlistData = (tickers, data) => {
  try {
    const key = `${WATCHLIST_CACHE_KEY}:${tickers.join(',')}`;
    sessionStorage.setItem(key, JSON.stringify(data));
  } catch (error) {
    console.error('Failed to cache watchlist data', error);
  }
};

const Watchlist = () => {
  const [tickers, setTickers] = useState(getInitialTickers);
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Effect to fetch data when the tickers list changes
  useEffect(() => {
    sessionStorage.setItem(WATCHLIST_STORAGE_KEY, JSON.stringify(tickers));

    if (tickers.length === 0) {
      setData([]);
      return;
    }

    const cachedData = getCachedWatchlistData(tickers);
    if (cachedData) {
      setData(cachedData);
      setError(null);
      setLoading(false);
      return;
    }

    async function load() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetchWatchlist(tickers);
        const sortedData = tickers
            .map(ticker => res.find(d => d.ticker === ticker))
            .filter(Boolean);

        setData(sortedData || []);
        setCachedWatchlistData(tickers, sortedData || []);
      } catch (err) {
        console.error(err);
        setError('Could not load watchlist data. Check your API keys and network connection.');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [tickers]);

  const handleAddStock = (newTicker) => {
    if (!tickers.includes(newTicker)) {
      setTickers([...tickers, newTicker]);
    }
  };

  const handleRemoveStock = (tickerToRemove) => {
    setTickers(tickers.filter(ticker => ticker !== tickerToRemove));
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">AI-Powered Watchlist</h1>
        <button
          onClick={() => setIsModalOpen(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md transition-colors"
        >
          + Add Stock
        </button>
      </div>

      {loading && <div className="text-gray-400">Loading watchlist...</div>}
      {error && <div className="text-red-400 p-4 bg-red-500/10 rounded-md">{error}</div>}

      {!loading && !error && tickers.length === 0 && (
         <div className="text-center py-16 bg-[#161B22] border border-dashed border-gray-700 rounded-lg">
           <h3 className="text-lg font-medium text-gray-300">Your Watchlist is Empty</h3>
           <p className="text-gray-500 text-sm mt-2">Click the "+ Add Stock" button to monitor new assets.</p>
         </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {data.map((stock) => (
          <StockCard
            key={stock.ticker}
            name={stock.name || stock.ticker}
            ticker={stock.ticker}
            price={stock.price}
            change={stock.change}
            percentage={`${stock.change_percent?.toFixed(2) ?? '0.00'}%`}
            isPositive={(stock.change ?? 0) >= 0}
            insight={stock.ai_insight ?? 'No insight available.'}
            onRemove={handleRemoveStock}
          />
        ))}
      </div>

      <AddStockModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onAddStock={handleAddStock}
      />
    </div>
  );
};

export default Watchlist;