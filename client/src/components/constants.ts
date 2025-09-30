export const THEMES = ['black_and_white', 'sepia'] as const;

export type Themes = (typeof THEMES)[number];

export const THEME_MODES = ['default', 'inverted'] as const;

export type ThemeModes = (typeof THEME_MODES)[number];
