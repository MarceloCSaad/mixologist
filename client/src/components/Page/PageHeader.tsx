export interface PageHeaderProps extends React.HTMLAttributes<HTMLDivElement> {
    children?: React.ReactNode;
    className?: string;
    style?: React.CSSProperties;
    title?: string;
}

const PageHeader = (props: PageHeaderProps) => {
    const { className, style } = props;
    return (
        <div className={`header ${className}`} style={style}>
            {props.title && <h1>{props.title}</h1>}
            {props.children}
        </div>
    );
};

export default PageHeader;
