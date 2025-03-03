# -------------------------- working fine with light blue color----------------------

# import os
# import cv2
# import numpy as np
# import shutil
# from fastapi import FastAPI, UploadFile, File
# from starlette.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware

# UPLOAD_DIR = "uploads"
# CROPPED_DIR = "cropped"
# DEBUG_DIR = "debug_cells"

# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(CROPPED_DIR, exist_ok=True)
# os.makedirs(DEBUG_DIR, exist_ok=True)

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def crop_board(image_path):
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
#     edges = cv2.Canny(thresh, 30, 100)
    
#     contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     board_contour = None
#     max_area = 0
    
#     for contour in contours:
#         approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
#         if len(approx) == 4:
#             x, y, w, h = cv2.boundingRect(approx)
#             area = w * h
#             if area > max_area:
#                 max_area = area
#                 board_contour = (x, y, w, h)
    
#     if board_contour:
#         x, y, w, h = board_contour
#         cropped_image = image[y:y+h, x:x+w]
#         cropped_path = os.path.join(CROPPED_DIR, os.path.basename(image_path))
#         cv2.imwrite(cropped_path, cropped_image)
#         return cropped_path
    
#     return None

# def process_image(image_path):
#     image = cv2.imread(image_path)
#     if image is None:
#         return None
    
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # Updated HSV range for blue detection
#     lower_blue = np.array([100, 40, 40])  
#     upper_blue = np.array([130, 255, 255])

#     # Create a blue mask
#     mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

#     # Enhance detection using brightness (V) and saturation (S) for blue areas
#     v_channel = hsv[:, :, 2]  # Brightness
#     s_channel = hsv[:, :, 1]  # Saturation

#     blue_threshold = (v_channel > 40) & (s_channel > 40)  # More inclusive range
#     refined_mask_blue = np.where(blue_threshold, mask_blue, 0).astype(np.uint8)

#     # Invert the refined blue mask for filled blocks
#     mask_filled = cv2.bitwise_not(refined_mask_blue)

#     height, width = image.shape[:2]
#     cell_size = width // 8  # Assuming an 8x8 grid

#     board_matrix = []
#     for row in range(8):
#         row_data = []
#         for col in range(8):
#             x_start, y_start = col * cell_size, row * cell_size
#             x_end, y_end = x_start + cell_size, y_start + cell_size
#             cell_blue = refined_mask_blue[y_start:y_end, x_start:x_end]
#             cell_filled = mask_filled[y_start:y_end, x_start:x_end]

#             # Save debug images
#             debug_blue_path = os.path.join(DEBUG_DIR, f"cell_blue_{row}_{col}.png")
#             debug_filled_path = os.path.join(DEBUG_DIR, f"cell_filled_{row}_{col}.png")
#             cv2.imwrite(debug_blue_path, cell_blue)
#             cv2.imwrite(debug_filled_path, cell_filled)

#             # If a block has more non-blue pixels, it's filled (1); otherwise, it's empty (0)
#             filled = np.count_nonzero(cell_filled) > (cell_size * cell_size * 0.2)
#             row_data.append(1 if filled else 0)
#         board_matrix.append(row_data)

#     return board_matrix

# @app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
    
#     cropped_path = crop_board(file_path)
#     if not cropped_path:
#         return JSONResponse(content={"error": "Board detection failed"}, status_code=400)
    
#     board_matrix = process_image(cropped_path)
#     if board_matrix is None:
#         return JSONResponse(content={"error": "Image processing failed"}, status_code=400)
    
#     return {"board_matrix": board_matrix}












# -------------------------------------detects blocks of all colors from board------------------


# import os
# import cv2
# import numpy as np
# import shutil
# from fastapi import FastAPI, UploadFile, File
# from starlette.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware

# UPLOAD_DIR = "uploads"
# CROPPED_DIR = "cropped"
# DEBUG_DIR = "debug_cells"

# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(CROPPED_DIR, exist_ok=True)
# os.makedirs(DEBUG_DIR, exist_ok=True)

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def crop_board(image_path):
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
#     edges = cv2.Canny(thresh, 30, 100)
    
#     contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     board_contour = None
#     max_area = 0
    
#     for contour in contours:
#         approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
#         if len(approx) == 4:
#             x, y, w, h = cv2.boundingRect(approx)
#             area = w * h
#             if area > max_area:
#                 max_area = area
#                 board_contour = (x, y, w, h)
    
#     if board_contour:
#         x, y, w, h = board_contour
#         cropped_image = image[y:y+h, x:x+w]
#         cropped_path = os.path.join(CROPPED_DIR, os.path.basename(image_path))
#         cv2.imwrite(cropped_path, cropped_image)
#         return cropped_path
    
#     return None

# def process_image(image_path):
#     image = cv2.imread(image_path)
#     if image is None:
#         return None
    
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # Adjusted HSV ranges
#     lower_filled_blue = np.array([110, 130, 60])
#     upper_filled_blue = np.array([120, 160, 80])

#     lower_empty_blue = np.array([110, 100, 30])
#     upper_empty_blue = np.array([120, 130, 60])

