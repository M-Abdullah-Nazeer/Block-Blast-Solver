import os
import cv2
import numpy as np
import shutil
from fastapi import FastAPI, UploadFile, File
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from scipy.stats import mode
from math import ceil
import copy

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

    # Directory to save cropped images
    output_dir = "cropped_shapes"
    os.makedirs(output_dir, exist_ok=True)

    shape_paths = []  # List to store cropped image paths

    for i, contour in enumerate(filtered_contours):
        x, y, w, h = cv2.boundingRect(contour)

        # Ensure the bounding box is large enough
        if w < 10 or h < 10:
            continue

        # Crop the shape
        cropped_shape = image[y:y+h, x:x+w]

        # Save cropped shape
        shape_filename = f"{output_dir}/shape_{i}.jpg"
        cv2.imwrite(shape_filename, cropped_shape)
        shape_paths.append(shape_filename)

    # Debugging images
    if debug:
        debug_dir = "debug_images"
        os.makedirs(debug_dir, exist_ok=True)
        cv2.imwrite(f"{debug_dir}/debug_threshold.jpg", thresh)

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
    debug_dir = os.path.join(directory, "debug")
    os.makedirs(debug_dir, exist_ok=True)

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
        debug_img = img.copy()
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(debug_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cx, cy = int(x+w/2), int(y+h/2)
            cv2.circle(debug_img, (cx, cy), 3, (0, 0, 255), -1)
        cv2.imwrite(os.path.join(debug_dir, f"debug_{filename}"), debug_img)

        detected_shapes[filename] = grid.tolist()

    return detected_shapes






# def clear_completed_lines(board):
#     """
#     Returns a new board in which any row or column that is completely filled
#     (i.e. has no 0's) is cleared (all nonzero cells set to 0).
#     """
#     new_board = [row.copy() for row in board]
#     # Clear complete rows.
#     for i in range(len(new_board)):
#         if all(cell != 0 for cell in new_board[i]):
#             new_board[i] = [0] * len(new_board[i])
#     # Clear complete columns.
#     for j in range(len(new_board[0])):
#         if all(new_board[i][j] != 0 for i in range(len(new_board))):
#             for i in range(len(new_board)):
#                 new_board[i][j] = 0
#     return new_board


# def find_shape_placement_stepwise(original_board, shapes_dict):
#     """
#     Processes the shapes one by one. For each shape (except the first),
#     first clear any complete row or column from the board (by replacing all 
#     nonzero values with 0) then place the shape. The placement is accepted only 
#     if it creates at least one complete row or column. One board state is saved 
#     per shape, so if there are N shapes the results list will have N steps.
#     """
#     # Start with a copy of the original board.
#     current_board = [row.copy() for row in original_board]
#     results = []
#     placement_value = 2  # Start shape placements with 2.
    
#     # Process shapes in sorted order of their keys.
#     shape_keys = sorted(shapes_dict.keys())
    
#     for idx, filename in enumerate(shape_keys):
#         # For all iterations except the first, clear any complete lines from previous step.
#         if idx > 0:
#             current_board = clear_completed_lines(current_board)
        
#         shape = shapes_dict[filename]
#         if not shape:
#             results.append([row.copy() for row in current_board])
#             continue
        
#         placed = False
#         shape_rows = len(shape)
#         shape_cols = len(shape[0]) if shape_rows > 0 else 0
        
#         # Try every possible placement position.
#         for y in range(8 - shape_rows + 1):
#             for x in range(8 - shape_cols + 1):
#                 valid = True
#                 for i in range(shape_rows):
#                     for j in range(shape_cols):
#                         if shape[i][j] == 1 and current_board[y + i][x + j] != 0:
#                             valid = False
#                             break
#                     if not valid:
#                         break
#                 if not valid:
#                     continue
                
#                 # Make a temporary board for the placement attempt.
#                 temp_board = [row.copy() for row in current_board]
#                 for i in range(shape_rows):
#                     for j in range(shape_cols):
#                         if shape[i][j] == 1:
#                             temp_board[y + i][x + j] = placement_value
                
#                 # Check if this placement produces any complete row or column.
#                 row_completed = any(all(cell != 0 for cell in row) for row in temp_board)
#                 col_completed = any(all(temp_board[r][col] != 0 for r in range(8)) for col in range(8))
                
#                 if row_completed or col_completed:
#                     # Accept the placement.
#                     current_board = temp_board
#                     placed = True
#                     break
#             if placed:
#                 break
        
#         if placed:
#             placement_value += 1
        
#         # Save the current board state after placement (with clearing applied in this iteration).
#         results.append([row.copy() for row in current_board])
    
#     return results















# def clear_completed_lines(board):
#     """
#     Returns a new board in which any row or column that is completely filled 
#     (i.e. has no zeros) is cleared (all nonzero cells replaced with 0).
#     """
#     new_board = [row.copy() for row in board]
#     # Clear complete rows.
#     for i in range(len(new_board)):
#         if all(cell != 0 for cell in new_board[i]):
#             new_board[i] = [0] * len(new_board[i])
#     # Clear complete columns.
#     for j in range(len(new_board[0])):
#         if all(new_board[i][j] != 0 for i in range(len(new_board))):
#             for i in range(len(new_board)):
#                 new_board[i][j] = 0
#     return new_board

# def count_completed_lines(board):
#     """
#     Returns the total number of complete rows and complete columns in board.
#     A complete line is one that has no zeros.
#     """
#     completed_rows = sum(1 for row in board if all(cell != 0 for cell in row))
#     completed_cols = 0
#     for j in range(len(board[0])):
#         if all(board[i][j] != 0 for i in range(len(board))):
#             completed_cols += 1
#     return completed_rows + completed_cols

# def find_shape_placement_stepwise(original_board, shapes_dict):
#     """
#     At each step, among all remaining shapes, this function finds the placement 
#     that yields the maximum number of complete rows/columns.
    
#     For each step (except the first), the board is first cleared by replacing 
#     all nonzero cells in any complete row or column with 0. Then, among the 
#     remaining shapes, the one that can be placed with the best "score" (number 
#     of completed rows+columns) is chosen. Its cells are marked with the current 
#     placement value (2 for the first placed shape, 3 for the second, 4 for the 
#     third, etc.). The board state after placement is saved, and then cleared 
#     (if needed) before the next iteration.
    
#     The function returns a list of board states (one per placed shape) showing 
#     the efficient placement order.
#     """
#     # Start with a copy of the original board.
#     current_board = [row.copy() for row in original_board]
#     results = []
#     # Use a fixed placement value for each shape:
#     placement_value = 2
#     # Available shapes: use a dictionary copy (or list of keys) so we can remove the chosen one.
#     available_shapes = dict(shapes_dict)  # copy

#     # Continue while there are available shapes.
#     while available_shapes:
#         best_score = -1
#         best_board = None
#         best_shape_key = None

#         # Try each remaining shape.
#         for key, shape in available_shapes.items():
#             shape_rows = len(shape)
#             shape_cols = len(shape[0]) if shape_rows > 0 else 0

#             # Try every possible placement on current_board.
#             for y in range(8 - shape_rows + 1):
#                 for x in range(8 - shape_cols + 1):
#                     valid = True
#                     # Check that shape fits into empty cells.
#                     for i in range(shape_rows):
#                         for j in range(shape_cols):
#                             if shape[i][j] == 1 and current_board[y + i][x + j] != 0:
#                                 valid = False
#                                 break
#                         if not valid:
#                             break
#                     if not valid:
#                         continue

#                     # Simulate placement.
#                     temp_board = [row.copy() for row in current_board]
#                     for i in range(shape_rows):
#                         for j in range(shape_cols):
#                             if shape[i][j] == 1:
#                                 temp_board[y + i][x + j] = placement_value

#                     # Evaluate the board: count the number of complete rows/cols.
#                     score = count_completed_lines(temp_board)
#                     if score > best_score:
#                         best_score = score
#                         best_board = temp_board
#                         best_shape_key = key
#                     # If scores are equal, you might choose based on additional criteria (if desired).

#         # If no valid placement was found for any shape, break out.
#         if best_board is None:
#             break

#         # Accept the best placement found.
#         current_board = best_board
#         # Remove that shape from the available set.
#         del available_shapes[best_shape_key]
#         # Record the board state after placement.
#         results.append([row.copy() for row in current_board])
#         # Increment placement value so that each shape gets a distinct marker.
#         placement_value += 1

#         # Before next iteration, clear complete rows/columns.
#         current_board = clear_completed_lines(current_board)

#     return results






# ---------debug----------

# def clear_completed_lines(board):
#     """
#     Returns a new board where any row or column that is completely filled
#     (i.e. has no zeros) is cleared (all nonzero cells replaced with 0).
#     """
#     new_board = [row.copy() for row in board]
#     # Clear complete rows
#     for i in range(len(new_board)):
#         if all(cell != 0 for cell in new_board[i]):
#             new_board[i] = [0] * len(new_board[i])
#     # Clear complete columns
#     for j in range(len(new_board[0])):
#         if all(new_board[i][j] != 0 for i in range(len(new_board))):
#             for i in range(len(new_board)):
#                 new_board[i][j] = 0
#     return new_board



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
    base_name = shape_key.rsplit(".", 1)[0]  # e.g. "shape_0"
    
    # 2. Split by underscore and parse the last chunk
    suffix = base_name.split("_")[-1]        # e.g. "0"
    num = int(suffix)                        # e.g. 0

    return num + 2                           # "shape_0" -> 2, "shape_1" -> 3, etc.




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




    # def backtrack(current_board, remaining_shapes, current_sequence, lines_so_far):
    #     """
    #     current_board: the board after the last placement+clearing
    #     remaining_shapes: which shapes are still left to place
    #     current_sequence: list of board states so far (one per placed shape)
    #     lines_so_far: total lines completed across all steps so far
    #     """
    #     # If no shapes left, check if this path is the best.
    #     if not remaining_shapes:
    #         if lines_so_far > best_result["max_lines"]:
    #             best_result["max_lines"] = lines_so_far
    #             best_result["boards_sequence"] = [step for step in current_sequence]
    #         return

    #     # Otherwise, try each shape from remaining_shapes.
    #     for shape_key in remaining_shapes:
    #         shape = shapes_dict[shape_key]
    #         block_value = shape_key_to_block_value(shape_key)

    #         # Get all valid placements for this shape on the current board.
    #         valid_placements = get_all_valid_placements(current_board, shape, block_value)

    #         if not valid_placements:
    #             # If we can't place this shape at all, we can skip it (or place "no-op").
    #             # But typically, you'd want to consider "skipping" if that's allowed.
    #             continue

    #         for (placed_board, lines_now) in valid_placements:
    #             # lines_now is how many lines are completed by placing this shape.
    #             # Next, we CLEAR those completed lines before going to the next shape.
    #             cleared_board = clear_completed_lines(placed_board)

    #             # Record the board state AFTER placement (before clearing), or after clearing?
    #             # This depends on your preference. Let's store the board *after placement*:
    #             new_sequence = current_sequence + [[row.copy() for row in placed_board]]

    #             # Recurse with the next shape set (excluding the one we just used).
    #             new_remaining = [s for s in remaining_shapes if s != shape_key]
    #             backtrack(
    #                 cleared_board,
    #                 new_remaining,
    #                 new_sequence,
    #                 lines_so_far + lines_now
    #             )

    # # Kick off the recursion.
    # backtrack(start_board, shape_keys, [], 0)

    # return best_result["boards_sequence"]





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
            block_value = shape_key_to_block_value(shape_key)
            
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


def get_shapes_colors(directory: str = SHAPES_DIR) -> dict:
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

# Example usage:
# colors = get_shapes_colors()
# print(colors)  # e.g., {'shape 0': '#ffffff', 'shape 1': '#123456', ...}



# -----------------------------------------------------



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
    # processed_shapes = process_shapes(shapes_matrices["shapes"])
    # processed_cropped_shapes = process_cropped_shapes(SHAPES_DIR)
    processed_cropped_shapes = detect_blocks_final_v2(SHAPES_DIR)
    # final_output = find_shape_placement(board_matrix, processed_cropped_shapes)
    stepwise_boards = find_shape_placement_stepwise(board_matrix, processed_cropped_shapes)
    shape_colors = get_shapes_colors()

    print(shape_colors)
    for name, arr in processed_cropped_shapes.items():
        print(f"{name} =>")
        for row in arr:
            print(row)
        print()

    

    for idx, board in enumerate(stepwise_boards):
        print(f"Step {idx+1}:")
        for row in board:
            print(row)
        print("--------------------")

    return {
    
        # "board_matrix": board_matrix,
        # "shapes": shapes_matrices,
        # "processed_shapes": processed_shapes,
        # "process_cropped_shapes": processed_cropped_shapes,
        "shape_colors": shape_colors,
        "final_output":  stepwise_boards

    }






# make UI better
# create other pages