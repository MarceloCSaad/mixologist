import { createContext, useContext } from 'react';
import { THEME_MODES, type ThemeModes } from '../constants';

export type PageSessionThemeContextValue = ThemeModes;

export const PageSessionThemeContext = createContext<ThemeModes>(
    THEME_MODES[0],
);

export function useSessionThemeModeContext(): PageSessionThemeContextValue {
    return useContext(PageSessionThemeContext);
}
