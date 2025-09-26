import React from 'react';
import Bubble from './Bubble';
import { usePageSession } from './Page/PageSessionContext';

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
    const { palette } = usePageSession();
    return (
        <div className="cocktail-presentation session-content flex w-full flex-row">
            <div className="cocktail-image flex-shrink-0">
                <img
                    src={imageUrl}
                    alt={name}
                    className="h-64 w-64 rounded-lg object-cover"
                />
            </div>
            <div className="ml-10 flex h-full flex-1 flex-col justify-start">
                <h2>{name}</h2>
                {tags && (
                    <div className="mb-2 flex flex-wrap">
                        {tags.map((tag, index) => (
                            <Bubble key={index} label={tag} />
                        ))}
                    </div>
                )}
                <hr
                    className="my-2 mb-4 w-1/3"
                    style={{ borderColor: palette.contrastMuted }}
                />
                <p className="muted" style={{ color: palette.contrastMuted }}>
                    {description}
                </p>
            </div>
        </div>
    );
};

export default CocktailPresentation;
