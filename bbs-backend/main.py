# import os
# import cv2
# import numpy as np
# import shutil
# from fastapi import FastAPI, UploadFile, File
# from starlette.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from scipy.stats import mode
# from math import ceil
# import copy
# from pydantic import BaseModel




# class SolveRequest(BaseModel):
#     grid: list
#     shape1: list
#     shape2: list
#     shape3: list

# UPLOAD_DIR = "uploads"
# CROPPED_DIR = "cropped"
# # DEBUG_DIR = "debug_cells"
# SHAPES_DIR = "cropped_shapes"

# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(CROPPED_DIR, exist_ok=True)
# # os.makedirs(DEBUG_DIR, exist_ok=True)
# os.makedirs(SHAPES_DIR, exist_ok=True)

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
#     shape_area_start = y + h + 30 # Start right after the board
#     shape_area_height = h // 2  # Adjust this if needed
    
#     cropped_shapes = image[shape_area_start:shape_area_start+shape_area_height, x:x+w]
    
#     shapes_path = os.path.join(CROPPED_DIR, "cropped_shapes.jpg")
#     cv2.imwrite(shapes_path, cropped_shapes)
#     return shapes_path






# def detect_shapes(image_path, debug=True):
#     # Load image and convert to grayscale
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Apply adaptive thresholding for better shape detection
#     thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
#                                    cv2.THRESH_BINARY_INV, 101, 10)

#     # Use morphological closing to merge broken parts of shapes
#     kernel = np.ones((3, 3), np.uint8)
#     thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

#     # Find contours
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Sort contours from left to right
#     contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

#     # Filter out small contours
#     min_area = 100  # Adjusted to detect smaller shapes
#     filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

#     # Directory to save cropped images
#     output_dir = "cropped_shapes"
#     os.makedirs(output_dir, exist_ok=True)

#     shape_paths = []  # List to store cropped image paths

#     for i, contour in enumerate(filtered_contours):
#         x, y, w, h = cv2.boundingRect(contour)

#         # Ensure the bounding box is large enough
#         if w < 10 or h < 10:
#             continue

#         # Crop the shape
#         cropped_shape = image[y:y+h, x:x+w]

#         # Save cropped shape
#         shape_filename = f"{output_dir}/shape_{i}.jpg"
#         cv2.imwrite(shape_filename, cropped_shape)
#         shape_paths.append(shape_filename)

#     # Debugging images
#     # if debug:
#     #     debug_dir = "debug_images"
#     #     os.makedirs(debug_dir, exist_ok=True)
#     #     cv2.imwrite(f"{debug_dir}/debug_threshold.jpg", thresh)

#     return {"shapes": shape_paths}  # Returning JSON-serializable format



# # all shapes getting detected



# def cluster_coords(coords, threshold):
#     """
#     Group sorted coordinate values into clusters where successive values
#     differ by no more than the threshold. Returns the cluster centers.
#     """
#     coords_sorted = np.sort(coords)
#     clusters = []
#     current_cluster = [coords_sorted[0]]
#     for coord in coords_sorted[1:]:
#         if abs(coord - current_cluster[-1]) <= threshold:
#             current_cluster.append(coord)
#         else:
#             clusters.append(np.mean(current_cluster))
#             current_cluster = [coord]
#     clusters.append(np.mean(current_cluster))
#     return clusters




# def detect_blocks_final_v2(directory):
#     detected_shapes = {}
#     # debug_dir = os.path.join(directory, "debug")
#     # os.makedirs(debug_dir, exist_ok=True)

#     filenames = sorted([f for f in os.listdir(directory) if f.endswith(".jpg")])
#     for filename in filenames:
#         img_path = os.path.join(directory, filename)
#         img = cv2.imread(img_path)
#         if img is None:
#             print(f"Failed to load {filename}. Skipping.")
#             continue

#         # Check for purple color using HSV color space
#         hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#         # Convert your original values to OpenCV's HSV ranges:
#         h = 263.8 / 2  # → ~131.9
#         s = 58 * 2.55  # → ~148
#         v = 82 * 2.55  # → ~209

#         # With tolerance ranges:
#         lower_purple = np.array([h-5, s-20, v-30])  # [127, 128, 179]
#         upper_purple = np.array([h+5, s+20, v+30])  # [137, 168, 239]

#         # Round to integers:
#         lower_purple = np.array([125, 140, 190], dtype=np.uint8)
#         upper_purple = np.array([140, 200, 220], dtype=np.uint8)
#         mask = cv2.inRange(hsv, lower_purple, upper_purple)
#         has_purple = cv2.countNonZero(mask) > 0

#                 # After creating the mask:
#         # purple_debug = cv2.bitwise_and(img, img, mask=mask)
#         # cv2.imwrite(os.path.join(debug_dir, f"purple_{filename}"), purple_debug)

#         # Set kernel size based on purple presence
#         kernel_size = (3, 3) if has_purple else (2, 2)
#         kernel = np.ones(kernel_size, np.uint8)

#         # Preprocess image: grayscale and threshold
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

#         # Apply morphological operations
#         closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
#         eroded = cv2.erode(closed, kernel, iterations=1)

#         # Find contours of the blocks
#         contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         if not contours:
#             detected_shapes[filename] = []
#             continue

#         # Compute centroids for each detected contour
#         centroids = []
#         widths = []
#         heights = []
#         for c in contours:
#             x, y, w, h = cv2.boundingRect(c)
#             centroids.append((x + w/2, y + h/2))
#             widths.append(w)
#             heights.append(h)
#         centroids = np.array(centroids)

#         # Use centroids' coordinates for clustering
#         xs = centroids[:, 0]
#         ys = centroids[:, 1]
        
#         # Dynamic threshold based on median block size
#         median_size = np.median(np.concatenate((widths, heights)))
#         thresh_val = median_size / 2.0

#         # Cluster coordinates
#         x_clusters = cluster_coords(xs, thresh_val)
#         y_clusters = cluster_coords(ys, thresh_val)
        
#         # Initialize grid
#         num_cols = len(x_clusters)
#         num_rows = len(y_clusters)
#         grid = np.zeros((num_rows, num_cols), dtype=int)
        
#         # Populate grid
#         for cx, cy in centroids:
#             col = np.argmin(np.abs(np.array(x_clusters) - cx))
#             row = np.argmin(np.abs(np.array(y_clusters) - cy))
#             grid[row, col] = 1

#         # Save debug visualization
#         # debug_img = img.copy()
#         # for c in contours:
#         #     x, y, w, h = cv2.boundingRect(c)
#         #     cv2.rectangle(debug_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
#         #     cx, cy = int(x+w/2), int(y+h/2)
#         #     cv2.circle(debug_img, (cx, cy), 3, (0, 0, 255), -1)
#         # cv2.imwrite(os.path.join(debug_dir, f"debug_{filename}"), debug_img)

#         detected_shapes[filename] = grid.tolist()

#     return detected_shapes





# def clear_completed_lines(board):
#     """
#     Repeatedly clears any fully filled row or column (i.e., those with no zeros)
#     until no more lines can be cleared.

#     This version identifies which rows and columns are complete from the
#     *original* board in each iteration, then clears them all at once.
#     """
#     while True:
#         old_board = [row.copy() for row in board]

