import { createContext, useContext } from 'react';
import { PALETTE, type PaletteType } from '../palette';
import type { PageSessionProps } from './PageSession';

export interface PageSessionContextValue
    extends Omit<PageSessionProps, 'children'> {
    palette: PaletteType;
}

export const PageSessionContext = createContext<PageSessionContextValue>({
    palette: PALETTE.default,
    contrastStyle: 'default',
});

export function usePageSession() {
    return useContext(PageSessionContext);
}
