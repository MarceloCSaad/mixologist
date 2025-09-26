import PageContent from './PageContent';
import PageFooter from './PageFooter';
import PageHeader from './PageHeader';
import GlobalNav from '../Nav/GlobalNav';
import PageSession from './PageSession';

export interface PageProps extends React.HTMLAttributes<HTMLDivElement> {
    title?: string;
    children?: React.ReactNode;
    header?: React.ReactNode;
    footer?: React.ReactNode;
    withNav?: boolean;
}

const Page = ({
    title,
    withNav,
    children,
    header,
    footer,
    ...rest
}: PageProps) => {
    return (
        <div className="page" {...rest}>
            {withNav && <GlobalNav className="global-nav" />}
            {header ? header : title && <PageHeader title={title} />}
            {children}
            {footer ? footer : <PageFooter className="page-footer" />}
        </div>
    );
};

Page.header = PageHeader;
Page.content = PageContent;
Page.footer = PageFooter;
Page.session = PageSession;

export default Page;
