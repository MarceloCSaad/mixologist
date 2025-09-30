import React from 'react';
import Button from '../Button';
import Searchbar from '../Searchbar';
import { THEMES, type Themes } from '../constants';

export type GlobalNavProps = React.HTMLAttributes<HTMLDivElement>;

const GlobalNav = (props: GlobalNavProps) => {
    const [theme, setTheme] = React.useState<Themes>('black_and_white');
    React.useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme);
    }, [theme]);

    return (
        <nav
            {...props}
            className={`global-nav ${props.className || ''}`.trim()}
        >
            <div className="inner px-8 py-3">
                <div className="logo">Mixologist</div>
                <div className="links flex flex-1 items-center justify-evenly">
                    <Button
                        onClick={() =>
                            setTheme((theme) => {
                                const currentIndex = THEMES.indexOf(theme);
                                const nextIndex =
                                    (currentIndex + 1) % THEMES.length;
                                return THEMES[nextIndex];
                            })
                        }
                    >
                        {theme}
                    </Button>
                    <Button variant="primary">Primary</Button>
                    <Button variant="secondary">Secondary</Button>
                    <Searchbar variant="nav" />
                </div>
            </div>
        </nav>
    );
};

export default GlobalNav;
