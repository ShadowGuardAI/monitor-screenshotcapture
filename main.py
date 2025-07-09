import argparse
import logging
import os
import sys
import time
from datetime import datetime

try:
    from PIL import ImageGrab  # type: ignore
except ImportError:
    print("Pillow (PIL) is required. Install with: pip install Pillow")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_argparse():
    """
    Sets up the argument parser for the screenshot capture tool.
    """
    parser = argparse.ArgumentParser(description="Captures screenshots of the active window at set intervals.")

    parser.add_argument("-i", "--interval", type=int, default=60,
                        help="Interval in seconds between screenshots (default: 60). Must be a positive integer.")

    parser.add_argument("-o", "--output_dir", type=str, default="screenshots",
                        help="Output directory for screenshots (default: screenshots).")

    parser.add_argument("-n", "--name_prefix", type=str, default="screenshot",
                        help="Prefix for screenshot filenames (default: screenshot).")

    parser.add_argument("-q", "--quality", type=int, default=90,
                        help="JPEG quality of screenshots (0-100, default: 90). Higher value means better quality, but larger file size.")
    
    parser.add_argument("-f", "--format", type=str, default="JPEG", choices=["JPEG", "PNG", "BMP"],
                        help="Format of screenshots (default: JPEG). Options: JPEG, PNG, BMP.")
    
    parser.add_argument("-d", "--duration", type=int, default=0,
                        help="Duration to capture screenshots in seconds. 0 means run indefinitely (default: 0).")
                        

    return parser.parse_args()


def capture_screenshot(output_dir, name_prefix, quality, format):
    """
    Captures a screenshot of the active window and saves it to the specified directory.

    Args:
        output_dir (str): The directory to save the screenshot to.
        name_prefix (str): The prefix for the screenshot filename.
        quality (int): The quality of the JPEG image (0-100).
        format (str): The image format (JPEG, PNG, BMP).
    """
    try:
        # Capture the screenshot
        screenshot = ImageGrab.grab()

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Generate the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(output_dir, f"{name_prefix}_{timestamp}.{format.lower()}")

        # Save the screenshot
        if format == "JPEG":
            screenshot.save(filename, "JPEG", quality=quality)
        else:
            screenshot.save(filename, format)

        logging.info(f"Screenshot saved to: {filename}")

    except Exception as e:
        logging.error(f"Error capturing screenshot: {e}")


def validate_args(args):
    """
    Validates the command line arguments.

    Args:
        args (argparse.Namespace): The parsed command line arguments.

    Returns:
        bool: True if the arguments are valid, False otherwise.
    """
    if args.interval <= 0:
        logging.error("Interval must be a positive integer.")
        return False

    if not 0 <= args.quality <= 100:
        logging.error("Quality must be between 0 and 100.")
        return False
    
    if args.duration < 0:
        logging.error("Duration must be a non-negative integer.")
        return False

    return True


def main():
    """
    Main function to run the screenshot capture tool.
    """
    args = setup_argparse()

    if not validate_args(args):
        sys.exit(1)

    interval = args.interval
    output_dir = args.output_dir
    name_prefix = args.name_prefix
    quality = args.quality
    format = args.format
    duration = args.duration

    logging.info("Starting screenshot capture...")
    logging.info(f"Interval: {interval} seconds")
    logging.info(f"Output directory: {output_dir}")
    logging.info(f"Name prefix: {name_prefix}")
    logging.info(f"Quality: {quality}")
    logging.info(f"Format: {format}")
    logging.info(f"Duration: {duration} seconds")
    
    start_time = time.time()
    
    try:
        while True:
            capture_screenshot(output_dir, name_prefix, quality, format)
            time.sleep(interval)
            
            if duration > 0 and time.time() - start_time >= duration:
                logging.info("Screenshot capture duration reached. Exiting.")
                break
    except KeyboardInterrupt:
        logging.info("Screenshot capture interrupted by user.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        logging.info("Screenshot capture stopped.")


if __name__ == "__main__":
    # Usage examples:
    # 1. Capture screenshots every 60 seconds and save to the "screenshots" directory with the prefix "screenshot":
    #    python main.py
    #
    # 2. Capture screenshots every 10 seconds and save to the "my_screenshots" directory with the prefix "window":
    #    python main.py -i 10 -o my_screenshots -n window
    #
    # 3. Capture screenshots with JPEG quality 75:
    #    python main.py -q 75
    #
    # 4. Capture screenshots in PNG format:
    #    python main.py -f PNG
    #
    # 5. Capture screenshots for 300 seconds (5 minutes):
    #    python main.py -d 300
    
    main()