#         # 1) Identify completed rows in the *old* board
#         completed_rows = [
#             i for i in range(len(old_board))
#             if all(cell != 0 for cell in old_board[i])
#         ]

#         # 2) Identify completed columns in the *old* board
#         completed_cols = []
#         for j in range(len(old_board[0])):
#             if all(old_board[i][j] != 0 for i in range(len(old_board))):
#                 completed_cols.append(j)

#         # 3) Clear them all at once in a new copy
#         new_board = [row.copy() for row in old_board]

#         # Clear completed rows
#         for i in completed_rows:
#             new_board[i] = [0] * len(new_board[i])

#         # Clear completed columns
#         for j in completed_cols:
#             for i in range(len(new_board)):
#                 new_board[i][j] = 0

#         # 4) If no change, we're done
#         if new_board == board:
#             break

#         board = new_board

#     return board





# def count_completed_lines(board):
#     """
#     Returns the total number of complete rows plus complete columns in board.
#     A 'complete' line is one that has no zeros.
#     """
#     completed_rows = sum(1 for row in board if all(cell != 0 for cell in row))
#     completed_cols = 0
#     for j in range(len(board[0])):
#         if all(board[i][j] != 0 for i in range(len(board))):
#             completed_cols += 1
#     return completed_rows + completed_cols


# def shape_key_to_block_value(shape_key: str) -> int:
#     """
#     Example: shape_key = "shape_0.jpg"
#     1. Remove extension -> "shape_0"
#     2. Split by underscore -> ["shape", "0"]
#     3. Parse the last part as int -> 0
#     4. Return int + 2 -> 2
#     """
#     # 1. Remove the extension
#     base_name = shape_key.rsplit(".", 1)[0]  # e.g. "shape_0"
    
#     # 2. Split by underscore and parse the last chunk
#     suffix = base_name.split("_")[-1]        # e.g. "0"
#     num = int(suffix)                        # e.g. 0

#     return num + 2                           # "shape_0" -> 2, "shape_1" -> 3, etc.




# def get_all_valid_placements(board, shape, block_value):
#     """
#     Returns a list of (new_board, lines_completed_before_clearing).
#     Each new_board is the result of placing `shape` on `board` at some valid position.
#     """
#     shape_rows = len(shape)
#     shape_cols = len(shape[0]) if shape_rows > 0 else 0
#     valid_placements = []

#     for y in range(8 - shape_rows + 1):
#         for x in range(8 - shape_cols + 1):
#             # Check validity
#             is_valid = True
#             for i in range(shape_rows):
#                 for j in range(shape_cols):
#                     if shape[i][j] == 1 and board[y + i][x + j] != 0:
#                         is_valid = False
#                         break
#                 if not is_valid:
#                     break
#             if not is_valid:
#                 continue

#             # Simulate placement
#             temp_board = [row.copy() for row in board]
#             for i in range(shape_rows):
#                 for j in range(shape_cols):
#                     if shape[i][j] == 1:
#                         temp_board[y + i][x + j] = block_value

#             # Count how many lines this placement completes (before clearing)
#             lines_now = count_completed_lines(temp_board)
#             valid_placements.append((temp_board, lines_now))

#     return valid_placements



# def find_shape_placement_stepwise(original_board, shapes_dict):
#     """
#     Backtracking approach that tries all orders and placements of the given shapes
#     to maximize the total lines completed over all steps.
    
#     Returns a list of board states, one per placed shape, showing the best sequence.
#     """
#     # Copy the board so we don't mutate the original.
#     start_board = [row.copy() for row in original_board]
#     shape_keys = list(shapes_dict.keys())  # e.g. ["shape 0", "shape 1", "shape 2", ...]

#     # We'll keep track of the best overall result.
#     best_result = {
#         "max_lines": -1,
#         "boards_sequence": []  # will hold a list of board states, one per step
#     }




#     def backtrack(current_board, remaining_shapes, current_sequence, lines_so_far):
#         """
#         Recursively try each placement for remaining shapes.
#         """
#         if not remaining_shapes:
#             if lines_so_far > best_result["max_lines"]:
#                 best_result["max_lines"] = lines_so_far
#                 best_result["boards_sequence"] = [step for step in current_sequence]
#             return
        
#         for shape_key in remaining_shapes:
#             shape = shapes_dict[shape_key]
#             block_value = shape_key_to_block_value(shape_key)
            
#             # Get all valid placements for this shape on current_board.
#             valid_placements = get_all_valid_placements(current_board, shape, block_value)
#             if not valid_placements:
#                 continue  # Skip if shape cannot be placed.
            
#             for (placed_board, lines_now) in valid_placements:
#                 # Clear completed lines to prepare for next placement.
#                 cleared_board = clear_completed_lines(placed_board)
                
#                 # Record the step with the board state (after placement, before clearing)
#                 # and the number of completed lines from this placement.
#                 new_sequence = current_sequence + [{
#                     "board": [row.copy() for row in placed_board],
#                     "completedLines": lines_now
#                 }]
                
#                 new_remaining = [s for s in remaining_shapes if s != shape_key]
#                 backtrack(cleared_board, new_remaining, new_sequence, lines_so_far + lines_now)
    
#     # Kick off recursion.
#     backtrack(start_board, shape_keys, [], 0)
    
#     # If no placements were found, return an empty list rather than None.
#     return best_result["boards_sequence"] if best_result["boards_sequence"] is not None else []


# # ---------------------------



# def detect_shape_block_color(image_path: str) -> str:
#     """
#     Detects the representative color of a shape image by averaging
#     the central region's BGR values and converting them to a hex color.
#     """
#     img = cv2.imread(image_path)
#     if img is None:
#         raise ValueError(f"Unable to load image: {image_path}")
    
#     # Get image dimensions and define a central region to avoid any border effects.
#     h, w = img.shape[:2]
#     # Define a central block (here, using the middle 50% of width and height)
#     region = img[h // 4: 3 * h // 4, w // 4: 3 * w // 4]
    
#     # Compute the average color of the region (in BGR format)
#     avg_color = np.mean(region.reshape(-1, 3), axis=0)
#     # Convert average color from BGR to RGB
#     r, g, b = int(avg_color[2]), int(avg_color[1]), int(avg_color[0])
#     hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
#     return hex_color


# def get_shapes_colors(directory: str = SHAPES_DIR) -> dict:
#     """
#     Iterates through all JPG shape images in the given directory,
#     detects the color of one block in each image, and returns a dictionary
#     mapping shape names (e.g., "shape 0") to their hex color strings.
#     """
#     shape_colors = {}
#     filenames = sorted([f for f in os.listdir(directory) if f.endswith(".jpg")])
#     for i, filename in enumerate(filenames):
#         image_path = os.path.join(directory, filename)
#         color = detect_shape_block_color(image_path)
#         shape_colors[f"shape {i}"] = color
#     return shape_colors





# # -----------------------------------------------------



# @app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     cropped_board_path, board_coords = crop_board(file_path)
    
#     if not cropped_board_path or board_coords is None:
#         return JSONResponse(content={"error": "Board detection failed"}, status_code=400)

