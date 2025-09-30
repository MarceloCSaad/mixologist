import React, { useMemo } from 'react';
import { useSessionThemeModeContext } from './Page/page-session-context';
import { THEME_MODES } from './constants';

export type ButtonVariant = 'default' | 'primary' | 'secondary';

export interface ButtonProps
    extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: ButtonVariant;
    onClick?: () => void;
}

const getDarkVariantClass = (variant: ButtonVariant): string =>
    ({
        default: `border-[var(--color-main)] border hover:bg-[var(--color-contrast-muted)] active:text-[var(--color-contrast)] active:bg-[var(--color-main)]`,
        primary: `border-[var(--color-main)] border bg-[var(--color-main)] text-[var(--color-contrast)] hover:bg-[var(--color-main-highlight)] hover:text-[var(--color-contrast-highlight)] active:bg-[var(--color-contrast-muted)] active:text-[var(--color-main)]`,
        secondary: `border-[var(--color-contrast-muted)] border bg-[var(--color-contrast-muted)] text-[var(--color-main)] hover:bg-[var(--color-main-muted)] hover:text-[var(--color-contrast)] hover:border-[var(--color-main)] active:bg-[var(--color-main)] active:text-[var(--color-contrast-highlight)]`,
    })[variant];

const getLightVariantClass = (variant: ButtonVariant): string =>
    ({
        default: `border-[var(--color-contrast)] border hover:bg-[var(--color-contrast)] hover:text-[var(--color-main)] active:bg-[var(--color-contrast-highlight)] active:text-[var(--color-main-highlight)]`,
        primary: `bg-[var(--color-contrast)] text-[var(--color-main)] border-[var(--color-contrast)] border hover:bg-[var(--color-contrast-highlight)] hover:text-[var(--color-main-highlight)] active:hover:bg-[var(--color-main-muted)] active:text-[var(--color-contrast)]`,
        secondary: `bg-[var(--color-main-muted)] text-[var(--color-contrast)] border-[var(--color-main-muted)] border hover:bg-[var(--color-contrast-muted)] hover:text-[var(--color-main)] hover:border-[var(--color-contrast-muted)] active:bg-[var(--color-main-muted)] active:text-[var(--color-contrast-highlight)]`,
    })[variant];

const Button: React.FC<ButtonProps> = ({
    variant = 'default',
    onClick,
    className = '',
    children,
    ...rest
}) => {
    const themeMode = useSessionThemeModeContext();
    const variantClass = useMemo(
        () =>
            themeMode === THEME_MODES[0]
                ? getLightVariantClass(variant)
                : getDarkVariantClass(variant),
        [variant, themeMode],
    );
    console.log('Button variantClass:', variantClass);
    return (
        <button
            type="button"
            className={`${variantClass} ${className} rounded px-4 pt-1.5 pb-2 font-medium transition-colors duration-150`.trim()}
            onClick={onClick}
            {...rest}
        >
            {children}
        </button>
    );
};

export default Button;
