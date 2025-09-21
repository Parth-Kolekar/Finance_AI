import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/layout/Sidebar';
import Header from './components/layout/Header';
import Dashboard from './pages/Dashboard';
import Watchlist from './pages/Watchlist';
import SentimentAnalysis from './pages/SentimentAnalysis';
import AIAssistant from './pages/AIAssistant';
import MarketNews from './pages/MarketNews';


function App() {
  return (
    <Router>
      <div className="flex bg-[#0D1117] text-gray-200 min-h-screen font-sans">
        <Sidebar />
        <div className="flex-1 flex flex-col">
          <Header />
          <main className="flex-1 p-6 lg:p-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/sentiment-analysis" element={<SentimentAnalysis />} />
              
              <Route path="/ai-assistant" element={<AIAssistant />} />
              <Route path="/watchlist" element={<Watchlist />} />
              <Route path="/market-news" element={<MarketNews />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
