import React from 'react';

export type SearchbarVariant = 'default' | 'nav';

export interface SearchbarProps
    extends React.InputHTMLAttributes<HTMLInputElement> {
    variant?: SearchbarVariant;
    onSearch?: (value: string) => void;
}

const variantClasses: Record<SearchbarVariant, string> = {
    default:
        'w-full max-w-md border border-gray-300 rounded px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500',
    nav: 'w-40 border border-gray-200 rounded px-2 py-1 text-sm focus:outline-none focus:ring-1 focus:ring-blue-400',
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
        <input
            type="search"
            value={value}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            className={`${variantClasses[variant]} ${className}`.trim()}
            placeholder="Search..."
            {...rest}
        />
    );
};

export default Searchbar;
