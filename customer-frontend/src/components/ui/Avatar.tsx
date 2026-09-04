import { FC } from 'react';

export interface AvatarProps {
  src?: string;
  name: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  variant?: 'circle' | 'square';
  className?: string;
}

export const Avatar: FC<AvatarProps> = ({
  src,
  name,
  size = 'md',
  variant = 'circle',
  className = '',
}) => {
  const getInitials = (str: string) => {
    const parts = str.trim().split(/\s+/);
    if (parts.length >= 2) {
      return `${parts[0]?.[0] || ''}${parts[1]?.[0] || ''}`.toUpperCase();
    }
    return (parts[0]?.[0] || 'U').toUpperCase();
  };

  const sizeStyles = {
    sm: 'h-8 w-8 text-xs',
    md: 'h-10 w-10 text-sm',
    lg: 'h-12 w-12 text-base',
    xl: 'h-16 w-16 text-xl',
  };

  const shapeStyles = variant === 'circle' ? 'rounded-full' : 'rounded-2xl';

  if (src) {
    return (
      <img
        src={src}
        alt={name}
        className={`object-cover border border-slate-200 ${sizeStyles[size]} ${shapeStyles} ${className}`}
      />
    );
  }

  return (
    <div
      className={`flex items-center justify-center font-bold bg-[#2563EB]/10 text-[#2563EB] border border-[#2563EB]/20 select-none ${sizeStyles[size]} ${shapeStyles} ${className}`}
    >
      {getInitials(name)}
    </div>
  );
};
