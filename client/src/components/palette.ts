export type PaletteType = {
    main: string;
    mainMuted: string;
    contrast: string;
    contrastMuted: string;
    details: string;
    highlight: string;
    alert: string;
};

export const PALETTE: Record<string, PaletteType> = {
    default: {
        main: '--color-main',
        mainMuted: '--color-main-muted',
        contrast: '--color-contrast',
        contrastMuted: '--color-contrast-muted',
        details: '--color-details',
        highlight: '--color-highlight',
        alert: '--color-alert',
    },
    inverted: {
        main: '--color-contrast',
        mainMuted: '--color-contrast-muted',
        contrast: '--color-main',
        contrastMuted: '--color-main-muted',
        details: '--color-details',
        highlight: '--color-highlight',
        alert: '--color-alert',
    },
};
