materials_in_order = [
    "white_wool",
    "light_gray_wool",
    "gray_wool",
    "black_wool",
    "brown_wool",
    "red_wool",
    "orange_wool",
    "cyan_wool",
    "light_blue_wool",
    "blue_wool",
    "pink_wool",
    "white_terracotta",
    "light_gray_terracotta",
    "gray_terracotta",
    "black_terracotta",
    "brown_terracotta",
    "red_terracotta",
    "orange_terracotta",
    "yellow_terracotta",
    "lime_terracotta",
    "green_terracotta",
    "cyan_terracotta",
    "light_blue_terracotta",
    "blue_terracotta",
    "purple_terracotta",
    "magenta_terracotta",
    "pink_terracotta",
    "birch_log (sideways)",
    "birch_log",
    "birch_planks",
    "jungle_planks",
    "spruce_planks",
    "oak_planks",
    "warped_hyphae",
    "crimson_hyphae",
    "mushroom_stem",
    "raw_iron_block",
    "iron_block",
    "gold_block",
    "cobblestone",
    "cobbled_deepslate",
    "clay",
    "netherrack",
    "warped_nylium",
    "crimson_nylium",
    "glow_lichen (horizontal)",
    "glow_lichen",
]

material_order_dict = {}

for material_index, material in enumerate(materials_in_order):
    material_order_dict[material] = material_index