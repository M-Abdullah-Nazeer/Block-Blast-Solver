python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1 --loop asyncio --timeout-keep-alive 300





Which to choose?
If you already have a good board-warping pipeline, definitely try re-using it on the shapes area so you can do simple center-patch sampling.

If warping is unreliable, the template-matching/classifier approach will give you the best long-term maintainability.

The blur + snap trick can sometimes rescue a contour pipeline in just a few lines of code.




Here's a breakdown of the key functions and their approaches in this Block Blast Solver system:

### 1. **Image Upload & Preprocessing**
**Function**: `upload_file` (API endpoint)
**Approach**:
- Receives game screenshot via POST request
- Creates unique directories for each request using UUID
- Resizes image to standard dimensions (1080x2400) with aspect ratio preservation
- Saves original and processed images
- Coordinates the entire processing pipeline

### 2. **Board Detection & Cropping**
**Functions**: `crop_board`, `crop_board_small`, `crop_board_standard`
**Approach**:
1. **Small Image Handling** (<600px width):
   - Upsamples to 800x800
   - Uses adaptive thresholding and edge detection
   - Finds largest quadrilateral contour in top half of image

2. **Standard Image Handling**:
   - Gaussian blur for noise reduction
   - Adaptive thresholding with dynamic block size
   - Canny edge detection with dynamic thresholds
   - Morphological operations to clean edges
   - Contour analysis to find largest 4-point polygon

### 3. **Board Matrix Conversion**
**Function**: `process_image`
**Approach**:
- Resizes board to 800x800
- Converts to HSV color space and extracts Value channel
- Divides into 8x8 grid
- Samples central region of each cell to avoid grid lines
- Classifies cells as filled (0) or empty (1) based on brightness

### 4. **Shape Extraction**
**Functions**: `crop_shapes`, `remove_ad_banner`
**Approach**:
- Locates shape area below detected board
- Dynamic cropping with fallback mechanisms
- Ad banner removal using:
  - Bottom region analysis
  - Adaptive thresholding
  - Contour detection for large elements
  - Automatic banner position detection

### 5. **Shape Processing**
**Functions**: `detect_shapes`, `detect_blocks_final_v2`
**Approach**:
1. **Shape Isolation**:
   - Thresholding and morphological operations
   - Contour detection and sorting (left-to-right)
   - Individual shape cropping

2. **Shape Analysis**:
   - Color detection for purple blocks (HSV range)
   - Adaptive kernel sizing based on color presence
   - Contour centroid calculation
   - Dynamic clustering of block positions
   - Grid matrix creation for shape structure

### 6. **Game Solving Core**
**Functions**: `find_shape_placement_stepwise`, `get_all_valid_placements`
**Approach**:
- Backtracking algorithm with pruning:
  1. Try all permutations of shape order
  2. For each shape, test all valid positions
  3. Score placements by immediate lines cleared
  4. Maintain best-found solution
- Uses recursive depth-first search
- Memoization through board state tracking

### 7. **Line Clearance Logic**
**Functions**: `clear_completed_lines`, `count_completed_lines`
**Approach**:
- Iterative line clearing:
  1. Detect fully filled rows/columns
  2. Clear all complete lines simultaneously
  3. Repeat until no more lines can be cleared
- Uses matrix operations for efficiency

### 8. **Support Functions**
**Key Utilities**:
- `cluster_coords`: Dynamic position clustering using median-based thresholds
- `trim_shape`: Matrix optimization by removing empty borders
- `detect_shape_block_color`: Central region color averaging for UI display
- `cleanup_directory`: Safe directory removal with retries

### Processing Flow
1. Image Upload → 2. Board Detection → 3. Board Analysis → 4. Shape Extraction → 
5. Shape Processing → 6. Game Solving → 7. Solution Formatting

This pipeline combines computer vision techniques (OpenCV) with algorithmic problem solving (backtracking) to create an automated solution generator for the Block Blast game. The system handles various image qualities and device resolutions through adaptive thresholding and dynamic parameter calculation.