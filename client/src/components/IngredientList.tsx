import React from 'react';
import { usePageSession } from './Page/PageSessionContext';

export interface Ingredient {
    id: string;
    name: string;
    amount: string;
    icon?: React.ReactNode; // Optional: pass a React element for the icon
}

interface IngredientListProps {
    ingredients: Ingredient[];
}

const IngredientList: React.FC<IngredientListProps> = ({ ingredients }) => {
    const { palette } = usePageSession();
    return (
        <section className="ingredient-list">
            <h2 className="ingredient-list__title">Ingredients</h2>
            <ul className="ingredient-list__items">
                {ingredients.map((ingredient) => (
                    <li
                        key={ingredient.id}
                        className="ingredient-list__item flex items-center gap-3 py-2"
                    >
                        <span className="ingredient-list__icon text-xl">
                            {ingredient.icon ? ingredient.icon : '🥃'}
                        </span>
                        <span className="ingredient-list__name font-medium">
                            {ingredient.name}
                        </span>
                        <span
                            className="ingredient-list__amount ml-auto"
                            style={{ color: palette.contrastMuted }}
                        >
                            {ingredient.amount}
                        </span>
                    </li>
                ))}
            </ul>
        </section>
    );
};

export default IngredientList;
