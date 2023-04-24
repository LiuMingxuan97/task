# Import necessary libraries
import sqlite3
import zlib
from PIL import Image
import io

def get_tile_data(zoom_level, tile_column, tile_row):
    # Connect to the mbtiles file
    conn = sqlite3.connect('tianditu-img_w-113.27_42.4_119.5_36.05-16_54466_54522_24229_25723.mbtiles')

    # Create a cursor object
    c = conn.cursor()

    # Execute a query to retrieve the tile data
    c.execute("SELECT tile_data FROM tiles WHERE zoom_level = ? AND tile_column = ? AND tile_row = ?", (zoom_level, tile_column, tile_row))

    # Fetch the tile data
    tile_data = c.fetchone()[0]

    # Decompress the tile data
    decompressed_data = zlib.decompress(tile_data,16+zlib.MAX_WBITS)

    # Create an image object from the decompressed data
    img = Image.open(io.BytesIO(decompressed_data))

    # Display the image
    img.show()

get_tile_data(16, 54500, 39812)
