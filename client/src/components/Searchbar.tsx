import React from 'react';

export type SearchbarVariant = 'default' | 'nav';

export interface SearchbarProps
    extends React.InputHTMLAttributes<HTMLInputElement> {
    variant?: SearchbarVariant;
    onSearch?: (value: string) => void;
}

const variantClasses: Record<SearchbarVariant, string> = {
    default:
        'w-full p-5 max-w-md border border-[var(--color-muted-text)] bg-[var(--color-main-muted)] rounded-full py-2 focus:outline-none focus:ring-1 focus:ring-[var(--color-text)]',
    nav: 'w-1/2 border-0 bg-[var(--color-main-muted)] rounded-full px-4 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-[var(--color-muted-text)]',
};

const Searchbar: React.FC<SearchbarProps> = ({
    variant = 'default',
    onSearch,
    className = '',
    ...rest
}) => {
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
                className={`${variantClasses[variant]} ${className}`.trim()}
                placeholder="Search..."
                {...rest}
            />
        </>
    );
};

export default Searchbar;
