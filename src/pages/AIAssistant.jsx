import { LuSend } from 'react-icons/lu';
import { useState } from 'react';
import { askAssistant } from '../api';

// Very small, safe markdown -> HTML renderer (supports headings and unordered lists)
function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function renderSimpleMarkdownToHtml(md) {
  if (!md) return '';
  const lines = md.split(/\r?\n/);
  let html = '';
  let inList = false;

  for (let rawLine of lines) {
    const line = rawLine.trim();
    if (!line) {
      if (inList) { html += '</ul>'; inList = false; }
      html += '<br/>';
      continue;
    }

    // Headings: #, ##, ### (map to h1,h2,h3)
    const headingMatch = line.match(/^(#{1,3})\s+(.*)$/);
    if (headingMatch) {
      if (inList) { html += '</ul>'; inList = false; }
      const level = headingMatch[1].length;
  const content = escapeHtml(headingMatch[2]);
  html += `<h${level} class='text-white font-semibold'>${content}</h${level}>`;
      continue;
    }

    // Unordered list: start with -, *, +
    const listMatch = line.match(/^[-*+]\s+(.*)$/);
    if (listMatch) {
  const content = escapeHtml(listMatch[1]);
  if (!inList) { html += "<ul class='ml-4 list-disc text-gray-300'>"; inList = true; }
  html += `<li>${content}</li>`;
      continue;
    }

    // Default paragraph
    if (inList) { html += '</ul>'; inList = false; }
  html += `<p class='text-sm text-gray-200'>${escapeHtml(line)}</p>`;
  }

  if (inList) html += '</ul>';
  return html;
}

const AIAssistant = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { role: 'system', text: 'Chat cleared! How can I help you with financial analysis today?' }
  ]);
  const [loading, setLoading] = useState(false);

  async function handleSend() {
    if (!input.trim()) return;
    const userMsg = { role: 'user', text: input };
    setMessages((m) => [...m, userMsg]);
    setInput('');
    setLoading(true);
    try {
      const res = await askAssistant(input);
      const aiText = res?.answer || 'No response';
      setMessages((m) => [...m, { role: 'assistant', text: aiText }]);
    } catch (error) {
      console.error('askAssistant error', error);
      setMessages((m) => [...m, { role: 'assistant', text: 'Error contacting assistant.' }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="h-full flex flex-col max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">AI Financial Assistant</h1>
        <button className="text-sm text-gray-400 hover:text-white" onClick={() => setMessages([{ role: 'system', text: 'Chat cleared! How can I help you with financial analysis today?' }])}>Clear Chat</button>
      </div>

      <div className="flex-1 bg-[#161B22] border border-gray-800 rounded-lg p-6 overflow-auto">
        <div className="space-y-4">
          {messages.map((m, i) => (
            <div key={i} className={`flex items-start gap-4 ${m.role === 'assistant' ? 'text-gray-200' : 'text-gray-300'}`}>
              <div className={`p-2 rounded-full ${m.role === 'assistant' ? 'bg-purple-500/20 text-purple-400' : 'bg-gray-800 text-gray-200'}`}>
                <p className="font-bold text-sm">{m.role === 'assistant' ? 'AI' : m.role === 'system' ? 'SYS' : 'You'}</p>
              </div>
              <div className="prose prose-invert max-w-full">
                {m.role === 'assistant' ? (
                  <div dangerouslySetInnerHTML={{ __html: renderSimpleMarkdownToHtml(m.text) }} />
                ) : (
                  <p className="text-sm">{m.text}</p>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="mt-6">
        <div className="relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask me anything about finance..."
            className="w-full bg-[#161B22] border border-gray-700 rounded-lg pl-4 pr-12 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            onKeyDown={(e) => { if (e.key === 'Enter') handleSend(); }}
            disabled={loading}
          />
          <button disabled={loading} onClick={handleSend} className="absolute top-1/2 right-3 -translate-y-1/2 bg-blue-600 p-2 rounded-md hover:bg-blue-700 disabled:opacity-60">
            <LuSend size={20} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default AIAssistant;