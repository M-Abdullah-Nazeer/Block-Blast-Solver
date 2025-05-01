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


import traceback

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








# --------------------experiment-------------





def crop_board(image_path: str, output_dir: str):
    img = cv2.imread(image_path)
    if img is None:
        return None, None

    h0, w0 = img.shape[:2]

    # If it’s a small image, use the “fixed” routine:
    if w0 < 600 or (h0/w0) > 2:
        return crop_board_small(img, output_dir)

    # Otherwise fall back to your original crop_board logic:
    return crop_board_standard(img, output_dir)


# def crop_board_small(img, output_dir):
#     """
#     - img: the original cv2 image (any width <600)
#     - output_dir: where we save the board crop & debug
#     Returns (board_crop_path, (x0, y0, w0_box, h0_box)) 
#     where coords are in the ORIGINAL image's space.
#     """


#     # 1) keep original
#     orig = img.copy()
#     h0, w0 = orig.shape[:2]

#     # 2) upsample to square 800×800 for board detection
#     resized = cv2.resize(orig, (800, 800), interpolation=cv2.INTER_AREA)
#     debug_dir = os.path.join(output_dir, "debug_small")
#     os.makedirs(debug_dir, exist_ok=True)
#     cv2.imwrite(os.path.join(debug_dir, "resized_800.jpg"), resized)

#     gray = cv2.cvtColor(cv2.GaussianBlur(resized, (5,5), 0), cv2.COLOR_BGR2GRAY)
#     h, w = gray.shape

#     # 3) threshold & edge
#     block = max(3, (w//20)|1)
#     thresh = cv2.adaptiveThreshold(
#         gray, 255,
#         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY_INV,
#         block, 2
#     )
#     cv2.imwrite(os.path.join(debug_dir, "thresh.jpg"), thresh)

#     low, high = max(10, int(255*0.01)), max(30, int(255*0.03))
#     edges = cv2.Canny(thresh, low, high)
#     cv2.imwrite(os.path.join(debug_dir, "edges.jpg"), edges)

#     # 4) close & dilate
#     k = max(3, (w//200)|1)
#     kernel = np.ones((k, k), np.uint8)
#     clean = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)
#     dilated = cv2.dilate(clean, kernel, iterations=1)
#     cv2.imwrite(os.path.join(debug_dir, "dilated.jpg"), dilated)

#     # 5) find 4-point quads in top half
#     quads = []
#     contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     for cnt in contours:
#         approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
#         if len(approx) != 4:
#             continue
#         x, y, ww, hh = cv2.boundingRect(approx)
#         if y > h * 0.5:
#             continue
#         ar = ww / float(hh)
#         if 0.8 <= ar <= 1.25:
#             quads.append((ww * hh, (x, y, ww, hh)))

#     # fallback to largest quad anywhere
#     if quads:
#         _, (x8, y8, w8, h8) = max(quads, key=lambda t: t[0])
#     else:
#         x8 = y8 = w8 = h8 = None
#         max_area = 0
#         for cnt in contours:
#             approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
#             if len(approx) == 4:
#                 x, y, ww, hh = cv2.boundingRect(approx)
#                 area = ww * hh
#                 if area > max_area:
#                     max_area = area
#                     x8, y8, w8, h8 = x, y, ww, hh

#     if x8 is None:
#         return None, None

#     # 6) draw debug rectangle on the 800×800
#     vis = resized.copy()
#     cv2.rectangle(vis, (x8, y8), (x8 + w8, y8 + h8), (0, 255, 0), 2)
#     cv2.imwrite(os.path.join(debug_dir, "contours_800.jpg"), vis)

#     # 7) map coords *back* to original image:
#     sx = w0 / 800.0
#     sy = h0 / 800.0
#     x0 = int(x8 * sx)
#     y0 = int(y8 * sy)
#     w0_box = int(w8 * sx)
#     h0_box = int(h8 * sy)

#     # clamp to original bounds
#     x0 = max(0, min(x0, w0 - 1))
#     y0 = max(0, min(y0, h0 - 1))
#     w0_box = max(1, min(w0_box, w0 - x0))
#     h0_box = max(1, min(h0_box, h0 - y0))

