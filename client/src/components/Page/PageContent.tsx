export interface PageContentProps extends React.HTMLAttributes<HTMLDivElement> {
    children?: React.ReactNode;
}

const PageContent = (props: PageContentProps) => {
    const { className = '', ...rest } = props;
    return (
        <div className={`page-content ${className}`} {...rest}>
            {props.children}
        </div>
    );
};

export default PageContent;
