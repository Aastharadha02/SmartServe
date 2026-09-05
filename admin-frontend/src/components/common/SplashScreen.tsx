import React, { useEffect, useRef, useState } from 'react';

// ═══════════════════════════════════════════════════════════════════════════
// SmartServe Admin Splash Screen (~8-Second Cinematic Sequence)
// ═══════════════════════════════════════════════════════════════════════════
// Sequence Timeline:
// 0.0s – 0.5s: Background videos softly blurred with ivory overlay; center empty.
// 0.5s – 2.2s: GOLDEN BOX boundary is progressively sketched with real SVG stroke
//              (monoline draw from top-center -> corners -> sides -> closes).
//              A glowing golden stylus tip tracks the leading edge.
// 1.0s – 2.8s: S is progressively sketched with real SVG stroke (Forest Green + Gold).
//              A glowing golden stylus tip tracks the leading edge.
// 2.8s – 3.2s: S + golden box complete; gentle settling pause & subtle breath.
// 3.0s – 4.2s: Original SmartServe wordmark reveals smoothly ("Smart" + "Serve").
// 4.0s – 4.8s: "HOME SERVICES" subtitle appears between delicate golden rules.
// 4.5s – 7.4s: Loading / progress bar fills gradually from 0% to 100%.
// 7.4s – 8.0s: Smooth fade-out and seamless transition to existing Admin Login.
// Total Duration: ~8.0 seconds (Maximum: 10 seconds).
// ═══════════════════════════════════════════════════════════════════════════

interface SplashScreenProps {
  onFinish?: () => void;
  durationMs?: number;
}

const VIDEOS = [
  '/videos/cleaning.mp4',
  '/videos/repair.mp4',
  '/videos/home-service.mp4',
];

const easeInOutCubic = (t: number) =>
  t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

const easeOutCubic = (t: number) => 1 - Math.pow(1 - t, 3);

function clamp01(val: number): number {
  return Math.max(0, Math.min(1, val));
}

// Exact rounded rectangle path (width=84, height=84, rx=18, center at 48,48)
// Starts at top-center (48, 6) -> draws clockwise and closes back at (48, 6)
const BOX_PATH_D =
  'M 48 6 L 72 6 A 18 18 0 0 1 90 24 L 90 72 A 18 18 0 0 1 72 90 L 24 90 A 18 18 0 0 1 6 72 L 6 24 A 18 18 0 0 1 24 6 L 48 6 Z';

// Authentic SmartServe S curve
const S_PATH_D =
  'M 62 30 C 62 23, 34 22, 34 38 C 34 54, 62 48, 62 64 C 62 80, 34 78, 34 70';

