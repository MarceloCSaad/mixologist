const paddingMap = {
    none: '0',
    xxs: '1',
    xs: '2',
    s: '4',
    m: '8',
    l: '16',
    xl: '40',
    xxl: '80',
};

export interface PageSessionProps extends React.HTMLAttributes<HTMLDivElement> {
    light?: boolean;
    children?: React.ReactNode;
    innerPadding?: keyof typeof paddingMap | number;
}

const PageSession = (props: PageSessionProps) => {
    const { className = '', light = false, innerPadding, ...rest } = props;
    let paddingClass = 'p-md';
    if (typeof innerPadding === 'number') {
        paddingClass = `p-${innerPadding}`;
    } else if (innerPadding && innerPadding in paddingMap) {
        paddingClass = `p-${paddingMap[innerPadding]}`;
    }

    return (
        <div
            className={`session ${light ? 'light' : 'dark'} ${className}`}
            {...rest}
        >
            <div className={`session-inner ${paddingClass}`}>
                {props.children}
            </div>
        </div>
    );
};

export default PageSession;
