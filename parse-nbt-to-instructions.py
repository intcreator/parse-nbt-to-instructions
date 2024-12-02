import nbtlib

nbt_file = nbtlib.load("brandon-mosaic-full.nbt")

chunks = {}
BLOCKS_PER_CHUNK = 16

materials = []
for material in nbt_file["palette"]:
    materials.append(material["Name"][10:])

for block in nbt_file["blocks"]:
    x_coord = block["pos"][0]
    y_coord = block["pos"][1]
    z_coord = block["pos"][2]
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
    current_chunk[z_coord][x_coord] = {
        "material": materials[block["state"]],
        "y_coord": y_coord,
    }

# print(chunks)

for chunk_x, chunk_row in chunks.items():
    for chunk_z, chunk in chunk_row.items():
        chunk_file_data = ""
        chunk_materials = {}
        for coord_z, row in chunk.items():
            chunk_file_data += f"z: {str(int(coord_z)): <5}"
            for coord_x, block in row.items():
                material = str(block["material"])
                if material not in chunk_materials:
                    chunk_materials[material] = 0
                chunk_materials[material] += 1
                chunk_file_data += f"{material: <25}"
            chunk_file_data += "\n"
        chunk_file_data += "\nMaterials:\n"
        for material in dict(sorted(chunk_materials.items(), key=lambda item: item[1])):
            chunk_file_data += f"{material: <25} {chunk_materials[material]}\n"
        with open(f"chunks/{chunk_x}-{chunk_z}.txt", "w") as chunk_file:
            chunk_file.write(chunk_file_data)
