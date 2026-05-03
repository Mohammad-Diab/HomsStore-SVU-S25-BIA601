// ── Category icon/color map ───────────────────────────────────────────────────
const CATEGORY_CONFIG = {
    Electronics: { icon: 'fa-laptop',   color: 'blue',   label: 'Electronics' },
    Clothing:    { icon: 'fa-tshirt',   color: 'pink',   label: 'Clothing'    },
    Sports:      { icon: 'fa-dumbbell', color: 'green',  label: 'Sports'      },
    Home:        { icon: 'fa-home',     color: 'orange', color2: 'orange',    label: 'Home' },
    Books:       { icon: 'fa-book',     color: 'purple', label: 'Books'       },
};

// ── Templates ─────────────────────────────────────────────────────────────────
const Navbar = `
<nav class="glass fixed w-full top-0 z-50 px-6 py-4 flex justify-between items-center transition-all duration-300" id="navbar">
    <div class="flex items-center gap-4">
        <button id="mobile-menu-btn" class="lg:hidden text-gray-700 hover:text-purple-600 transition">
            <i class="fas fa-bars text-xl"></i>
        </button>
        <a href="/index.html" class="flex items-center gap-2">
            <div class="w-10 h-10 rounded-full bg-gradient-to-tr from-purple-400 to-pink-300 flex items-center justify-center text-white font-bold text-xl shadow-lg">H</div>
            <span class="text-2xl font-bold text-gray-800 tracking-wide hidden sm:block">Homs<span class="text-purple-500">Store</span></span>
        </a>
    </div>
    <div class="hidden md:flex flex-1 max-w-xl mx-8 relative">
        <input type="text" id="navbar-search-input" placeholder="Search products, categories..." class="w-full bg-white/50 backdrop-blur-sm border border-white/60 rounded-full py-2.5 px-6 pl-12 focus:outline-none focus:ring-2 focus:ring-purple-300 shadow-sm transition">
        <i class="fas fa-search absolute left-5 top-3.5 text-gray-400"></i>
        <div id="search-suggestions" class="absolute top-full left-0 w-full mt-1 glass-card rounded-2xl shadow-xl z-50 hidden overflow-hidden"></div>
    </div>
    <div class="flex items-center gap-4">
        <a href="/pages/recommendations.html" class="hidden sm:flex items-center gap-2 glass-button px-4 py-2 text-sm font-medium text-purple-700">
            <i class="fas fa-magic"></i> AI Matches
        </a>
        <a href="/pages/dashboard.html" class="text-gray-600 hover:text-purple-600 transition relative p-2"><i class="far fa-user text-xl"></i></a>
        <a href="#" class="text-gray-600 hover:text-purple-600 transition relative p-2">
            <i class="far fa-heart text-xl"></i>
            <span class="absolute top-0 right-0 w-4 h-4 bg-pink-400 text-white text-[10px] flex items-center justify-center rounded-full font-bold shadow">3</span>
        </a>
        <a href="#" class="text-gray-600 hover:text-purple-600 transition relative p-2">
            <i class="fas fa-shopping-bag text-xl"></i>
            <span class="absolute top-0 right-0 w-4 h-4 bg-purple-500 text-white text-[10px] flex items-center justify-center rounded-full font-bold shadow">0</span>
        </a>
    </div>
</nav>`;

