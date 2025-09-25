import { type Config } from 'prettier';

const config: Config = {
    trailingComma: 'all',
    tabWidth: 4,
    semi: true,
    singleQuote: true,
    plugins: ['prettier-plugin-tailwindcss'],
};

export default config;
