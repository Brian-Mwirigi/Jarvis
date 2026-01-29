'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, Send, Terminal, Activity, Cpu, Wifi, WifiOff, Shield, Globe, Database, Zap } from 'lucide-react';
import clsx from 'clsx';
import ArcReactor from '@/components/ArcReactor';
import AudioVisualizer from '@/components/AudioVisualizer';
import { Howl } from 'howler';

// Sound Effects
const sounds = {
  startup: new Howl({ src: ['/sounds/startup.mp3'], volume: 0.5 }), // Placeholder paths
  hover: new Howl({ src: ['/sounds/hover.mp3'], volume: 0.1 }),
  click: new Howl({ src: ['/sounds/click.mp3'], volume: 0.2 }),
  message: new Howl({ src: ['/sounds/message.mp3'], volume: 0.3 }),
};

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
}

export default function Home() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isOnline, setIsOnline] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Play startup sound (simulated)
    // sounds.startup.play();

    const checkStatus = async () => {
      try {
        const res = await fetch('http://localhost:8000/');
        if (res.ok) setIsOnline(true);
        else setIsOnline(false);
      } catch {
        setIsOnline(false);
      }
    };
    checkStatus();
    const interval = setInterval(checkStatus, 10000);
    return () => clearInterval(interval);
  }, []);

  const sendMessage = async () => {
    if (!input.trim() || isProcessing) return;

    // sounds.click.play();

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: Date.now(),
    };

    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsProcessing(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg.content }),
      });

      if (!response.ok) throw new Error('Network response was not ok');

      const data = await response.json();

      const botMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        timestamp: Date.now(),
      };

      setMessages(prev => [...prev, botMsg]);
      // sounds.message.play();
    } catch (error) {
      console.error('Error:', error);
      const errorMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: "CONNECTION FAILED. BACKEND OFFLINE. PLEASE INITIALIZE NEURAL LINK (COLAB).",
        timestamp: Date.now(),
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <main className="flex h-screen w-full bg-black text-cyan-500 overflow-hidden relative selection:bg-cyan-500/30 font-mono">
      {/* 3D Background */}
      <div className="absolute inset-0 z-0">
        <ArcReactor />
      </div>

      {/* Overlay Gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/40 via-transparent to-black/80 z-0 pointer-events-none" />

      {/* Scanlines */}
      <div className="scanline z-50" />

      {/* Left HUD Panel */}
      <aside className="hidden lg:flex flex-col w-80 p-6 border-r border-cyan-900/30 bg-black/20 backdrop-blur-sm z-10 justify-between h-full">
        <div className="space-y-8">
          <div className="border-l-4 border-cyan-500 pl-6 py-2 relative overflow-hidden group">
            <div className="absolute inset-0 bg-cyan-500/10 translate-x-[-100%] group-hover:translate-x-0 transition-transform duration-500" />
            <h1 className="text-4xl font-black tracking-tighter text-white italic">JARVIS</h1>
            <p className="text-xs text-cyan-400 tracking-[0.3em] mt-1">MARK VII INTERFACE</p>
          </div>

          <div className="space-y-6">
            {/* CPU Module */}
            <div className="p-4 glass-panel rounded-xl border-l-2 border-l-cyan-500 relative overflow-hidden">
              <div className="absolute top-0 right-0 p-2 opacity-50"><Cpu size={16} /></div>
              <div className="text-xs font-bold mb-2 text-cyan-300 tracking-wider">PROCESSOR CORE</div>
              <div className="flex items-end gap-2 h-12 mb-2">
                {[...Array(8)].map((_, i) => (
                  <motion.div
                    key={i}
                    animate={{ height: ["20%", "80%", "40%"] }}
                    transition={{ duration: 0.5 + Math.random(), repeat: Infinity, repeatType: "reverse" }}
                    className="flex-1 bg-cyan-500/80 rounded-t-sm"
                  />
                ))}
              </div>
              <div className="text-right text-xs font-mono text-cyan-400">3.8 GHz // 12 CORES</div>
            </div>

            {/* Memory Module */}
            <div className="p-4 glass-panel rounded-xl border-l-2 border-l-blue-500 relative overflow-hidden">
              <div className="absolute top-0 right-0 p-2 opacity-50"><Database size={16} /></div>
              <div className="text-xs font-bold mb-2 text-blue-300 tracking-wider">MEMORY BANKS</div>
              <div className="grid grid-cols-4 gap-1 mb-2">
                {[...Array(16)].map((_, i) => (
                  <motion.div
                    key={i}
                    animate={{ opacity: [0.2, 1, 0.2] }}
                    transition={{ duration: 2, delay: i * 0.1, repeat: Infinity }}
                    className="h-2 bg-blue-500 rounded-sm"
                  />
                ))}
              </div>
              <div className="text-right text-xs font-mono text-blue-400">64 TB // OPTIMIZED</div>
            </div>

            {/* Network Module */}
            <div className="p-4 glass-panel rounded-xl border-l-2 border-l-purple-500 relative overflow-hidden">
              <div className="absolute top-0 right-0 p-2 opacity-50"><Globe size={16} /></div>
              <div className="text-xs font-bold mb-2 text-purple-300 tracking-wider">GLOBAL LINK</div>
              <div className="h-20 flex items-center justify-center border border-purple-500/20 rounded bg-black/40 relative">
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="w-16 h-16 border border-purple-500/30 rounded-full animate-[spin_10s_linear_infinite]" />
                  <div className="absolute w-12 h-12 border border-purple-400/50 rounded-full animate-[spin_5s_linear_infinite_reverse]" />
                </div>
                <span className="text-[10px] text-purple-300 z-10">CONNECTED</span>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-2 text-[10px] text-cyan-500/40 font-mono border-t border-cyan-900/30 pt-4">
          <div className="flex justify-between"><span>UPTIME</span><span>14:22:09</span></div>
          <div className="flex justify-between"><span>ENCRYPTION</span><span>QUANTUM-256</span></div>
          <div className="flex justify-between"><span>PROTOCOL</span><span>TCP/IP-V6</span></div>
        </div>
      </aside>

      {/* Center Area */}
      <div className="flex-1 flex flex-col relative z-0 h-full">
        {/* Top Bar */}
        <header className="flex items-center justify-between px-8 py-4 bg-gradient-to-b from-black/80 to-transparent z-20">
          <div className="flex items-center gap-6">
            <div className={clsx("flex items-center gap-2 px-4 py-1.5 rounded-sm border-l-2 text-xs font-bold transition-all uppercase tracking-wider",
              isOnline ? "border-cyan-500 bg-cyan-950/30 text-cyan-400" : "border-red-500 bg-red-950/30 text-red-400"
            )}>
              {isOnline ? <Wifi size={14} /> : <WifiOff size={14} />}
              {isOnline ? "Systems Online" : "Systems Offline"}
            </div>
            <div className="flex items-center gap-2 px-4 py-1.5 rounded-sm border-l-2 border-blue-500 bg-blue-950/30 text-blue-400 text-xs font-bold uppercase tracking-wider">
              <Shield size={14} />
              Defense Level 4
            </div>
          </div>
          <div className="flex items-center gap-4">
            <AudioVisualizer isActive={isProcessing} />
            <div className="text-cyan-500/50 text-xs font-mono">
              {new Date().toLocaleTimeString()}
            </div>
          </div>
        </header>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto p-8 space-y-8 relative z-10 scrollbar-hide">
          <AnimatePresence initial={false}>
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 20, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                className={clsx(
                  "flex w-full",
                  msg.role === 'user' ? "justify-end" : "justify-start"
                )}
              >
                <div className={clsx(
                  "max-w-[70%] relative group",
                  msg.role === 'user' ? "text-right" : "text-left"
                )}>
                  {/* Tech Decoration Lines */}
                  <div className={clsx(
                    "absolute top-0 w-4 h-[1px] bg-current opacity-50",
                    msg.role === 'user' ? "right-0 bg-cyan-400" : "left-0 bg-blue-400"
                  )} />

                  {/* Message Content */}
                  <div className={clsx(
                    "p-6 backdrop-blur-md border border-opacity-20 shadow-lg",
                    msg.role === 'user'
                      ? "bg-cyan-950/40 border-cyan-400 rounded-2xl rounded-tr-none"
                      : "bg-slate-950/60 border-blue-400 rounded-2xl rounded-tl-none"
                  )}>
                    <p className={clsx(
                      "text-xs font-bold mb-2 tracking-[0.2em] opacity-70",
                      msg.role === 'user' ? "text-cyan-300" : "text-blue-300"
                    )}>
                      {msg.role === 'user' ? 'USER_INPUT' : 'AI_RESPONSE'}
                    </p>
                    <p className={clsx(
                      "text-lg leading-relaxed font-light",
                      msg.role === 'user' ? "text-cyan-50" : "text-blue-50"
                    )}>
                      {msg.content}
                    </p>
                  </div>

                  {/* Timestamp */}
                  <div className="mt-1 text-[10px] font-mono opacity-30 uppercase">
                    T-{msg.timestamp} // {new Date(msg.timestamp).toLocaleTimeString()}
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-8 relative z-20">
          <div className="max-w-4xl mx-auto relative group">
            {/* Glowing border effect */}
            <div className="absolute -inset-0.5 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full opacity-30 group-hover:opacity-70 transition duration-1000 group-hover:duration-200 blur"></div>

            <form
              onSubmit={(e) => { e.preventDefault(); sendMessage(); }}
              className="relative flex items-center gap-4 bg-black/80 rounded-full px-8 py-5 border border-cyan-500/30 backdrop-blur-xl"
            >
              <div className="p-2 bg-cyan-500/10 rounded-full text-cyan-400">
                <Terminal size={20} />
              </div>

              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="INITIATE COMMAND SEQUENCE..."
                className="flex-1 bg-transparent border-none outline-none text-cyan-50 placeholder-cyan-800/50 font-mono tracking-wider text-lg"
                disabled={isProcessing}
                autoFocus
              />

              <button
                type="submit"
                disabled={!input.trim() || isProcessing}
                className="text-cyan-400 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-all transform hover:scale-110 active:scale-95 p-2"
              >
                <Send size={24} />
              </button>
            </form>
          </div>
        </div>
      </div>

      {/* Right Status Panel */}
      <aside className="hidden xl:flex flex-col w-20 border-l border-cyan-900/30 bg-black/20 backdrop-blur-sm z-10 items-center py-8 gap-8">
        <div className="flex flex-col items-center gap-2 text-cyan-500/50 hover:text-cyan-400 transition-colors cursor-pointer">
          <Zap size={20} />
          <span className="text-[10px] rotate-180 writing-mode-vertical">POWER</span>
        </div>
        <div className="w-full h-[1px] bg-cyan-900/50" />
        <div className="flex-1 flex flex-col items-center gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="w-1 h-16 bg-cyan-900/30 rounded-full overflow-hidden">
              <motion.div
                animate={{ height: ["30%", "80%", "40%"] }}
                transition={{ duration: 2 + i, repeat: Infinity }}
                className="w-full bg-cyan-500/50 bottom-0 absolute"
              />
            </div>
          ))}
        </div>
      </aside>
    </main>
  );
}