#     board_matrix = process_image(cropped_board_path)
#     cropped_shapes_path = crop_shapes(file_path, board_coords)
#     shapes_matrices = detect_shapes(cropped_shapes_path)
#     # processed_shapes = process_shapes(shapes_matrices["shapes"])
#     # processed_cropped_shapes = process_cropped_shapes(SHAPES_DIR)
#     processed_cropped_shapes = detect_blocks_final_v2(SHAPES_DIR)
#     # final_output = find_shape_placement(board_matrix, processed_cropped_shapes)
#     stepwise_boards = find_shape_placement_stepwise(board_matrix, processed_cropped_shapes)
#     shape_colors = get_shapes_colors()

#     print(shape_colors)
#     for name, arr in processed_cropped_shapes.items():
#         print(f"{name} =>")
#         for row in arr:
#             print(row)
#         print()

    

#     for idx, board in enumerate(stepwise_boards):
#         print(f"Step {idx+1}:")
#         for row in board:
#             print(row)
#         print("--------------------")

#     return {
    
#         "shape_colors": shape_colors,
#         "final_output":  stepwise_boards

#     }








# # -------------------------------------------------


# def trim_shape(shape_array):
#     """Trim all-zero rows and columns from a 2D array"""
#     arr = np.array(shape_array)
    
#     # Remove all-zero rows
#     arr = arr[~np.all(arr == 0, axis=1)]
#     # Remove all-zero columns
#     arr = arr[:, ~np.all(arr == 0, axis=0)]
    
#     return arr.tolist()



# @app.post("/fm")
# async def get_stepwise_boards(request: SolveRequest):
#     """
#     Endpoint for stepwise board placements
#     """
#     try:
#         # Process and trim all shapes into DICTIONARY format
#         processed_shapes = {
#             f"shape_{i}": trim_shape(shape)
#             for i, shape in enumerate([
#                 request.shape1,
#                 request.shape2,
#                 request.shape3
#             ])
#         }

#         # Process with trimmed shapes (now in required dict format)
#         stepwise_boards = find_shape_placement_stepwise(
#             request.grid,
#             processed_shapes  # Now properly formatted as dict
#         )
#         shape_colors = {
#             'shape 0': '#00BFFF', 'shape 1': '#fb00ff', 'shape 2': '#ffc800'
#         }
#         # Convert numpy arrays to lists if needed
#         if isinstance(stepwise_boards, np.ndarray):
#             stepwise_boards = stepwise_boards.tolist()
#         elif isinstance(stepwise_boards, list):
#             stepwise_boards = [
#                 board.tolist() if isinstance(board, np.ndarray) else board
#                 for board in stepwise_boards
#             ]

#         return {
#             "shape_colors": shape_colors,
#             "final_output": stepwise_boards}
    
#     except Exception as e:
#         return JSONResponse(
#             content={"error": str(e)},
#             status_code=500
#         )


















# # Add this import at the top with other imports
# import aiofiles  # Required for async file operations
# import concurrent.futures  # Required for thread pools

# # Rest of your existing imports
# import os
# import cv2
# import uuid
# import numpy as np
# import shutil
# import asyncio
# import aiofiles
# from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Request
# from starlette.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from scipy.stats import mode
# from math import ceil
# import copy
# from pydantic import BaseModel
# from fastapi.concurrency import run_in_threadpool

# from slowapi import Limiter, _rate_limit_exceeded_handler  # Uncomment for rate limiting
# from slowapi.util import get_remote_address                 # Requires redis
# from prometheus_fastapi_instrumentator import Instrumentator  # Uncomment for monitoring


# class SolveRequest(BaseModel):
#     grid: list
#     shape1: list
#     shape2: list
#     shape3: list

# UPLOAD_DIR = "uploads"
# CROPPED_DIR = "cropped"
# # DEBUG_DIR = "debug_cells"
# SHAPES_DIR = "cropped_shapes"

# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(CROPPED_DIR, exist_ok=True)
# # os.makedirs(DEBUG_DIR, exist_ok=True)
# os.makedirs(SHAPES_DIR, exist_ok=True)



# # Processing pool for CPU-bound tasks
# PROCESSING_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=4)


# app = FastAPI()




# # NEW: Add monitoring (uncomment)
# Instrumentator().instrument(app).expose(app)

# # NEW: Rate limiter (uncomment and install redis)
# limiter = Limiter(key_func=get_remote_address)
# app.state.limiter = limiter
# app.add_exception_handler(Exception, _rate_limit_exceeded_handler)


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )




# # NEW: Priority middleware
# @app.middleware("http")
# async def priority_middleware(request: Request, call_next):
#     if request.headers.get("X-Priority") == "high":
#         return await call_next(request)
#     return await call_next(request)  # Add actual queue logic here





# # Utility Functions
# # --------------------------

# def cleanup_directory(path: str):
#     """Safely remove directory with retries"""
#     try:
#         shutil.rmtree(path, ignore_errors=True)
#     except Exception as e:
#         print(f"Cleanup error {path}: {str(e)}")

# async def async_image_read(file: UploadFile):
#     """Read image file directly into memory"""
#     contents = await file.read()
#     return cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)

# def fast_image_processing(image):
#     """Optimized OpenCV pipeline"""
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                  cv2.THRESH_BINARY, 11, 2)



# async def process_image_async(image_path: str):
#     """Run CPU-bound processing in thread pool"""
#     return await run_in_threadpool(process_image, image_path)

# def crop_board(image_path: str):
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


# def process_image(image_path: str):
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
#     shape_area_start = y + h + 30 # Start right after the board
#     shape_area_height = h // 2  # Adjust this if needed
    
#     cropped_shapes = image[shape_area_start:shape_area_start+shape_area_height, x:x+w]
    
#     shapes_path = os.path.join(CROPPED_DIR, "cropped_shapes.jpg")
#     cv2.imwrite(shapes_path, cropped_shapes)
#     return shapes_path






# def detect_shapes(image_path: str):
#     # Load image and convert to grayscale
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Apply adaptive thresholding for better shape detection
#     thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
#                                    cv2.THRESH_BINARY_INV, 101, 10)

#     # Use morphological closing to merge broken parts of shapes
#     kernel = np.ones((3, 3), np.uint8)
#     thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

#     # Find contours
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Sort contours from left to right
#     contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

#     # Filter out small contours
#     min_area = 100  # Adjusted to detect smaller shapes
#     filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

#     # Directory to save cropped images
#     output_dir = "cropped_shapes"
#     os.makedirs(output_dir, exist_ok=True)

#     shape_paths = []  # List to store cropped image paths

#     for i, contour in enumerate(filtered_contours):
#         x, y, w, h = cv2.boundingRect(contour)

#         # Ensure the bounding box is large enough
#         if w < 10 or h < 10:
#             continue

#         # Crop the shape
#         cropped_shape = image[y:y+h, x:x+w]

#         # Save cropped shape
#         shape_filename = f"{output_dir}/shape_{i}.jpg"
#         cv2.imwrite(shape_filename, cropped_shape)
#         shape_paths.append(shape_filename)

#     # Debugging images
#     # if debug:
#     #     debug_dir = "debug_images"
#     #     os.makedirs(debug_dir, exist_ok=True)
#     #     cv2.imwrite(f"{debug_dir}/debug_threshold.jpg", thresh)

