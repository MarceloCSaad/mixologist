import type { ThemeModes } from '../constants';
import { PageSessionThemeContext } from './page-session-context';

export function PageSessionThemeContextProvider({
    children,
    themeMode,
}: {
    children: React.ReactNode;
    themeMode: ThemeModes;
}) {
    return (
        <PageSessionThemeContext.Provider value={themeMode}>
            {children}
        </PageSessionThemeContext.Provider>
    );
}
