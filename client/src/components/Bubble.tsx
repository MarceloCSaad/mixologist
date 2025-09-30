import React, { useMemo } from 'react';
import type { ThemeModes } from './constants';
import { useSessionThemeModeContext } from './Page/page-session-context';

interface BubbleProps {
    label: string;
    className?: string;
    variant?: 'default' | 'highlight';
    withBorder?: boolean;
}

const getThemeModeClass = (themeMode: ThemeModes): string =>
    ({
        default: `bg-[var(--color-main-muted)] text-[var(--color-contrast)] border-[var(--color-contrast)] hover:bg-[var(--color-contrast)] hover:text-[var(--color-main)]`,
        inverted: `bg-[var(--color-contrast-muted)] text-[var(--color-main)] border-[var(--color-main)] hover:bg-[var(--color-main)] hover:text-[var(--color-contrast)]`,
    })[themeMode];

const Bubble: React.FC<BubbleProps> = ({
    label,
    className = '',
    withBorder = false,
}) => {
    const themeMode = useSessionThemeModeContext();
    const tailwindClass = useMemo(() => {
        return [
            className,
            getThemeModeClass(themeMode),
            withBorder ? ' border' : ' border-0',
        ]
            .join(' ')
            .trim();
    }, [className, themeMode, withBorder]);

    return (
        <span
            className={`shadow-black-650 mr-2 mb-0 inline-block cursor-default rounded-full px-2.5 py-1 pb-1.5 text-sm leading-3 font-semibold shadow-md ${tailwindClass}`}
        >
            <div>{label}</div>
        </span>
    );
};

export default Bubble;