const Sidebar = `
<aside id="sidebar" class="glass fixed left-0 top-0 h-full w-64 z-40 transform -translate-x-full lg:translate-x-0 transition-transform duration-300 pt-24 pb-8 px-6 overflow-y-auto flex flex-col">
    <div class="mb-8">
        <h3 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-4">Discover</h3>
        <ul class="space-y-2">
            <li><a href="/index.html" class="sidebar-link flex items-center gap-3 px-4 py-2.5 rounded-xl text-gray-700 hover:bg-white/50 hover:text-purple-600 transition font-medium group">
                <i class="fas fa-home text-gray-400 group-hover:text-purple-500 transition"></i> Home
            </a></li>
            <li><a href="/pages/products.html" class="sidebar-link flex items-center gap-3 px-4 py-2.5 rounded-xl text-gray-700 hover:bg-white/50 hover:text-purple-600 transition font-medium group">
                <i class="fas fa-compass text-gray-400 group-hover:text-purple-500 transition"></i> Browse All
            </a></li>
            <li><a href="/pages/recommendations.html" class="sidebar-link flex items-center gap-3 px-4 py-2.5 rounded-xl text-gray-700 hover:bg-white/50 hover:text-purple-600 transition font-medium group">
                <i class="fas fa-magic text-purple-400 group-hover:text-purple-600 transition"></i> For You
            </a></li>
            <li><a href="/pages/dashboard.html" class="sidebar-link flex items-center gap-3 px-4 py-2.5 rounded-xl text-gray-700 hover:bg-white/50 hover:text-purple-600 transition font-medium group">
                <i class="fas fa-chart-bar text-gray-400 group-hover:text-purple-500 transition"></i> Dashboard
            </a></li>
        </ul>
    </div>
    <div class="mb-8">
        <h3 class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-4">Categories</h3>
        <ul id="sidebar-categories" class="space-y-2">
            <!-- Dynamically loaded -->
            <li class="px-4 py-2 animate-pulse"><div class="h-4 bg-gray-200 rounded w-3/4"></div></li>
            <li class="px-4 py-2 animate-pulse"><div class="h-4 bg-gray-200 rounded w-2/3"></div></li>
            <li class="px-4 py-2 animate-pulse"><div class="h-4 bg-gray-200 rounded w-3/4"></div></li>
        </ul>
    </div>
    <div class="mt-auto">
        <div class="glass-card p-4 rounded-2xl relative overflow-hidden">
            <div class="absolute -right-4 -top-4 w-16 h-16 bg-purple-300 rounded-full blur-xl opacity-50"></div>
            <h4 class="font-bold text-sm text-gray-800 mb-1">🧬 AI Powered</h4>
            <p class="text-xs text-gray-500 mb-3">Genetic algorithm recommends products just for you.</p>
            <a href="/pages/recommendations.html" class="block w-full py-2 text-center bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-xl text-sm font-semibold shadow-md hover:shadow-lg transition hover:-translate-y-0.5">Get Recommendations</a>
        </div>
    </div>
</aside>
<div id="sidebar-overlay" class="fixed inset-0 bg-black/20 backdrop-blur-sm z-30 hidden lg:hidden transition-opacity"></div>`;

