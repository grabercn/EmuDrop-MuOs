"""
Main entry point for the Game Downloader application.

This module initializes and runs the main application loop, handling any top-level
exceptions that might occur during execution.
"""
from typing import NoReturn
import sys

def main() -> NoReturn:
    """
    Main entry point for the game downloader application.
    
    Initializes the GameDownloaderApp and handles any uncaught exceptions,
    ensuring they are properly logged before the application exits.
    """
    # Import logger first
    try:
        from utils.logger import logger
    except ImportError as e:
        print(f"CRITICAL: Failed to import logger: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        logger.info("Starting application...")
        
        #load .env file if in development
        if not getattr(sys, 'frozen', False):
            from dotenv import load_dotenv
            load_dotenv()
            logger.info("Environment variables have been loaded successfully from .env file")
            
        # Import app here to catch dependency errors (SDL2, Pillow, etc.)
        from app import GameDownloaderApp
        
        app = GameDownloaderApp()
        app.run()
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
    except Exception as e:
        logger.error(f"Application failed to start: {e}", exc_info=True)
        # Also print to stderr in case file logging failed
        print(f"CRITICAL ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
    finally:
        sys.exit(0)

if __name__ == "__main__":
    main()