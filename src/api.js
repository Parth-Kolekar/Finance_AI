const BASE_URL = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000';

async function getJSON(path, opts = {}) {
  const res = await fetch(`${BASE_URL}${path}`, opts);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

export async function fetchNews() {
  return getJSON('/api/news');
}

export async function fetchDashboardOverview() {
  return getJSON('/api/dashboard/overview');
}

export async function fetchMarketTrends() {
  return getJSON('/api/market-trends');
}

export async function fetchWatchlist(tickers) {
  return getJSON('/api/watchlist', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ tickers })
  });
}

export async function askAssistant(query) {
  return getJSON('/api/ask', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query })
  });
}

export default { fetchNews, fetchWatchlist, askAssistant, fetchDashboardOverview, fetchMarketTrends };