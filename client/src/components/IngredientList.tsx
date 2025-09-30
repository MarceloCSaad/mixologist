import React from 'react';
import IngredientCard from './IngredientCard';
import { type Ingredient } from '../types/ingredient';

interface IngredientListProps {
    ingredients: Ingredient[];
}

const IngredientList: React.FC<IngredientListProps> = ({ ingredients }) => {
    return (
        <section className="flex w-full flex-col items-center">
            <h2 className="mb-4">Ingredients</h2>
            <div className="flex w-full flex-wrap items-center justify-center gap-10">
                {ingredients.map((ingredient) => (
                    <IngredientCard
                        key={ingredient.id}
                        ingredient={ingredient}
                    />
                ))}
            </div>
        </section>
    );
};

export default IngredientList;
