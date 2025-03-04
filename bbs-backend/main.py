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






def detect_shapes(image_path, debug=True):
    # Load image and convert to grayscale
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to segment shapes
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Use morphological closing to merge broken shapes
    kernel = np.ones((5, 5), np.uint8)  # Adjust kernel size if needed
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Apply dilation for separation (reintroduced 'dilated' to avoid errors)
    dilated = cv2.dilate(thresh, kernel, iterations=2)

    if debug:
        debug_dir = "debug_images"
        os.makedirs(debug_dir, exist_ok=True)
        cv2.imwrite(f"{debug_dir}/debug_threshold.jpg", thresh)
        cv2.imwrite(f"{debug_dir}/debug_dilated.jpg", dilated)

    # Find external contours to avoid inner artifacts
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours from left to right
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

    min_area = 1000  # Adjust based on shape size
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

    shape_arrays = []
    for i, contour in enumerate(filtered_contours):  # Use filtered contours
        x, y, w, h = cv2.boundingRect(contour)

        # Ignore small noise
        if w < 3 or h < 3:
            continue

        # Crop shape
        cropped_shape = thresh[y:y+h, x:x+w]

        # Save cropped shape for debugging
        if debug:
            cv2.imwrite(f"{debug_dir}/shape_{i}_cropped.jpg", cropped_shape)

        # Resize while keeping aspect ratio
        max_dim = max(w, h)
        scale = 8 / max_dim
        new_w, new_h = int(w * scale), int(h * scale)

        if new_w > 0 and new_h > 0:
            resized_shape = cv2.resize(cropped_shape, (new_w, new_h), interpolation=cv2.INTER_NEAREST)
        else:
            print(f"Skipping resize: Invalid dimensions (w={new_w}, h={new_h})")
            continue  # Skip this shape

        # Save resized shape for debugging
        if debug:
            cv2.imwrite(f"{debug_dir}/shape_{i}_resized.jpg", resized_shape)

        # Create 8x8 array and center the shape
        shape_grid = np.zeros((8, 8), dtype=int)
        offset_x = (8 - new_w) // 2
        offset_y = (8 - new_h) // 2
        shape_grid[offset_y:offset_y+new_h, offset_x:offset_x+new_w] = (resized_shape > 0).astype(int)

        shape_arrays.append(shape_grid)

    return [shape.tolist() for shape in shape_arrays]
















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

    for i, shape in enumerate(shapes_matrices):
        print(f"Shape {i+1}:")
        for row in shape:
            print(" ".join(map(str, row)))
        print("\n")

    return {
        "cropped_board": cropped_board_path,
        "cropped_shapes": cropped_shapes_path,
        "board_matrix": board_matrix,
        "shapes": shapes_matrices
    }
