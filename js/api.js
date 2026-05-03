/**
 * Homs Store - API Layer with Picsum Images + Static Fallback
 */

const API_BASE = 'http://localhost:5000/api';

// ── Image URL ────────────────────────────────────────────────────────────────
function getProductImageUrl(product) {
    // Priority 1: use image_url from backend (Unsplash CDN URLs)
    const url = product.image_url || '';
    if (url && url.startsWith('https://') && !url.includes('seed/') && url !== 'nan') {
        return url;
    }

    // Fallback: specific Unsplash photos by product_id (matches backend mapping)
    const pid = parseInt(product.product_id) || 1;
    const IMAGES = {
        1:'photo-1525547719571-a2d4ac8945e2', 2:'photo-1505740420928-5e560c06d30e',
        3:'photo-1593359677879-a4bb92f829d1', 4:'photo-1541140532154-b024d705b90a',
        5:'photo-1527814050087-3793815479db', 6:'photo-1510557880182-3d4d3cba35a5',
        7:'photo-1567581935884-3349723552ca', 8:'photo-1544244015-0df4b3ffc6b0',
        9:'photo-1607853202273-797f1c22a38e', 10:'photo-1484704849700-f032a568e944',
        11:'photo-1473968512647-3e447244af8f',12:'photo-1434056886845-dac89ffe9b56',
        13:'photo-1527814050087-3793815479db',14:'photo-1527443224154-c4a573d5f5d6',
        15:'photo-1496181133206-80ce9b88a853',16:'photo-1608043152269-423dbba4e7e1',
        17:'photo-1557597774-9d273605dfa9', 18:'photo-1590658268037-6bf12165a8df',
        19:'photo-1519389950473-47ba0277781c',20:'photo-1593642632559-0c6d3fc62b89',
        21:'photo-1507679799987-c73779587ccf',22:'photo-1568252542512-9fe8fe9c87bb',
        23:'photo-1495105787522-5334e3ffa0ef',24:'photo-1506629082955-511b1aa562c8',
        25:'photo-1551698618-1dfe5d97d256', 26:'photo-1434389677669-e08b4cac3105',
        27:'photo-1473966968600-fa801b869a1a',28:'photo-1594938298603-c8148c4b1df6',
        29:'photo-1521572163474-6864f9cf17ab',30:'photo-1512436991641-6745cdb1723f',
        31:'photo-1556821840-3a63f15732ce', 32:'photo-1591047139829-d91aecb6caea',
        33:'photo-1596755094514-f87e34085b2c',34:'photo-1542272604-327c114c3384',
        35:'photo-1434389677669-e08b4cac3105',36:'photo-1485965120184-e220f721d03e',
        37:'photo-1542291026-7eec264c27ff', 38:'photo-1601925228008-87f4dda9ba38',
        39:'photo-1534438327276-14e5300c3a48',40:'photo-1546519638-68e109498ffc',
        41:'photo-1553062407-98eeb64c6a62', 42:'photo-1575311373937-040b8e1fd5b6',
        43:'photo-1517963879433-6ad2a56b9727',44:'photo-1614632537197-38a17061c2bd',
        45:'photo-1587280501635-68a0e82cd5ff',46:'photo-1434682966068-8c56d34a2b1c',
        47:'photo-1530549387789-4c1017266635',48:'photo-1599901860904-17e6ed7083a0',
        49:'photo-1491553895911-0055eca6402d',50:'photo-1570197788417-0e82375c9371',
        51:'photo-1558618666-fcd25c85cd64', 52:'photo-1585771724684-38269d6639fd',
        53:'photo-1556909114-f6e7ad7d3136', 54:'photo-1507003211169-0a1dd7228f2d',
        55:'photo-1510591509098-f4fdc6d0ff04',56:'photo-1556911073-a517e752729c',
        57:'photo-1558618047-3c8c76ca7d13', 58:'photo-1558618666-fcd25c85cd64',
        59:'photo-1560472355-536de3962603', 60:'photo-1585032226651-773f5a3585a2',
        61:'photo-1577916297339-beff89a403d7',62:'photo-1604608672516-f1b9c4cd1ca1',
        63:'photo-1485955900006-10f4d324d411',64:'photo-1602607920945-5cd34a75db5e',
        65:'photo-1513694203232-719a280e022f',66:'photo-1544947950-fa07a98d237f',
        67:'photo-1554224155-6726b3ff858f', 68:'photo-1512820790803-83ca734da794',
        69:'photo-1532012197267-da84d127e765',70:'photo-1461749280684-dccba630e2f6',
        71:'photo-1456324504439-367cee3b3c32',72:'photo-1579621970795-87facc2f976d',
        73:'photo-1544947950-fa07a98d237f', 74:'photo-1499750310107-5fef28a66643',
        75:'photo-1507003211169-0a1dd7228f2d',
    };
    const base = ((pid - 1) % 75) + 1;
    const photo = IMAGES[base] || IMAGES[1];
    return `https://images.unsplash.com/${photo}?w=600&q=80`;
}

