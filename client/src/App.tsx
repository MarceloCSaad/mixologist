import CocktailPresentation from './components/CocktailPresentation';
import IngredientList from './components/IngredientList';
import Page from './components/Page/Page';

const App = () => {
    return (
        <Page title="Welcome to Mixologist" withNav>
            <Page.content>
                <Page.session>
                    <CocktailPresentation
                        name={'Caipirinha'}
                        description={
                            'A refreshing Brazilian cocktail made with cachaça, sugar, and lime.'
                        }
                        imageUrl={
                            'https://assets.epicurious.com/photos/579a2d8e437fcffe02f7230b/16:9/w_1920,c_limit/caipirinha-072816.jpg'
                        }
                        tags={['cachaça', 'lime', 'sugar', 'refreshing']}
                    />{' '}
                </Page.session>
                <Page.session light>
                    <IngredientList
                        ingredients={[
                            { id: '1', name: 'Cachaça', amount: '50ml' },
                            { id: '2', name: 'Sugar', amount: '2 tsp' },
                            { id: '3', name: 'Lime', amount: '1, juiced' },
                        ]}
                    />
                </Page.session>
                <Page.session light>
                    Lorem ipsum dolor sit amet consectetur, adipisicing elit. Id
                    sapiente voluptatibus quod ratione doloribus molestiae,
                    dolor blanditiis neque similique ut totam harum veniam esse
                    ex, fuga, numquam fugiat corrupti at?
                </Page.session>
                <Page.session>
                    <p>
                        Lorem ipsum dolor sit amet consectetur, adipisicing
                        elit. Id sapiente voluptatibus quod ratione doloribus
                        molestiae, dolor blanditiis neque similique ut totam
                        harum veniam esse ex, fuga, numquam fugiat corrupti at?
                    </p>
                </Page.session>
            </Page.content>
            <Page.footer className="footer">A footer</Page.footer>
        </Page>
    );
};

export default App;
