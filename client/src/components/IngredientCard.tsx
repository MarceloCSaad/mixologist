import React from 'react';
import { type Ingredient } from '../types/ingredient';
import type { ThemeModes } from './constants';
import { useSessionThemeModeContext } from './Page/page-session-context';

interface IngredientCardProps {
    ingredient: Ingredient;
}

const getThemeModeClass = (themeMode: ThemeModes): string =>
    ({
        default: `border-t-[var(--color-main-highlight)] shadow-md`,
        inverted: `border-t-[var(--color-contrast-highlight)] shadow-md`,
    })[themeMode];

const IngredientCard: React.FC<IngredientCardProps> = ({ ingredient }) => {
    const themeMode = useSessionThemeModeContext();
    return (
        <div
            className={`ingredient-card flex min-w-30 flex-col items-center justify-start overflow-hidden rounded-lg border-t-1 p-0 ${getThemeModeClass(themeMode)}`}
        >
            <div className="flex h-28 w-full items-center justify-center overflow-hidden bg-gray-100">
                {ingredient.imageUrl ? (
                    <img
                        src={ingredient.imageUrl}
                        alt={ingredient.name}
                        className="h-full w-full object-cover"
                    />
                ) : (
                    <span className="text-4xl">
                        {ingredient.imageUrl ? ingredient.imageUrl : '🥃'}
                    </span>
                )}
            </div>
            <div className="flex w-full flex-col items-center justify-center p-3">
                <span className="mb-1 text-center font-semibold">
                    {ingredient.name}
                </span>
                <span className="text-xs text-[var(--color-main-muted)]">
                    {ingredient.amount}
                </span>
            </div>
        </div>
    );
};

export default IngredientCard;
