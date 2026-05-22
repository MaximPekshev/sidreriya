const { useState, useEffect } = React;

function DishItem({ item, checked, onSelect }) {
    return (
        <div className="lunch_set_dish">
            <div className="lunch_set_dish_info">
                <input 
                    type="radio" 
                    className="input-radio" 
                    name={item.dish_type} 
                    value={item.dish.slug} 
                    checked={checked}
                    onChange={() => onSelect(item.dish_type, item.dish.slug)}
                />
                <div className={`dish_label ${ checked ? 'checked' : ''}`}>{item.dish.title}</div>
            </div>
            { item.dish.picture && 
                <div onClick={() => onSelect(item.dish_type, item.dish.slug)} className={`lunch_set_dish_image_box`}>
                    <div className={`label_checked ${ checked ? 'checked' : ''}`}>
                        <span className="menu-icon icon flaticon-label36"></span>
                    </div>
                    <div className={`lunch_set_dish_image_overlay ${ checked ? 'checked' : ''}`}></div>
                    <img src={item.dish.picture} alt={item.dish.title} className="dish_image" /> 
                </div>
            }
            { !item.dish.picture && 
                <div onClick={() => onSelect(item.dish_type, item.dish.slug)} className={`lunch_set_dish_image_box`}>
                    <div className={`label_checked ${ checked ? 'checked' : ''}`}>
                        <span className="menu-icon icon flaticon-label36"></span>
                    </div>
                    <div className={`lunch_set_dish_image_overlay ${ checked ? 'checked' : ''}`}></div>
                    <img src="https://sidreriyabelgorod.ru/static/images/products/no-photo.png" alt={item.dish.title} className="dish_image" /> 
                </div>
            }
        </div>
    );
}

const DAYS_OF_WEEK = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];

function getDayOfWeek(dateStr) {
    const [year, month, day] = dateStr.split('-').map(Number);
    const date = new Date(year, month - 1, day);
    return DAYS_OF_WEEK[date.getDay()];
}

function LunchSetCard({ lunchSet }) {
    const [selectedDishes, setSelectedDishes] = useState({});
    const [ cart, setCart ] = useState([]);

    useEffect(() => {
        const initialSelection = {};

        Object.keys(lunchSet.composition).forEach((dishType) => {
            const firstDish = lunchSet.composition[dishType]?.[0];
            if (firstDish?.dish?.slug) {
                initialSelection[dishType] = firstDish.dish.slug;
            }
        });

        setSelectedDishes(initialSelection);
    }, [lunchSet]);

    const handleDishSelect = (dishType, dishSlug) => {
        setSelectedDishes((prev) => ({
            ...prev,
            [dishType]: dishSlug,
        }));
    };

    const addLunchSetToCart = () => {
        const selectedEntries = Object.entries(selectedDishes)
            .filter(([, dishSlug]) => Boolean(dishSlug))
            .sort(([typeA], [typeB]) => typeA.localeCompare(typeB));

        if (!selectedEntries.length) {
            return;
        }

        const selectedItems = selectedEntries.map(([dishType, dishSlug]) => {
            const dishObj = lunchSet.composition[dishType]?.find((entry) => entry.dish.slug === dishSlug);

            return {
                dish_type: dishType,
                dish: dishObj?.dish || null,
            };
        });

        const isValidSelection = selectedItems.every((entry) => entry.dish);
        if (!isValidSelection) {
            return;
        }

        const comboKey = selectedEntries
            .map(([dishType, dishSlug]) => `${dishType}:${dishSlug}`)
            .join('|');

        setCart((prevCart) => {
            const existingIndex = prevCart.findIndex((item) => item.comboKey === comboKey);

            if (existingIndex === -1) {
                return [
                    ...prevCart,
                    {
                        comboKey,
                        lunch_set_id: lunchSet.id,
                        lunch_set_date: lunchSet.date,
                        quantity: 1,
                        selected_dishes: selectedItems,
                    },
                ];
            }

            return prevCart.map((item, index) => {
                if (index !== existingIndex) {
                    return item;
                }

                return {
                    ...item,
                    quantity: item.quantity + 1,
                };
            });
        });
    };

    const removeFromCart = (comboKey) => {
        setCart((prevCart) => prevCart.filter((item) => item.comboKey !== comboKey));
    };

    // console.log('Текущая корзина:', cart);

    return (
        <div className="lunch-set">
            <div className="col-sm-12 col-md-8 lunch_set_wrapper">
                <div className="lunch_set_information">
                    <h2>Дружеские обеды</h2>
                    <p className="set_lunch_time">с 11:00 до 18:00</p>
                    <div className="set_lunch_price">430Р</div>
                    <div className="set_lunch_date"><div></div>{getDayOfWeek(lunchSet.date)}<div></div></div>
                    <div className="set_lunch_address">Левобережная 22, Костюкова 36</div>
                </div>    
                {lunchSet.comment && <p>{lunchSet.comment}</p>}
                <div className="panel">
                    <div id method="" className="lunch_set_form">
                        <div className="lunch_set_item">
                            {Object.keys(lunchSet.composition).map(dishType => (
                                <div className="lunch_set_item_wrapper" key={dishType}>
                                    <h3 className="lunch_set_item_title">{dishType}</h3>
                                    <div className="lunch_set_content">
                                        {lunchSet.composition[dishType].map((item, index) => (
                                            <DishItem
                                                key={`${dishType}-${index}`}
                                                checked={selectedDishes[dishType] === item.dish.slug}
                                                item={item}
                                                onSelect={handleDishSelect}
                                            />
                                        ))}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="lunch_set_submit">
                        <button type="button" className="btn primary" onClick={addLunchSetToCart}>Добавить</button>
                    </div>
                </div>
            </div>  
            <div className="col-sm-12 col-md-4 sidebar border blog-sidebar">
                <div className="block-form">
                    <div className="panel" style={{ borderBottomStyle: 'none' }}>
                        <h3 className="form-heading">Форма заказа обеда</h3>
                        { !cart.length && 
                            <p className="set_lunch_cart_warning">
                                Вы еще не выбрали блюда для обеда. Пожалуйста, выберите блюда из 
                                меню и добавьте их в корзину.
                            </p> 
                        }
                        { cart.length > 0 && 
                            <div className="set_lunch_cart">
                                <h4>В корзине:</h4>
                                {cart.map((item, index) => (
                                    <div key={index} className="set_lunch_cart_item">
                                        <div className="cart_item_header">
                                            <span>Дружеский обед</span>
                                        </div>
                                        <ul className="cart_item_dishes">
                                            {item.selected_dishes.map((dishEntry, dishIndex) => (
                                                <li key={dishIndex}>
                                                    {dishEntry.dish.title}
                                                </li>
                                            ))}
                                        </ul>
                                        <div className="set_lunch_item_qty">x {item.quantity} шт.</div>
                                        <div className="set_lunch_item_action">
                                            <div className="set_lunch_item_delete">
                                                <i onClick={() => removeFromCart(item.comboKey)} className="fa fa-trash"></i>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                         }
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
