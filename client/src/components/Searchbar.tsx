import React from 'react';

export type SearchbarVariant = 'default' | 'nav';

export interface SearchbarProps
    extends React.InputHTMLAttributes<HTMLInputElement> {
    variant?: SearchbarVariant;
    onSearch?: (value: string) => void;
}

const getVariantClass = (variant: SearchbarVariant): string =>
    ({
        default: `w-full p-5 max-w-md border rounded-full py-2 focus:outline-none focus:ring-1 focus:ring-[var(--color-contrast)]`,
        nav: `w-1/2 border-0 rounded-full px-4 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[var(--color-contrast-muted)]`,
    })[variant];

const Searchbar = ({
    variant = 'default',
    onSearch,
    className = '',
    ...rest
}: SearchbarProps) => {
    const variantClass = getVariantClass(variant);
    const [value, setValue] = React.useState('');

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setValue(e.target.value);
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter' && onSearch) {
            onSearch(value);
        }
    };

    return (
        <>
            <style>{`
                input[type="search"]::-webkit-search-cancel-button {
                    filter: invert(0.5) sepia(1) saturate(5) hue-rotate(180deg);
                }
            `}</style>
            <input
                type="search"
                value={value}
                onChange={handleChange}
                onKeyDown={handleKeyDown}
                className={`${className} ${variantClass} border-[var(--color-contrast-muted)] bg-[var(--color-main-muted)] text-[var(--color-contrast)]`.trim()}
                aria-label="Search"
                placeholder="Search..."
                {...rest}
            />
        </>
    );
};

export default Searchbar;
