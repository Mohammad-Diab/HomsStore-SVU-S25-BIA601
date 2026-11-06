# HomsStore

An online store with product recommendations from a genetic algorithm, made for the Intelligent Algorithms course (BIA601) at the Syrian Virtual University (SVU), semester S25. A Flask API in Python reads the store data from Excel files; the front end is HTML and JavaScript with Tailwind CSS.

## Features

- Products page with categories and search, and a product page with similar products.
- Recommendations for each user from a genetic algorithm (`backend/algorithms/genetic_algorithm.py`): it scores products by views, clicks, purchases, ratings and the user's tracked behaviour, then evolves sets of 10 products (population 50, 20 generations, crossover rate 0.8, adaptive mutation from 0.1, elitism 2). The settings are in `backend/config/settings.py`.
- Tracking of views, clicks, add-to-cart, searches and purchases in a SQLite database (`backend/data/tracking.db`).
- Dashboard and analytics pages with charts.
- Login by user id, and registration with age and location.

The data is a generated sample in `backend/data`: 1,000 users, 200 products, ratings and behaviour.

## Requirements

Python 3 (3.9 to 3.12 for the pinned package versions) and a browser.

## Running

```
git clone https://github.com/Mohammad-Diab/HomsStore-SVU-S25-BIA601.git
cd HomsStore-SVU-S25-BIA601/backend
pip install -r requirements.txt
python app.py
```

On Windows, `تشغيل الموقع.bat` starts the backend the same way. The API runs on `http://localhost:5000`; keep it running and open `index.html` in a browser.

`backend/update_products.py` rebuilds `products.xlsx` from the product list in the script, and `backend/generate_images.py` gives each product an Unsplash image URL.

## Credits

- Product pictures: [Unsplash](https://unsplash.com) and [Lorem Picsum](https://picsum.photos), loaded by URL; they are not in this repository.
- [Tailwind CSS](https://tailwindcss.com), [Font Awesome Free](https://fontawesome.com) 6.4.0, [Swiper](https://swiperjs.com) 10, [GSAP](https://gsap.com) 3.12.2, [AOS](https://michalsnik.github.io/aos/) 2.3.1 and [Chart.js](https://www.chartjs.org), loaded from CDNs.
- Product and brand names belong to their owners.

## Author

Mohammad Diab

## License

[Apache 2.0](LICENSE)
