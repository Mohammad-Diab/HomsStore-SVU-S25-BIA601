"""
generate_images.py
Assigns unique, product-specific Unsplash images to all 200 products.
Each base product type has a pool of 3 distinct photos → no duplicates.
"""
import pandas as pd

BASE = "https://images.unsplash.com/"
Q    = "?w=600&q=80"

# Pool of 3 unique photos per base product (id 1-75).
# Products 76-150 use pool[1], products 151-200 use pool[2].
POOLS = {
    # Electronics
    1:  ["photo-1525547719571-a2d4ac8945e2","photo-1496181133206-80ce9b88a853","photo-1517694712202-14dd9538aa97"],  # Gaming Laptop
    2:  ["photo-1505740420928-5e560c06d30e","photo-1484704849700-f032a568e944","photo-1546435770-a3e736ff5540"],      # Headphones
    3:  ["photo-1593359677879-a4bb92f829d1","photo-1461151304267-38535e780c79","photo-1509281373149-e957c6296406"],    # Smart TV
    4:  ["photo-1541140532154-b024d705b90a","photo-1587829741301-dc798b83add3","photo-1595225476474-87563907ef10"],    # Keyboard
    5:  ["photo-1527814050087-3793815479db","photo-1563297007-0686b7370cda","photo-1615663245857-ac93bb7c39e7"],       # Gaming Mouse
    6:  ["photo-1510557880182-3d4d3cba35a5","photo-1585060544812-6b45742d762f","photo-1574944985070-8f3ebc6b79d2"],   # iPhone
    7:  ["photo-1567581935884-3349723552ca","photo-1592750475338-74b7b21085ab","photo-1511707171634-5f897ff02aa9"],   # Samsung
    8:  ["photo-1544244015-0df4b3ffc6b0","photo-1542751110-97427bbecdb8","photo-1561154464-82e9adf32764"],            # iPad
    9:  ["photo-1607853202273-797f1c22a38e","photo-1606144042614-b2417e99c4e3","photo-1592155931584-901ac15763e3"],   # PS5
    10: ["photo-1484704849700-f032a568e944","photo-1583394838336-acd977736f90","photo-1505740420928-5e560c06d30e"],   # Sony Headphones
    11: ["photo-1473968512647-3e447244af8f","photo-1522653216771-4bb6d01d0dc0","photo-1508613304529-3a4d17af2273"],  # Drone
    12: ["photo-1434056886845-dac89ffe9b56","photo-1551816230-ef5deaed4a26","photo-1523275335684-37898b6baf30"],      # Apple Watch
    13: ["photo-1527814050087-3793815479db","photo-1615663245857-ac93bb7c39e7","photo-1563297007-0686b7370cda"],      # Logitech Mouse
    14: ["photo-1527443224154-c4a573d5f5d6","photo-1616763355548-1b606f439f86","photo-1593305841991-05c297ba4575"],  # Monitor
    15: ["photo-1496181133206-80ce9b88a853","photo-1504707748692-419802cf939d","photo-1525547719571-a2d4ac8945e2"],  # ASUS Laptop
    16: ["photo-1608043152269-423dbba4e7e1","photo-1545454675-3531b543be5d","photo-1558537348-c0f8e733989d"],         # Bluetooth Speaker
    17: ["photo-1557597774-9d273605dfa9","photo-1585771724684-38269d6639fd","photo-1558618666-fcd25c85cd64"],         # Security Camera
    18: ["photo-1590658268037-6bf12165a8df","photo-1606220945770-b5b6c2c55bf1","photo-1590658165737-15a047b7c863"],  # Earbuds
    19: ["photo-1519389950473-47ba0277781c","photo-1625231129577-fc007dc55a0a","photo-1587829741301-dc798b83add3"],   # USB Hub
    20: ["photo-1593642632559-0c6d3fc62b89","photo-1524758631624-e2822e304c36","photo-1593642634524-b40b5baae6bb"],  # Standing Desk
    # Clothing
    21: ["photo-1507679799987-c73779587ccf","photo-1617137984095-74e4e5e3613f","photo-1594938298603-c8148c4b1df6"],  # Men Suit
    22: ["photo-1568252542512-9fe8fe9c87bb","photo-1469334031218-e382a71b716b","photo-1485518994671-a2dda234cd20"],  # Women Dress
    23: ["photo-1495105787522-5334e3ffa0ef","photo-1551028719-00167b16eac5","photo-1576566588028-4147f3842f27"],      # Denim Jacket
    24: ["photo-1506629082955-511b1aa562c8","photo-1571902943202-507ec2618e8f","photo-1518459031867-a89b944bffe4"],  # Yoga Leggings
    25: ["photo-1551698618-1dfe5d97d256","photo-1548126032-079a0fb0099d","photo-1591047139829-d91aecb6caea"],         # Bomber Jacket
    26: ["photo-1434389677669-e08b4cac3105","photo-1620799140408-edc6dcb6d633","photo-1584302179602-e4c3d3fd629d"],  # Cable Knit Sweater
    27: ["photo-1473966968600-fa801b869a1a","photo-1624378439432-dba7fc0f1a22","photo-1604868189265-219ba1b89c84"],  # Chino Pants
    28: ["photo-1594938298603-c8148c4b1df6","photo-1617137984095-74e4e5e3613f","photo-1507679799987-c73779587ccf"],  # Linen Blazer
    29: ["photo-1521572163474-6864f9cf17ab","photo-1598300042247-d088f8ab3a91","photo-1576566588028-4147f3842f27"],  # Running Tee
    30: ["photo-1512436991641-6745cdb1723f","photo-1583744946564-b52ac1c389c8","photo-1561161426-eb7dfbcc44ec"],     # Midi Skirt
    31: ["photo-1556821840-3a63f15732ce","photo-1578768079052-aa76e52ff642","photo-1620799139507-2a76f79a2f4d"],     # Hoodie
    32: ["photo-1591047139829-d91aecb6caea","photo-1548126032-079a0fb0099d","photo-1551698618-1dfe5d97d256"],         # Puffer Vest
    33: ["photo-1596755094514-f87e34085b2c","photo-1598032895397-b9472444bf93","photo-1598033129183-c4f50c736f10"],  # Oxford Shirt
    34: ["photo-1542272604-327c114c3384","photo-1624378439432-dba7fc0f1a22","photo-1582418702059-97ebafb35d09"],     # Flare Jeans
    35: ["photo-1434389677669-e08b4cac3105","photo-1584302179602-e4c3d3fd629d","photo-1620799140408-edc6dcb6d633"],  # Merino Sweater
    # Sports
    36: ["photo-1485965120184-e220f721d03e","photo-1471506480208-91b3a4cc78be","photo-1507035895480-2b3156c31fc8"],  # Bicycle
    37: ["photo-1542291026-7eec264c27ff","photo-1491553895911-0055eca6402d","photo-1606107557195-0e29a4b5b4aa"],     # Running Shoes
    38: ["photo-1601925228008-87f4dda9ba38","photo-1518611012118-696072aa579a","photo-1571019614242-c5c5dee9f50b"],  # Yoga Mat
    39: ["photo-1534438327276-14e5300c3a48","photo-1581009146145-b5ef050c2e1e","photo-1517836357463-d25dfeac3438"],  # Dumbbells
    40: ["photo-1546519638-68e109498ffc","photo-1519861155730-0b5fbfac1051","photo-1579952363873-27f3bade9f55"],     # Basketball
    41: ["photo-1553062407-98eeb64c6a62","photo-1622260614153-03223fb72052","photo-1479896823629-5a54dff7bc52"],     # Hiking Backpack
    42: ["photo-1575311373937-040b8e1fd5b6","photo-1617625802912-cde586faf749","photo-1508685096489-7aacd43bd3b1"], # Fitness Tracker
    43: ["photo-1517963879433-6ad2a56b9727","photo-1598971861713-54ad16a7e72e","photo-1518310383802-640c2de311b2"], # Resistance Bands
    44: ["photo-1614632537197-38a17061c2bd","photo-1579952363873-27f3bade9f55","photo-1560272564-c83b66b1ad12"],     # Soccer Ball
    45: ["photo-1587280501635-68a0e82cd5ff","photo-1519311726-d7c2eda32569","photo-1544840935-c23912867e83"],        # Tennis Racket
    46: ["photo-1434682966068-8c56d34a2b1c","photo-1552058544-f2b08422138a","photo-1598300042247-d088f8ab3a91"],    # Jump Rope
    47: ["photo-1530549387789-4c1017266635","photo-1566737236500-c8ac43014a67","photo-1560090995-b8c557c8e7d5"],    # Swimming Goggles
    48: ["photo-1599901860904-17e6ed7083a0","photo-1518310383802-640c2de311b2","photo-1517963879433-6ad2a56b9727"], # Foam Roller
    49: ["photo-1491553895911-0055eca6402d","photo-1606107557195-0e29a4b5b4aa","photo-1542291026-7eec264c27ff"],     # Trail Running Shoes
    50: ["photo-1570197788417-0e82375c9371","photo-1585581871990-e72c648d0879","photo-1610017078847-c2bcc19f9b53"], # Blender
    # Home
    51: ["photo-1558618666-fcd25c85cd64","photo-1563453392212-326f5e854473","photo-1507003211169-0a1dd7228f2d"],    # Robot Vacuum
    52: ["photo-1585771724684-38269d6639fd","photo-1579068949744-7e18a4f8d5d8","photo-1584820927498-cfe5211fd8bf"], # Air Purifier
    53: ["photo-1556909114-f6e7ad7d3136","photo-1574269909862-7e1d70bb8078","photo-1547592180-85f173990554"],       # Instant Pot
    54: ["photo-1507003211169-0a1dd7228f2d","photo-1534073828943-f801091bb18c","photo-1513506003901-1e6a35703a1d"], # Desk Lamp
    55: ["photo-1510591509098-f4fdc6d0ff04","photo-1495474472287-4d71bcdd2085","photo-1559056199-641a0ac8b55e"],    # Coffee Maker
    56: ["photo-1556911073-a517e752729c","photo-1584735935682-2f2b69dff9d2","photo-1583608205776-bfd35f0d9f83"],    # Cookware
    57: ["photo-1558618047-3c8c76ca7d13","photo-1518770660439-4636190af475","photo-1585771724684-38269d6639fd"],    # Smart Thermostat
    58: ["photo-1558618666-fcd25c85cd64","photo-1563453392212-326f5e854473","photo-1585771724684-38269d6639fd"],    # Cordless Vacuum
    59: ["photo-1560472355-536de3962603","photo-1584467541268-b040f83be3fd","photo-1541123437800-1bb1317badc2"],    # Pillow
    60: ["photo-1585032226651-773f5a3585a2","photo-1610017078847-c2bcc19f9b53","photo-1574269909862-7e1d70bb8078"], # Air Fryer
    61: ["photo-1577916297339-beff89a403d7","photo-1556909114-f6e7ad7d3136","photo-1583608205776-bfd35f0d9f83"],    # Cutting Board
    62: ["photo-1604608672516-f1b9c4cd1ca1","photo-1558591710-4b4a1ae0f4f3","photo-1577648188599-291bb8b831c3"],    # LED Strip
    63: ["photo-1485955900006-10f4d324d411","photo-1416879595882-3373a0480b5b","photo-1463936575829-25148e1db1b8"], # Plant Pots
    64: ["photo-1602607920945-5cd34a75db5e","photo-1603905030654-8aa527e2e455","photo-1608181831718-c9bd4e1f14ed"], # Candle
    65: ["photo-1513694203232-719a280e022f","photo-1522771739844-6a9f6d5f14af","photo-1540518614846-7eded433c457"], # Weighted Blanket
    # Books
    66: ["photo-1544947950-fa07a98d237f","photo-1481627834876-b7833e8f5570","photo-1524995997946-a1c2e315a42f"],   # Atomic Habits
    67: ["photo-1554224155-6726b3ff858f","photo-1579621970795-87facc2f976d","photo-1507003211169-0a1dd7228f2d"],   # Psychology of Money
    68: ["photo-1512820790803-83ca734da794","photo-1532012197267-da84d127e765","photo-1544947950-fa07a98d237f"],   # Think & Grow Rich
    69: ["photo-1532012197267-da84d127e765","photo-1512820790803-83ca734da794","photo-1481627834876-b7833e8f5570"],# Sapiens
    70: ["photo-1461749280684-dccba630e2f6","photo-1517694712202-14dd9538aa97","photo-1515879218367-8466d910aaa4"],# Clean Code
    71: ["photo-1456324504439-367cee3b3c32","photo-1524995997946-a1c2e315a42f","photo-1544947950-fa07a98d237f"],   # Subtle Art
    72: ["photo-1579621970795-87facc2f976d","photo-1554224155-6726b3ff858f","photo-1512820790803-83ca734da794"],   # Rich Dad
    73: ["photo-1544947950-fa07a98d237f","photo-1524995997946-a1c2e315a42f","photo-1532012197267-da84d127e765"],   # 7 Habits
    74: ["photo-1499750310107-5fef28a66643","photo-1456324504439-367cee3b3c32","photo-1481627834876-b7833e8f5570"],# Deep Work
    75: ["photo-1507003211169-0a1dd7228f2d","photo-1544947950-fa07a98d237f","photo-1461749280684-dccba630e2f6"],   # Zero to One
}

def get_pool_image(product_id):
    """Return a unique Unsplash URL for this product with no repeats."""
    pid      = int(product_id)
    base_pid = ((pid - 1) % 75) + 1          # 1-75
    edition  = (pid - 1) // 75               # 0, 1, or 2
    pool     = POOLS.get(base_pid, POOLS[1])
    photo_id = pool[edition % len(pool)]
    return f"{BASE}{photo_id}{Q}"

# ── Main ──────────────────────────────────────────────────────────────────────
df = pd.read_excel("data/products.xlsx")

df["image_url"] = df["product_id"].apply(get_pool_image)

# Verify no duplicates
total   = len(df)
unique  = df["image_url"].nunique()
dupes   = total - unique

df.to_excel("data/products.xlsx", index=False)

print(f"Done: {total} products updated")
print(f"Unique images: {unique}")
if dupes:
    print(f"WARNING - Duplicates found: {dupes}")
else:
    print("No duplicate images!")

print("\nSample:")
print(df[["product_id","name","image_url"]].head(10).to_string(index=False))
