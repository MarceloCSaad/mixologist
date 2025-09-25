import React from 'react';
import Button from '../Button';
import Searchbar from '../Searchbar';

export type GlobalNavProps = React.HTMLAttributes<HTMLDivElement>;

const GlobalNav = (props: GlobalNavProps) => {
    const [theme, setTheme] = React.useState('light');
    React.useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme);
    }, [theme]);

    return (
        <nav
            {...props}
            className={`global-nav ${props.className || ''}`.trim()}
        >
            <div className="inner">
                <div className="logo">Mixologist</div>
                <div className="links flex flex-1 items-center justify-evenly">
                    <Button
                        onClick={() =>
                            setTheme((theme) => {
                                if (theme === 'light') {
                                    return 'dark';
                                } else if (theme === 'dark') {
                                    return 'sepia';
                                } else {
                                    return 'light';
                                }
                            })
                        }
                    >
                        {theme}
                    </Button>
                    <Searchbar variant="nav" />
                </div>
            </div>
        </nav>
    );
};

export default GlobalNav;