// ── Stars HTML ────────────────────────────────────────────────────────────────
function renderStars(rating) {
    const r = parseFloat(rating) || 4;
    const full = Math.floor(r), half = r % 1 >= 0.5 ? 1 : 0, empty = 5 - full - half;
    return `${'<i class="fas fa-star text-yellow-400"></i>'.repeat(full)}${'<i class="fas fa-star-half-alt text-yellow-400"></i>'.repeat(half)}${'<i class="far fa-star text-yellow-300"></i>'.repeat(empty)}`;
}

// ── Product Card ──────────────────────────────────────────────────────────────
function buildProductCard(p, basePath = '') {
    const img    = getProductImageUrl(p);
    const base   = ((parseInt(p.product_id)||1) - 1) % 75 + 1;
    const fallbackImg = `https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=600&q=80`;
    const rating = parseFloat(p.rating) || 4.0;
    const price  = parseFloat(p.price)  || 0;
    const stock  = parseInt(p.stock)    || 10;
    const badge  = stock === 0 ? '<div class="absolute top-3 left-3 bg-red-100 text-red-600 px-2 py-1 rounded-lg text-xs font-bold">Out of Stock</div>'
                 : stock < 20 ? '<div class="absolute top-3 left-3 bg-orange-100 text-orange-600 px-2 py-1 rounded-lg text-xs font-bold">Low Stock</div>' : '';
    return `
    <div class="glass-card p-4 group flex flex-col justify-between" data-product-id="${p.product_id}">
        <div class="relative rounded-2xl overflow-hidden mb-4 aspect-square bg-gray-100">
            <img src="${img}" alt="${p.name}"
                class="w-full h-full object-cover transition duration-500 group-hover:scale-105"
                onerror="this.onerror=null;this.src='${fallbackImg}'">
            ${badge}
            <button class="absolute top-3 right-3 w-8 h-8 rounded-full bg-white/80 text-gray-500 hover:text-pink-500 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity" title="Wishlist">
                <i class="far fa-heart"></i>
            </button>
            <div class="absolute bottom-0 left-0 w-full p-3 translate-y-full group-hover:translate-y-0 transition-transform duration-300">
                <a href="${basePath}pages/product-details.html?id=${p.product_id}"
                   class="block text-center w-full py-2 bg-white/90 backdrop-blur-sm text-gray-900 rounded-xl font-semibold text-sm shadow-lg hover:bg-gray-900 hover:text-white transition">
                    View Details
                </a>
            </div>
        </div>
        <div>
            <div class="text-xs text-purple-500 font-semibold uppercase tracking-wide mb-1">${p.category}</div>
            <h3 class="font-bold text-gray-800 text-sm mb-1 line-clamp-2">
                <a href="${basePath}pages/product-details.html?id=${p.product_id}" class="hover:text-purple-600 transition">${p.name}</a>
            </h3>
            <div class="flex items-center gap-1 mb-2 text-xs">${renderStars(rating)}<span class="text-gray-500 ml-1">${rating.toFixed(1)}</span></div>
            <div class="flex justify-between items-center">
                <span class="font-bold text-gray-900 text-base">$${price.toFixed(2)}</span>
                ${stock > 0 ? '<span class="text-xs text-green-500 font-medium"><i class="fas fa-check-circle"></i> In Stock</span>' : '<span class="text-xs text-red-400 font-medium">Out of Stock</span>'}
            </div>
        </div>
    </div>`;
}