#     return {"shapes": shape_paths}  # Returning JSON-serializable format



# # all shapes getting detected



# def cluster_coords(coords, threshold):
#     """
#     Group sorted coordinate values into clusters where successive values
#     differ by no more than the threshold. Returns the cluster centers.
#     """
#     coords_sorted = np.sort(coords)
#     clusters = []
#     current_cluster = [coords_sorted[0]]
#     for coord in coords_sorted[1:]:
#         if abs(coord - current_cluster[-1]) <= threshold:
#             current_cluster.append(coord)
#         else:
#             clusters.append(np.mean(current_cluster))
#             current_cluster = [coord]
#     clusters.append(np.mean(current_cluster))
#     return clusters




# def detect_blocks_final_v2(directory):
#     detected_shapes = {}
#     # debug_dir = os.path.join(directory, "debug")
#     # os.makedirs(debug_dir, exist_ok=True)

#     filenames = sorted([f for f in os.listdir(directory) if f.endswith(".jpg")])
#     for filename in filenames:
#         img_path = os.path.join(directory, filename)
#         img = cv2.imread(img_path)
#         if img is None:
#             print(f"Failed to load {filename}. Skipping.")
#             continue

#         # Check for purple color using HSV color space
#         hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#         # Convert your original values to OpenCV's HSV ranges:
#         h = 263.8 / 2  # → ~131.9
#         s = 58 * 2.55  # → ~148
#         v = 82 * 2.55  # → ~209

#         # With tolerance ranges:
#         lower_purple = np.array([h-5, s-20, v-30])  # [127, 128, 179]
#         upper_purple = np.array([h+5, s+20, v+30])  # [137, 168, 239]

#         # Round to integers:
#         lower_purple = np.array([125, 140, 190], dtype=np.uint8)
#         upper_purple = np.array([140, 200, 220], dtype=np.uint8)
#         mask = cv2.inRange(hsv, lower_purple, upper_purple)
#         has_purple = cv2.countNonZero(mask) > 0

#                 # After creating the mask:
#         # purple_debug = cv2.bitwise_and(img, img, mask=mask)
#         # cv2.imwrite(os.path.join(debug_dir, f"purple_{filename}"), purple_debug)

#         # Set kernel size based on purple presence
#         kernel_size = (3, 3) if has_purple else (2, 2)
#         kernel = np.ones(kernel_size, np.uint8)

#         # Preprocess image: grayscale and threshold
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

#         # Apply morphological operations
#         closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
#         eroded = cv2.erode(closed, kernel, iterations=1)

#         # Find contours of the blocks
#         contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         if not contours:
#             detected_shapes[filename] = []
#             continue

#         # Compute centroids for each detected contour
#         centroids = []
#         widths = []
#         heights = []
#         for c in contours:
#             x, y, w, h = cv2.boundingRect(c)
#             centroids.append((x + w/2, y + h/2))
#             widths.append(w)
#             heights.append(h)
#         centroids = np.array(centroids)

#         # Use centroids' coordinates for clustering
#         xs = centroids[:, 0]
#         ys = centroids[:, 1]
        
#         # Dynamic threshold based on median block size
#         median_size = np.median(np.concatenate((widths, heights)))
#         thresh_val = median_size / 2.0

#         # Cluster coordinates
#         x_clusters = cluster_coords(xs, thresh_val)
#         y_clusters = cluster_coords(ys, thresh_val)
        
#         # Initialize grid
#         num_cols = len(x_clusters)
#         num_rows = len(y_clusters)
#         grid = np.zeros((num_rows, num_cols), dtype=int)
        
#         # Populate grid
#         for cx, cy in centroids:
#             col = np.argmin(np.abs(np.array(x_clusters) - cx))
#             row = np.argmin(np.abs(np.array(y_clusters) - cy))
#             grid[row, col] = 1

#         # Save debug visualization
#         # debug_img = img.copy()
#         # for c in contours:
#         #     x, y, w, h = cv2.boundingRect(c)
#         #     cv2.rectangle(debug_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
#         #     cx, cy = int(x+w/2), int(y+h/2)
#         #     cv2.circle(debug_img, (cx, cy), 3, (0, 0, 255), -1)
#         # cv2.imwrite(os.path.join(debug_dir, f"debug_{filename}"), debug_img)

#         detected_shapes[filename] = grid.tolist()

#     return detected_shapes





# def clear_completed_lines(board):
#     """
#     Repeatedly clears any fully filled row or column (i.e., those with no zeros)
#     until no more lines can be cleared.

#     This version identifies which rows and columns are complete from the
#     *original* board in each iteration, then clears them all at once.
#     """
#     while True:
#         old_board = [row.copy() for row in board]

#         # 1) Identify completed rows in the *old* board
#         completed_rows = [
#             i for i in range(len(old_board))
#             if all(cell != 0 for cell in old_board[i])
#         ]

#         # 2) Identify completed columns in the *old* board
#         completed_cols = []
#         for j in range(len(old_board[0])):
#             if all(old_board[i][j] != 0 for i in range(len(old_board))):
#                 completed_cols.append(j)

#         # 3) Clear them all at once in a new copy
#         new_board = [row.copy() for row in old_board]

#         # Clear completed rows
#         for i in completed_rows:
#             new_board[i] = [0] * len(new_board[i])

#         # Clear completed columns
#         for j in completed_cols:
#             for i in range(len(new_board)):
#                 new_board[i][j] = 0

#         # 4) If no change, we're done
#         if new_board == board:
#             break

#         board = new_board

#     return board





# def count_completed_lines(board):
#     """
#     Returns the total number of complete rows plus complete columns in board.
#     A 'complete' line is one that has no zeros.
#     """
#     completed_rows = sum(1 for row in board if all(cell != 0 for cell in row))
#     completed_cols = 0
#     for j in range(len(board[0])):
#         if all(board[i][j] != 0 for i in range(len(board))):
#             completed_cols += 1
#     return completed_rows + completed_cols


# def shape_key_to_block_value(shape_key: str) -> int:
#     """
#     Example: shape_key = "shape_0.jpg"
#     1. Remove extension -> "shape_0"
#     2. Split by underscore -> ["shape", "0"]
#     3. Parse the last part as int -> 0
#     4. Return int + 2 -> 2
#     """
#     # 1. Remove the extension
#     base_name = shape_key.rsplit(".", 1)[0]  # e.g. "shape_0"
    
#     # 2. Split by underscore and parse the last chunk
#     suffix = base_name.split("_")[-1]        # e.g. "0"
#     num = int(suffix)                        # e.g. 0

#     return num + 2                           # "shape_0" -> 2, "shape_1" -> 3, etc.




# def get_all_valid_placements(board, shape, block_value):
#     """
#     Returns a list of (new_board, lines_completed_before_clearing).
#     Each new_board is the result of placing `shape` on `board` at some valid position.
#     """
#     shape_rows = len(shape)
#     shape_cols = len(shape[0]) if shape_rows > 0 else 0
#     valid_placements = []

