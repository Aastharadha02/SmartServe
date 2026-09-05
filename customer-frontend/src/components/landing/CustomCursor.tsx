import { FC, useEffect, useRef } from 'react';

/**
 * CustomCursor — a 12px dot that follows the mouse and tints sage-green
 * when hovering elements marked with [data-cursor-interactive].
 * Hidden on touch-only devices via CSS (@media hover:none).
 */
export const CustomCursor: FC = () => {
  const cursorRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = cursorRef.current;
    if (!el) return;

    let rafId: number;
    let mouseX = -100;
    let mouseY = -100;
    let currentX = -100;
    let currentY = -100;

    const onMove = (e: MouseEvent) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    };

    const onEnterInteractive = () => el.classList.add('is-hovering');
    const onLeaveInteractive = () => el.classList.remove('is-hovering');

    // Smooth lerp loop
    const loop = () => {
      currentX += (mouseX - currentX) * 0.12;
      currentY += (mouseY - currentY) * 0.12;
      el.style.transform = `translate(${currentX}px, ${currentY}px) translate(-50%, -50%)`;
      rafId = requestAnimationFrame(loop);
    };

    rafId = requestAnimationFrame(loop);
    window.addEventListener('mousemove', onMove, { passive: true });

    // Delegate hover state to any interactive element
    const attachToInteractive = () => {
      document.querySelectorAll('[data-cursor-interactive]').forEach((el) => {
        el.addEventListener('mouseenter', onEnterInteractive);
        el.addEventListener('mouseleave', onLeaveInteractive);
      });
    };

    // Observe DOM mutations so dynamically mounted elements are covered
    const observer = new MutationObserver(attachToInteractive);
    observer.observe(document.body, { childList: true, subtree: true });
    attachToInteractive();

    return () => {
      cancelAnimationFrame(rafId);
      window.removeEventListener('mousemove', onMove);
      observer.disconnect();
      document.querySelectorAll('[data-cursor-interactive]').forEach((el) => {
        el.removeEventListener('mouseenter', onEnterInteractive);
        el.removeEventListener('mouseleave', onLeaveInteractive);
      });
    };
  }, []);

  return <div ref={cursorRef} className="lp-cursor" aria-hidden="true" />;
};