// ── Static Fallback Data (shows when backend is offline) ──────────────────────
const FALLBACK_PRODUCTS = [
    {product_id:1,  name:"Gaming Laptop Pro 15",               category:"Electronics", price:1299.99, rating:4.7, stock:45, description:"High-performance gaming laptop with RTX 4070, 32GB RAM, 165Hz display"},
    {product_id:2,  name:"Wireless Noise-Cancelling Headphones",category:"Electronics", price:349.99,  rating:4.8, stock:120,description:"Premium ANC headphones with 30hr battery, Hi-Res Audio"},
    {product_id:3,  name:'4K Smart Android TV 55"',             category:"Electronics", price:699.99,  rating:4.6, stock:30, description:"4K OLED smart TV with HDR10, Dolby Vision, built-in streaming"},
    {product_id:4,  name:"Mechanical Gaming Keyboard RGB",      category:"Electronics", price:129.99,  rating:4.5, stock:85, description:"Tactile mechanical switches, per-key RGB, aluminum frame"},
    {product_id:5,  name:"Wireless Gaming Mouse 25K DPI",       category:"Electronics", price:89.99,   rating:4.7, stock:95, description:"Ultra-precise 25K DPI sensor, 70hr battery, lightweight 65g"},
    {product_id:6,  name:"Men's Premium Business Suit",         category:"Clothing",    price:399.99,  rating:4.6, stock:25, description:"Slim-fit wool-blend suit, wrinkle-resistant, available in 3 colors"},
    {product_id:7,  name:"Women's Floral Maxi Dress",           category:"Clothing",    price:89.99,   rating:4.5, stock:60, description:"Flowy chiffon maxi dress with floral print, perfect for summer"},
    {product_id:8,  name:"Premium Yoga Mat Non-Slip",           category:"Sports",      price:79.99,   rating:4.8, stock:150,description:"Extra thick 6mm, non-slip surface, includes carry strap"},
    {product_id:9,  name:"Adjustable Dumbbell Set 5-52.5 lb",   category:"Sports",      price:349.99,  rating:4.9, stock:20, description:"Space-saving adjustable dumbbells, 15 weight settings"},
    {product_id:10, name:"Robot Vacuum Cleaner Pro",            category:"Home",        price:499.99,  rating:4.7, stock:35, description:"Smart mapping, auto-empty base, works with Alexa & Google"},
    {product_id:11, name:"Air Purifier HEPA H13",               category:"Home",        price:249.99,  rating:4.8, stock:55, description:"True HEPA H13 filter, covers 1500 sq ft, ultra-quiet 22dB"},
    {product_id:12, name:"Atomic Habits - James Clear",         category:"Books",       price:18.99,   rating:4.9, stock:200,description:"Build good habits and break bad ones — #1 New York Times bestseller"},
    {product_id:13, name:"iPhone 16 Pro Max 256GB",             category:"Electronics", price:1199.99, rating:4.8, stock:40, description:"A18 Pro chip, 48MP ProRAW camera, titanium design, USB-C"},
    {product_id:14, name:"Women's Running Shoes Ultra",         category:"Sports",      price:129.99,  rating:4.6, stock:75, description:"Lightweight responsive foam, breathable mesh, reflective details"},
    {product_id:15, name:"Instant Pot Duo 7-in-1",             category:"Home",        price:99.99,   rating:4.7, stock:90, description:"Pressure cooker, slow cooker, rice cooker, steamer, sauté — 7 functions"},
    {product_id:16, name:"The Psychology of Money",             category:"Books",       price:16.99,   rating:4.8, stock:180,description:"Timeless lessons on wealth, greed and happiness by Morgan Housel"},
    {product_id:17, name:"Samsung Galaxy S24 Ultra",            category:"Electronics", price:1299.99, rating:4.7, stock:50, description:"200MP camera, built-in S Pen, Snapdragon 8 Gen 3, 5000mAh"},
    {product_id:18, name:"Men's Slim Fit Chino Pants",          category:"Clothing",    price:59.99,   rating:4.4, stock:110,description:"Stretch cotton blend, slim fit, available in 8 colors"},
    {product_id:19, name:"Resistance Bands Set (5-pack)",       category:"Sports",      price:39.99,   rating:4.7, stock:200,description:"5 resistance levels, natural latex, includes door anchor & handles"},
    {product_id:20, name:"Air Fryer XL 5.8 Qt",                category:"Home",        price:119.99,  rating:4.6, stock:65, description:"1700W, 5.8-quart capacity, dishwasher-safe basket, 8 presets"},
];