#     for y in range(8 - shape_rows + 1):
#         for x in range(8 - shape_cols + 1):
#             # Check validity
#             is_valid = True
#             for i in range(shape_rows):
#                 for j in range(shape_cols):
#                     if shape[i][j] == 1 and board[y + i][x + j] != 0:
#                         is_valid = False
#                         break
#                 if not is_valid:
#                     break
#             if not is_valid:
#                 continue

#             # Simulate placement
#             temp_board = [row.copy() for row in board]
#             for i in range(shape_rows):
#                 for j in range(shape_cols):
#                     if shape[i][j] == 1:
#                         temp_board[y + i][x + j] = block_value

#             # Count how many lines this placement completes (before clearing)
#             lines_now = count_completed_lines(temp_board)
#             valid_placements.append((temp_board, lines_now))

#     return valid_placements



# def find_shape_placement_stepwise(original_board, shapes_dict):
#     """
#     Backtracking approach that tries all orders and placements of the given shapes
#     to maximize the total lines completed over all steps.
    
#     Returns a list of board states, one per placed shape, showing the best sequence.
#     """
#     # Copy the board so we don't mutate the original.
#     start_board = [row.copy() for row in original_board]
#     shape_keys = list(shapes_dict.keys())  # e.g. ["shape 0", "shape 1", "shape 2", ...]

#     # We'll keep track of the best overall result.
#     best_result = {
#         "max_lines": -1,
#         "boards_sequence": []  # will hold a list of board states, one per step
#     }




#     def backtrack(current_board, remaining_shapes, current_sequence, lines_so_far):
#         """
#         Recursively try each placement for remaining shapes.
#         """
#         if not remaining_shapes:
#             if lines_so_far > best_result["max_lines"]:
#                 best_result["max_lines"] = lines_so_far
#                 best_result["boards_sequence"] = [step for step in current_sequence]
#             return
        
#         for shape_key in remaining_shapes:
#             shape = shapes_dict[shape_key]
#             block_value = shape_key_to_block_value(shape_key)
            
#             # Get all valid placements for this shape on current_board.
#             valid_placements = get_all_valid_placements(current_board, shape, block_value)
#             if not valid_placements:
#                 continue  # Skip if shape cannot be placed.
            
#             for (placed_board, lines_now) in valid_placements:
#                 # Clear completed lines to prepare for next placement.
#                 cleared_board = clear_completed_lines(placed_board)
                
#                 # Record the step with the board state (after placement, before clearing)
#                 # and the number of completed lines from this placement.
#                 new_sequence = current_sequence + [{
#                     "board": [row.copy() for row in placed_board],
#                     "completedLines": lines_now
#                 }]
                
#                 new_remaining = [s for s in remaining_shapes if s != shape_key]
#                 backtrack(cleared_board, new_remaining, new_sequence, lines_so_far + lines_now)
    
#     # Kick off recursion.
#     backtrack(start_board, shape_keys, [], 0)
    
#     # If no placements were found, return an empty list rather than None.
#     return best_result["boards_sequence"] if best_result["boards_sequence"] is not None else []


# # ---------------------------



# def detect_shape_block_color(image_path: str) -> str:
#     """
#     Detects the representative color of a shape image by averaging
#     the central region's BGR values and converting them to a hex color.
#     """
#     img = cv2.imread(image_path)
#     if img is None:
#         raise ValueError(f"Unable to load image: {image_path}")
    
#     # Get image dimensions and define a central region to avoid any border effects.
#     h, w = img.shape[:2]
#     # Define a central block (here, using the middle 50% of width and height)
#     region = img[h // 4: 3 * h // 4, w // 4: 3 * w // 4]
    
#     # Compute the average color of the region (in BGR format)
#     avg_color = np.mean(region.reshape(-1, 3), axis=0)
#     # Convert average color from BGR to RGB
#     r, g, b = int(avg_color[2]), int(avg_color[1]), int(avg_color[0])
#     hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
#     return hex_color


# def get_shapes_colors(directory: str = SHAPES_DIR) -> dict:
#     """
#     Iterates through all JPG shape images in the given directory,
#     detects the color of one block in each image, and returns a dictionary
#     mapping shape names (e.g., "shape 0") to their hex color strings.
#     """
#     shape_colors = {}
#     filenames = sorted([f for f in os.listdir(directory) if f.endswith(".jpg")])
#     for i, filename in enumerate(filenames):
#         image_path = os.path.join(directory, filename)
#         color = detect_shape_block_color(image_path)
#         shape_colors[f"shape {i}"] = color
#     return shape_colors





# # -----------------------------------------------------



# # --------------------------
# # API Endpoints
# # --------------------------

# @app.post("/upload/")
# async def upload_file(
#     request: Request,
#     file: UploadFile = File(...),
#     background_tasks: BackgroundTasks = BackgroundTasks()
# ):
#     request_id = str(uuid.uuid4())
#     user_upload_dir = os.path.join(UPLOAD_DIR, request_id)
#     user_cropped_dir = os.path.join(CROPPED_DIR, request_id)

#     try:
#         os.makedirs(user_upload_dir, exist_ok=True)
#         os.makedirs(user_cropped_dir, exist_ok=True)

#         # Async file upload
#         file_path = os.path.join(user_upload_dir, file.filename)
#         async with aiofiles.open(file_path, "wb") as buffer:
#             while chunk := await file.read(8192):
#                 await buffer.write(chunk)

#         # Process board
#         cropped_board_path, board_coords = await run_in_threadpool(
#             crop_board, 
#             file_path
#         )

#         if not cropped_board_path:
#             raise ValueError("Board detection failed")

#         # Concurrent processing
#         cropped_shapes_path = await run_in_threadpool(
#             crop_shapes,
#             file_path,
#             board_coords
#         )

#         # Parallel execution
#         board_matrix, shapes_result = await asyncio.gather(
#             process_image_async(cropped_board_path),
#             run_in_threadpool(detect_shapes, cropped_shapes_path)
#         )

#         processed_cropped_shapes = await run_in_threadpool(
#             detect_blocks_final_v2, SHAPES_DIR
#         )
        
#         # Parallel shape placement
#         stepwise_boards = await run_in_threadpool(
#             find_shape_placement_stepwise,
#             board_matrix,
#             processed_cropped_shapes
#         )

#         shape_colors = await run_in_threadpool(get_shapes_colors)

#         # Schedule cleanup after response
#         background_tasks.add_task(cleanup_directory, user_upload_dir)
#         background_tasks.add_task(cleanup_directory, user_cropped_dir)

#         return {
#             "shape_colors": shape_colors,
#             "final_output": stepwise_boards
#         }

#     except Exception as e:
#         # Cleanup on error
#         cleanup_directory(user_upload_dir)
#         cleanup_directory(user_cropped_dir)
#         return JSONResponse(
#             content={"error": f"Processing failed: {str(e)}"},
#             status_code=500
#         )
        








# # -------------------------------------------------


# def trim_shape(shape_array):
#     """Trim all-zero rows and columns from a 2D array"""
#     arr = np.array(shape_array)
    
#     # Remove all-zero rows
#     arr = arr[~np.all(arr == 0, axis=1)]
#     # Remove all-zero columns
#     arr = arr[:, ~np.all(arr == 0, axis=0)]
    
