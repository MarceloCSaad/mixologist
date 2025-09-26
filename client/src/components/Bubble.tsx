import React, { useMemo } from 'react';
import { usePageSession } from './Page/PageSessionContext';

interface BubbleProps {
    label: string;
    className?: string;
    variant?: 'default' | 'highlight';
    withBorder?: boolean;
}

const Bubble: React.FC<BubbleProps> = ({
    label,
    className = '',
    variant = 'default',
    withBorder = false,
}) => {
    const { palette } = usePageSession();
    const { main, mainMuted, contrast, details } = palette;

    const tailwindClass = useMemo(() => {
        const styleMapper = {
            default: `bg-[var(${mainMuted})] text-[var(${contrast})] border-[var(${contrast})] hover:bg-[var(${contrast})] hover:text-[var(${main})]`,
            highlight: `bg-[var(${details})] text-[var(${contrast})] border-[var(${contrast})] hover:bg-[var(${contrast})] hover:text-[var(${main})]`,
        };
        let bubbleClass =
            className + ' ' + (styleMapper[variant] || styleMapper['default']);
        bubbleClass += withBorder ? ' border' : ' border-0';

        console.log('Palette in Bubble:', palette);
        return bubbleClass.trim();
    }, [
        mainMuted,
        contrast,
        main,
        details,
        className,
        variant,
        withBorder,
        palette,
    ]);

    return (
        <span
            className={`shadow-gray-350 mr-2 mb-0 inline-block cursor-default rounded-full px-2.5 py-1 pb-1.5 text-sm leading-3 font-semibold shadow-md ${tailwindClass}`}
        >
            <div>{label}</div>
        </span>
    );
};

export default Bubble;
