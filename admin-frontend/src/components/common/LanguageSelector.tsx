import React from 'react';
import { useTranslation } from 'react-i18next';
import { Globe } from 'lucide-react';

interface LanguageOption {
  code: string;
  shortLabel: string;
  fullLabel: string;
}

const LANGUAGES: LanguageOption[] = [
  { code: 'en', shortLabel: 'EN', fullLabel: 'English' },
  { code: 'hi', shortLabel: 'हि', fullLabel: 'हिन्दी' },
  { code: 'gu', shortLabel: 'ગુ', fullLabel: 'ગુજરાતી' },
];

export const LanguageSelector: React.FC<{ compact?: boolean }> = ({ compact: _compact = false }) => {
  const { i18n, t } = useTranslation();
  const currentLang = i18n.language || 'en';

  const handleLanguageChange = (code: string) => {
    i18n.changeLanguage(code);
    if (typeof document !== 'undefined') {
      document.documentElement.lang = code;
    }
  };

  return (
    <div
      className="flex items-center gap-1 bg-white p-1 rounded-xl border border-[#E5DEC9] shadow-2xs"
      role="region"
      aria-label={t('common.select_language', { defaultValue: 'Select language' })}
    >
      <div className="px-1.5 text-[#1F2A1E]/50 flex items-center">
        <Globe className="w-3.5 h-3.5 text-[#2F5233]" />
      </div>
      <div className="flex items-center gap-1">
        {LANGUAGES.map((lang) => {
          const isSelected = currentLang.startsWith(lang.code);
          return (
            <button
              key={lang.code}
              onClick={() => handleLanguageChange(lang.code)}
              title={lang.fullLabel}
              aria-label={lang.fullLabel}
              aria-pressed={isSelected}
              className={`px-2 py-1 rounded-lg text-xs font-bold transition-all cursor-pointer ${
                isSelected
                  ? 'bg-[#2F5233] text-white shadow-2xs'
                  : 'text-[#1F2A1E]/70 hover:text-[#1F2A1E] hover:bg-[#F2EDE1]'
              }`}
            >
              {lang.shortLabel}
            </button>
          );
        })}
      </div>
    </div>
  );
};