#     return arr.tolist()



# @app.post("/fm")
# async def get_stepwise_boards(
#     request: SolveRequest,
#     background_tasks: BackgroundTasks = BackgroundTasks()
# ):
#     """Handle shape solving with memory optimization"""
#     try:
#         processed_shapes = {
#             f"shape_{i}": trim_shape(shape)
#             for i, shape in enumerate([
#                 request.shape1,
#                 request.shape2,
#                 request.shape3
#             ])
#         }

#         stepwise_boards = await run_in_threadpool(
#             find_shape_placement_stepwise,
#             request.grid,
#             processed_shapes
#         )

#         return {
#             "shape_colors": {
#                 'shape 0': '#00BFFF',
#                 'shape 1': '#fb00ff',
#                 'shape 2': '#ffc800'
#             },
#             "final_output": stepwise_boards
#         }

#     except Exception as e:
#         return JSONResponse(
#             content={"error": str(e)},
#             status_code=500
#         )







# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         "main:app",
#         host="0.0.0.0",
#         port=8000,
#         workers=4,
#         loop="asyncio",
#         timeout_keep_alive=300
#     )






















# -------------------------latest fixes-----------








# Add this import at the top with other imports
import aiofiles  # Required for async file operations
import concurrent.futures  # Required for thread pools

# Rest of your existing imports
import os
import cv2
import uuid
import numpy as np
import shutil
import asyncio
import aiofiles
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Request
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from scipy.stats import mode
from math import ceil
import copy
from pydantic import BaseModel
from fastapi.concurrency import run_in_threadpool
from slowapi.errors import RateLimitExceeded  # Add this
from slowapi import Limiter, _rate_limit_exceeded_handler  # Uncomment for rate limiting
from slowapi.util import get_remote_address                 # Requires redis
from prometheus_fastapi_instrumentator import Instrumentator  # Uncomment for monitoring


from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse


import redis  # NEW: Required for rate limiting


from dotenv import load_dotenv
load_dotenv()  # Add this before app = FastAPI()

# NEW: Dynamic thread pool based on CPU cores
PROCESSING_EXECUTOR = concurrent.futures.ThreadPoolExecutor(
    max_workers=os.cpu_count() * 2 + 1
)


class SolveRequest(BaseModel):
    grid: list
    shape1: list
    shape2: list
    shape3: list

# NEW: Base directories
UPLOAD_DIR = "uploads"
CROPPED_DIR = "cropped"
SHAPES_BASE_DIR = "cropped_shapes"  # NEW: Changed to base directory

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CROPPED_DIR, exist_ok=True)
os.makedirs(SHAPES_BASE_DIR, exist_ok=True)  # NEW: Create base dir




# Processing pool for CPU-bound tasks
PROCESSING_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=4)




# redis_connection = redis.Redis(
#     host='localhost',  # Use Redis URL in production
#     port=6379,
#     db=0,
#     decode_responses=True
# )


REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Parse the URL to create a Redis connection
redis_connection = redis.Redis.from_url(REDIS_URL, decode_responses=True)

app = FastAPI()




# NEW: Add monitoring (uncomment)
Instrumentator().instrument(app).expose(app)

# NEW: Rate limiter setup
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=REDIS_URL  # Use your Redis URL
)
app.state.limiter = limiter
# app.add_exception_handler(Exception, _rate_limit_exceeded_handler)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  

# NEW: Generate unique paths per request
def get_user_dirs(request_id: str):
    """Return all user-specific directories"""
    return {
        "upload": os.path.join(UPLOAD_DIR, request_id),
        "cropped": os.path.join(CROPPED_DIR, request_id),
        "shapes": os.path.join(SHAPES_BASE_DIR, request_id)  # NEW: User-specific shapes
    }


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# NEW: Priority middleware
@app.middleware("http")
async def priority_middleware(request: Request, call_next):
    if request.headers.get("X-Priority") == "high":
        return await call_next(request)
    return await call_next(request)  # Add actual queue logic here





# Utility Functions
# --------------------------

def cleanup_directory(path: str):
    """Safely remove directory with retries"""
    try:
        shutil.rmtree(path, ignore_errors=True)
    except Exception as e:
        print(f"Cleanup error {path}: {str(e)}")

async def async_image_read(file: UploadFile):
    """Read image file directly into memory"""
    contents = await file.read()
    return cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)

def fast_image_processing(image):
    """Optimized OpenCV pipeline"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 11, 2)



async def process_image_async(image_path: str):
    """Run CPU-bound processing in thread pool"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    return await run_in_threadpool(process_image, image_path)

def crop_board(image_path: str, output_dir: str):
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
        # Generate UUID filename for cropped board
        cropped_filename = f"board_{uuid.uuid4()}.jpg"
        cropped_path = os.path.join(output_dir, cropped_filename)
        cv2.imwrite(cropped_path, cropped_image)
        return cropped_path, (x, y, w, h)

    return None, None


def process_image(image_path: str):
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
    

def crop_shapes(image_path: str, board_coords: tuple, output_path: str):
    image = cv2.imread(image_path)
    
    if board_coords is None or len(board_coords) != 4:
        raise ValueError(f"Expected 4 values in board_coords, got {board_coords}")

    x, y, w, h = board_coords  # Now safe to unpack
    
    # Extending height dynamically
    shape_area_start = y + h + 30 # Start right after the board
    shape_area_height = h // 2  # Adjust this if needed
    
    cropped_shapes = image[shape_area_start:shape_area_start+shape_area_height, x:x+w]
    
    # shapes_path = os.path.join(CROPPED_DIR, "cropped_shapes.jpg")
    cv2.imwrite(output_path, cropped_shapes)
    return output_path







def detect_shapes(image_path: str, user_shapes_dir: str):
    # Load image and convert to grayscale
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding for better shape detection
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 101, 10)

    # Use morphological closing to merge broken parts of shapes
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours from left to right
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

    # Filter out small contours
    min_area = 100  # Adjusted to detect smaller shapes
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]


    shape_paths = []  # List to store cropped image paths

    for i, contour in enumerate(filtered_contours):
        x, y, w, h = cv2.boundingRect(contour)

        # Ensure the bounding box is large enough
        if w < 10 or h < 10:
            continue

        # Crop the shape
        cropped_shape = image[y:y+h, x:x+w]

        # Modified file saving
        # shape_filename = os.path.join(user_shapes_dir, f"shape_{uuid.uuid4()}.jpg")  
        shape_filename = os.path.join(user_shapes_dir, f"shape_{i}.jpg")
        cv2.imwrite(shape_filename, cropped_shape)
        shape_paths.append(shape_filename)

    # Debugging images
    # if debug:
    #     debug_dir = "debug_images"
    #     os.makedirs(debug_dir, exist_ok=True)
    #     cv2.imwrite(f"{debug_dir}/debug_threshold.jpg", thresh)

    return {"shapes": shape_paths}  # Returning JSON-serializable format



# all shapes getting detected



