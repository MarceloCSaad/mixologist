import React, { useMemo } from 'react';
import { PageSessionContext } from './PageSessionContext';
import { PALETTE } from '../palette';

const paddingMap = {
    none: '0',
    xxs: '1',
    xs: '2',
    sm: '4',
    md: '8',
    lg: '16',
    xl: '40',
    xxl: '80',
};

export interface PageSessionProps extends React.HTMLAttributes<HTMLDivElement> {
    children?: React.ReactNode;
    innerPadding?: keyof typeof paddingMap | number;
    contrastStyle?: 'default' | 'inverted';
}

export interface PageSessionContentProps {
    children?: React.ReactNode;
}

export const PageSessionContent = ({ children }: PageSessionContentProps) => {
    const { innerPadding } = React.useContext(PageSessionContext);
    let paddingClass = 'p-md';
    if (typeof innerPadding === 'number') {
        paddingClass = `p-${innerPadding}`;
    } else if (innerPadding) {
        paddingClass = `p-${paddingMap[innerPadding]}`;
    }

    return (
        <div
            className={`${paddingClass} mx-auto w-full max-w-[var(--max-content-width)]`}
        >
            {children}
        </div>
    );
};

const PageSession = ({
    className = '',
    innerPadding = 'md',
    children,
    contrastStyle = 'default',
    ...rest
}: PageSessionProps) => {
    const contextValue = useMemo(
        () => ({
            palette: PALETTE[contrastStyle] || PALETTE.default,
            contrastStyle,
            innerPadding,
        }),
        [contrastStyle, innerPadding],
    );

    return (
        <PageSessionContext.Provider value={contextValue}>
            <div
                className={`session bg-[var(${contextValue.palette.main})] text-[var(${contextValue.palette.contrast})] ${className}`}
                {...rest}
            >
                <PageSessionContent>{children}</PageSessionContent>
            </div>
        </PageSessionContext.Provider>
    );
};

PageSession.Content = PageSessionContent;

export default PageSession;