#     # 8) crop on the ORIGINAL
#     board_crop = orig[y0 : y0 + h0_box, x0 : x0 + w0_box]
#     fname = f"board_{uuid.uuid4()}.jpg"
#     path = os.path.join(output_dir, fname)
#     cv2.imwrite(path, board_crop)

#     # 9) return the path + ORIGINAL coords
#     return path, (x0, y0, w0_box, h0_box)




# working

# def crop_board_standard(img, output_dir):
#     # 1) Remove redundant image load, use provided 'img'
#     debug_dir = os.path.join(output_dir, "debug")
#     os.makedirs(debug_dir, exist_ok=True)

#     # 2) blur to suppress high-frequency JPEG artifacts
#     blur = cv2.GaussianBlur(img, (5, 5), 0)
#     gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
#     cv2.imwrite(os.path.join(debug_dir, "gray.jpg"), gray)

#     # 3) adaptive threshold with a blocksize ~1/20 of width (and odd)
#     h, w = gray.shape
#     # block = max(3, (w // 20) | 1) 
#     block = max(3, ((w // 40) | 1))  # half as big a window
    
#     thresh = cv2.adaptiveThreshold(
#         gray, 255,
#         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY_INV,
#         block, 2
#     )
#     cv2.imwrite(os.path.join(debug_dir, "thresh.jpg"), thresh)

#     # 4) dynamic Canny: low/high = 1%/3% of 255
#     low = max(10, int(255 * 0.01))
#     high = max(30, int(255 * 0.03))
#     edges = cv2.Canny(thresh, low, high)
#     cv2.imwrite(os.path.join(debug_dir, "edges.jpg"), edges)

#     # # 5) morphology: close + dilate with a kernel ~1/200 of width
#     ksize = max(3, (w // 200) | 1)
#     kernel = np.ones((ksize, ksize), np.uint8)
#     closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=1)
#     dilated = cv2.dilate(closed, kernel, iterations=1)
#     cv2.imwrite(os.path.join(debug_dir, "edges_fixed.jpg"), dilated)






#     # 6) find the largest 4-point contour
#     contours, _ = cv2.findContours(
#         dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
#     )
#     board = None
#     max_area = 0
#     for cnt in contours:
#         approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
#         if len(approx) == 4:
#             x, y, ww, hh = cv2.boundingRect(approx)
#             area = ww*hh
#             if area > max_area:
#                 max_area = area
#                 board = (x, y, ww, hh)

#     if not board:
#         return None, None

#     x, y, ww, hh = board
#     # debug overlay
#     vis = img.copy()
#     cv2.rectangle(vis, (x,y), (x+ww, y+hh), (0,255,0), 3)
#     cv2.imwrite(os.path.join(debug_dir, "contours.jpg"), vis)

#     # crop & save
#     crop = img[y:y+hh, x:x+ww]
#     fname = f"board_{uuid.uuid4()}.jpg"
#     path  = os.path.join(output_dir, fname)
#     cv2.imwrite(path, crop)
#     return path, board