#     # Masks for filled and empty blue blocks
#     mask_filled_blue = cv2.inRange(hsv, lower_filled_blue, upper_filled_blue)
#     mask_empty_blue = cv2.inRange(hsv, lower_empty_blue, upper_empty_blue)

#     # Ensure non-overlapping detection
#     mask_blue = mask_filled_blue - mask_empty_blue  # Remove empty blocks from filled blocks

#     height, width = image.shape[:2]
#     cell_size = width // 8  # Assuming an 8x8 grid

#     board_matrix = []
#     for row in range(8):
#         row_data = []
#         for col in range(8):
#             x_start, y_start = col * cell_size, row * cell_size
#             x_end, y_end = x_start + cell_size, y_start + cell_size
#             cell_mask = mask_blue[y_start:y_end, x_start:x_end]

#             # Count nonzero pixels (filled block detection)
#             filled = np.count_nonzero(cell_mask) > (cell_size * cell_size * 0.2)
#             row_data.append(0 if filled else 1)
#         board_matrix.append(row_data)

#     return board_matrix


# @app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
    
#     cropped_path = crop_board(file_path)
#     if not cropped_path:
#         return JSONResponse(content={"error": "Board detection failed"}, status_code=400)
    
#     board_matrix = process_image(cropped_path)
#     if board_matrix is None:
#         return JSONResponse(content={"error": "Image processing failed"}, status_code=400)
    
#     return {"board_matrix": board_matrix}


# -------------------------------------------- croping shapes image----------------------------------------------------


# import os
# import cv2
# import numpy as np
# import shutil
# from fastapi import FastAPI, UploadFile, File
# from starlette.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware

# UPLOAD_DIR = "uploads"
# CROPPED_DIR = "cropped"
# DEBUG_DIR = "debug_cells"

# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(CROPPED_DIR, exist_ok=True)
# os.makedirs(DEBUG_DIR, exist_ok=True)

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def crop_board(image_path):
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
#     edges = cv2.Canny(thresh, 30, 100)
    
#     contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     board_contour = None
#     max_area = 0
    
#     for contour in contours:
#         approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
#         if len(approx) == 4:
#             x, y, w, h = cv2.boundingRect(approx)
#             area = w * h
#             if area > max_area:
#                 max_area = area
#                 board_contour = (x, y, w, h)
    
#     if board_contour:
#         x, y, w, h = board_contour
#         cropped_image = image[y:y+h, x:x+w]
#         cropped_path = os.path.join(CROPPED_DIR, os.path.basename(image_path))
#         cv2.imwrite(cropped_path, cropped_image)
#         return cropped_path, (x, y, w, h)

#     return None, None  # Return both cropped path and board coordinates


# def process_image(image_path):
#     if not image_path or not os.path.exists(image_path):
#         raise ValueError(f"Invalid image path: {image_path}")

#     image = cv2.imread(image_path)
#     if image is None:
#         raise ValueError(f"Failed to load image: {image_path}")

#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # Adjusted HSV ranges
#     lower_filled_blue = np.array([110, 130, 60])
#     upper_filled_blue = np.array([120, 160, 80])

#     lower_empty_blue = np.array([110, 100, 30])
#     upper_empty_blue = np.array([120, 130, 60])

#     # Masks for filled and empty blue blocks
#     mask_filled_blue = cv2.inRange(hsv, lower_filled_blue, upper_filled_blue)
#     mask_empty_blue = cv2.inRange(hsv, lower_empty_blue, upper_empty_blue)

#     # Ensure non-overlapping detection
#     mask_blue = mask_filled_blue - mask_empty_blue  # Remove empty blocks from filled blocks

#     height, width = image.shape[:2]
#     cell_size = width // 8  # Assuming an 8x8 grid

#     board_matrix = []
#     for row in range(8):
#         row_data = []
#         for col in range(8):
#             x_start, y_start = col * cell_size, row * cell_size
#             x_end, y_end = x_start + cell_size, y_start + cell_size
#             cell_mask = mask_blue[y_start:y_end, x_start:x_end]

#             # Count nonzero pixels (filled block detection)
#             filled = np.count_nonzero(cell_mask) > (cell_size * cell_size * 0.2)
#             row_data.append(0 if filled else 1)
#         board_matrix.append(row_data)

#     return board_matrix

# def crop_shapes(image_path, board_coords):
#     image = cv2.imread(image_path)
    
#     if board_coords is None or len(board_coords) != 4:
#         raise ValueError(f"Expected 4 values in board_coords, got {board_coords}")

#     x, y, w, h = board_coords  # Now safe to unpack
    
#     # Extending height dynamically
#     shape_area_start = y + h  # Start right after the board
#     shape_area_height = h // 2  # Adjust this if needed
    
#     cropped_shapes = image[shape_area_start:shape_area_start+shape_area_height, x:x+w]
    
#     shapes_path = os.path.join(CROPPED_DIR, "cropped_shapes.jpg")
#     cv2.imwrite(shapes_path, cropped_shapes)
#     return shapes_path

# @app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     # Unpack tuple properly
#     cropped_board_path, board_coords = crop_board(file_path)
    
