import React from 'react';

interface BubbleProps {
    label: string;
    className?: string;
    variant?: 'default' | 'muted' | 'highlight';
    withBorder?: boolean;
}

const Bubble: React.FC<BubbleProps> = ({
    label,
    className = '',
    variant = 'default',
    withBorder = true,
}) => {
    const variantStyles = {
        default:
            'bg-[var(--color-main-muted)] text-[var(--color-text)] border-[var(--color-text)] hover:bg-[var(--color-text)] hover:text-[var(--color-main)]',
        muted: 'bg-[var(--color-main-muted)] text-[var(--color-muted-text)] border-[var(--color-muted)] hover:bg-[var(--color-muted-text)] hover:text-[var(--color-main)]',
        highlight:
            'bg-[var(--color-details)] text-[var(--color-text)] border-[var(--color-text)] hover:bg-[var(--color-text)] hover:text-[var(--color-main)]',
    };
    className += ' ' + (variantStyles[variant] || variantStyles['default']);
    className += withBorder ? ' border' : ' border-0';
    return (
        <span
            className={`mr-2 mb-0 inline-block cursor-default rounded-full px-3 py-1 pb-1.5 text-sm leading-3 font-semibold shadow-md ${className}`}
        >
            <div>{label}</div>
        </span>
    );
};

export default Bubble;