def crop_board_standard(img, output_dir):
    # 1) Debug folder
    debug_dir = os.path.join(output_dir, "debug")
    os.makedirs(debug_dir, exist_ok=True)

    # 2) Blur + grayscale
    blur = cv2.GaussianBlur(img, (5,5), 0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(debug_dir, "gray.jpg"), gray)

    # 3) Adaptive threshold
    h_img, w_img = gray.shape
    block = max(3, ((w_img // 40) | 1))
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        block, 2
    )
    cv2.imwrite(os.path.join(debug_dir, "thresh.jpg"), thresh)

    # 4) Canny edges
    low  = max(10, int(255 * 0.01))
    high = max(30, int(255 * 0.03))
    edges = cv2.Canny(thresh, low, high)
    cv2.imwrite(os.path.join(debug_dir, "edges.jpg"), edges)

    # 5) Try closing with increasing strength until we get a 4-point rectangle
    def find_board_from(masked_edges):
        contours, _ = cv2.findContours(
            masked_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        best = (None, 0)  # (coords, area)
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
            if len(approx) != 4:
                continue
            x,y,ww,hh = cv2.boundingRect(approx)
            area = ww * hh
            # filter out tiny quads
            if ww < 0.5 * w_img or hh < 0.5 * h_img:
                continue
            # roughly square
            ratio = hh / float(ww)
            if not (0.7 <= ratio <= 1.3):
                continue
            if area > best[1]:
                best = ((x,y,ww,hh), area)
        return best[0]

    # We will mask out the top 15% (score/diamond) before any closing
    H, W = edges.shape
    y0   = int(0.15 * H)
    base = edges.copy()
    base[:y0,:] = edges[:y0,:]  # preserve top, though it won't be closed

    board = None
    trials = [
        # (kernel_div, iterations)
        (200, 1),  # gentle: (w//200)//2 inside
        (150, 1),  # a bit stronger
        (150, 2),  # stronger still
        (100, 2),  # fallback: bigger kernel
    ]

    for div, iters in trials:
        raw = (W // div) // 2
        ksize = max(3, (raw | 1))
        ksize = min(ksize, 15)                 # cap at 15×15
        kernel = np.ones((ksize, ksize), np.uint8)

        # apply closing only to the bottom 85%
        closed = base.copy()
        roi    = closed[y0:,:]
        closed_roi = cv2.morphologyEx(roi, cv2.MORPH_CLOSE, kernel, iterations=iters)
        closed[y0:,:] = closed_roi

        fname = f"edges_closed_{ksize}x{ksize}_iter{iters}.jpg"
        cv2.imwrite(os.path.join(debug_dir, fname), closed)

        board = find_board_from(closed)
        if board:
            edges_fixed = closed
            cv2.imwrite(os.path.join(debug_dir, "edges_fixed.jpg"), edges_fixed)
            break

    if not board:
        # final debug dump
        cv2.imwrite(os.path.join(debug_dir, "edges_failed.jpg"), base)
        return None, None

    # 6) We have our board rectangle
    x, y, ww, hh = board

    # 7) Debug draw
    vis = img.copy()
    cv2.rectangle(vis, (x, y), (x+ww, y+hh), (0,255,0), 3)
    cv2.imwrite(os.path.join(debug_dir, "contours.jpg"), vis)

    # 8) Crop & save
    crop = img[y:y+hh, x:x+ww]
    fname = f"board_{uuid.uuid4()}.jpg"
    path  = os.path.join(output_dir, fname)
    cv2.imwrite(path, crop)
    return path, board




# --------------------experiment-------------







# old working



# def crop_board(image_path: str, output_dir: str):
#     # 1) load and optional debug folder
#     img = cv2.imread(image_path)
#     debug_dir = os.path.join(output_dir, "debug")
#     os.makedirs(debug_dir, exist_ok=True)

#     # 2) blur to suppress high-frequency JPEG artifacts
#     blur = cv2.GaussianBlur(img, (5, 5), 0)
#     gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
#     cv2.imwrite(os.path.join(debug_dir, "gray.jpg"), gray)

#     # 3) adaptive threshold with a blocksize ~1/20 of width (and odd)
#     h, w = gray.shape
#     block = max(3, (w // 20) | 1)  # ensure odd, >=3
#     thresh = cv2.adaptiveThreshold(
#         gray, 255,
#         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY_INV,
#         block, 2
#     )
#     cv2.imwrite(os.path.join(debug_dir, "thresh.jpg"), thresh)

#     # 4) dynamic Canny: low/high = 1%/3% of 255
#     low = max(10, int(255 * 0.01))
#     high = max(30, int(255 * 0.03))
#     edges = cv2.Canny(thresh, low, high)
#     cv2.imwrite(os.path.join(debug_dir, "edges.jpg"), edges)

#     # 5) morphology: close + dilate with a kernel ~1/200 of width
#     ksize = max(3, (w // 200) | 1)
#     kernel = np.ones((ksize, ksize), np.uint8)
#     closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)
#     dilated = cv2.dilate(closed, kernel, iterations=1)
#     cv2.imwrite(os.path.join(debug_dir, "edges_fixed.jpg"), dilated)

#     # 6) find the largest 4-point contour
#     contours, _ = cv2.findContours(
#         dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
#     )
#     board = None
#     max_area = 0
#     for cnt in contours:
#         approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
#         if len(approx) == 4:
#             x, y, ww, hh = cv2.boundingRect(approx)
#             area = ww*hh
#             if area > max_area:
#                 max_area = area
#                 board = (x, y, ww, hh)

#     if not board:
#         return None, None

#     x, y, ww, hh = board
#     # debug overlay
#     vis = img.copy()
#     cv2.rectangle(vis, (x,y), (x+ww, y+hh), (0,255,0), 3)
#     cv2.imwrite(os.path.join(debug_dir, "contours.jpg"), vis)

#     # crop & save
#     crop = img[y:y+hh, x:x+ww]
#     fname = f"board_{uuid.uuid4()}.jpg"
#     path  = os.path.join(output_dir, fname)
#     cv2.imwrite(path, crop)
#     return path, board













# ----------------------------------------------------------------------


def process_image(image_path: str):
    # 0) sanity check
    if not image_path or not os.path.exists(image_path):
        raise ValueError(f"Invalid image path: {image_path}")

    # 1) load & resize square
    img = cv2.imread(image_path)
    img = cv2.resize(img, (800, 800), interpolation=cv2.INTER_AREA)
    cv2.imwrite('resized_image.jpg', img)

    # 2) convert to HSV and pull out V channel
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    V   = hsv[:, :, 2]

    # 3) chop into 8×8 grid
    h, w = V.shape
    cell_h = h // 8
    cell_w = w // 8

    # optional debug folder
    debug_dir = os.path.splitext(image_path)[0] + "_v_debug"
    os.makedirs(debug_dir, exist_ok=True)

    # 4) for each cell, sample a central patch to avoid grid lines
    margin_h = int(0.1 * cell_h)
    margin_w = int(0.1 * cell_w)

    board = []
    for r in range(8):
        row = []
        for c in range(8):
            y0 = r * cell_h + margin_h
            y1 = (r + 1) * cell_h - margin_h
            x0 = c * cell_w + margin_w
            x1 = (c + 1) * cell_w - margin_w

            patch = V[y0:y1, x0:x1]
            mean_val = float(patch.mean())

            # DEBUG: write out each patch as an image so you can eyeball it
            # cv2.imwrite(os.path.join(debug_dir, f"cell_{r}_{c}.jpg"), patch)

            # if we’re bright enough → there’s a colored block here:
            #  → 0 = filled, 1 = empty (to match your existing convention)
            row.append(1 if mean_val > 100 else 0)
        board.append(row)

    # 5) optional: save a diagnostic “board of means”
    #    (you can print board or log it)
    return board










# def process_image(board_img_path: str):
#     img = cv2.imread(board_img_path)
#     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#     # looser blue-threshold
#     lower = np.array([100,  80,  40])
#     upper = np.array([130, 255, 255])
#     mask  = cv2.inRange(hsv, lower, upper)

#     h, w = mask.shape
#     cell_w = w / 8.0
#     cell_h = h / 8.0

#     board = []
#     for r in range(8):
#         y0 = int(r * cell_h)
#         y1 = int((r + 1) * cell_h)
#         row = []
#         for c in range(8):
#             x0 = int(c * cell_w)
#             x1 = int((c + 1) * cell_w)
#             cell = mask[y0:y1, x0:x1]

#             # fraction of blue pixels
#             fill_ratio = np.count_nonzero(cell) / float(cell.size)
#             # 0 = block, 1 = empty
#             row.append(0 if fill_ratio > 0.2 else 1)
#         board.append(row)

#     return board


















# def crop_shapes(image_path: str, board_coords: tuple, output_path: str):
#     image = cv2.imread(image_path)
    
#     if board_coords is None or len(board_coords) != 4:
#         raise ValueError(f"Expected 4 values in board_coords, got {board_coords}")

#     x, y, w, h = board_coords  # Now safe to unpack
    
#     # Extending height dynamically
#     shape_area_start = y + h + 30 # Start right after the board
#     shape_area_height = h // 2  # Adjust this if needed
    
#     cropped_shapes = image[shape_area_start:shape_area_start+shape_area_height, x:x+w]
    
#     # shapes_path = os.path.join(CROPPED_DIR, "cropped_shapes.jpg")
#     cv2.imwrite(output_path, cropped_shapes)
#     return output_path






# old working


# def crop_shapes(image_path: str, board_coords: tuple, output_path: str):
#     image = cv2.imread(image_path)
    
#     if board_coords is None or len(board_coords) != 4:
#         raise ValueError(f"Expected 4 values in board_coords, got {board_coords}")

#     x, y, w, h = board_coords

#     # Original cropping logic
#     shape_area_start = y + h + 30
#     shape_area_height = h // 2
#     cropped_shapes = image[shape_area_start:shape_area_start+shape_area_height, x:x+w]

#     # New: Detect and remove ad banner from bottom
#     cropped_shapes = remove_ad_banner(cropped_shapes)

#     cv2.imwrite(output_path, cropped_shapes)
#     return output_path




# def remove_ad_banner(cropped_image):
#     # Process only bottom 30% of the image
#     height, width = cropped_image.shape[:2]
#     bottom_region = cropped_image[int(height*0.7):, :]

#     # Use similar processing to detect_shapes()
#     gray = cv2.cvtColor(bottom_region, cv2.COLOR_BGR2GRAY)
#     thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                  cv2.THRESH_BINARY_INV, 101, 10)
#     kernel = np.ones((3, 3), np.uint8)
#     thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

#     # Find large contours in bottom region
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     min_area = (width * height * 0.3) * 0.15  # 15% of bottom region area
#     ad_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

#     if not ad_contours:
#         return cropped_image  # No ad detected

#     # Find the highest point of the ad banner
#     ad_top = min([cv2.boundingRect(cnt)[1] for cnt in ad_contours])
    
#     # Convert coordinate back to original image space
#     ad_top_absolute = int(height*0.7) + ad_top
    
#     # Crop out the ad banner region
#     return cropped_image[:ad_top_absolute, :]





# -------------------------------experiment-----------------------------







# def crop_shapes(image_path: str, board_coords: tuple, output_path: str):
#     """
#     Always crop the “below‐board” area. For narrow (<600px) images, 
#     resize to 800px wide (preserving aspect ratio) so that
#     board_coords line up, then crop in that space.
#     """
#     # 1) load
#     image = cv2.imread(image_path)
#     if image is None:
#         raise FileNotFoundError(f"Cannot read {image_path}")
#     h0, w0 = image.shape[:2]
    
#     # 2) if narrow, resize to 800px wide, preserve aspect ratio
#     if w0 < 600:
#         scale = 800.0 / w0
#         new_w, new_h = 800, int(h0 * scale)
#         image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        
#         # scale the board coordinates
#         x, y, w, h = board_coords
#         x = int(x * scale)
#         y = int(y * scale)
#         w = int(w * scale)
#         h = int(h * scale)
#     else:
#         x, y, w, h = board_coords

#     H, W = image.shape[:2]

#     # 3) define the region just below the board, half the remaining height
#     start_y = min(y + h + 30, H)
#     end_y   = min(start_y + (H - (y + h)) // 2, H)
#     cropped = image[start_y:end_y, x:x+w]

#     # 4) fallback if it came out empty
#     if cropped.size == 0:
#         cropped = image[y+h:, x:x+w]
#         if cropped.size == 0:
#             # give up—save the full image
#             cv2.imwrite(output_path, image)
#             return output_path

#     # 5) remove any ad banner at the bottom
#     try:
#         cleaned = remove_ad_banner(cropped)
#     except Exception:
#         cleaned = cropped

#     # 6) write result
#     cv2.imwrite(output_path, cleaned)
#     return output_path


















def remove_ad_banner(cropped_image):
    h, w = cropped_image.shape[:2]
    bottom_y = int(h * 0.7)
    if bottom_y >= h or h < 20 or w < 20:
        return cropped_image

    bottom_region = cropped_image[bottom_y:, :]
    if bottom_region.size == 0:
        return cropped_image

    gray = cv2.cvtColor(bottom_region, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        101, 10
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    min_area = (w * (h - bottom_y)) * 0.15
    ads = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

    if not ads:
        return cropped_image

    # crop off everything below the top of the ad
    ad_top = min(cv2.boundingRect(cnt)[1] for cnt in ads)
    ad_top_absolute = bottom_y + ad_top
    return cropped_image[:ad_top_absolute, :]


def crop_board_small(orig, output_dir):
    """
    Detect the board in any <600px‐wide screenshot by
    upscaling to 800px wide (preserve aspect), finding
    the largest quad, then mapping coords back 1:1.
    """
    h0, w0 = orig.shape[:2]

    # ——— 1) upscale to 800px wide, keep aspect ratio ———
    scale = 800.0 / w0
    new_w, new_h = 800, int(h0 * scale)
    resized = cv2.resize(orig, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # standard preprocessing on resized
    gray = cv2.cvtColor(cv2.GaussianBlur(resized, (5,5), 0),
                        cv2.COLOR_BGR2GRAY)
    block = max(3, (new_w // 20) | 1)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        block, 2
    )
    edges = cv2.Canny(thresh,
                      max(10, int(255*0.01)),
                      max(30, int(255*0.03)))
    k = max(3, (new_w // 200) | 1)
    kernel = np.ones((k, k), np.uint8)
    clean = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)
    dilated = cv2.dilate(clean, kernel, iterations=1)

    # ——— 2) find the biggest 4-point contour in top half ———
    quads = []
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
        if len(approx) == 4:
            x, y, ww, hh = cv2.boundingRect(approx)
            # if y < new_h * 0.5 and 0.8 <= ww/float(hh) <= 1.25:
            # allow quads anywhere, with a broader shape tolerance
            if 0.6 <= ww/float(hh) <= 1.4:
                quads.append((ww*hh, (x, y, ww, hh)))
    if quads:
        _, (x8, y8, w8, h8) = max(quads, key=lambda t: t[0])
    else:
        # fallback: largest quad anywhere
        x8 = y8 = w8 = h8 = None
        max_area = 0
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
            if len(approx) == 4:
                x, y, ww, hh = cv2.boundingRect(approx)
                if ww*hh > max_area:
                    max_area = ww*hh
                    x8, y8, w8, h8 = x, y, ww, hh
    if x8 is None:
        return None, None

    # ——— 3) map coords *back* to original (uniform scaling) ———
    inv_scale = w0 / float(new_w)
    x0 = int(x8 * inv_scale)
    y0 = int(y8 * inv_scale)
    w0_box = int(w8 * inv_scale)
    h0_box = int(h8 * inv_scale)

    # clamp to bounds
    x0 = max(0, min(x0, w0-1))
    y0 = max(0, min(y0, h0-1))
    w0_box = max(1, min(w0_box, w0-x0))
    h0_box = max(1, min(h0_box, h0-y0))

    # ——— 4) crop & save on original ———
    board_crop = orig[y0:y0+h0_box, x0:x0+w0_box]
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"board_{uuid.uuid4()}.jpg")
    cv2.imwrite(path, board_crop)
    return path, (x0, y0, w0_box, h0_box)


def crop_shapes(image_path: str, board_coords: tuple, output_path: str):
    """
    Given a board_coords in the ORIGINAL image space:
     1) Load.
     2) If narrow, upscale to 800px wide (same as board_small),
        scale coords back onto that.
     3) Compute a dynamic vertical gap and crop-height.
     4) Fallback if empty.
     5) Strip any ad-banner.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Cannot read {image_path}")
    h0, w0 = img.shape[:2]
    x, y, w, h = board_coords

    # ——— 1) upscale narrow images exactly like crop_board_small ———
    if w0 < 600:
        scale = 800.0 / w0
        new_w, new_h = 800, int(h0 * scale)
        img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
        x, y, w, h = (int(x * scale), int(y * scale),
                      int(w * scale), int(h * scale))

    H, W = img.shape[:2]

    # ——— 2) dynamic gap & crop height ———
    # gap is at least 3% of full height _or_ 10% of the board height
    gap = max(int(0.03 * H), int(0.10 * h))
    below_px = H - (y + h)
    # crop_h  = int(0.4 * below_px)
    # take up to 40% but no more than, say, 500px
    crop_h = min(int(0.4 * below_px), 500)


    start_y = min(y + h + gap, H)
    end_y   = min(start_y + crop_h, H)
    cropped = img[start_y:end_y, x:x+w]

    # ——— 3) fallback if empty ———
    if cropped.size == 0:
        cropped = img[y+h:, x:x+w]
        if cropped.size == 0:
            cv2.imwrite(output_path, img)
            return output_path

    # ——— 4) remove any ad banner ———
    try:
        cleaned = remove_ad_banner(cropped)
    except Exception:
        cleaned = cropped

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, cleaned)
    return output_path



# -------------------------------experiment-----------------------------



# old working


# def crop_shapes(image_path: str, board_coords: tuple, output_path: str):
#     """
#     Always crop the “below‐board” shapes area, but for narrow (<600px)
#     images we first resize to 800×800 so that board_coords line up,
#     then crop in that space.
#     """
#     # 1) load
#     image = cv2.imread(image_path)
#     if image is None:
#         raise FileNotFoundError(f"Cannot read {image_path}")
#     h0, w0 = image.shape[:2]

#     # 2) if narrow, resize entire screenshot to 800×800
#     #    so that board_coords from crop_board_small make sense
#     if w0 < 600:
#         image = cv2.resize(image, (800, 800), interpolation=cv2.INTER_AREA)

#     # 3) unpack coords (these are now in the same coordinate space)
#     x, y, w, h = board_coords
#     H, W = image.shape[:2]

#     # 4) define the region just below the board, half the remaining height
#     start_y = min(y + h + 30, H)
#     end_y   = min(start_y + (H - (y + h)) // 2, H)

#     cropped = image[start_y:end_y, x:x+w]

#     # 5) fallback if it came out empty
#     if cropped.size == 0:
#         cropped = image[y+h:, x:x+w]
#         if cropped.size == 0:
#             # give up—save the full image
#             cv2.imwrite(output_path, image)
#             return output_path

#     # 6) remove any ad banner at the bottom
#     try:
#         cleaned = remove_ad_banner(cropped)
#     except Exception:
#         cleaned = cropped

#     # 7) write result
#     cv2.imwrite(output_path, cleaned)
#     return output_path


# def remove_ad_banner(cropped_image):
#     h, w = cropped_image.shape[:2]
#     # if image is too small or bottom slice would be empty, skip
#     bottom_y = int(h * 0.7)
#     if bottom_y >= h or h < 20 or w < 20:
#         return cropped_image

#     bottom_region = cropped_image[bottom_y:, :]
#     if bottom_region.size == 0:
#         return cropped_image

#     # Convert to gray _only_ if we actually have some pixels
#     gray = cv2.cvtColor(bottom_region, cv2.COLOR_BGR2GRAY)
#     thresh = cv2.adaptiveThreshold(
#         gray, 255,
#         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY_INV,
#         101, 10
#     )
#     kernel = np.ones((3, 3), np.uint8)
#     thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

#     # find any big “ad” contours...
#     contours, _ = cv2.findContours(
#         thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
#     )
#     min_area = (w * (h - bottom_y)) * 0.15
#     ads = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

#     if not ads:
#         return cropped_image

#     # find the top‐most pixel of any ad contour
#     ad_top = min(cv2.boundingRect(cnt)[1] for cnt in ads)
#     ad_top_absolute = bottom_y + ad_top

#     return cropped_image[:ad_top_absolute, :]













# -----------------------------------------------------------

# working

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
    
    debug_dir = "debug_images"
    os.makedirs(debug_dir, exist_ok=True)
    cv2.imwrite(f"{debug_dir}/debug_threshold.jpg", thresh)

    return {"shapes": shape_paths}  # Returning JSON-serializable format



# # all shapes getting detected



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
        contour_img = img.copy()
        cv2.drawContours(contour_img, contours, -1, (0,255,0), 2)
        cv2.imwrite(f"4_contours_{filename}", contour_img)
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


# -----------------------experimant--------------------




# -----------------------experimant--------------------


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




def process_and_resize_image(contents: bytes) -> bytes:
    """Resize image to 1080x2400 while preserving aspect ratio and padding if needed"""
    # Decode image
    image = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Invalid image file")

    # Target dimensions (width, height)
    target_width = 1080
    target_height = 2400

    # Skip if already at target size
    if image.shape[1] == target_width and image.shape[0] == target_height:
        return contents

    # Calculate new size preserving aspect ratio
    h, w = image.shape[:2]
    scale = min(target_width / w, target_height / h)
    new_w, new_h = int(w * scale), int(h * scale)

    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

    # Padding to fit target size
    delta_w = target_width - new_w
    delta_h = target_height - new_h
    top, bottom = delta_h // 2, delta_h - (delta_h // 2)
    left, right = delta_w // 2, delta_w - (delta_w // 2)

    padded = cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))

    # Final encode with JPEG optimization
    success, encoded = cv2.imencode(
        '.jpg',
        padded,
        [int(cv2.IMWRITE_JPEG_QUALITY), 90,
         int(cv2.IMWRITE_JPEG_OPTIMIZE), 1]
    )

    if not success:
        raise ValueError("Image encoding failed")

    return encoded.tobytes()


# def process_and_resize_board(contents: bytes) -> bytes:
#     """Resize image to 1080x2400 while preserving aspect ratio and padding if needed"""
#     # Decode image
#     image = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
#     if image is None:
#         raise ValueError("Invalid image file")

#     # Target dimensions (width, height)
#     target_width = 994
#     target_height = 969

#     # Skip if already at target size
#     if image.shape[1] == target_width and image.shape[0] == target_height:
#         return contents

#     # Calculate new size preserving aspect ratio
#     h, w = image.shape[:2]
#     scale = min(target_width / w, target_height / h)
#     new_w, new_h = int(w * scale), int(h * scale)

#     resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

#     # Padding to fit target size
#     delta_w = target_width - new_w
#     delta_h = target_height - new_h
#     top, bottom = delta_h // 2, delta_h - (delta_h // 2)
#     left, right = delta_w // 2, delta_w - (delta_w // 2)

#     padded = cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))

#     # Final encode with JPEG optimization
#     success, encoded = cv2.imencode(
#         '.jpg',
#         padded,
#         [int(cv2.IMWRITE_JPEG_QUALITY), 90,
#          int(cv2.IMWRITE_JPEG_OPTIMIZE), 1]
#     )

#     if not success:
#         raise ValueError("Image encoding failed")

#     return encoded.tobytes()



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


        contents = await file.read()





        # Decode just for dimension check
        image = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Invalid image file")


        processed = contents
        # h, w = image.shape[:2]
        # needs_resize = not (w == 1080 and h == 2400)

        # if needs_resize:
        #     processed = await run_in_threadpool(process_and_resize_image, contents)
        #     was_resized = True
        # else:
        #     processed = contents
        #     was_resized = False




        # # Process and resize
        # processed = await run_in_threadpool(
        #     process_and_resize_image, 
        #     contents  # Removed explicit size parameter
        # )
        
        # # Save resized image
        file_path = os.path.join(dirs["upload"], file.filename)
        async with aiofiles.open(file_path, "wb") as buffer:
            await buffer.write(processed)
        


        # # Verify file exists before processing
        # if not os.path.exists(file_path):
        #     raise RuntimeError("Resized image not saved")








        # Save uploaded file
        # file_path = os.path.join(dirs["upload"], file.filename)
        # async with aiofiles.open(file_path, "wb") as buffer:
        #     while chunk := await file.read(8192):
        #         await buffer.write(chunk)

        # Process board
        cropped_board_path, board_coords = await run_in_threadpool(
            crop_board, 
            file_path,
            dirs["cropped"],  
           

        )

        if not board_coords:
            raise ValueError("Failed to detect game board")


        cropped = cv2.imread(cropped_board_path)
        cropped_std = cv2.resize(cropped, (800, 800), interpolation=cv2.INTER_AREA)
        cv2.imwrite(cropped_board_path, cropped_std)    


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
        # background_tasks.add_task(cleanup_directory, dirs["upload"])
        # background_tasks.add_task(cleanup_directory, dirs["cropped"])
        # background_tasks.add_task(cleanup_directory, dirs["shapes"])
        

        # for name, arr in processed_cropped_shapes.items():
        #     print(f"{name} =>")
        #     for row in arr:
        #         print(row)
        #     print()

        for row in board_matrix:
            print(' '.join(map(str, row)))

        for idx, board in enumerate(stepwise_boards):
            print(f"Step {idx+1}:")
            for row in board:
                print(row)
            print("--------------------")

        for shape_name, matrix in processed_shapes.items():
            print(f"\n{shape_name}:")
            for row in matrix:
                print(' '.join(str(val) for val in row))


        return {
            "shape_colors": shape_colors,
            "final_output": stepwise_boards
        }

    except Exception as e:
        # Cleanup on error
        # for d in dirs.values():
        #     cleanup_directory(d)
        traceback.print_exc()
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

