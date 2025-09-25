export interface PageFooterProps extends React.HTMLAttributes<HTMLDivElement> {
    children?: React.ReactNode;
    className?: string;
    style?: React.CSSProperties;
}

const PageFooter = (props: PageFooterProps) => {
    const { className, style, ...rest } = props;
    return (
        <footer
            className={`page-footer ${className || ''}`.trim()}
            style={style}
            {...rest}
        >
            <div className="inner">{props.children}</div>
        </footer>
    );
};

export default PageFooter;
