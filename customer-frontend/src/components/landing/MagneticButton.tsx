import { FC, ReactNode, useRef, useState } from 'react';
import { motion, useSpring, useTransform } from 'framer-motion';

interface MagneticButtonProps {
  children: ReactNode;
  className?: string;
  strength?: number; // default 0.35
  radius?: number;   // px radius for effect, default 80
}

/**
 * MagneticButton — wraps any element with a Framer Motion spring pull
 * toward the cursor when hovered within `radius` pixels.
 * Falls back gracefully: if motion is disabled, renders children as-is.
 */
export const MagneticButton: FC<MagneticButtonProps> = ({
  children,
  className,
  strength = 0.35,
  radius = 80,
}) => {
  const ref = useRef<HTMLDivElement>(null);
  const [isHovered, setIsHovered] = useState(false);

  const springConfig = { stiffness: 180, damping: 18, mass: 0.8 };
  const rawX = useSpring(0, springConfig);
  const rawY = useSpring(0, springConfig);

  const x = useTransform(rawX, (v) => v);
  const y = useTransform(rawY, (v) => v);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    const dx = e.clientX - cx;
    const dy = e.clientY - cy;
    const dist = Math.hypot(dx, dy);

    if (dist < radius) {
      rawX.set(dx * strength);
      rawY.set(dy * strength);
      setIsHovered(true);
    }
  };

  const handleMouseLeave = () => {
    rawX.set(0);
    rawY.set(0);
    setIsHovered(false);
  };

  return (
    <motion.div
      ref={ref}
      style={{ x, y, display: 'inline-block' }}
      className={className}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      data-hovered={isHovered}
      whileTap={{ scale: 0.97 }}
      transition={{ type: 'spring', stiffness: 300, damping: 20 }}
    >
      {children}
    </motion.div>
  );
};
