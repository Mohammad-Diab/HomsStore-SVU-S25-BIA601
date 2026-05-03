from flask import Blueprint, jsonify, request
from data.data_manager import data_manager
import pandas as pd

products_bp = Blueprint('products', __name__)

def get_image_url(product):
    """Return the product image URL. Excel image_url takes priority."""
    existing = str(product.get('image_url', ''))
    if existing and existing != 'nan' and existing.startswith('https://images.unsplash.com/photo-'):
        return existing

    # Fallback: curated mapping by product_id
    pid = int(product.get('product_id', 1))
    IMAGES = {
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
    }
    base_pid = ((pid - 1) % 75) + 1
    photo_id = IMAGES.get(base_pid, 'photo-1525547719571-a2d4ac8945e2')
    return f'https://images.unsplash.com/{photo_id}?w=600&q=80'



@products_bp.route('/products', methods=['GET'])

def get_products():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    category = request.args.get('category', '')
    sort = request.args.get('sort', '')
    query = request.args.get('q', '').lower()
    
    df = data_manager.products_df.copy()
    
    # Reload fresh data each request
    data_manager.reload_data()
    df = data_manager.products_df.copy()
    
    if category:
        df = df[df['category'].str.lower() == category.lower()]
    
    if query:
        mask = (
            df['name'].str.lower().str.contains(query, na=False) |
            df['category'].str.lower().str.contains(query, na=False) |
            df.get('description', pd.Series(dtype=str)).str.lower().str.contains(query, na=False)
        )
        df = df[mask]
    
    if sort == 'price_asc':
        df = df.sort_values('price')
    elif sort == 'price_desc':
        df = df.sort_values('price', ascending=False)
    elif sort == 'rating':
        df = df.sort_values('rating', ascending=False)
    elif sort == 'newest':
        df = df.sort_values('product_id', ascending=False)
    
    total = len(df)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    page_df = df.iloc[start_idx:end_idx]
    
    products = []
    for _, p in page_df.iterrows():
        prod = p.to_dict()
        # Clean NaN values
        for k, v in list(prod.items()):
            try:
                if pd.isna(v):
                    prod[k] = '' if k not in ['price','stock','rating','product_id'] else 0
            except (TypeError, ValueError):
                pass
        # Always generate a properly-sized image URL via get_image_url()
        prod['image_url'] = get_image_url(prod)
        products.append(prod)
    
    return jsonify({
        "products": products,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total // limit) + (1 if total % limit > 0 else 0)
    }), 200

@products_bp.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    data_manager.reload_data()
    product = data_manager.products_df[data_manager.products_df['product_id'] == product_id]
    if product.empty:
        return jsonify({"error": "Product not found"}), 404
    
    prod = product.to_dict(orient='records')[0]
    for k, v in list(prod.items()):
        try:
            if pd.isna(v):
                prod[k] = '' if k not in ['price','stock','rating','product_id'] else 0
        except (TypeError, ValueError):
            pass
    prod['image_url'] = get_image_url(prod)
    return jsonify(prod), 200

@products_bp.route('/product/<int:product_id>/similar', methods=['GET'])
def get_similar_products(product_id):
    data_manager.reload_data()
    product = data_manager.products_df[data_manager.products_df['product_id'] == product_id]
    if product.empty:
        return jsonify({"error": "Product not found"}), 404
    
    cat = product.iloc[0]['category']
    similar = data_manager.products_df[
        (data_manager.products_df['category'] == cat) &
        (data_manager.products_df['product_id'] != product_id)
    ].head(8)
    
    results = []
    for _, p in similar.iterrows():
        prod = p.to_dict()
        for k, v in list(prod.items()):
            try:
                if pd.isna(v):
                    prod[k] = '' if k not in ['price','stock','rating','product_id'] else 0
            except (TypeError, ValueError):
                pass
        prod['image_url'] = get_image_url(prod)
        results.append(prod)
    
    return jsonify({"similar_products": results, "category": cat}), 200

@products_bp.route('/categories', methods=['GET'])
def get_categories():
    data_manager.reload_data()
    df = data_manager.products_df
    cats = df.groupby('category').size().reset_index(name='count')
    result = [{"name": row['category'], "count": int(row['count'])} for _, row in cats.iterrows()]
    return jsonify({"categories": result}), 200

@products_bp.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('q', '').lower()
    category = request.args.get('category', '')
    data_manager.reload_data()
    df = data_manager.products_df.copy()
    
    if query:
        mask = (
            df['name'].str.lower().str.contains(query, na=False) |
            df['category'].str.lower().str.contains(query, na=False)
        )
        if 'description' in df.columns:
            mask = mask | df['description'].str.lower().str.contains(query, na=False)
        df = df[mask]
    if category:
        df = df[df['category'].str.lower() == category.lower()]
    
    results = []
    for _, p in df.head(20).iterrows():
        prod = p.to_dict()
        for k, v in list(prod.items()):
            try:
                if pd.isna(v):
                    prod[k] = '' if k not in ['price','stock','rating','product_id'] else 0
            except (TypeError, ValueError):
                pass
        prod['image_url'] = get_image_url(prod)
        results.append(prod)
    
    return jsonify(results), 200
