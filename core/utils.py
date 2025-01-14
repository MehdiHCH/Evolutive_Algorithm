import math

def haversine_distance(lat1, lon1, lat2, lon2, radius=6378.1370):
    """
    Calculate the great-circle distance between two points on the Earth's surface.
    
    Args:
        lat1, lon1: Latitude and longitude of the first point (in degrees).
        lat2, lon2: Latitude and longitude of the second point (in degrees).
        radius: Radius of the Earth (default is 6371 km).
    
    Returns:
        Distance between the two points (in the same unit as the radius).
    """
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Differences in coordinates
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    
    # Haversine formula
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Distance
    distance = radius * c
    return distance

def get_scale(spherical_coords, radius=6378.1370, canvas_size=(600, 600), padding=50):
    width, height = canvas_size
    min_x, min_y, max_x, max_y = float('inf'), float('inf'), float('-inf'), float('-inf')

    for ID, latitude, longitude in spherical_coords:
        # Convert degrees to radians
        theta = math.radians(90 - latitude)  # Latitude is converted to polar angle
        phi = math.radians(longitude)       # Longitude is the azimuthal angle

        # Apply spherical to cartesian formulas
        x = radius * math.sin(theta) * math.cos(phi)
        y = radius * math.sin(theta) * math.sin(phi)
        z = radius * math.cos(theta)

        # Update bounds
        min_x, max_x = min(min_x, x), max(max_x, x)
        min_y, max_y = min(min_y, y), max(max_y, y)

    # Scale cartesian coordinates to canvas dimensions
    scale_x = (width - 2 * padding) / (max_x - min_x) if max_x != min_x else 1
    scale_y = (height - 2 * padding) / (max_y - min_y) if max_y != min_y else 1
    scale = min(scale_x, scale_y)  # Uniform scaling to maintain aspect ratio

    min_values = (min_x, min_y)
    max_values = (max_x, max_y)

    return scale, min_values, max_values, padding

def spherical_to_cartesian(spherical_coords, radius=6378.1370, scale=1, min_values=None, max_values=None, padding=50):
    """
    Convert spherical coordinates to cartesian coordinates scaled to a canvas.
    
    Args:
        spherical_coords: List of tuples [(r, theta, phi), ...] where:
            - r: radial distance
            - theta: polar angle (in degrees).
            - phi: azimuthal angle (in degrees).
        radius (float): Radius (default is 1; use Earth's radius if necessary).
        canvas_size (tuple): Dimensions of the canvas (width, height).
    
    Returns:
        List of tuples [(x, y)] scaled to the canvas dimensions.
    """

    if min_values is None:
        return None
    if max_values is None:
        return None
    
    min_x, min_y = min_values
    max_x, max_y = max_values

    ID, latitude, longitude = spherical_coords

    # Convert degrees to radians
    theta = math.radians(90 - latitude)  # Latitude is converted to polar angle
    phi = math.radians(longitude)       # Longitude is the azimuthal angle

    # Apply spherical to cartesian formulas
    x = radius * math.sin(theta) * math.cos(phi)
    y = radius * math.sin(theta) * math.sin(phi)
    z = radius * math.cos(theta)

    # Scale coordinates to canvas dimensions
    # x_canvas = int((x + radius) / (2 * radius) * width)
    # y_canvas = int((y + radius) / (2 * radius) * height)
    x_canvas = float((x - min_x) * scale + padding)
    y_canvas = float((y - min_y) * scale + padding)

    converted_coords = (ID, x_canvas, y_canvas)

    return converted_coords