#     # Ensure board detection succeeded
#     if not cropped_board_path or board_coords is None:
#         return JSONResponse(content={"error": "Board detection failed"}, status_code=400)

#     board_matrix = process_image(cropped_board_path)
#     cropped_shapes_path = crop_shapes(file_path, board_coords)

#     return {
#         "cropped_board": cropped_board_path,
#         "cropped_shapes": cropped_shapes_path,
#         "board_matrix": board_matrix
#     }













# ---------------------------------------debug-----------------------



import os
import cv2
import numpy as np
import shutil
from fastapi import FastAPI, UploadFile, File
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

UPLOAD_DIR = "uploads"
CROPPED_DIR = "cropped"
DEBUG_DIR = "debug_cells"
SHAPES_DIR = "cropped_shapes"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CROPPED_DIR, exist_ok=True)
os.makedirs(DEBUG_DIR, exist_ok=True)
os.makedirs(SHAPES_DIR, exist_ok=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def crop_board(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    edges = cv2.Canny(thresh, 30, 100)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    board_contour = None
    max_area = 0
    
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            area = w * h
            if area > max_area:
                max_area = area
                board_contour = (x, y, w, h)
    
    if board_contour:
        x, y, w, h = board_contour
        cropped_image = image[y:y+h, x:x+w]
        cropped_path = os.path.join(CROPPED_DIR, os.path.basename(image_path))
        cv2.imwrite(cropped_path, cropped_image)
        return cropped_path, (x, y, w, h)

    return None, None  # Return both cropped path and board coordinates

def process_image(image_path):
    if not image_path or not os.path.exists(image_path):
        raise ValueError(f"Invalid image path: {image_path}")

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to load image: {image_path}")

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Adjusted HSV ranges
    lower_filled_blue = np.array([110, 130, 60])
    upper_filled_blue = np.array([120, 160, 80])

    lower_empty_blue = np.array([110, 100, 30])
    upper_empty_blue = np.array([120, 130, 60])

    # Masks for filled and empty blue blocks
    mask_filled_blue = cv2.inRange(hsv, lower_filled_blue, upper_filled_blue)
    mask_empty_blue = cv2.inRange(hsv, lower_empty_blue, upper_empty_blue)

    # Ensure non-overlapping detection
    mask_blue = mask_filled_blue - mask_empty_blue  # Remove empty blocks from filled blocks

    height, width = image.shape[:2]
    cell_size = width // 8  # Assuming an 8x8 grid

    board_matrix = []
    for row in range(8):
        row_data = []
        for col in range(8):
            x_start, y_start = col * cell_size, row * cell_size
            x_end, y_end = x_start + cell_size, y_start + cell_size
            cell_mask = mask_blue[y_start:y_end, x_start:x_end]

            # Count nonzero pixels (filled block detection)
            filled = np.count_nonzero(cell_mask) > (cell_size * cell_size * 0.2)
            row_data.append(0 if filled else 1)
        board_matrix.append(row_data)

    return board_matrix

def crop_shapes(image_path, board_coords):
    image = cv2.imread(image_path)
    
    if board_coords is None or len(board_coords) != 4:
        raise ValueError(f"Expected 4 values in board_coords, got {board_coords}")

    x, y, w, h = board_coords  # Now safe to unpack
    
    # Extending height dynamically
    shape_area_start = y + h + 30 # Start right after the board
    shape_area_height = h // 2  # Adjust this if needed
    
    cropped_shapes = image[shape_area_start:shape_area_start+shape_area_height, x:x+w]
    
    shapes_path = os.path.join(CROPPED_DIR, "cropped_shapes.jpg")
    cv2.imwrite(shapes_path, cropped_shapes)
    return shapes_path




def detect_shapes(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to load image: {image_path}")

    # Convert to grayscale and apply threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    height, width = binary.shape
    cell_size = width // 8  # Assuming the shapes area is also 8x8

    shape_matrix = []
    for row in range(8):
        row_data = []
        for col in range(8):
            x_start, y_start = col * cell_size, row * cell_size
            x_end, y_end = x_start + cell_size, y_start + cell_size
            cell_region = binary[y_start:y_end, x_start:x_end]

            # Count nonzero pixels (detect filled blocks)
            filled = np.count_nonzero(cell_region) > (cell_size * cell_size * 0.2)
            row_data.append(1 if filled else 0)  # 1 = filled, 0 = empty
        shape_matrix.append(row_data)

    return [shape_matrix]  # Returning as a list of matrices to match API response format




@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    cropped_board_path, board_coords = crop_board(file_path)
    
    if not cropped_board_path or board_coords is None:
        return JSONResponse(content={"error": "Board detection failed"}, status_code=400)

    board_matrix = process_image(cropped_board_path)
    cropped_shapes_path = crop_shapes(file_path, board_coords)
    shapes_matrices = detect_shapes(cropped_shapes_path)

    return {
        "cropped_board": cropped_board_path,
        "cropped_shapes": cropped_shapes_path,
        "board_matrix": board_matrix,
       "shapes": [list(map(list, shape)) for shape in shapes_matrices]
    }
