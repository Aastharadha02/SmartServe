import { FC, HTMLAttributes, ElementType } from 'react';

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  padding?: 'none' | 'sm' | 'md' | 'lg';
  hoverable?: boolean;
  as?: ElementType;
}

export const Card: FC<CardProps> = ({
  padding = 'md',
  hoverable = false,
  as: Component = 'div',
  className = '',
  children,
  ...props
}) => {
  const paddingStyles = {
    none: 'p-0',
    sm: 'p-3 sm:p-4',
    md: 'p-5 sm:p-6',
    lg: 'p-6 sm:p-8',
  };

  const hoverStyles = hoverable
    ? 'transition-all duration-200 hover:shadow-md hover:-translate-y-0.5 cursor-pointer hover:border-slate-300'
    : '';

  return (
    <Component
      className={`rounded-2xl border border-slate-200/80 bg-white shadow-xs ${paddingStyles[padding]} ${hoverStyles} ${className}`}
      {...props}
    >
      {children}
    </Component>
  );
};
