import { LuSend } from 'react-icons/lu';

const AIAssistant = () => {
  return (
    <div className="h-full flex flex-col max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">AI Financial Assistant</h1>
        <button className="text-sm text-gray-400 hover:text-white">Clear Chat</button>
      </div>
      <div className="flex-1 bg-[#161B22] border border-gray-800 rounded-lg p-6">
        <div className="flex items-start gap-4">
            <div className="bg-purple-500/20 text-purple-400 p-2 rounded-full mt-1">
                <p className="font-bold text-lg">AI</p>
            </div>
            <div>
                <p className="font-semibold">FinanceAI Assistant</p>
                <p className="text-gray-400">Chat cleared! How can I help you with financial analysis today?</p>
            </div>
        </div>
      </div>
      <div className="mt-6">
        <div className="relative">
          <input
            type="text"
            placeholder="Ask me anything about finance..."
            className="w-full bg-[#161B22] border border-gray-700 rounded-lg pl-4 pr-12 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button className="absolute top-1/2 right-3 -translate-y-1/2 bg-blue-600 p-2 rounded-md hover:bg-blue-700">
            <LuSend size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default AIAssistant;