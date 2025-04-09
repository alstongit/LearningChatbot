import { useState } from "react";
import axios from "axios";
import { X } from "lucide-react"; // You can also use any icon lib or emoji

const ChatBox = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [open, setOpen] = useState(false);

  const sendQuery = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await axios.get("http://localhost:8000/chat", {
        params: { query: input },
      });

      const botReply = {
        sender: "bot",
        text: response.data.response || "Sorry, I couldn’t find anything.",
      };

      setMessages((prev) => [...prev, botReply]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Error talking to backend." },
      ]);
    }

    setInput("");
  };

  return (
    <div>
      {/* Floating Chat Icon */}
      {!open && (
        <button
          onClick={() => setOpen(true)}
          className="fixed bottom-6 right-6 bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700"
        >
          💬
        </button>
      )}

      {/* Chat Window */}
      {open && (
        <div className="fixed bottom-6 right-6 w-80 h-[450px] bg-white border rounded-xl shadow-xl flex flex-col">
          {/* Header */}
          <div className="bg-blue-600 text-white px-4 py-2 flex justify-between items-center rounded-t-xl">
            <h2 className="text-lg font-semibold">🏠 Chatbot</h2>
            <button onClick={() => setOpen(false)}>
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-3 bg-gray-50">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`my-2 ${
                  msg.sender === "user" ? "text-right" : "text-left"
                }`}
              >
                <span
                  className={`inline-block p-2 rounded-lg ${
                    msg.sender === "user"
                      ? "bg-blue-500 text-white"
                      : "bg-gray-200 text-black"
                  }`}
                >
                  {msg.text}
                </span>
              </div>
            ))}
          </div>

          {/* Input */}
          <div className="p-2 border-t flex gap-2">
            <input
              type="text"
              value={input}
              placeholder="Ask something..."
              className="flex-1 border p-2 rounded text-sm"
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendQuery()}
            />
            <button
              className="bg-blue-600 text-white px-3 rounded"
              onClick={sendQuery}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatBox;
