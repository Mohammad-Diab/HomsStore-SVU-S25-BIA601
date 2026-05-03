import pandas as pd
import random

products = [
    # Electronics
    (1,"Gaming Laptop Pro 15","Electronics","High-performance gaming laptop with RTX 4070, 32GB RAM, 165Hz display",1299.99,45,4.7,"Laptop,RTX4070,32GB RAM,1TB SSD,165Hz,Win11"),
    (2,"Wireless Noise-Cancelling Headphones","Electronics","Premium ANC headphones with 40h battery and Hi-Res Audio",249.99,120,4.8,"Bluetooth 5.3,40h battery,ANC,Hi-Res Audio,USB-C"),
    (3,"4K Smart Android TV 55\"","Electronics","Ultra HD Smart TV with Google TV and Dolby Vision",699.99,30,4.6,"4K,55inch,Google TV,Dolby Vision,HDR10+,HDMI 2.1"),
    (4,"Mechanical Gaming Keyboard RGB","Electronics","Full-size mechanical keyboard with Cherry MX switches",129.99,85,4.5,"Cherry MX Red,RGB,USB-C,Anti-ghosting,Wired"),
    (5,"Wireless Gaming Mouse 25K DPI","Electronics","Ultra-lightweight wireless gaming mouse",89.99,95,4.7,"25000 DPI,Wireless,70h battery,RGB,6 buttons"),
    (6,"iPhone 15 Pro Max 256GB","Electronics","Apple flagship with A17 Pro chip and 48MP ProRAW camera",1199.99,25,4.9,"A17 Pro,256GB,48MP Camera,5G,Titanium Frame"),
    (7,"Samsung Galaxy S24 Ultra","Electronics","Premium Android with S Pen and 200MP camera",1099.99,20,4.8,"Snapdragon 8 Gen3,512GB,200MP,S Pen,5G"),
    (8,"iPad Pro 12.9 M2 Chip","Electronics","Professional tablet with M2 chip and Liquid Retina XDR display",1099.99,35,4.8,"M2 Chip,12.9inch,Liquid Retina XDR,5G,USB-C"),
    (9,"Sony PlayStation 5 Console","Electronics","Next-gen gaming console with ultra-high speed SSD",499.99,15,4.9,"825GB SSD,4K 120fps,Ray Tracing,DualSense,Blu-ray"),
    (10,"Sony WH-1000XM5 Headphones","Electronics","Industry-leading noise cancellation with 30h battery",349.99,60,4.8,"30h battery,ANC,360 Audio,USB-C,LDAC"),
    (11,"DJI Mini 4 Pro Drone","Electronics","Compact 4K drone with omnidirectional obstacle sensing",759.99,20,4.7,"4K 60fps,34min flight,Omnidirectional sensors,GPS"),
    (12,"Apple Watch Series 9 45mm","Electronics","Advanced smartwatch with Double Tap gesture",429.99,50,4.8,"S9 Chip,45mm,Always-On Display,GPS+Cellular,ECG"),
    (13,"Logitech MX Master 3S Mouse","Electronics","Advanced wireless mouse with 8K DPI MagSpeed scroll",99.99,110,4.7,"8000 DPI,USB-C,MagSpeed Scroll,Multi-device"),
    (14,"Dell UltraSharp 27 4K Monitor","Electronics","Professional 4K IPS monitor with USB-C 90W charging",599.99,40,4.6,"27inch,4K IPS,100% sRGB,USB-C 90W,HDMI 2.0"),
    (15,"ASUS ROG Zephyrus G14 Laptop","Electronics","Ultra-slim gaming laptop with AMD Ryzen 9",1499.99,30,4.7,"Ryzen 9,RX 6700S,16GB RAM,14inch 144Hz"),
    (16,"Portable Bluetooth Speaker","Electronics","Waterproof speaker with 360 sound and 24h battery",79.99,150,4.5,"360 Sound,24h battery,IPX7,Bluetooth 5.0"),
    (17,"Smart Home Security Camera","Electronics","1080p indoor security camera with night vision",49.99,200,4.4,"1080p,Night Vision,Motion Detection,Two-Way Audio"),
    (18,"Wireless Earbuds Pro ANC","Electronics","True wireless earbuds with active noise cancellation",149.99,90,4.6,"ANC,6h playtime,Transparency mode,IPX4,Fast Charge"),
    (19,"USB-C Hub 10-in-1","Electronics","Multiport adapter with 4K HDMI and 100W PD charging",59.99,180,4.5,"4K HDMI,100W PD,SD Card,USB 3.0,Gigabit Ethernet"),
    (20,"Electric Standing Desk","Electronics","Height-adjustable standing desk with memory settings",499.99,25,4.7,"Electric Motor,4 Memory Settings,1800x800mm,Anti-Collision"),
    # Clothing
    (21,"Men Classic Slim Fit Suit","Clothing","Professional slim-fit suit in premium wool blend",299.99,60,4.4,"Wool Blend,Slim Fit,2-Button,Wrinkle Resistant"),
    (22,"Women Floral Maxi Dress","Clothing","Elegant floral-print maxi dress with ruffle detailing",79.99,90,4.5,"100% Polyester,Maxi Length,Adjustable Straps,Flowy"),
    (23,"Men Casual Denim Jacket","Clothing","Classic stone-washed denim jacket",89.99,75,4.6,"100% Cotton Denim,Stone Wash,Button Front,Chest Pockets"),
    (24,"Women High-Waist Yoga Leggings","Clothing","Ultra-soft 4-way stretch leggings with pocket",49.99,130,4.7,"Nylon/Spandex,4-Way Stretch,High Waist,Pocket"),
    (25,"Men Bomber Jacket Olive Green","Clothing","Premium bomber jacket with ribbed cuffs",129.99,55,4.5,"Polyester Shell,Quilted Lining,Zip Pockets,Water Resistant"),
    (26,"Women Oversized Cable Knit Sweater","Clothing","Cozy oversized merino wool blend sweater",99.99,80,4.6,"Merino Wool Blend,Oversized Fit,Cable Knit,Drop Shoulder"),
    (27,"Men Premium Chino Pants","Clothing","Versatile slim-fit stretch cotton chinos",69.99,100,4.4,"Stretch Cotton,Slim Fit,Flat Front,Hidden Pocket"),
    (28,"Women Linen Summer Blazer","Clothing","Lightweight linen blazer for office or casual wear",119.99,45,4.3,"55% Linen 45% Viscose,Relaxed Fit,Notch Lapel"),
    (29,"Men Performance Running Tee","Clothing","Moisture-wicking running t-shirt with reflective details",34.99,150,4.6,"Recycled Polyester,Moisture Wicking,Reflective,UPF 40+"),
    (30,"Women Wrap Midi Skirt","Clothing","Versatile wrap skirt in soft crepe fabric",59.99,70,4.4,"100% Viscose,Midi Length,Wrap Style,Machine Wash"),
    (31,"Men Heavyweight Hooded Sweatshirt","Clothing","Cozy 400gsm fleece hoodie with kangaroo pocket",89.99,95,4.7,"80% Cotton 20% Polyester,400GSM Fleece,Kangaroo Pocket"),
    (32,"Women Puffer Vest Sleeveless","Clothing","Lightweight insulated puffer vest",79.99,65,4.5,"Water Resistant Shell,Recycled Fill,Quilted,Packable"),
    (33,"Men Oxford Button-Down Shirt","Clothing","Classic Oxford shirt in breathable cotton",54.99,85,4.4,"100% Cotton Oxford,Button-Down Collar,Regular Fit"),
    (34,"Women Flare Jeans High Rise","Clothing","Vintage-inspired high-rise flare jeans",69.99,75,4.5,"98% Cotton 2% Elastane,High Rise,Flare Leg,5-Pocket"),
    (35,"Men Merino Wool V-Neck Sweater","Clothing","Ultra-fine merino wool sweater in classic V-neck",119.99,55,4.6,"100% Merino Wool,V-Neck,Ribbed Cuffs,Machine Wash"),
    # Sports
    (36,"Carbon Road Bicycle 21-Speed","Sports","Lightweight carbon road bike with Shimano groupset",899.99,10,4.7,"Carbon Frame,21-Speed Shimano,700C Wheels,Disc Brakes"),
    (37,"Men Running Shoes Air Cushion","Sports","Ultra-responsive running shoes with air cushion",119.99,90,4.6,"Air Cushion,Knit Upper,Rubber Outsole,Reflective"),
    (38,"Yoga Mat Premium Non-Slip 6mm","Sports","Professional non-slip yoga mat with alignment guides",49.99,200,4.7,"TPE Material,6mm Thick,Non-Slip,Alignment Lines,Eco-Friendly"),
    (39,"Adjustable Dumbbell Set 5-52lbs","Sports","Space-saving adjustable dumbbell set",349.99,25,4.8,"5-52lbs,15 weight settings,Ergonomic Handle,Safety Lock"),
    (40,"Portable Basketball System 10ft","Sports","Adjustable portable basketball hoop for driveway",299.99,15,4.5,"10ft Height,44inch Backboard,Base Fill 35gal,Shatterproof"),
    (41,"Waterproof Hiking Backpack 50L","Sports","Durable 50L hiking backpack with rain cover",129.99,60,4.6,"50L Capacity,Waterproof,Hip Belt,Multiple Compartments,Rain Cover"),
    (42,"Smart Fitness Tracker Watch","Sports","Advanced fitness band with heart rate and SpO2",79.99,120,4.5,"SpO2 Monitor,Heart Rate,GPS,7-day battery,50m Water Resistant"),
    (43,"Resistance Bands Set 5 Levels","Sports","Professional resistance bands with accessories",29.99,175,4.6,"5 Resistance Levels,Natural Latex,Anti-Snap,Handles"),
    (44,"Professional Soccer Ball Size 5","Sports","FIFA Quality Pro certified soccer ball",39.99,80,4.5,"FIFA Quality Pro,Size 5,Hand Stitched,Butyl Bladder"),
    (45,"Tennis Racket Carbon Fiber Pro","Sports","Professional carbon fiber tennis racket",149.99,45,4.6,"Carbon Fiber,100 sq inch Head,285g,String Included"),
    (46,"Jump Rope Speed Cable 4mm","Sports","High-speed aluminium jump rope with ball bearings",24.99,300,4.7,"4mm Steel Cable,Ball Bearing,Adjustable Length,Counter"),
    (47,"Swimming Goggles Anti-Fog UV","Sports","Professional swimming goggles with UV400 protection",24.99,150,4.5,"Anti-Fog,UV400,Wide Lens,Silicone Gasket,Case Included"),
    (48,"Foam Roller Deep Tissue Massage","Sports","High-density foam roller for muscle recovery",34.99,220,4.6,"High Density EVA,33cm Length,Hollow Core,Grid Pattern"),
    (49,"Men Trail Running Shoes GTX","Sports","Waterproof Gore-Tex trail running shoes",169.99,55,4.7,"Gore-Tex,Vibram Outsole,Rock Plate,Wide Toe Box"),
    (50,"Portable Blender 300W USB","Sports","Compact USB-rechargeable blender for smoothies",49.99,180,4.4,"300W Motor,6 Blades,USB-C Charge,420ml,Travel Lid"),
    # Home
    (51,"Robot Vacuum Cleaner LiDAR","Home","Smart robot vacuum with LiDAR navigation and auto-empty",499.99,20,4.7,"LiDAR Navigation,Auto-Empty,Mopping,App Control,HEPA"),
    (52,"Air Purifier HEPA H13 500sqft","Home","True HEPA H13 air purifier for 500 sq ft rooms",199.99,40,4.8,"True HEPA H13,500sqft,PM2.5 Sensor,Auto Mode,CADR 300"),
    (53,"Instant Pot Duo 7-in-1 6Qt","Home","Multi-cooker combining 7 appliances in one",99.99,65,4.8,"7-in-1,6 Quart,14 Smart Programs,Stainless Steel"),
    (54,"Smart LED Desk Lamp Wireless Charging","Home","Modern desk lamp with wireless charging pad",69.99,90,4.6,"5 Color Temps,10W Wireless Charge,USB-A Port,Touch Control"),
    (55,"Nespresso Vertuo Next Coffee Maker","Home","Premium coffee machine with Centrifusion technology",179.99,35,4.7,"Centrifusion Tech,1.1L Tank,15 bar,Wifi+Bluetooth"),
    (56,"Non-Stick Cookware Set 10-Piece","Home","Professional granite-coated non-stick cookware set",149.99,50,4.6,"Granite Coating,Induction Safe,Oven Safe 450F,PFOA-Free"),
    (57,"Smart Thermostat WiFi Learning","Home","AI learning thermostat that adapts to your schedule",249.99,55,4.7,"WiFi,AI Learning,Remote Control,Alexa Compatible"),
    (58,"Cordless Stick Vacuum 250W","Home","Powerful cordless vacuum with 60-min runtime",299.99,45,4.6,"250W Brushless,60min Runtime,HEPA,LED Headlights"),
    (59,"Memory Foam Pillow Cooling Gel","Home","Ergonomic cervical memory foam pillow with cooling gel",79.99,130,4.7,"Cooling Gel,CertiPUR-US,Washable Cover,Hypoallergenic"),
    (60,"Digital Air Fryer 5.8QT XXL","Home","Extra-large digital air fryer with 8 presets",89.99,75,4.7,"5.8QT,8 Presets,Digital Display,Non-Stick Basket"),
    (61,"Bamboo Cutting Board Set 3-Piece","Home","Eco-friendly bamboo cutting board set with juice groove",39.99,160,4.5,"Organic Bamboo,3 Sizes,Juice Groove,Handle,Antimicrobial"),
    (62,"LED Strip Lights 32.8ft RGB","Home","Smart RGB LED strip with app control and music sync",29.99,200,4.5,"32.8ft,RGB+W,App Control,Music Sync,Alexa,Waterproof"),
    (63,"Ceramic Plant Pots Set of 3","Home","Modern minimalist ceramic pots with bamboo saucers",44.99,110,4.4,"Matte Ceramic,Drainage Hole,Bamboo Saucer,3 Sizes"),
    (64,"Scented Candle Luxury Gift Set","Home","Premium soy wax candles in hand-crafted glass jars",59.99,80,4.6,"Soy Wax,60h Burn Time,Natural Fragrance,Hand Poured"),
    (65,"Weighted Blanket 15lbs Cotton","Home","Therapeutic weighted blanket for better sleep",89.99,60,4.8,"15lbs,100% Cotton,Glass Beads,Washable,Breathable"),
    # Books
    (66,"Atomic Habits","Books","The life-changing book about building good habits",16.99,500,4.9,"Paperback,320 pages,Self-Help,Penguin Publishing"),
    (67,"The Psychology of Money","Books","Timeless lessons on wealth, greed, and happiness",14.99,400,4.8,"Paperback,256 pages,Finance,Harriman House"),
    (68,"Think and Grow Rich","Books","Classic personal development book on achieving success",12.99,350,4.7,"Paperback,238 pages,Classic,Self-Help,Original Edition"),
    (69,"Sapiens: A Brief History of Humankind","Books","Yuval Noah Hararis journey through human history",17.99,300,4.8,"Paperback,512 pages,History,Harper Perennial"),
    (70,"Clean Code - Robert C. Martin","Books","Handbook of agile software craftsmanship for developers",44.99,250,4.7,"Paperback,431 pages,Programming,Prentice Hall"),
    (71,"The Subtle Art of Not Giving F*ck","Books","Mark Mansons counterintuitive approach to good life",15.99,450,4.6,"Paperback,224 pages,Self-Help,Harper One"),
    (72,"Rich Dad Poor Dad","Books","Robert Kiyosakis personal finance classic on wealth",14.99,600,4.7,"Paperback,336 pages,Finance,Plata Publishing"),
    (73,"The 7 Habits of Highly Effective People","Books","Stephen Coveys powerful lessons on effectiveness",15.99,380,4.8,"Paperback,432 pages,Business,Simon & Schuster"),
    (74,"Deep Work - Cal Newport","Books","Rules for focused success in a distracted world",16.99,290,4.7,"Paperback,304 pages,Productivity,Grand Central Publishing"),
    (75,"Zero to One - Peter Thiel","Books","Notes on startups and how to build the future",14.99,320,4.6,"Paperback,224 pages,Business,Crown Business"),
]

# Extend to 200 with variations
random.seed(42)
categories = ["Electronics","Clothing","Sports","Home","Books"]
for i in range(76, 201):
    cat = categories[(i-1) % 5]
    base = products[(i-76) % len(products)]
    products.append((
        i,
        f"{base[1]} - Edition {i}",
        cat,
        base[3],
        round(base[4] * random.uniform(0.7, 1.3), 2),
        random.randint(10, 200),
        round(min(5.0, base[6] + random.uniform(-0.3, 0.3)), 1),
        base[7]
    ))

rows = []
for p in products:
    rows.append({
        "product_id": p[0],
        "name": p[1],
        "category": p[2],
        "description": p[3],
        "price": p[4],
        "stock": p[5],
        "rating": p[6],
        "specifications": p[7],
        "image_url": ""
    })

df = pd.DataFrame(rows)
df.to_excel("data/products.xlsx", index=False)
print(f"Done: {len(df)} products saved")
print(df[["product_id","name","category","price","rating"]].head())