def cluster_coords(coords, threshold):
    """
    Group sorted coordinate values into clusters where successive values
    differ by no more than the threshold. Returns the cluster centers.
    """
    coords_sorted = np.sort(coords)
    clusters = []
    current_cluster = [coords_sorted[0]]
    for coord in coords_sorted[1:]:
        if abs(coord - current_cluster[-1]) <= threshold:
            current_cluster.append(coord)
        else:
            clusters.append(np.mean(current_cluster))
            current_cluster = [coord]
    clusters.append(np.mean(current_cluster))
    return clusters




def detect_blocks_final_v2(directory):
    detected_shapes = {}
    # debug_dir = os.path.join(directory, "debug")
    # os.makedirs(debug_dir, exist_ok=True)

    filenames = sorted([f for f in os.listdir(directory) if f.endswith(".jpg")])
    for filename in filenames:
        img_path = os.path.join(directory, filename)
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to load {filename}. Skipping.")
            continue

        # Check for purple color using HSV color space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Convert your original values to OpenCV's HSV ranges:
        h = 263.8 / 2  # → ~131.9
        s = 58 * 2.55  # → ~148
        v = 82 * 2.55  # → ~209

        # With tolerance ranges:
        lower_purple = np.array([h-5, s-20, v-30])  # [127, 128, 179]
        upper_purple = np.array([h+5, s+20, v+30])  # [137, 168, 239]

        # Round to integers:
        lower_purple = np.array([125, 140, 190], dtype=np.uint8)
        upper_purple = np.array([140, 200, 220], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_purple, upper_purple)
        has_purple = cv2.countNonZero(mask) > 0

                # After creating the mask:
        # purple_debug = cv2.bitwise_and(img, img, mask=mask)
        # cv2.imwrite(os.path.join(debug_dir, f"purple_{filename}"), purple_debug)

        # Set kernel size based on purple presence
        kernel_size = (3, 3) if has_purple else (2, 2)
        kernel = np.ones(kernel_size, np.uint8)

        # Preprocess image: grayscale and threshold
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

        # Apply morphological operations
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        eroded = cv2.erode(closed, kernel, iterations=1)

        # Find contours of the blocks
        contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            detected_shapes[filename] = []
            continue

        # Compute centroids for each detected contour
        centroids = []
        widths = []
        heights = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            centroids.append((x + w/2, y + h/2))
            widths.append(w)
            heights.append(h)
        centroids = np.array(centroids)

        # Use centroids' coordinates for clustering
        xs = centroids[:, 0]
        ys = centroids[:, 1]
        
        # Dynamic threshold based on median block size
        median_size = np.median(np.concatenate((widths, heights)))
        thresh_val = median_size / 2.0

        # Cluster coordinates
        x_clusters = cluster_coords(xs, thresh_val)
        y_clusters = cluster_coords(ys, thresh_val)
        
        # Initialize grid
        num_cols = len(x_clusters)
        num_rows = len(y_clusters)
        grid = np.zeros((num_rows, num_cols), dtype=int)
        
        # Populate grid
        for cx, cy in centroids:
            col = np.argmin(np.abs(np.array(x_clusters) - cx))
            row = np.argmin(np.abs(np.array(y_clusters) - cy))
            grid[row, col] = 1

        # Save debug visualization
        # debug_img = img.copy()
        # for c in contours:
        #     x, y, w, h = cv2.boundingRect(c)
        #     cv2.rectangle(debug_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #     cx, cy = int(x+w/2), int(y+h/2)
        #     cv2.circle(debug_img, (cx, cy), 3, (0, 0, 255), -1)
        # cv2.imwrite(os.path.join(debug_dir, f"debug_{filename}"), debug_img)

        detected_shapes[filename] = grid.tolist()

    return detected_shapes





def clear_completed_lines(board):
    """
    Repeatedly clears any fully filled row or column (i.e., those with no zeros)
    until no more lines can be cleared.

    This version identifies which rows and columns are complete from the
    *original* board in each iteration, then clears them all at once.
    """
    while True:
        old_board = [row.copy() for row in board]

        # 1) Identify completed rows in the *old* board
        completed_rows = [
            i for i in range(len(old_board))
            if all(cell != 0 for cell in old_board[i])
        ]

        # 2) Identify completed columns in the *old* board
        completed_cols = []
        for j in range(len(old_board[0])):
            if all(old_board[i][j] != 0 for i in range(len(old_board))):
                completed_cols.append(j)

        # 3) Clear them all at once in a new copy
        new_board = [row.copy() for row in old_board]

        # Clear completed rows
        for i in completed_rows:
            new_board[i] = [0] * len(new_board[i])

        # Clear completed columns
        for j in completed_cols:
            for i in range(len(new_board)):
                new_board[i][j] = 0

        # 4) If no change, we're done
        if new_board == board:
            break

        board = new_board

    return board





def count_completed_lines(board):
    """
    Returns the total number of complete rows plus complete columns in board.
    A 'complete' line is one that has no zeros.
    """
    completed_rows = sum(1 for row in board if all(cell != 0 for cell in row))
    completed_cols = 0
    for j in range(len(board[0])):
        if all(board[i][j] != 0 for i in range(len(board))):
            completed_cols += 1
    return completed_rows + completed_cols


def shape_key_to_block_value(shape_key: str) -> int:
    """
    Example: shape_key = "shape_0.jpg"
    1. Remove extension -> "shape_0"
    2. Split by underscore -> ["shape", "0"]
    3. Parse the last part as int -> 0
    4. Return int + 2 -> 2
    """
    # 1. Remove the extension
    base_name = os.path.splitext(shape_key)[0] # e.g. "shape_0"
    
    # Split into parts and keep all parts after "shape_"
    parts = base_name.split('_')
    if len(parts) < 2:
        return 2  # Default value if format unexpected

    # 2. Split by underscore and parse the last chunk
    # suffix = base_name.split("_")[-1]        # e.g. "0"
    # num = int(suffix)                        # e.g. 0

    # return num + 2                           # "shape_0" -> 2, "shape_1" -> 3, etc.

    return hash(shape_key) % 4 + 2 




def get_all_valid_placements(board, shape, block_value):
    """
    Returns a list of (new_board, lines_completed_before_clearing).
    Each new_board is the result of placing `shape` on `board` at some valid position.
    """
    shape_rows = len(shape)
    shape_cols = len(shape[0]) if shape_rows > 0 else 0
    valid_placements = []

    for y in range(8 - shape_rows + 1):
        for x in range(8 - shape_cols + 1):
            # Check validity
            is_valid = True
            for i in range(shape_rows):
                for j in range(shape_cols):
                    if shape[i][j] == 1 and board[y + i][x + j] != 0:
                        is_valid = False
                        break
                if not is_valid:
                    break
            if not is_valid:
                continue

            # Simulate placement
            temp_board = [row.copy() for row in board]
            for i in range(shape_rows):
                for j in range(shape_cols):
                    if shape[i][j] == 1:
                        temp_board[y + i][x + j] = block_value

            # Count how many lines this placement completes (before clearing)
            lines_now = count_completed_lines(temp_board)
            valid_placements.append((temp_board, lines_now))

    return valid_placements



