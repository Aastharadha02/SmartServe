import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { SupportedLanguage, translations, Translations } from './translations';

interface LanguageContextType {
  language: SupportedLanguage;
  setLanguage: (lang: SupportedLanguage) => Promise<void>;
  t: (key: keyof Translations) => string;
  isReady: boolean;
}

const LANGUAGE_STORAGE_KEY = 'smartserve_app_language';

const LanguageContext = createContext<LanguageContextType>({
  language: 'en',
  setLanguage: async () => {},
  t: (key) => translations.en[key] || String(key),
  isReady: false,
});

export const LanguageProvider = ({ children }: { children: ReactNode }) => {
  const [language, setLanguageState] = useState<SupportedLanguage>('en');
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const stored = await AsyncStorage.getItem(LANGUAGE_STORAGE_KEY);
        if (stored === 'en' || stored === 'hi' || stored === 'gu') {
          setLanguageState(stored);
        }
      } catch {
        // Fallback to default 'en'
      } finally {
        setIsReady(true);
      }
    })();
  }, []);

  const setLanguage = async (newLang: SupportedLanguage) => {
    try {
      setLanguageState(newLang);
      await AsyncStorage.setItem(LANGUAGE_STORAGE_KEY, newLang);
    } catch (e) {
      console.warn('Failed to persist language preference', e);
    }
  };

  const t = (key: keyof Translations): string => {
    const langDict = translations[language] || translations.en;
    return langDict[key] || translations.en[key] || String(key);
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t, isReady }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => useContext(LanguageContext);

