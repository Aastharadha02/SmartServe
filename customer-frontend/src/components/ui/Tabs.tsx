import { FC, ReactNode } from 'react';

export interface TabItem {
  id: string;
  label: string;
  icon?: ReactNode;
  count?: number;
}

export interface TabsProps {
  activeTab: string;
  onChange: (id: string) => void;
  items: TabItem[];
  className?: string;
}

export const Tabs: FC<TabsProps> = ({
  activeTab,
  onChange,
  items,
  className = '',
}) => {
  return (
    <div className={`flex border-b border-slate-200 gap-2 overflow-x-auto scrollbar-none ${className}`}>
      {items.map((item) => {
        const isActive = activeTab === item.id;
        return (
          <button
            key={item.id}
            onClick={() => onChange(item.id)}
            className={`flex items-center gap-2 border-b-2 px-4 py-3 text-sm font-semibold whitespace-nowrap transition-colors ${
              isActive
                ? 'border-[#2563EB] text-[#2563EB]'
                : 'border-transparent text-slate-600 hover:border-slate-300 hover:text-slate-900'
            }`}
            role="tab"
            aria-selected={isActive}
          >
            {item.icon && <span className="shrink-0">{item.icon}</span>}
            <span>{item.label}</span>
            {item.count !== undefined && (
              <span
                className={`rounded-full px-2 py-0.5 text-xs ${
                  isActive ? 'bg-[#EFF6FF] text-[#2563EB]' : 'bg-slate-100 text-slate-600'
                }`}
              >
                {item.count}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
};
