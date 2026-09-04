import { FC } from 'react';
import { Star } from 'lucide-react';

export interface RatingProps {
  value: number;
  max?: number;
  interactive?: boolean;
  onChange?: (rating: number) => void;
  size?: 'sm' | 'md' | 'lg';
  showValue?: boolean;
  className?: string;
}

export const Rating: FC<RatingProps> = ({
  value,
  max = 5,
  interactive = false,
  onChange,
  size = 'md',
  showValue = false,
  className = '',
}) => {
  const sizeStyles = {
    sm: 'h-4 w-4',
    md: 'h-5 w-5',
    lg: 'h-6 w-6',
  };

  const stars = Array.from({ length: max }, (_, index) => index + 1);

  return (
    <div className={`inline-flex items-center gap-1 ${className}`}>
      <div className="flex items-center gap-0.5">
        {stars.map((starVal) => {
          const isFilled = starVal <= Math.round(value);
          return (
            <button
              key={starVal}
              type="button"
              disabled={!interactive}
              onClick={() => interactive && onChange?.(starVal)}
              className={`transition-colors ${
                interactive ? 'cursor-pointer hover:scale-110' : 'cursor-default'
              }`}
            >
              <Star
                className={`${sizeStyles[size]} ${
                  isFilled
                    ? 'fill-amber-400 text-amber-400'
                    : 'fill-slate-100 text-slate-300'
                }`}
              />
            </button>
          );
        })}
      </div>
      {showValue && (
        <span className="ml-1 text-sm font-semibold text-slate-700">
          {value.toFixed(1)}
        </span>
      )}
    </div>
  );
};
