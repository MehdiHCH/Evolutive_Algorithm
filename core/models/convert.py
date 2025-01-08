from math import math

def convert(La,Lo):
    fi0=sum(La)/len(La)
    psi0=sum(Lo)/len(Lo)

    fi=La*(math.pi/180)
    psi=Lo*(math.pi/180)
    r=6371
    x=r*math.cos(psi-psi0)*(psi)
    y=r*(fi-fi0)

    return x,y 


import math

def convert_to_cartesian(data, phi0=0, lambda0=0, R=6371):
    """
    Convert geographic coordinates (longitude, latitude) to Cartesian coordinates (x, y)
    using an equirectangular projection.

    Parameters:
    - data (str): Multiline string of coordinates with format "index longitude latitude".
    - phi0 (float): Central latitude in degrees (default: 0, for equator).
    - lambda0 (float): Central longitude in degrees (default: 0, for prime meridian).
    - R (float): Radius of the Earth in kilometers (default: 6371 km).

    Returns:
    - list of tuples: [(index, x, y), ...]
    """
    cartesian_coords = []
    phi0_rad = math.radians(phi0)
    lambda0_rad = math.radians(lambda0)

    for line in data.strip().split("\n"):
        parts = line.split()
        if len(parts) == 3: 
            index = int(parts[0])
            longitude = float(parts[1])
            latitude = float(parts[2])

           
            lambda_rad = math.radians(longitude)
            phi_rad = math.radians(latitude)

            x = R * math.cos(phi0_rad) * (lambda_rad - lambda0_rad)
            y = R * (phi_rad - phi0_rad)

            cartesian_coords.append((index, x, y))

    return cartesian_coords