function getFallbackProducts(params = {}) {
    let products = [...FALLBACK_PRODUCTS];
    const { category, q, sort, page = 1, limit = 12 } = params;

    if (category) products = products.filter(p => p.category.toLowerCase() === category.toLowerCase());
    if (q)        products = products.filter(p => p.name.toLowerCase().includes(q.toLowerCase()) || p.category.toLowerCase().includes(q.toLowerCase()));

    if (sort === 'price_asc')  products.sort((a,b) => a.price - b.price);
    if (sort === 'price_desc') products.sort((a,b) => b.price - a.price);
    if (sort === 'rating')     products.sort((a,b) => b.rating - a.rating);

    const total = products.length;
    const pages = Math.ceil(total / limit);
    const start = (page - 1) * limit;
    return { products: products.slice(start, start + limit), total, pages, page };
}

function getFallbackCategories() {
    const counts = {};
    FALLBACK_PRODUCTS.forEach(p => { counts[p.category] = (counts[p.category] || 0) + 1; });
    return { categories: Object.entries(counts).map(([name, count]) => ({ name, count })) };
}

// ── API Fetch with Fallback ───────────────────────────────────────────────────
async function apiFetch(endpoint, options = {}) {
    try {
        const res = await fetch(`${API_BASE}${endpoint}`, {
            headers: { 'Content-Type': 'application/json' },
            ...options
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (e) {
        console.warn(`API offline [${endpoint}] — using fallback data`);
        return null;
    }
}

// ── Products API ──────────────────────────────────────────────────────────────
const ProductsAPI = {
    getAll: async (params = {}) => {
        const q = new URLSearchParams(params).toString();
        const data = await apiFetch(`/products${q ? '?' + q : ''}`);
        if (data) return data;
        // Fallback
        return getFallbackProducts(params);
    },
    getOne: async (id) => {
        const data = await apiFetch(`/product/${id}`);
        if (data && !data.error) return data;
        return FALLBACK_PRODUCTS.find(p => p.product_id === parseInt(id)) || FALLBACK_PRODUCTS[0];
    },
    getSimilar: async (id) => {
        const data = await apiFetch(`/product/${id}/similar`);
        if (data) return data;
        const p = FALLBACK_PRODUCTS.find(x => x.product_id === parseInt(id));
        const similar = FALLBACK_PRODUCTS.filter(x => x.category === (p?.category || '') && x.product_id !== parseInt(id)).slice(0, 4);
        return { similar_products: similar };
    },
    getCategories: async () => {
        const data = await apiFetch('/categories');
        return data || getFallbackCategories();
    },
    search: async (query, category = '') => {
        const q = new URLSearchParams({ q: query, category }).toString();
        const data = await apiFetch(`/search?${q}`);
        if (data) return data;
        return FALLBACK_PRODUCTS.filter(p => p.name.toLowerCase().includes(query.toLowerCase())).slice(0, 8);
    },
};

// ── Recommendations API ───────────────────────────────────────────────────────
const RecommendationsAPI = {
    getForUser: async (userId = 1) => {
        const data = await apiFetch(`/recommendations/${userId}`);
        if (data) return data;
        return {
            recommended_products: FALLBACK_PRODUCTS.sort(() => 0.5 - Math.random()).slice(0, 6),
            match_percentage: 82,
            fitness_score: 0.74,
            mutation_rate: 0.05,
            recommendation_reason: 'Based on your browsing activity (fallback mode)'
        };
    },
    getUserInterests: (userId = 1) => apiFetch(`/user-interest/${userId}`),
    sendFeedback: (userId, productId, score) => apiFetch('/recommendation-score', {
        method: 'POST',
        body: JSON.stringify({ user_id: userId, product_id: productId, score }),
    }),
};

// ── Dashboard API ─────────────────────────────────────────────────────────────
const DashboardAPI = {
    getStats:  () => apiFetch('/dashboard/stats'),
    getCharts: () => apiFetch('/dashboard/charts'),
};

// ── Analytics API ─────────────────────────────────────────────────────────────
const AnalyticsAPI = {
    getSummary:    () => apiFetch('/analytics'),
    getUserBehavior: () => apiFetch('/user-behavior'),
    getClickRate:  () => apiFetch('/click-rate'),
    getPurchaseRate: () => apiFetch('/purchase-rate'),
};

// ── Tracking API ──────────────────────────────────────────────────────────────
const TrackingAPI = {
    track: (eventType, data = {}) => apiFetch('/track', {
        method: 'POST',
        body: JSON.stringify({ user_id: 1, event_type: eventType, ...data }),
    }),
};
