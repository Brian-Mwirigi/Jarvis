'use client';

import { motion } from 'framer-motion';

export default function JarvisCore({ isProcessing }: { isProcessing: boolean }) {
    return (
        <div className="relative w-64 h-64 flex items-center justify-center">
            {/* Outer Ring */}
            <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                className="absolute inset-0 border-2 border-cyan-500/20 rounded-full border-t-cyan-400 border-r-transparent border-b-cyan-400 border-l-transparent"
            />

            {/* Middle Ring (Counter-rotating) */}
            <motion.div
                animate={{ rotate: -360 }}
                transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
                className="absolute inset-4 border border-cyan-400/30 rounded-full border-t-transparent border-r-cyan-300 border-b-transparent border-l-cyan-300"
            />

            {/* Inner Ring (Pulsing) */}
            <motion.div
                animate={{ scale: isProcessing ? [1, 1.1, 1] : 1 }}
                transition={{ duration: 2, repeat: Infinity }}
                className="absolute inset-8 border-4 border-cyan-500/10 rounded-full"
            />

            {/* Core Glow */}
            <motion.div
                animate={{
                    opacity: isProcessing ? [0.5, 1, 0.5] : 0.5,
                    scale: isProcessing ? [1, 1.2, 1] : 1,
                }}
                transition={{ duration: 1.5, repeat: Infinity }}
                className="absolute w-32 h-32 bg-cyan-500/20 rounded-full blur-xl"
            />

            {/* Central Reactor */}
            <div className="relative z-10 w-24 h-24 bg-cyan-950/50 rounded-full border border-cyan-400/50 flex items-center justify-center backdrop-blur-sm">
                <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
                    className="absolute inset-0 rounded-full border-t-2 border-cyan-200/80"
                />
                <div className="w-16 h-16 bg-cyan-400/10 rounded-full flex items-center justify-center">
                    <div className="w-2 h-2 bg-white rounded-full shadow-[0_0_15px_#fff]" />
                </div>
            </div>

            {/* Scanning Lines */}
            <div className="absolute inset-0 rounded-full overflow-hidden opacity-30 pointer-events-none">
                <motion.div
                    animate={{ top: ['0%', '100%'] }}
                    transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                    className="absolute left-0 right-0 h-1 bg-cyan-400/50 blur-sm"
                />
            </div>
        </div>
    );
}
