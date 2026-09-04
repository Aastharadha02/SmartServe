import { TextareaHTMLAttributes, FC, forwardRef } from 'react';

export interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  hint?: string;
  maxLength?: number;
  showCount?: boolean;
}

export const Textarea: FC<TextareaProps> = forwardRef<HTMLTextAreaElement, TextareaProps>(({
  label,
  error,
  hint,
  maxLength,
  showCount = false,
  className = '',
  id,
  value,
  disabled,
  ...props
}, ref) => {
  const textareaId = id || (label ? label.toLowerCase().replace(/\s+/g, '-') : undefined);
  const currentLength = typeof value === 'string' ? value.length : 0;

  return (
    <div className="flex w-full flex-col gap-1.5">
      <div className="flex items-center justify-between">
        {label && (
          <label htmlFor={textareaId} className="text-sm font-medium text-slate-700 select-none">
            {label}
          </label>
        )}
        {showCount && maxLength && (
          <span className="text-xs text-slate-400">
            {currentLength} / {maxLength}
          </span>
        )}
      </div>
      <textarea
        ref={ref}
        id={textareaId}
        maxLength={maxLength}
        value={value}
        disabled={disabled}
        className={`w-full rounded-xl border bg-white px-3.5 py-2.5 text-base text-slate-900 placeholder:text-slate-400 transition duration-150 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/30 focus:border-[#2563EB] disabled:bg-slate-50 disabled:text-slate-500 disabled:cursor-not-allowed ${
          error ? 'border-rose-500 focus:ring-rose-500/30 focus:border-rose-500' : 'border-slate-300'
        } ${className}`}
        {...props}
      />
      {error ? (
        <p className="text-xs font-medium text-rose-600 animate-fade-in">{error}</p>
      ) : hint ? (
        <p className="text-xs text-slate-500">{hint}</p>
      ) : null}
    </div>
  );
});

Textarea.displayName = 'Textarea';