export const SplashScreen: React.FC<SplashScreenProps> = ({
  onFinish,
  durationMs = 8000,
}) => {
  // Video carousel state
  const [activeVideoIndex, setActiveVideoIndex] = useState(0);
  const videoRefs = useRef<(HTMLVideoElement | null)[]>([]);

  // SVG Path References & Lengths
  const boxPathRef = useRef<SVGPathElement>(null);
  const sPathRef = useRef<SVGPathElement>(null);
  const [boxPathLength, setBoxPathLength] = useState<number>(305);
  const [sPathLength, setSPathLength] = useState<number>(186);

  // Animation Timeline States
  const [boxProgress, setBoxProgress] = useState<number>(0);
  const [boxPenPos, setBoxPenPos] = useState<{ x: number; y: number } | null>(null);
  const [boxPenOpacity, setBoxPenOpacity] = useState<number>(0);

  const [sProgress, setSProgress] = useState<number>(0);
  const [sPenPos, setSPenPos] = useState<{ x: number; y: number } | null>(null);
  const [sPenOpacity, setPenOpacity] = useState<number>(0);

  const [sScale, setSScale] = useState<number>(1);
  const [wordmarkProgress, setWordmarkProgress] = useState<number>(0);
  const [tagProgress, setTagProgress] = useState<number>(0);
  const [barProgress, setBarProgress] = useState<number>(0);
  const [splashOpacity, setSplashOpacity] = useState<number>(1);

  const rafRef = useRef<number>(0);
  const startRef = useRef<number>(0);
  const doneRef = useRef(false);

  // Initialize precise SVG path lengths once mounted
  useEffect(() => {
    if (boxPathRef.current) {
      try {
        const len = boxPathRef.current.getTotalLength();
        if (len > 0) setBoxPathLength(len);
      } catch {
        setBoxPathLength(305);
      }
    }
    if (sPathRef.current) {
      try {
        const len = sPathRef.current.getTotalLength();
        if (len > 0) setSPathLength(len);
      } catch {
        setSPathLength(186);
      }
    }
  }, []);

  // Continuous background video carousel crossfade (rotates every ~2.6s across 8s)
  useEffect(() => {
    const interval = setInterval(() => {
      setActiveVideoIndex((prev) => (prev + 1) % VIDEOS.length);
    }, 2600);
    return () => clearInterval(interval);
  }, []);

  // Safely trigger video play
  useEffect(() => {
    const currVideo = videoRefs.current[activeVideoIndex];
    if (currVideo) {
      currVideo.play().catch(() => {});
    }
  }, [activeVideoIndex]);

  // Main 8-Second Animation Timeline
  useEffect(() => {
    // Exact timeline boundaries (in seconds):
    const T_BOX_START = 0.50;      // 0.5s: Golden box sketching begins
    const T_BOX_END = 2.20;        // 2.2s: Golden box drawing completes (1.7s draw)
    const T_S_START = 1.00;        // 1.0s: S drawing begins
    const T_S_END = 2.80;          // 2.8s: S drawing completes (1.8s draw)
    const T_SETTLE_START = 2.80;   // 2.8s: S + Golden box subtle settling breath
    const T_SETTLE_END = 3.20;     // 3.2s: Settling ends
    const T_W_START = 3.00;        // 3.0s: SmartServe wordmark starts reveal
    const T_W_END = 4.20;          // 4.2s: SmartServe wordmark fully visible
    const T_TAG_START = 4.00;      // 4.0s: "HOME SERVICES" subtitle begins reveal
    const T_TAG_END = 4.80;        // 4.8s: "HOME SERVICES" fully visible
    const T_BAR_START = 4.50;      // 4.5s: Loading bar begins filling
    const T_BAR_END = 7.40;        // 7.4s: Loading bar reaches 100%
    const T_FADE_START = 7.40;     // 7.4s: Splash screen fade-out begins
    const TOTAL_SECONDS = durationMs / 1000; // 8.0s total

    function render(ts: number) {
      if (doneRef.current) return;
      if (!startRef.current) startRef.current = ts;

      const elapsed = (ts - startRef.current) / 1000;

      // 1. Sketched Golden Box Boundary (0.5s – 2.2s)
      if (elapsed < T_BOX_START) {
        setBoxProgress(0);
        setBoxPenOpacity(0);
      } else if (elapsed <= T_BOX_END) {
        const rawT = clamp01((elapsed - T_BOX_START) / (T_BOX_END - T_BOX_START));
        const easedT = easeInOutCubic(rawT);
        setBoxProgress(easedT);

        // Golden pen tip tracking the leading edge of the golden box
        if (boxPathRef.current) {
          try {
            const currentDist = easedT * boxPathLength;
            const pt = boxPathRef.current.getPointAtLength(currentDist);
            setBoxPenPos({ x: pt.x, y: pt.y });
            setBoxPenOpacity(1);
          } catch {}
        }
      } else {
        setBoxProgress(1);
        // Fade out box pen tip gently
        const fadeT = clamp01((elapsed - T_BOX_END) / 0.35);
        setBoxPenOpacity(Math.max(0, 1 - fadeT));
      }

      // 2. Sketched "S" Path Drawing (1.0s – 2.8s)
      if (elapsed < T_S_START) {
        setSProgress(0);
        setPenOpacity(0);
      } else if (elapsed <= T_S_END) {
        const rawT = clamp01((elapsed - T_S_START) / (T_S_END - T_S_START));
        const easedT = easeInOutCubic(rawT);
        setSProgress(easedT);

        // Golden stylus tip tracking leading edge of S stroke
        if (sPathRef.current) {
          try {
            const currentDist = easedT * sPathLength;
            const pt = sPathRef.current.getPointAtLength(currentDist);
            setSPenPos({ x: pt.x, y: pt.y });
            setPenOpacity(1);
          } catch {}
        }
      } else {
        setSProgress(1);
        // Fade out S pen tip gently
        const fadeT = clamp01((elapsed - T_S_END) / 0.35);
        setPenOpacity(Math.max(0, 1 - fadeT));
      }

      // 3. S + Golden Box Settling Pulse (2.8s – 3.2s)
      if (elapsed >= T_SETTLE_START && elapsed <= T_SETTLE_END) {
        const p = (elapsed - T_SETTLE_START) / (T_SETTLE_END - T_SETTLE_START);
        const pulse = 1 + Math.sin(p * Math.PI) * 0.025;
        setSScale(pulse);
      } else {
        setSScale(1);
      }

      // 4. SmartServe Wordmark Reveal (3.0s – 4.2s)
      if (elapsed < T_W_START) {
        setWordmarkProgress(0);
      } else if (elapsed <= T_W_END) {
        const rawT = clamp01((elapsed - T_W_START) / (T_W_END - T_W_START));
        setWordmarkProgress(easeOutCubic(rawT));
      } else {
        setWordmarkProgress(1);
      }

      // 5. "HOME SERVICES" Subtitle Reveal (4.0s – 4.8s)
      if (elapsed < T_TAG_START) {
        setTagProgress(0);
      } else if (elapsed <= T_TAG_END) {
        const rawT = clamp01((elapsed - T_TAG_START) / (T_TAG_END - T_TAG_START));
        setTagProgress(easeOutCubic(rawT));
      } else {
        setTagProgress(1);
      }

      // 6. Pill Loading / Progress Bar (4.5s – 7.4s)
      if (elapsed < T_BAR_START) {
        setBarProgress(0);
      } else if (elapsed <= T_BAR_END) {
        const rawT = clamp01((elapsed - T_BAR_START) / (T_BAR_END - T_BAR_START));
        setBarProgress(easeOutCubic(rawT));
      } else {
        setBarProgress(1);
      }

      // 7. Smooth Fade-Out (7.4s – 8.0s)
      if (elapsed >= T_FADE_START) {
        const fadeProg = clamp01((elapsed - T_FADE_START) / (TOTAL_SECONDS - T_FADE_START));
        setSplashOpacity(Math.max(0, 1 - fadeProg));
      }

      // Expose progress for verification
      try {
        (window as any).__splashElapsed = elapsed;
        (window as any).__splashBoxProgress = boxProgress;
        (window as any).__splashSProgress = sProgress;
      } catch {}

      // Continue or trigger complete
      if (elapsed < TOTAL_SECONDS) {
        rafRef.current = requestAnimationFrame(render);
      } else {
        doneRef.current = true;
        onFinish?.();
      }
    }

    rafRef.current = requestAnimationFrame(render);

    // Failsafe timer (guarantees transition around 8s)
    const failsafeTimer = setTimeout(() => {
      if (!doneRef.current) {
        doneRef.current = true;
        onFinish?.();
      }
    }, durationMs + 500);

    return () => {
      cancelAnimationFrame(rafRef.current);
      clearTimeout(failsafeTimer);
    };
  }, [durationMs, onFinish, boxPathLength, sPathLength]);

  // Stroke Dash Calculations for real SVG stroke-drawing
  const boxDashoffset = boxPathLength * (1 - boxProgress);
  const sDashoffset = sPathLength * (1 - sProgress);

  return (
    <div
      className="fixed inset-0 z-[9999] flex items-center justify-center overflow-hidden select-none transition-opacity duration-300"
      style={{ opacity: splashOpacity }}
      aria-label="SmartServe Admin Splash Screen"
    >
      {/* Skip Intro Button */}
      <button
        onClick={() => {
          doneRef.current = true;
          onFinish?.();
        }}
        className="absolute top-6 right-6 z-50 px-4 py-2 rounded-full bg-black/50 hover:bg-black/80 text-white/90 hover:text-white text-xs font-bold backdrop-blur-md border border-white/20 transition-all cursor-pointer shadow-lg"
        aria-label="Skip Intro"
      >
        Skip Intro ✕
      </button>

      {/* ── 1. Full-Screen Background Video Carousel ── */}
      <div className="absolute inset-0 w-full h-full overflow-hidden pointer-events-none bg-[#1F2A1E]">
        {VIDEOS.map((videoSrc, idx) => (
          <video
            key={videoSrc}
            ref={(el) => {
              videoRefs.current[idx] = el;
            }}
            src={videoSrc}
            muted
            playsInline
            loop
            preload="auto"
            className={`absolute inset-0 w-full h-full object-cover transition-opacity duration-1000 ease-in-out ${
              activeVideoIndex === idx ? 'opacity-100' : 'opacity-0'
            }`}
            style={{
              filter: 'blur(10px) brightness(0.92)',
              transform: 'scale(1.08)',
            }}
          />
        ))}

        {/* Soft Ivory / Japandi Translucent Overlay */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            backgroundColor: 'rgba(250, 247, 240, 0.48)',
            backgroundImage:
              'radial-gradient(ellipse at center, rgba(250, 247, 240, 0.38) 0%, rgba(250, 247, 240, 0.65) 100%)',
          }}
        />
      </div>

      {/* ── 2. Central Identity Lockup ── */}
      <div className="relative z-10 flex flex-col items-center justify-center px-4 max-w-lg w-full text-center">
        
        {/* ── S & Sketched Golden Box Boundary Container ── */}
        <div
          className="relative w-36 h-36 md:w-44 md:h-44 flex items-center justify-center mb-6 transition-transform duration-200 ease-out"
          style={{ transform: `scale(${sScale})` }}
        >
          {/* Subtle Ambient Gold Glow behind S */}
          <div
            className="absolute inset-0 rounded-3xl bg-[#C9A15A]/15 blur-2xl transition-opacity duration-700 pointer-events-none"
            style={{ opacity: sProgress > 0.1 || boxProgress > 0.1 ? 0.8 : 0 }}
          />

          <svg
            className="relative z-10 w-full h-full"
            viewBox="0 0 96 96"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            {/* Defs: Forest Green and Warm Gold Gradient */}
            <defs>
              <linearGradient id="sStrokeGradient" x1="62" y1="23" x2="34" y2="80" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stopColor="#C9A15A" />
                <stop offset="18%" stopColor="#2F5233" />
                <stop offset="82%" stopColor="#2F5233" />
                <stop offset="100%" stopColor="#C9A15A" />
              </linearGradient>
            </defs>

            {/* ── 1. SKETCHED GOLDEN BOX BOUNDARY (Real SVG Path Stroke-Draw) ── */}
            <path
              ref={boxPathRef}
              d={BOX_PATH_D}
              stroke="#C9A15A"
              strokeWidth={1.85}
              strokeLinecap="round"
              strokeLinejoin="round"
              fill="none"
              style={{
                strokeDasharray: `${boxPathLength} ${boxPathLength}`,
                strokeDashoffset: boxDashoffset,
                strokeOpacity: boxProgress > 0 ? 0.95 : 0,
                filter: boxProgress > 0.05 ? 'drop-shadow(0 2px 8px rgba(201,161,90,0.22))' : 'none',
                transition: 'none',
              }}
            />

            {/* Glowing Golden Nib tracking the leading edge of the Golden Box */}
            {boxPenOpacity > 0 && boxPenPos && (
              <g style={{ opacity: boxPenOpacity }}>
                <circle cx={boxPenPos.x} cy={boxPenPos.y} r={7.5} fill="#C9A15A" fillOpacity={0.4} />
                <circle cx={boxPenPos.x} cy={boxPenPos.y} r={3.5} fill="#C9A15A" />
                <circle cx={boxPenPos.x} cy={boxPenPos.y} r={1.5} fill="#FFFFFF" />
              </g>
            )}

            {/* ── 2. SKETCHED "S" PATH (Real SVG Stroke-Draw) ── */}
            <path
              ref={sPathRef}
              d={S_PATH_D}
              stroke="url(#sStrokeGradient)"
              strokeWidth={6.8}
              strokeLinecap="round"
              strokeLinejoin="round"
              fill="none"
              style={{
                strokeDasharray: `${sPathLength} ${sPathLength}`,
                strokeDashoffset: sDashoffset,
                strokeOpacity: sProgress > 0 ? 1 : 0,
                transition: 'none',
              }}
            />

            {/* Glowing Golden Nib tracking leading edge of S */}
            {sPenOpacity > 0 && sPenPos && (
              <g style={{ opacity: sPenOpacity }}>
                <circle cx={sPenPos.x} cy={sPenPos.y} r={9} fill="#C9A15A" fillOpacity={0.4} />
                <circle cx={sPenPos.x} cy={sPenPos.y} r={4.2} fill="#C9A15A" />
                <circle cx={sPenPos.x} cy={sPenPos.y} r={1.8} fill="#FFFFFF" />
              </g>
            )}
          </svg>
        </div>

        {/* ── 3. Brand Typography Reveal (Appears at 3.0s – 4.2s) ── */}
        <div
          className="transition-all duration-500 ease-out"
          style={{
            opacity: wordmarkProgress,
            transform: `translateY(${(1 - wordmarkProgress) * 14}px)`,
          }}
        >
          {/* Authentic Wordmark: "Smart" (Forest Green) + "Serve" (Warm Gold) */}
          <h1 className="font-serif-display text-5xl md:text-6xl tracking-tight leading-none text-[#2F5233] drop-shadow-[0_2px_8px_rgba(250,247,240,0.8)]">
            <span>Smart</span>
            <span className="text-[#C9A15A] ml-1">Serve</span>
          </h1>

          {/* Subtitle (Appears at 4.0s – 4.8s): "HOME SERVICES" */}
          <div
            className="mt-3 flex items-center justify-center gap-3 transition-all duration-500 ease-out"
            style={{
              opacity: tagProgress,
              transform: `translateY(${(1 - tagProgress) * 8}px)`,
            }}
          >
            <span className="h-[1px] w-8 bg-[#C9A15A]/60" />
            <p className="font-jakarta text-xs md:text-sm font-bold tracking-[0.35em] text-[#1F2A1E] uppercase drop-shadow-xs">
              HOME SERVICES
            </p>
            <span className="h-[1px] w-8 bg-[#C9A15A]/60" />
          </div>
        </div>

        {/* ── 4. Minimalist Pill Loading / Progress Bar (Progresses 4.5s – 7.4s) ── */}
        <div
          className="mt-8 flex flex-col items-center transition-opacity duration-400"
          style={{ opacity: tagProgress > 0.3 ? 1 : 0 }}
        >
          {/* Pill Track */}
          <div className="w-52 md:w-60 h-1.5 rounded-full bg-[#E5DEC9] overflow-hidden shadow-inner p-[1px]">
            {/* Fill Bar */}
            <div
              className="h-full rounded-full bg-gradient-to-r from-[#2F5233] via-[#3D6B42] to-[#C9A15A] transition-[width] duration-75 ease-linear"
              style={{ width: `${Math.round(barProgress * 100)}%` }}
            />
          </div>

          {/* Status Micro-label */}
          <span className="font-jakarta mt-2.5 text-[10px] md:text-[11px] font-semibold tracking-widest text-[#1F2A1E]/80 uppercase">
            {barProgress < 0.35
              ? 'Initializing'
              : barProgress < 0.85
              ? 'Curating Sanctuary'
              : 'Welcome'}
          </span>
        </div>
      </div>
    </div>
  );
};

export default SplashScreen;
