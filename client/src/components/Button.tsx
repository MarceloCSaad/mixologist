import React from 'react';
import { usePageSession } from './Page/PageSessionContext';
import type { PaletteType } from './palette';

export type ButtonVariant = 'default' | 'primary' | 'secondary';

export interface ButtonProps
    extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: ButtonVariant;
    onClick?: () => void;
}

// Use palette from context for all color values
const getVariantClasses = (
    palette: PaletteType,
): Record<ButtonVariant, string> => ({
    default: `bg-[${palette.main}] text-[${palette.contrast}] border-[${palette.contrast}] border hover:bg-[${palette.contrast}] hover:text-[${palette.main}] active:bg-[${palette.contrast})/70`,
    primary: `bg-[${palette.contrast}] text-[${palette.main}] border-[${palette.contrast}] border hover:bg-[${palette.contrast}]/85 active:hover:bg-[${palette.contrast}]/70`,
    secondary: `bg-[${palette.mainMuted}] text-[${palette.contrast}] border-[${palette.mainMuted}] border hover:bg-[${palette.contrast}] hover:text-[${palette.main}] active:opacity-80`,
});

const Button: React.FC<ButtonProps> = ({
    variant = 'default',
    onClick,
    className = '',
    children,
    ...rest
}) => {
    const { palette } = usePageSession();
    const variantClasses = getVariantClasses(palette);
    return (
        <button
            type="button"
            className={`rounded px-4 pt-1.5 pb-2 font-medium transition-colors duration-150 ${variantClasses[variant]} ${className}`.trim()}
            onClick={onClick}
            {...rest}
        >
            {children}
        </button>
    );
};

export default Button;
