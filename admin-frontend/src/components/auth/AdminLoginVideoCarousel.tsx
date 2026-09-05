import React, { useState, useEffect, useRef, useCallback } from 'react';

interface VideoItem {
  id: string;
  videoSrc: string;
  posterSrc: string;
}

const VIDEOS: VideoItem[] = [
  {
    id: 'video-1',
    videoSrc: '/videos/cleaning.mp4',
    posterSrc: '/videos/cleaning-poster.jpg',
  },
  {
    id: 'video-2',
    videoSrc: '/videos/repair.mp4',
    posterSrc: '/videos/repair-poster.jpg',
  },
  {
    id: 'video-3',
    videoSrc: '/videos/home-service.mp4',
    posterSrc: '/videos/home-service-poster.jpg',
  },
];

const FALLBACK_TIMER_MS = 7500; // 7.5 seconds fallback timer

export const AdminLoginVideoCarousel: React.FC = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const videoRefs = useRef<(HTMLVideoElement | null)[]>([]);

  const advance = useCallback(() => {
    setCurrentIndex((prev) => (prev + 1) % VIDEOS.length);
  }, []);

  // Synchronize playback and reset active video
  useEffect(() => {
    videoRefs.current.forEach((video, idx) => {
      if (!video) return;
      if (idx === currentIndex) {
        video.currentTime = 0;
        video.play().catch(() => {
          // Autoplay policy fallback: muted video will play, poster shows if blocked
        });
      } else {
        video.pause();
      }
    });
  }, [currentIndex]);

  // Fallback timer: advances after FALLBACK_TIMER_MS if video hasn't ended
  useEffect(() => {
    const timer = setTimeout(() => {
      advance();
    }, FALLBACK_TIMER_MS);

    return () => clearTimeout(timer);
  }, [currentIndex, advance]);

  return (
    <div
      className="relative w-full h-full overflow-hidden bg-black select-none"
      role="region"
      aria-label="Service Video Carousel"
    >
      {/* ── Video Stack with Smooth Cross-Fade ── */}
      {VIDEOS.map((item, idx) => {
        const isActive = idx === currentIndex;
        return (
          <div
            key={item.id}
            className={`absolute inset-0 transition-opacity duration-700 ease-in-out ${
              isActive ? 'opacity-100 z-10' : 'opacity-0 z-0 pointer-events-none'
            }`}
          >
            <video
              ref={(el) => {
                videoRefs.current[idx] = el;
              }}
              src={item.videoSrc}
              poster={item.posterSrc}
              autoPlay={idx === 0}
              muted
              playsInline
              preload="auto"
              onEnded={() => {
                if (idx === currentIndex) {
                  advance();
                }
              }}
              className="w-full h-full object-cover"
            />
          </div>
        );
      })}

      {/* ── Minimal 1/3, 2/3, 3/3 Indicator (No extra overlays/captions) ── */}
      <div className="absolute bottom-5 right-5 z-20">
        <div
          data-testid="carousel-indicator"
          id="carousel-indicator"
          className="px-3 py-1 rounded-full bg-black/50 backdrop-blur-sm text-white/90 text-xs font-mono font-medium tracking-widest border border-white/10 shadow-sm"
        >
          {currentIndex + 1}/{VIDEOS.length}
        </div>
      </div>
    </div>
  );
};
