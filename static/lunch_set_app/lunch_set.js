const { useState, useEffect } = React;
// const { NavLink } = ReactRouterDOM;

function DishItem({ item, checked }) {
    return (
        <div className="lunch_set_dish">
            <div className="lunch_set_dish_info">
                <input 
                    type="radio" 
                    className="input-radio" 
                    name={item.dish_type} 
                    value={item.dish.slug} 
                    defaultChecked={checked} 
                />
                <div className="label">{item.dish.title}</div>
            </div>
            { item.dish.picture && 
                <div className="lunch_set_dish_image_box">
                    <img src={item.dish.picture} alt={item.dish.title} className="dish_image" /> 
                </div>
            }
        </div>
    );
}

function LunchSetCard({ lunchSet }) {
    return (
        <div className="lunch-set">
            <h2>Обед на {lunchSet.date}</h2>
            {lunchSet.comment && <p>{lunchSet.comment}</p>}
            <div className="col-12 sidebar border blog-sidebar">
                <div className="block-form">
                    <div className="panel">
						<h3 className="form-heading">Форма заказа</h3>
                        <form method="" className="lunch_set_form">
                            <div className="lunch_set_item">
                                {Object.keys(lunchSet.composition).map(dishType => (
                                    <div className="lunch_set_item_wrapper" key={dishType}>
                                        <h3 className="lunch_set_item_title">{dishType}</h3>
                                        <div className="lunch_set_content">
                                            {lunchSet.composition[dishType].map((item, index) => (
                                                <DishItem key={`${dishType}-${index}`} checked={index === 0} item={item} />
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </form>
                    </div>
                </div>
            </div>    
        </div>
    );
}

function LunchSetList() {
    const [lunchSet, setLunchSet] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const today = new Date();
    const todayFormatted = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;

    useEffect(() => {
        fetch(`/api/v2/lunch-set/${todayFormatted}`)
            .then(res => {
                if (!res.ok) throw new Error('Ошибка сети');
                return res.json();
            })
            .then(data => {
                let object = {};
                data.composition?.map(item => {
                    object[item.dish_type] = data.composition.filter(el => el.dish_type === item.dish_type);
                });
                data.composition = object;
                setLunchSet(data);
                setLoading(false);
            })
            .catch(err => {
                setError(err.message);
                setLoading(false);
            });
    }, [todayFormatted]);

    return (
        <div class="main-container margin-bottom-30 right-sidebar">
            <div class="container">
                <nav class="woocommerce-breadcrumb breadcrumbs">
                    <a href="/">На главную</a>
                    <a href="/lunch-set-info">Дружеские обеды</a>
                    Сегодня в меню
                </nav>
                { loading && <p>Загрузка...</p> }
                { error && <p>Ошибка: {error}</p> }
                { !lunchSet && !loading && !error && <p>Обеды не найдены.</p> }
                { !loading && !error && <LunchSetCard lunchSet={lunchSet} /> }
            </div>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('lunch-sets-root'));
root.render(<LunchSetList />);
