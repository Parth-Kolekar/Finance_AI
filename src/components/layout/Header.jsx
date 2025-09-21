import { HiOutlineMagnifyingGlass } from 'react-icons/hi2';

const Header = () => {
    return (
        <header className="flex items-center justify-between p-4 border-b border-gray-800 bg-[#161B22]">
            <div className="text-sm text-gray-400">
                <span>FinanceAI</span>
                <span className="mx-2">/</span>
                <span className="text-white">Dashboard</span>
            </div>
            <div className="flex items-center gap-4">
                <div className="relative">
                    <HiOutlineMagnifyingGlass className="absolute top-1/2 left-3 -translate-y-1/2 text-gray-400" />
                    <input
                        type="text"
                        placeholder="Ask AI anything about finance..."
                        className="bg-[#0D1117] border border-gray-700 rounded-md pl-9 pr-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>
                <div className="flex items-center gap-2">
                    <span className="relative flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                    </span>
                    <span className="text-sm text-green-400 font-medium">Markets Open</span>
                </div>
            </div>
        </header>
    );
}

export default Header;
