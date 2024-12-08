import nbtlib
import os
import textwrap

nbt_file = nbtlib.load("mosaic_full.nbt")
with open("mosaic_full.snbt", "w") as snbt_file:
    snbt_file.write(nbt_file.snbt(indent=4))

chunks = {}
BLOCKS_PER_CHUNK = 16
BLOCKS_PER_MAP = 128
# modify these as needed
STARTING_X_COORD = 1344
STARTING_Y_COORD = 68
STARTING_Z_COORD = 1599
INSTRUCTIONS_FOLDER_NAME = "chunks"

half_map_width = BLOCKS_PER_MAP / 2
map_x_offset = (STARTING_X_COORD - half_map_width) / BLOCKS_PER_MAP
map_z_offset = (STARTING_Z_COORD + 1 - half_map_width) / BLOCKS_PER_MAP

if map_x_offset != int(map_x_offset) or map_z_offset != int(map_z_offset):
    print(
        "warning: starting coordinates are not aligned with map coordinates! this means art scaled to map size will show naturally generated terrain"
    )

materials = []
for material in nbt_file["palette"]:
    materials.append(material["Name"][10:])

all_materials = {}
highest_y_coord = -64

for block in nbt_file["blocks"]:
    x_coord = STARTING_X_COORD + block["pos"][0]
    y_coord = STARTING_Y_COORD + block["pos"][1]
    if y_coord > highest_y_coord:
        highest_y_coord = y_coord
    z_coord = STARTING_Z_COORD + block["pos"][2]
    x_chunk = int(x_coord / BLOCKS_PER_CHUNK)
    z_chunk = int(z_coord / BLOCKS_PER_CHUNK)
    if x_chunk not in chunks:
        chunks[x_chunk] = {}
    if z_chunk not in chunks[x_chunk]:
        chunks[x_chunk][z_chunk] = {}
    current_chunk = chunks[x_chunk][z_chunk]
    if z_coord not in current_chunk:
        current_chunk[z_coord] = {}
    if x_coord in current_chunk[z_coord]:
        print(x_coord, " already in ", z_coord, "!")
        break
    material = materials[block["state"]]
    palette_material = nbt_file["palette"][block["state"]]
    current_chunk[z_coord][x_coord] = {
        "material": material,
        "y_coord": y_coord,
    }
    if material not in all_materials:
        all_materials[material] = 0
    all_materials[material] += 1
    if "Properties" in palette_material:
        current_chunk[z_coord][x_coord]["Properties"] = palette_material["Properties"]

print(f"highest y coord is {int(highest_y_coord)}")

if not os.path.exists(INSTRUCTIONS_FOLDER_NAME):
    os.makedirs(INSTRUCTIONS_FOLDER_NAME)
for filename in os.listdir(INSTRUCTIONS_FOLDER_NAME):
    os.remove(f"{INSTRUCTIONS_FOLDER_NAME}/{filename}")
for chunk_x, chunk_row in chunks.items():
    for chunk_z, chunk in chunk_row.items():
        chunk_file_data = ""
        # chunk_file_data = f"{'':<8}"
        chunk_materials = {}
        # x coord column headers
        # for coord_x in list(chunk.values())[0]:
        #     chunk_file_data += f"x: {str(int(coord_x)): <22}"
        # chunk_file_data += "\n"
        for coord_z, row in sorted(chunk.items(), reverse=True):
            # z coord row headers
            # chunk_file_data += f"z: {str(int(coord_z)): <5}"
            for coord_x, block in row.items():
                material = str(block["material"])
                if "Properties" in block:
                    material += (
                        " (horizontal)"
                        if "down" in block["Properties"] and block["Properties"]["down"]
                        else ""
                    )
                    material += (
                        " (sideways)"
                        if "axis" in block["Properties"]
                        and block["Properties"]["axis"] == "x"
                        else ""
                    )
                if material not in chunk_materials:
                    chunk_materials[material] = 0
                chunk_materials[material] += 1
                coord_y = block["y_coord"]
                chunk_file_data += (
                    f"{coord_x:<4} {coord_y:<3} {coord_z:<4} {material: <25}"
                )
            chunk_file_data += "\n"
        chunk_file_data += "\nMaterials:\n"
        for material in dict(
            sorted(chunk_materials.items(), key=lambda item: item[1], reverse=True)
        ):
            chunk_file_data += f"{material: <25} {chunk_materials[material]}\n"
        with open(f"chunks/{chunk_x}-{chunk_z}.txt", "w") as chunk_file:
            chunk_file.write(chunk_file_data)

materials_list = f"All Materials:\n\n{'type':<25} {'quantity': <10} {'stacks': <8} {'double chests': <8}\n\n"
for material in dict(
    sorted(all_materials.items(), key=lambda item: item[1], reverse=True)
):
    materials_list += f"{material: <25} {all_materials[material]: <10} {round(all_materials[material] / 64, 1): <8} {round(all_materials[material] / (64 * 27 * 2), 1): <8}\n"

with open(f"materials_list.txt", "w") as materials_list_file:
    materials_list_file.write(materials_list)
