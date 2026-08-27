import React, { useEffect, useRef } from 'react';

// ═══════════════════════════════════════════════════════════════════════════
// High-Precision Geometry & Arc-Length Parameterization
// ═══════════════════════════════════════════════════════════════════════════

function bezier1D(t: number, p0: number, p1: number, p2: number, p3: number): number {
  const m = 1 - t;
  return m * m * m * p0 + 3 * m * m * t * p1 + 3 * m * t * t * p2 + t * t * t * p3;
}

function sampleBezierSegment(
  n: number,
  p0x: number, p0y: number,
  c1x: number, c1y: number,
  c2x: number, c2y: number,
  p3x: number, p3y: number
): [number, number][] {
  const pts: [number, number][] = [];
  for (let i = 0; i <= n; i++) {
    const t = i / n;
    pts.push([
      bezier1D(t, p0x, c1x, c2x, p3x),
      bezier1D(t, p0y, c1y, c2y, p3y)
    ]);
  }
  return pts;
}

function reparameterizeArcLength(rawPts: [number, number][], totalSamples: number): [number, number][] {
  if (rawPts.length < 2) return rawPts;

  const dists: number[] = [0];
  let totalLength = 0;
  for (let i = 1; i < rawPts.length; i++) {
    const dx = rawPts[i][0] - rawPts[i - 1][0];
    const dy = rawPts[i][1] - rawPts[i - 1][1];
    totalLength += Math.sqrt(dx * dx + dy * dy);
    dists.push(totalLength);
  }

  if (totalLength === 0) return rawPts;

  const uniformPts: [number, number][] = [];
  for (let i = 0; i <= totalSamples; i++) {
    const targetDist = (i / totalSamples) * totalLength;
    let segIdx = 0;
    while (segIdx < dists.length - 2 && dists[segIdx + 1] < targetDist) {
      segIdx++;
    }

    const segStartDist = dists[segIdx];
    const segEndDist = dists[segIdx + 1];
    const segLen = segEndDist - segStartDist;
    const factor = segLen > 0 ? (targetDist - segStartDist) / segLen : 0;

    const p0 = rawPts[segIdx];
    const p1 = rawPts[segIdx + 1];
    uniformPts.push([
      p0[0] + (p1[0] - p0[0]) * factor,
      p0[1] + (p1[1] - p0[1]) * factor
    ]);
  }

  return uniformPts;
}

/**
 * Geometric S path generation with 3 cubic curves:
 * Top lobe -> diagonal crossover -> bottom lobe
 */
function generateSPath(
  sx: number, sy: number,
  w: number, h: number,
  samplesPerSeg = 220
): [number, number][] {
  // 1. Top curve: start at top-right terminal, curve up & left, down left flank
  const seg1 = sampleBezierSegment(
    samplesPerSeg,
    sx + w * 0.82, sy + h * 0.18,  // Start top-right
    sx + w * 0.55, sy + h * 0.04,  // Control 1: pull up-right
    sx + w * 0.12, sy + h * 0.08,  // Control 2: pull up-left
    sx + w * 0.14, sy + h * 0.34   // End left crest
  );

  // 2. Middle crossover: from left crest, diagonal through center waist to right flank
  const seg2 = sampleBezierSegment(
    samplesPerSeg,
    sx + w * 0.14, sy + h * 0.34,
    sx + w * 0.16, sy + h * 0.50,  // Control 1: smooth waist entry
    sx + w * 0.84, sy + h * 0.50,  // Control 2: smooth waist exit
    sx + w * 0.86, sy + h * 0.66   // End right crest
  );

  // 3. Bottom curve: from right crest, down & left across bottom belly to bottom-left terminal
  const seg3 = sampleBezierSegment(
    samplesPerSeg,
    sx + w * 0.86, sy + h * 0.66,
    sx + w * 0.88, sy + h * 0.92,  // Control 1: pull down-right
    sx + w * 0.45, sy + h * 0.96,  // Control 2: pull down-left
    sx + w * 0.18, sy + h * 0.82   // End bottom-left terminal
  );

  const combined = [...seg1, ...seg2.slice(1), ...seg3.slice(1)];
  return reparameterizeArcLength(combined, 650);
}

