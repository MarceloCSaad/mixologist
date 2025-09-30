import React from 'react';
import { THEME_MODES, type ThemeModes } from '../constants';
import { PageSessionThemeContextProvider } from './PageSessionThemeContext';
import { useSessionThemeModeContext } from './page-session-context';

export interface PageSessionProps extends React.HTMLAttributes<HTMLDivElement> {
    children?: React.ReactNode;
    removePadding?: boolean;
    invertedTheme?: boolean;
}

export type PageSessionContentProps = Omit<PageSessionProps, 'themeMode'>;

const getThemeModeClass = (themeMode: ThemeModes): string =>
    ({
        default: 'bg-[var(--color-main)] text-[var(--color-contrast)]',
        inverted: 'bg-[var(--color-contrast)] text-[var(--color-main)]',
    })[themeMode];

const PageSessionContent = ({
    children,
    removePadding = false,
    className = '',
    ...rest
}: PageSessionContentProps) => {
    const themeMode = useSessionThemeModeContext();
    return (
        <div
            className={`session ${className} ${getThemeModeClass(themeMode)} min-h-screen w-full`}
            {...rest}
        >
            <div
                className={`p-md ${removePadding ? 'py-0' : ''} mx-auto w-full max-w-[var(--max-content-width)]`}
            >
                {children}
            </div>
        </div>
    );
};

const PageSession = ({
    children,
    invertedTheme = false,
    ...rest
}: PageSessionProps) => {
    const themeMode = invertedTheme ? THEME_MODES[1] : THEME_MODES[0];
    return (
        <PageSessionThemeContextProvider themeMode={themeMode}>
            <PageSessionContent {...rest}>{children}</PageSessionContent>
        </PageSessionThemeContextProvider>
    );
};

export default PageSession;