def find_shape_placement_stepwise(original_board, shapes_dict):
    """
    Backtracking approach that tries all orders and placements of the given shapes
    to maximize the total lines completed over all steps.
    
    Returns a list of board states, one per placed shape, showing the best sequence.
    """
    # Copy the board so we don't mutate the original.
    start_board = [row.copy() for row in original_board]
    shape_keys = list(shapes_dict.keys())  # e.g. ["shape 0", "shape 1", "shape 2", ...]

    # We'll keep track of the best overall result.
    best_result = {
        "max_lines": -1,
        "boards_sequence": []  # will hold a list of board states, one per step
    }




    def backtrack(current_board, remaining_shapes, current_sequence, lines_so_far):
        """
        Recursively try each placement for remaining shapes.
        """
        if not remaining_shapes:
            if lines_so_far > best_result["max_lines"]:
                best_result["max_lines"] = lines_so_far
                best_result["boards_sequence"] = [step for step in current_sequence]
            return
        
        for shape_key in remaining_shapes:
            shape = shapes_dict[shape_key]
            # block_value = shape_key_to_block_value(shape_key)
            block_value = int(shape_key.split("_")[1]) + 2
            
            # Get all valid placements for this shape on current_board.
            valid_placements = get_all_valid_placements(current_board, shape, block_value)
            if not valid_placements:
                continue  # Skip if shape cannot be placed.
            
            for (placed_board, lines_now) in valid_placements:
                # Clear completed lines to prepare for next placement.
                cleared_board = clear_completed_lines(placed_board)
                
                # Record the step with the board state (after placement, before clearing)
                # and the number of completed lines from this placement.
                new_sequence = current_sequence + [{
                    "board": [row.copy() for row in placed_board],
                    "completedLines": lines_now
                }]
                
                new_remaining = [s for s in remaining_shapes if s != shape_key]
                backtrack(cleared_board, new_remaining, new_sequence, lines_so_far + lines_now)
    
    # Kick off recursion.
    backtrack(start_board, shape_keys, [], 0)
    
    # If no placements were found, return an empty list rather than None.
    return best_result["boards_sequence"] if best_result["boards_sequence"] is not None else []


# ---------------------------



def detect_shape_block_color(image_path: str) -> str:
    """
    Detects the representative color of a shape image by averaging
    the central region's BGR values and converting them to a hex color.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Unable to load image: {image_path}")
    
    # Get image dimensions and define a central region to avoid any border effects.
    h, w = img.shape[:2]
    # Define a central block (here, using the middle 50% of width and height)
    region = img[h // 4: 3 * h // 4, w // 4: 3 * w // 4]
    
    # Compute the average color of the region (in BGR format)
    avg_color = np.mean(region.reshape(-1, 3), axis=0)
    # Convert average color from BGR to RGB
    r, g, b = int(avg_color[2]), int(avg_color[1]), int(avg_color[0])
    hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
    return hex_color


def get_shapes_colors(directory: str = SHAPES_BASE_DIR) -> dict:
    """
    Iterates through all JPG shape images in the given directory,
    detects the color of one block in each image, and returns a dictionary
    mapping shape names (e.g., "shape 0") to their hex color strings.
    """
    shape_colors = {}
    filenames = sorted([f for f in os.listdir(directory) if f.endswith(".jpg")])
    for i, filename in enumerate(filenames):
        image_path = os.path.join(directory, filename)
        color = detect_shape_block_color(image_path)
        shape_colors[f"shape {i}"] = color
    return shape_colors





# -----------------------------------------------------



# --------------------------
# API Endpoints
# --------------------------




@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Credentials": "true",
        }
    )

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        content={"error": "Rate limit exceeded"},
        status_code=429,
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Credentials": "true"
        }
    )






@app.post("/upload")
# @limiter.limit("100/minute")
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    request_id = str(uuid.uuid4())
    dirs = get_user_dirs(request_id)

    try:
        # Create all user directories
        for d in dirs.values():
            os.makedirs(d, exist_ok=True)

        # Save uploaded file
        file_path = os.path.join(dirs["upload"], file.filename)
        async with aiofiles.open(file_path, "wb") as buffer:
            while chunk := await file.read(8192):
                await buffer.write(chunk)

        # Process board
        cropped_board_path, board_coords = await run_in_threadpool(
            crop_board, 
            file_path,
            dirs["cropped"]  # Pass user-specific cropped directory
        )

        if not board_coords:
            raise ValueError("Failed to detect game board")

        # Get board matrix
        board_matrix = await run_in_threadpool(
            process_image, 
            cropped_board_path
        )

        # Crop shapes area
        cropped_shapes_path = os.path.join(dirs["cropped"], f"shapes_{uuid.uuid4()}.jpg")
        await run_in_threadpool(
            crop_shapes,
            file_path,
            board_coords,
            cropped_shapes_path
        )

        # Detect individual shapes
        shapes_result = await run_in_threadpool(
            detect_shapes,
            cropped_shapes_path,
            dirs["shapes"]
        )

        # Process detected shapes (FIXED SECTION)
        # First process all shapes in the directory
        all_shapes_data = await run_in_threadpool(
            detect_blocks_final_v2,
            dirs["shapes"]  # Pass directory path here
        )
        
        # Then create processed_shapes with ordered numbering
        processed_shapes = {
            f"shape_{i}": all_shapes_data[filename]
            for i, filename in enumerate(sorted(all_shapes_data.keys()))
        }

        # Process shape placements
        stepwise_boards = await run_in_threadpool(
            find_shape_placement_stepwise,
            board_matrix,
            processed_shapes
        )

        # Get shape colors for visualization
        shape_colors = await run_in_threadpool(
            get_shapes_colors,
            dirs["shapes"]
        )

        # Cleanup
        background_tasks.add_task(cleanup_directory, dirs["upload"])
        background_tasks.add_task(cleanup_directory, dirs["cropped"])
        background_tasks.add_task(cleanup_directory, dirs["shapes"])
        

        return {
            "shape_colors": shape_colors,
            "final_output": stepwise_boards
        }

    except Exception as e:
        # Cleanup on error
        for d in dirs.values():
            cleanup_directory(d)
        return JSONResponse(
        content={"error": f"Processing failed: {str(e)}"},
        status_code=500,
        headers={
            # Add CORS headers manually
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Credentials": "true"
        }
        )








# -------------------------------------------------


def trim_shape(shape_array):
    """Trim all-zero rows and columns from a 2D array"""
    arr = np.array(shape_array)
    
    # Remove all-zero rows
    arr = arr[~np.all(arr == 0, axis=1)]
    # Remove all-zero columns
    arr = arr[:, ~np.all(arr == 0, axis=0)]
    
    return arr.tolist()



@app.post("/fm")
async def get_stepwise_boards(
    request: SolveRequest,
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Handle shape solving with memory optimization"""
    try:
        processed_shapes = {
            f"shape_{i}": trim_shape(shape)
            for i, shape in enumerate([
                request.shape1,
                request.shape2,
                request.shape3
            ])
        }

        stepwise_boards = await run_in_threadpool(
            find_shape_placement_stepwise,
            request.grid,
            processed_shapes
        )

        return {
            "shape_colors": {
                'shape 0': '#00BFFF',
                'shape 1': '#fb00ff',
                'shape 2': '#ffc800'
            },
            "final_output": stepwise_boards
        }

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )







if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,
        loop="asyncio",
        timeout_keep_alive=300
    )