/**
 * Sample square perimeter clockwise starting from top-left:
 * Top-left -> Top-right -> Bottom-right -> Bottom-left -> Top-left
 */
function generateSquarePath(
  x: number, y: number,
  size: number,
  totalSamples = 600
): [number, number][] {
  const pts: [number, number][] = [];
  const perimeter = size * 4;

  for (let i = 0; i <= totalSamples; i++) {
    const d = (i / totalSamples) * perimeter;
    let px: number, py: number;

    if (d <= size) {
      px = x + d;
      py = y;
    } else if (d <= size * 2) {
      px = x + size;
      py = y + (d - size);
    } else if (d <= size * 3) {
      px = x + size - (d - size * 2);
      py = y + size;
    } else {
      px = x;
      py = y + size - (d - size * 3);
    }

    pts.push([px, py]);
  }

  return pts;
}

function clamp01(elapsed: number, start: number, end: number): number {
  return Math.max(0, Math.min(1, (elapsed - start) / (end - start)));
}

function penEase(t: number): number {
  return t < 0.5
    ? 2 * t * t
    : 1 - Math.pow(-2 * t + 2, 2) / 2;
}

const easeInOutCubic = (t: number) =>
  t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

const easeOutQuad = (t: number) => 1 - (1 - t) * (1 - t);

/** Progressive point-by-point path rendering with sub-pixel interpolation */
function drawProgressivePath(
  ctx: CanvasRenderingContext2D,
  pts: [number, number][],
  progress: number
): [number, number] | null {
  if (pts.length < 2 || progress <= 0) return null;

  const totalSegments = pts.length - 1;
  const rawIdx = progress * totalSegments;
  const fullIndex = Math.min(totalSegments, Math.floor(rawIdx));
  const remainder = rawIdx - fullIndex;

  ctx.beginPath();
  ctx.moveTo(pts[0][0], pts[0][1]);

  for (let i = 1; i <= fullIndex; i++) {
    ctx.lineTo(pts[i][0], pts[i][1]);
  }

  let headX = pts[fullIndex][0];
  let headY = pts[fullIndex][1];

  if (fullIndex < totalSegments && remainder > 0) {
    headX += (pts[fullIndex + 1][0] - pts[fullIndex][0]) * remainder;
    headY += (pts[fullIndex + 1][1] - pts[fullIndex][1]) * remainder;
    ctx.lineTo(headX, headY);
  }

  ctx.stroke();
  return [headX, headY];
}

/** Draw a subtle, refined pen-tip dot at the stroke head */
function drawPenTip(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  radius = 3.0,
  color = '#2563EB'
): void {
  ctx.save();
  ctx.fillStyle = color;
  ctx.shadowColor = 'rgba(37, 99, 235, 0.30)';
  ctx.shadowBlur = 5;
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}

// ═══════════════════════════════════════════════════════════════════════════
// SplashScreen Component
// ═══════════════════════════════════════════════════════════════════════════

interface SplashScreenProps {
  onFinish?: () => void;
  durationMs?: number;
}

