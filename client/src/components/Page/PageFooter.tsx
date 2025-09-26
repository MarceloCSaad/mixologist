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
            <div className="inner mx-auto flex w-full max-w-[var(--max-content-width)] items-center justify-center px-12 pt-8 pb-4">
                {props.children}
            </div>
        </footer>
    );
};

export default PageFooter;
