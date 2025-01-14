from core.utils import spherical_to_cartesian, get_scale
from core.io_utils import read_cities, save_cities
from tqdm import tqdm

file_path = "data/maroc.txt"

with open(file_path, "r") as file:
    num_cities = int(file.readline().strip())

    coords = []

    for _ in tqdm(range(num_cities), desc="Processing Get Scalling factor : "):
        line = file.readline().strip().split()
        ID = int(line[0])
        latitude, longitude = map(float, line[1:])

        coords.append((ID, latitude, longitude))
    
    scale, min_values, max_values, padding  = get_scale(coords)


    cartesian_coords = []

    for i in tqdm(range(num_cities), desc="Processing Conversion : "):
        ID, latitude, longitude = coords[i]
        
        cartesian_coord = spherical_to_cartesian(spherical_coords=(ID, latitude, longitude), scale=scale, min_values=min_values, max_values=max_values, padding=padding)
        
        cartesian_coords.append(cartesian_coord)

save_cities("data/maroc_1.txt", cartesian_coords)