export const SplashScreen: React.FC<SplashScreenProps> = ({
  onFinish,
  durationMs = 5400,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const rafRef = useRef<number>(0);
  const startRef = useRef<number>(0);
  const doneRef = useRef(false);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || doneRef.current) return;

    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const VW = window.innerWidth;
    const VH = window.innerHeight;

    canvas.width = Math.round(VW * dpr);
    canvas.height = Math.round(VH * dpr);
    canvas.style.width = `${VW}px`;
    canvas.style.height = `${VH}px`;

    const ctx = canvas.getContext('2d')!;
    ctx.scale(dpr, dpr);

    // ── Exact Timeline Boundaries (seconds) ─────────────────────────────
    const T_S_START = 0.30;       // Pen begins S stroke
    const T_S_END = 1.80;         // S stroke complete (1.5s genuine drawing)
    const T_SQ_START = 2.00;      // Pause ends, square outline begins
    const T_SQ_END = 2.75;        // Square outline complete (0.75s drawing)
    const T_W_START = 2.95;       // Pause ends, wordmark begins
    const T_W_END = 4.00;         // Wordmark complete (1.05s reveal)
    const T_TAG_START = 4.00;     // Tagline & subtle architectural detail
    const T_TAG_END = 4.30;
    const T_HOLD_END = 4.50;      // Complete logo holds
    const T_TRANSITION_START = 4.50; // Smooth logo handoff + background crossfade
    const TOTAL_TIME = durationMs / 1000;

    // ── Responsive Layout & Typography ──────────────────────────────────
    const FONT_SIZE = Math.max(32, Math.min(78, VW * 0.040));
    ctx.font = `800 ${FONT_SIZE}px 'Inter', system-ui, -apple-system, sans-serif`;
    const smartW = ctx.measureText('Smart').width;
    const wordW = ctx.measureText('SmartServe').width;

    const BOX_SZ = Math.round(FONT_SIZE * 1.50);
    const GAP = Math.max(14, Math.round(FONT_SIZE * 0.36));
    const LOGO_W = BOX_SZ + GAP + wordW;

    const logoLeft = Math.round(VW / 2 - LOGO_W / 2);
    const logoTop = Math.round(VH / 2 - BOX_SZ / 2 - Math.max(26, Math.round(VH * 0.058)));

    const wordX = logoLeft + BOX_SZ + GAP;
    const wordBase = logoTop + Math.round(BOX_SZ * 0.74);

    // S Bounds inside the square box
    const S_PAD = Math.round(BOX_SZ * 0.18);
    const SW = BOX_SZ - S_PAD * 2;
    const SH = BOX_SZ - S_PAD * 2;
    const SX = logoLeft + S_PAD;
    const SY = logoTop + S_PAD;

    // Stroke widths
    const sStrokeWidth = Math.max(3.2, FONT_SIZE * 0.075);
    const sqStrokeWidth = Math.max(1.5, FONT_SIZE * 0.024);

    // Continuous point-by-point paths
    const sPath = generateSPath(SX, SY, SW, SH);
    const sqPath = generateSquarePath(logoLeft, logoTop, BOX_SZ);

    // Lower section positions
    const tagY = logoTop + BOX_SZ + Math.max(42, Math.round(FONT_SIZE * 0.96));
    const lineY = tagY + Math.max(22, Math.round(FONT_SIZE * 0.40));
    const lineWidth = Math.min(260, Math.max(120, LOGO_W * 0.48));

    // ── Login Target Position (for smooth logo handoff) ─────────────────
    // Target matches the login card's top S-badge location (48x48 centered horizontally)
    const targetLoginY = Math.round(VH / 2 - 208);
    const targetScale = Math.min(1.0, 48 / BOX_SZ);
    const startCenterX = logoLeft + BOX_SZ / 2;
    const startCenterY = logoTop + BOX_SZ / 2;
    const targetCenterX = Math.round(VW / 2);
    const targetCenterY = targetLoginY + 24;

    let eventDispatched = false;

    // ─────────────────────────────────────────────────────────────────────
    // Render Loop (60/120 fps Frame-by-Frame)
    // ─────────────────────────────────────────────────────────────────────
    function render(ts: number): void {
      if (doneRef.current) return;
      if (!startRef.current) startRef.current = ts;

      const elapsed = (ts - startRef.current) / 1000;

      // ── Transition Progress & Timing ──────────────────────────────────
      let bgFade = 0;
      let canvasAlpha = 1.0;
      let transEase = 0;
      let wordmarkAlpha = 1.0;
      let tagAlphaVal = 1.0;

      if (elapsed >= T_TRANSITION_START) {
        const transProg = clamp01(elapsed, T_TRANSITION_START, TOTAL_TIME);
        transEase = easeInOutCubic(transProg);
        bgFade = easeOutQuad(transProg);

        // Wordmark and tagline fade out during the initial transition phase
        tagAlphaVal = Math.max(0, 1.0 - clamp01(elapsed, 4.50, 4.75));
        wordmarkAlpha = Math.max(0, 1.0 - clamp01(elapsed, 4.50, 4.90));

        // Dispatch transition start event to trigger login card reveal beneath
        if (elapsed >= 4.65 && !eventDispatched) {
          eventDispatched = true;
          window.dispatchEvent(new CustomEvent('smartserve:splash-transition-start'));
        }

        // Smooth canvas crossfade out in final 450ms
        if (elapsed >= 4.95) {
          canvasAlpha = Math.max(0, 1.0 - clamp01(elapsed, 4.95, TOTAL_TIME));
        }
      }

      // ── Background Color: Crossfade #FAFAF8 -> #F8FAFC ────────────────
      ctx.save();
      ctx.globalAlpha = canvasAlpha;

      if (bgFade <= 0) {
        ctx.fillStyle = '#FAFAF8';
      } else {
        const r = Math.round(250 + (248 - 250) * bgFade);
        const g = Math.round(250 + (250 - 250) * bgFade);
        const b = Math.round(248 + (252 - 248) * bgFade);
        ctx.fillStyle = `rgb(${r},${g},${b})`;
      }
      ctx.fillRect(0, 0, VW, VH);

      // Subtle editorial warmth gradient during opening
      if (elapsed < 3.0) {
        const wAlpha = Math.max(0, 0.028 * Math.min(1, elapsed / 0.8));
        const rg = ctx.createRadialGradient(VW * 0.5, VH * 0.46, 0, VW * 0.5, VH * 0.46, VW * 0.4);
        rg.addColorStop(0, `rgba(244, 238, 226, ${wAlpha})`);
        rg.addColorStop(1, 'rgba(250,250,248,0)');
        ctx.fillStyle = rg;
        ctx.fillRect(0, 0, VW, VH);
      }

      // ── Current S-Box Position & Scale for Logo Handoff ───────────────
      const currCenterX = startCenterX + (targetCenterX - startCenterX) * transEase;
      const currCenterY = startCenterY + (targetCenterY - startCenterY) * transEase;
      const currScale = 1.0 + (targetScale - 1.0) * transEase;

      // ══════════════════════════════════════════════════════════════════
      // S-BOX (S Stroke + Square Outline) with Smooth Handoff Transform
      // ══════════════════════════════════════════════════════════════════
      ctx.save();
      ctx.translate(currCenterX, currCenterY);
      ctx.scale(currScale, currScale);
      ctx.translate(-startCenterX, -startCenterY);

      // STEP 1 — S HAND-DRAWING (0.30s – 1.80s)
      if (elapsed >= T_S_START) {
        const rawProgress = clamp01(elapsed, T_S_START, T_S_END);
        const sProg = elapsed >= T_S_END ? 1.0 : penEase(rawProgress);

        ctx.save();
        ctx.strokeStyle = '#0F172A';
        ctx.lineWidth = sStrokeWidth;
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';

        const headPos = drawProgressivePath(ctx, sPath, sProg);

        if (sProg < 0.999 && headPos) {
          drawPenTip(ctx, headPos[0], headPos[1], Math.max(2.4, sStrokeWidth * 0.60), '#2563EB');
        }
        ctx.restore();
      }

      // STEP 2 — SQUARE HAND-DRAWING (2.00s – 2.75s)
      if (elapsed >= T_SQ_START) {
        const rawProgress = clamp01(elapsed, T_SQ_START, T_SQ_END);
        const sqProg = elapsed >= T_SQ_END ? 1.0 : penEase(rawProgress);

        ctx.save();
        ctx.strokeStyle = '#0F172A';
        ctx.lineWidth = sqStrokeWidth;
        ctx.lineCap = 'butt';
        ctx.lineJoin = 'miter';

        const headPos = drawProgressivePath(ctx, sqPath, sqProg);

        if (sqProg < 0.999 && headPos) {
          drawPenTip(ctx, headPos[0], headPos[1], Math.max(2.0, sqStrokeWidth * 1.2), '#2563EB');
        }
        ctx.restore();
      }

      ctx.restore(); // Restore S-Box transform

      // ══════════════════════════════════════════════════════════════════
      // STEP 3 — SMARTSERVE WORDMARK REVEAL (2.95s – 4.00s)
      // ══════════════════════════════════════════════════════════════════
      if (elapsed >= T_W_START && wordmarkAlpha > 0.001) {
        const rawProgress = clamp01(elapsed, T_W_START, T_W_END);
        const wProg = elapsed >= T_W_END ? 1.0 : penEase(rawProgress);

        ctx.save();
        ctx.globalAlpha = wordmarkAlpha;
        ctx.beginPath();
        ctx.rect(
          wordX - 4,
          wordBase - FONT_SIZE * 1.15,
          wordW * wProg + 8,
          FONT_SIZE * 1.35
        );
        ctx.clip();

        ctx.font = `800 ${FONT_SIZE}px 'Inter', system-ui, -apple-system, sans-serif`;
        ctx.fillStyle = '#0F172A';
        ctx.fillText('Smart', wordX, wordBase);

        ctx.fillStyle = '#2563EB';
        ctx.fillText('Serve', wordX + smartW, wordBase);
        ctx.restore();
      }

      // ══════════════════════════════════════════════════════════════════
      // STEP 4 — MINIMAL EDITORIAL LOWER SECTION (4.00s – 4.30s)
      // ══════════════════════════════════════════════════════════════════
      if (elapsed >= T_TAG_START && tagAlphaVal > 0.001) {
        const tagProg = clamp01(elapsed, T_TAG_START, T_TAG_END);
        const tagAlpha = easeInOutCubic(tagProg) * tagAlphaVal;
        const yOffset = (1 - tagAlpha) * 5;

        // Clean, elegant tagline
        ctx.save();
        ctx.globalAlpha = tagAlpha;
        ctx.font = `400 ${Math.max(13, Math.min(16, FONT_SIZE * 0.23))}px 'Inter', system-ui, sans-serif`;
        ctx.fillStyle = '#64748B';
        ctx.textAlign = 'center';
        ctx.fillText('Professional services, made simple.', VW / 2, tagY + yOffset);

        // Thin architectural brand baseline
        ctx.strokeStyle = '#E2E8F0';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(VW / 2 - lineWidth / 2, lineY);
        ctx.lineTo(VW / 2 + lineWidth / 2, lineY);
        ctx.stroke();

        // Subtle center accent node on the baseline
        ctx.fillStyle = '#94A3B8';
        ctx.beginPath();
        ctx.arc(VW / 2, lineY, 1.8, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();
      }

      ctx.restore(); // Restore canvas alpha

      if (elapsed < TOTAL_TIME) {
        rafRef.current = requestAnimationFrame(render);
      } else {
        doneRef.current = true;
        onFinish?.();
      }
    }

    // Start render once fonts are loaded
    document.fonts.ready.then(() => {
      rafRef.current = requestAnimationFrame(render);
    });

    // Failsafe: ensure onFinish is called even if backgrounded
    const failsafeTimer = setTimeout(() => {
      if (!doneRef.current) {
        doneRef.current = true;
        onFinish?.();
      }
    }, durationMs + 800);

    return () => {
      cancelAnimationFrame(rafRef.current);
      clearTimeout(failsafeTimer);
    };
  }, [durationMs, onFinish]);

  return (
    <canvas
      ref={canvasRef}
      aria-hidden="true"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        zIndex: 9999,
        display: 'block',
        pointerEvents: 'none',
      }}
    />
  );
};

export default SplashScreen;