// ── Init ──────────────────────────────────────────────────────────────────────
function injectComponents() {
    const isRoot = window.location.pathname.endsWith('index.html') || window.location.pathname === '/';
    const prefix = isRoot ? '.' : '..';

    const fmtNavbar  = Navbar.replace(/href="\/(?!\/)/g,  `href="${prefix}/`);
    const fmtSidebar = Sidebar.replace(/href="\/(?!\/)/g, `href="${prefix}/`);

    const header = document.createElement('header');
    header.innerHTML = fmtNavbar;
    document.body.prepend(header);

    const sidebarEl = document.createElement('div');
    sidebarEl.innerHTML = fmtSidebar;
    document.body.appendChild(sidebarEl);

    setTimeout(() => {
        setupMobileMenu();
        setupSearch(isRoot, prefix);
        loadSidebarCategories(isRoot, prefix);
        highlightActiveLink();
    }, 100);
}

function setupMobileMenu() {
    const btn     = document.getElementById('mobile-menu-btn');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    if (!btn || !sidebar || !overlay) return;
    btn.addEventListener('click', () => {
        sidebar.classList.toggle('-translate-x-full');
        overlay.classList.toggle('hidden');
    });
    overlay.addEventListener('click', () => {
        sidebar.classList.add('-translate-x-full');
        overlay.classList.add('hidden');
    });
}

async function loadSidebarCategories(isRoot, prefix) {
    const ul = document.getElementById('sidebar-categories');
    if (!ul) return;
    try {
        const data = await fetch('http://localhost:5000/api/categories').then(r => r.json());
        ul.innerHTML = '';
        const urlParams = new URLSearchParams(window.location.search);
        const activeCat = urlParams.get('category') || '';

        data.categories.forEach(cat => {
            const cfg   = CATEGORY_CONFIG[cat.name] || { icon: 'fa-tag', color: 'gray', label: cat.name };
            const isAct = activeCat.toLowerCase() === cat.name.toLowerCase();
            ul.insertAdjacentHTML('beforeend', `
            <li>
                <a href="${prefix}/pages/products.html?category=${encodeURIComponent(cat.name)}"
                   class="category-link flex items-center justify-between px-4 py-2.5 rounded-xl ${isAct ? 'bg-purple-100 text-purple-700 font-bold' : 'text-gray-700 hover:bg-white/50 hover:text-purple-600'} transition font-medium group">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-full bg-${cfg.color}-100 flex items-center justify-center text-${cfg.color}-500">
                            <i class="fas ${cfg.icon} text-sm"></i>
                        </div>
                        ${cfg.label}
                    </div>
                    <span class="text-xs text-gray-400 font-normal">${cat.count}</span>
                </a>
            </li>`);
        });
    } catch(e) {
        ul.innerHTML = '<li class="px-4 py-2 text-xs text-gray-400">Backend offline</li>';
    }
}

function setupSearch(isRoot, prefix) {
    const input = document.getElementById('navbar-search-input');
    const suggestions = document.getElementById('search-suggestions');
    if (!input || !suggestions) return;

    let debounceTimer;
    input.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        const q = input.value.trim();
        if (q.length < 2) { suggestions.classList.add('hidden'); return; }
        debounceTimer = setTimeout(() => fetchSuggestions(q, suggestions, prefix, isRoot), 300);
    });

    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && input.value.trim()) {
            suggestions.classList.add('hidden');
            window.location.href = `${prefix}/pages/products.html?q=${encodeURIComponent(input.value.trim())}`;
        }
        if (e.key === 'Escape') suggestions.classList.add('hidden');
    });

    document.addEventListener('click', (e) => {
        if (!input.contains(e.target) && !suggestions.contains(e.target)) suggestions.classList.add('hidden');
    });
}

async function fetchSuggestions(q, box, prefix, isRoot) {
    try {
        const data = await fetch(`http://localhost:5000/api/search?q=${encodeURIComponent(q)}`).then(r => r.json());
        if (!data || !data.length) { box.classList.add('hidden'); return; }
        box.innerHTML = data.slice(0, 6).map(p => `
        <a href="${prefix}/pages/product-details.html?id=${p.product_id}"
           class="flex items-center gap-3 px-4 py-3 hover:bg-purple-50 transition border-b border-gray-100 last:border-0">
            <img src="${p.image_url || getProductImageUrl(p)}" alt="${p.name}" class="w-10 h-10 rounded-lg object-cover" onerror="this.onerror=null;this.src='https://picsum.photos/seed/${(parseInt(p.product_id)||1)+50}/80/80'">
            <div>
                <div class="font-semibold text-gray-800 text-sm">${p.name}</div>
                <div class="text-xs text-gray-500">${p.category} · $${parseFloat(p.price).toFixed(2)}</div>
            </div>
        </a>`).join('');
        box.insertAdjacentHTML('beforeend', `
        <a href="${prefix}/pages/products.html?q=${encodeURIComponent(q)}"
           class="flex items-center gap-2 px-4 py-3 bg-purple-50 text-purple-600 text-sm font-semibold hover:bg-purple-100 transition">
            <i class="fas fa-search text-xs"></i> See all results for "${q}"
        </a>`);
        box.classList.remove('hidden');
    } catch(e) {
        box.classList.add('hidden');
    }
}

function highlightActiveLink() {
    const path = window.location.pathname;
    document.querySelectorAll('.sidebar-link').forEach(link => {
        const href = link.getAttribute('href') || '';
        if (href && path.endsWith(href.replace(/^\.\.?\//, ''))) {
            link.classList.add('bg-purple-50', 'text-purple-700', 'font-bold');
        }
    });
}

document.addEventListener('DOMContentLoaded', injectComponents);
