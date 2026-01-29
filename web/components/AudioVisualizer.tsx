'use client';

import { useEffect, useRef } from 'react';

export default function AudioVisualizer({ isActive }: { isActive: boolean }) {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const animationRef = useRef<number>();

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        const draw = () => {
            const width = canvas.width;
            const height = canvas.height;

            ctx.clearRect(0, 0, width, height);
            ctx.lineWidth = 2;
            ctx.strokeStyle = '#00f3ff';
            ctx.beginPath();

            const bufferLength = 50;
            const sliceWidth = width / bufferLength;
            let x = 0;

            for (let i = 0; i < bufferLength; i++) {
                // Simulate audio data if active, otherwise flatline
                const v = isActive
                    ? 0.5 + (Math.random() - 0.5) * 0.5
                    : 0.5 + (Math.random() - 0.5) * 0.05;

                const y = v * height;

                if (i === 0) {
                    ctx.moveTo(x, y);
                } else {
                    ctx.lineTo(x, y);
                }

                x += sliceWidth;
            }

            ctx.lineTo(canvas.width, canvas.height / 2);
            ctx.stroke();

            animationRef.current = requestAnimationFrame(draw);
        };

        draw();

        return () => {
            if (animationRef.current) {
                cancelAnimationFrame(animationRef.current);
            }
        };
    }, [isActive]);

    return (
        <canvas
            ref={canvasRef}
            width={300}
            height={50}
            className="w-full h-12 opacity-80"
        />
    );
}
