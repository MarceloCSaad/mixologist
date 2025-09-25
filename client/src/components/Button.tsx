import React from 'react';

export type ButtonVariant = 'default' | 'primary' | 'secondary';

export interface ButtonProps
    extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: ButtonVariant;
    onClick?: () => void;
}

const variantClasses: Record<ButtonVariant, string> = {
    default:
        'bg-[var(--color-main)] text-[var(--color-text)] border-[var(--color-text)] border hover:bg-[var(--color-text)] hover:text-[var(--color-main)] active:bg-[var(--color-text)]/70',
    primary:
        'bg-[var(--color-text)] text-[var(--color-main)] border-[var(--color-text)] border hover:bg-[var(--color-text)]/85 active:hover:bg-[var(--color-text)]/70',
    secondary:
        'bg-[var(--color-main-muted)] text-[var(--color-text)] border-[var(--color-main-muted)] border hover:bg-[var(--color-text)] hover:text-[var(--color-main)] active:opacity-80',
};

const Button: React.FC<ButtonProps> = ({
    variant = 'default',
    onClick,
    className = '',
    children,
    ...rest
}) => {
    return (
        <button
            type="button"
            className={`rounded px-4 py-2 font-medium transition-colors duration-150 ${variantClasses[variant]} ${className}`.trim()}
            onClick={onClick}
            {...rest}
        >
            {children}
        </button>
    );
};

export default Button;
