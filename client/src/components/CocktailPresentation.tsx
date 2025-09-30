import React from 'react';
import Bubble from './Bubble';

interface CocktailPresentationProps {
    name: string;
    description: string;
    imageUrl: string;
    tags?: string[];
}

const CocktailPresentation: React.FC<CocktailPresentationProps> = ({
    name,
    description,
    imageUrl,
    tags,
}) => {
    return (
        <div className="flex w-full flex-row items-start gap-10">
            <div className="flex-shrink-0">
                <img
                    src={imageUrl}
                    alt={name}
                    className="h-64 w-64 rounded-lg object-cover shadow-md"
                />
            </div>
            <div className="flex h-full flex-1 flex-col justify-start">
                <h2 className="mb-2 text-3xl font-bold">{name}</h2>
                {tags && (
                    <div className="mb-2 flex flex-wrap gap-2">
                        {tags.map((tag, index) => (
                            <Bubble key={index} label={tag} />
                        ))}
                    </div>
                )}
                <hr className="my-2 mb-4 w-1/3 border-t border-[color:var(--color-contrast-muted)]" />
                <p className="text-sm text-[color:var(--color-contrast)]">
                    {description}
                </p>
            </div>
        </div>
    );
};

export default CocktailPresentation;
