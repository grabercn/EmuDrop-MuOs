import os
import sys
import json
from typing import Optional

class Config:
    """Application configuration settings"""
    # Application metadata
    APP_NAME = "EmuDrop" 
    
    # Base screen settings (reference resolution)
    BASE_SCREEN_WIDTH = 1280
    BASE_SCREEN_HEIGHT = 720
    
    # Current screen settings
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    
    # Scaling factors
    SCALE_X = SCREEN_WIDTH / BASE_SCREEN_WIDTH
    SCALE_Y = SCREEN_HEIGHT / BASE_SCREEN_HEIGHT
    SCALE_FACTOR = min(SCALE_X, SCALE_Y)  # Use minimum to maintain aspect ratio
    
    FPS_LIMIT_LOW_POWER = 30  # Lower FPS limit for devices like Trimui Smart Pro
    FRAME_TIME = int(1000 / FPS_LIMIT_LOW_POWER)  # Frame time in milliseconds (33.33ms for 30 FPS)

    # Directory paths
    BASE_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))
    ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
    DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")  # For temporary downloads
    
    IMAGES_DIR = os.path.join(ASSETS_DIR, 'images')
    IMAGES_CONTROLS_DIR = os.path.join(IMAGES_DIR, 'controls')
    IMAGES_CONSOLES_DIR = os.path.join(IMAGES_DIR, 'consoles')
    IMAGES_CACHE_DIR = os.path.join(IMAGES_DIR, 'cache')
    FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')
    DEFAULT_IMAGE_PATH = os.path.join(IMAGES_DIR, 'default_image.png')
    MUOS_CATALOG_DIR = os.environ.get("MUOS_CATALOG_DIR")

    # Optional mapping from platform_id to muOS catalogue display folder
    MUOS_PLATFORM_NAMES = {
        # Nintendo
        "GB": "Nintendo Game Boy",
        "GBC": "Nintendo Game Boy Color",
        "GBA": "Nintendo Game Boy Advance",
        "NDS": "Nintendo DS",
        "3DS": "Nintendo 3DS",
        "FC": "Nintendo Famicom",
        "NES": "Nintendo Entertainment System",
        "SFC": "Nintendo Super Famicom",
        "SNES": "Nintendo Super Nintendo Entertainment System",
        "N64": "Nintendo 64",
        "N64DD": "Nintendo 64DD",
        "NGC": "Nintendo GameCube",
        "VB": "Nintendo Virtual Boy",
        "SATELLAVIEW": "Nintendo Satellaview",
        "SGB": "Nintendo Super Game Boy",
        # Sega
        "MS": "Sega Master System",
        "GG": "Sega Game Gear",
        "MD": "Sega Mega Drive",
        "GENESIS": "Sega Genesis",
        "SEGA32X": "Sega 32X",
        "SEGACD": "Sega CD",
        "DC": "Sega Dreamcast",
        "NAOMI": "Sega Naomi",
        "SATURN": "Sega Saturn",
        "SG1000": "Sega SG-1000",
        # Sony
        "PS": "Sony PlayStation",
        "PSP": "Sony PlayStation Portable",
        "PSPMINIS": "Sony PSP Minis",
        # Arcade / CPS / NeoGeo / MAME
        "MAME": "Arcade",
        "MAME2003PLUS": "Arcade",
        "MAME2010": "Arcade",
        "CPS1": "Capcom Play System",
        "CPS2": "Capcom Play System 2",
        "CPS3": "Capcom Play System 3",
        "FBNEO": "Final Burn Neo",
        "NEOGEO": "SNK Neo Geo",
        "NEOCD": "SNK Neo Geo CD",
        # NEC / PC Engine
        "PCE": "NEC PC Engine",
        "PCECD": "NEC PC Engine CD",
        "PCFX": "NEC PC-FX",
        # Atari
        "ATARI2600": "Atari 2600",
        "ATARI5200": "Atari 5200",
        "ATARI7800": "Atari 7800",
        "ATARIST": "Atari ST",
        "ATARI800": "Atari 800",
        "JAGUAR": "Atari Jaguar",
        "LYNX": "Atari Lynx",
        # Commodore / Amiga
        "C64": "Commodore 64",
        "AMIGA": "Commodore Amiga",
        "AMIGACD": "Commodore Amiga CD",
        "AMIGACDTV": "Commodore Amiga CDTV",
        # Bandai / Wonderswan
        "WS": "Bandai WonderSwan",
        "WSC": "Bandai WonderSwan Color",
        # SNK / Handhelds
        "NGP": "Neo Geo Pocket",
        # Misc handheld/retro
        "POKEMINI": "Nintendo PokeMini",
        "TI83": "TI-83",
        "VB": "Nintendo Virtual Boy",
        "PICO": "PICO",
        "ODYSSEY": "Magnavox Odyssey 2",
        "VIDEOPAC": "Magnavox Odyssey 2",
        "INTELLIVISION": "Mattel Intellivision",
        "COLECO": "ColecoVision",
        "COLSGM": "ColecoVision",
        "CHANNELF": "Fairchild Channel F",
        "CPC": "Amstrad CPC",
        "CPLUS4": "Commodore Plus 4",
        "CPET": "Commodore PET",
        "CANNONBALL": "OutRun Cannonball",
        "OPENBOR": "OpenBOR",
        "SCUMMVM": "ScummVM",
        "DOS": "MS-DOS",
        "PC98": "NEC PC-98",
        "PC88": "NEC PC-88",
        "X1": "Sharp X1",
        "X68000": "Sharp X68000",
        "ZXEIGHTYONE": "Sinclair ZX81",
        "ZXS": "Sinclair ZX Spectrum",
        "MSX": "MSX",
        "MSX2": "MSX2",
        "VMAC": "Apple Macintosh",
        # Others
        "DC": "Sega Dreamcast",
        "NAOMI": "Sega Naomi",
        "ARCADE": "Arcade",
        "MAME2010": "Arcade",
    }

    # Override with updated muOS folder display names
    MUOS_PLATFORM_NAMES = {
        # Arcade / multi
        "MAME": "Arcade",
        "MAME2003PLUS": "Arcade",
        "MAME2010": "Arcade",
        "FBNEO": "Arcade",
        "CPS1": "Arcade",
        "CPS2": "Arcade",
        "CPS3": "Arcade",
        "OPENBOR": "External - Ports",
        "CANNONBALL": "External - Ports",

        # Nintendo
        "GB": "Nintendo Game Boy",
        "GBC": "Nintendo Game Boy Color",
        "GBA": "Nintendo Game Boy Advance",
        "NDS": "Nintendo DS",
        "N64": "Nintendo 64",
        "N64DD": "Nintendo N64",
        "FC": "Nintendo NES - Famicom",
        "NES": "Nintendo NES - Famicom",
        "FDS": "Nintendo NES - Famicom",
        "SFC": "Nintendo SNES - SFC",
        "SFCMSU": "Nintendo SNES - SFC",
        "VB": "Nintendo Virtual Boy",
        "SGB": "Nintendo Game Boy",

        # Sega
        "MS": "Sega Master System",
        "GG": "Sega Game Gear",
        "MD": "Sega Mega Drive - Genesis",
        "GENESIS": "Sega Mega Drive - Genesis",
        "SEGA32X": "Sega 32X",
        "SEGACD": "Sega Mega CD - Sega CD",
        "DC": "Sega Dreamcast",
        "NAOMI": "Sega Atomiswave Naomi",
        "ATOMISWAVE": "Sega Atomiswave Naomi",
        "SATURN": "Sega Dreamcast",
        "SG1000": "Sega Master System",

        # Sony
        "PS": "Sony PlayStation",
        "PSP": "Sony PlayStation Portable",
        "PSPMINIS": "Sony PlayStation Portable",

        # NEC / PC Engine
        "PCE": "NEC PC Engine",
        "PCECD": "NEC PC Engine CD",
        "PCFX": "NEC PC Engine SuperGrafx",
        "SFX": "NEC PC Engine SuperGrafx",

        # SNK / Neo Geo
        "NEOGEO": "SNK Neo Geo",
        "NEOCD": "SNK Neo Geo CD",
        "NGP": "SNK Neo Geo Pocket - Color",

        # Atari
        "ATARI2600": "Atari 2600",
        "ATARI5200": "Atari 5200",
        "ATARI7800": "Atari 2600",
        "ATARIST": "Atari 2600",
        "ATARI800": "Atari 2600",
        "LYNX": "Atari Lynx",

        # Commodore / Amiga
        "AMIGA": "Commodore Amiga",
        "AMIGACD": "Commodore Amiga",
        "AMIGACDTV": "Commodore Amiga",
        "C64": "Commodore C64",

        # PC / Misc
        "DOS": "PC DOS",
        "SCUMMVM": "ScummVM",
        "PICO": "PICO-8",
    }

    # Load System OS
    with open(os.path.join(ASSETS_DIR, 'settings.json'), 'r') as f:
        SYSTEMS_OS = json.loads(f.read()).get('os', 'stock')
    
    # Load System Mapping
    with open(os.path.join(ASSETS_DIR, 'systems.json'), 'r') as f:
        SYSTEMS_MAPPING = json.loads(f.read())
    
    # Load Scrapper Config
    with open(os.path.join(ASSETS_DIR, 'settings.json'), 'r') as f:
        scrapper = json.loads(f.read())['scrapper']
        SCRAPER_API_MEDIA_TYPE = scrapper['SCRAPER_API_MEDIA_TYPE']
        SCRAPER_API_MEDIA_WIDTH = scrapper['SCRAPER_API_MEDIA_WIDTH']
        SCRAPER_API_MEDIA_HEIGHT = scrapper['SCRAPER_API_MEDIA_HEIGHT']
        SCRAPER_API_SOFTNAME = scrapper['SCRAPER_API_SOFTNAME']
        SCRAPER_ENCODED_API_USERNAME = scrapper['SCRAPER_ENCODED_API_USERNAME']
        SCRAPER_ENCODED_API_PASSWORD = scrapper['SCRAPER_ENCODED_API_PASSWORD']
        SCRAPER_API_USERSSID = scrapper['SCRAPER_API_USERSSID']
        SCRAPER_API_SSPASS = scrapper['SCRAPER_API_SSPASS']
    
    # Font settings
    BASE_FONT_SIZE = 24
    FONT_SIZE = int(BASE_FONT_SIZE * SCALE_FACTOR)
    FONT_NAME = "arial.ttf"

    # Logging settings
    LOG_FILE = f'{APP_NAME}.log'
    LOG_LEVEL = 'INFO'
    SKIP_SCRAPE = os.environ.get("SKIP_SCRAPE", "1") == "1"
    
    GAMES_PER_PAGE = 10
    CARDS_PER_ROW = 3
    CARDS_PER_PAGE = 9
    
    # Card dimensions (scaled)
    BASE_CARD_WIDTH = 250
    BASE_CARD_HEIGHT = 180
    BASE_CARD_IMAGE_HEIGHT = 120
    BASE_GRID_SPACING = 10
    
    CARD_WIDTH = int(BASE_CARD_WIDTH * SCALE_FACTOR)
    CARD_HEIGHT = int(BASE_CARD_HEIGHT * SCALE_FACTOR)
    CARD_IMAGE_HEIGHT = int(BASE_CARD_IMAGE_HEIGHT * SCALE_FACTOR)
    GRID_SPACING = int(BASE_GRID_SPACING * SCALE_FACTOR)

    # Game list settings (scaled)
    BASE_GAME_LIST_ITEM_HEIGHT = 40
    BASE_GAME_LIST_SPACING = 12
    BASE_GAME_LIST_WIDTH = 450
    BASE_GAME_LIST_START_Y = 120
    BASE_GAME_LIST_IMAGE_SIZE = 400
    BASE_GAME_LIST_CARD_PADDING = 20
    BASE_GAME_LIST_SPACING_BETWEEN = 120
    
    GAME_LIST_ITEM_HEIGHT = int(BASE_GAME_LIST_ITEM_HEIGHT * SCALE_FACTOR)
    GAME_LIST_SPACING = int(BASE_GAME_LIST_SPACING * SCALE_FACTOR)
    GAME_LIST_WIDTH = int(BASE_GAME_LIST_WIDTH * SCALE_FACTOR)
    GAME_LIST_START_Y = int(BASE_GAME_LIST_START_Y * SCALE_FACTOR)
    GAME_LIST_IMAGE_SIZE = int(BASE_GAME_LIST_IMAGE_SIZE * SCALE_FACTOR)
    GAME_LIST_CARD_PADDING = int(BASE_GAME_LIST_CARD_PADDING * SCALE_FACTOR)
    GAME_LIST_SPACING_BETWEEN = int(BASE_GAME_LIST_SPACING_BETWEEN * SCALE_FACTOR)

    # Control guide settings (scaled)
    BASE_CONTROL_SIZE = 75
    BASE_CONTROL_SPACING = 80
    BASE_CONTROL_MARGIN = 80
    BASE_CONTROL_BOTTOM_MARGIN = 60
    
    CONTROL_SIZE = int(BASE_CONTROL_SIZE * SCALE_FACTOR)
    CONTROL_SPACING = int(BASE_CONTROL_SPACING * SCALE_FACTOR)
    CONTROL_MARGIN = int(BASE_CONTROL_MARGIN * SCALE_FACTOR)
    CONTROL_BOTTOM_MARGIN = int(BASE_CONTROL_BOTTOM_MARGIN * SCALE_FACTOR)

    # Dialog settings (scaled)
    BASE_DIALOG_WIDTH = 600
    BASE_DIALOG_HEIGHT = 300
    BASE_DIALOG_PADDING = 40
    BASE_DIALOG_LINE_HEIGHT = 30
    BASE_DIALOG_TITLE_MARGIN = 40
    BASE_DIALOG_MESSAGE_MARGIN = 50
    BASE_DIALOG_BUTTON_Y = 220
    BASE_DIALOG_BUTTON_X = 250
    BASE_DIALOG_BUTTON_WIDTH = 100
    
    DIALOG_WIDTH = int(BASE_DIALOG_WIDTH * SCALE_FACTOR)
    DIALOG_HEIGHT = int(BASE_DIALOG_HEIGHT * SCALE_FACTOR)
    DIALOG_PADDING = int(BASE_DIALOG_PADDING * SCALE_FACTOR)
    DIALOG_LINE_HEIGHT = int(BASE_DIALOG_LINE_HEIGHT * SCALE_FACTOR)
    DIALOG_TITLE_MARGIN = int(BASE_DIALOG_TITLE_MARGIN * SCALE_FACTOR)
    DIALOG_MESSAGE_MARGIN = int(BASE_DIALOG_MESSAGE_MARGIN * SCALE_FACTOR)
    DIALOG_BUTTON_Y = int(BASE_DIALOG_BUTTON_Y * SCALE_FACTOR)
    DIALOG_BUTTON_X = int(BASE_DIALOG_BUTTON_X * SCALE_FACTOR)
    DIALOG_BUTTON_WIDTH = int(BASE_DIALOG_BUTTON_WIDTH * SCALE_FACTOR)

    # Image cache settings
    IMAGE_CACHE_MAX_SIZE_MB = 500
    IMAGE_DOWNLOAD_MAX_RETRIES = 3
    IMAGE_DOWNLOAD_RETRY_DELAYS = [1, 3, 5]  # Delays between retries in seconds
    IMAGE_DOWNLOAD_TIMEOUT = (3, 10)  # (connect timeout, read timeout)
    
    # Loading button mapping
    with open(os.path.join(ASSETS_DIR, 'settings.json'), 'r') as f:
        buttons = json.loads(f.read())['keyMapping']
        # Controller button mapping
        CONTROLLER_BUTTON_A = buttons['CONTROLLER_BUTTON_A']      
        CONTROLLER_BUTTON_B = buttons['CONTROLLER_BUTTON_B']     
        CONTROLLER_BUTTON_X = buttons['CONTROLLER_BUTTON_X']      
        CONTROLLER_BUTTON_Y = buttons['CONTROLLER_BUTTON_Y']    
        CONTROLLER_BUTTON_L = buttons['CONTROLLER_BUTTON_L']   
        CONTROLLER_BUTTON_R = buttons['CONTROLLER_BUTTON_R']     
        CONTROLLER_BUTTON_SELECT = buttons['CONTROLLER_BUTTON_SELECT'] 
        CONTROLLER_BUTTON_START = buttons['CONTROLLER_BUTTON_START']  
        CONTROLLER_BUTTON_MENU = buttons.get('CONTROLLER_BUTTON_MENU', 8)
        
        # D-pad button mappings
        CONTROLLER_BUTTON_UP = buttons['CONTROLLER_BUTTON_UP']     
        CONTROLLER_BUTTON_DOWN = buttons['CONTROLLER_BUTTON_DOWN']   
        CONTROLLER_BUTTON_LEFT = buttons['CONTROLLER_BUTTON_LEFT']  
        CONTROLLER_BUTTON_RIGHT = buttons['CONTROLLER_BUTTON_RIGHT'] 

    CONTROLLER_BUTTON_REPEAT_RATE = 250
    
    # Animation settings
    ANIMATION_DURATION = 300  # milliseconds
    LOADING_ANIMATION_SPEED = 100  # milliseconds per frame
    IMAGE_LOAD_DELAY = 500  # milliseconds to wait before loading game images

    # Download view settings (scaled)
    BASE_DOWNLOAD_VIEW_START_Y = 70
    BASE_DOWNLOAD_VIEW_ITEM_HEIGHT = 110
    BASE_DOWNLOAD_VIEW_SPACING = 15
    BASE_DOWNLOAD_VIEW_PROGRESS_BAR_HEIGHT = 16
    BASE_DOWNLOAD_VIEW_SIDE_PADDING = 30
    BASE_DOWNLOAD_VIEW_INNER_PADDING = 20
    BASE_DOWNLOAD_VIEW_TEXT_PADDING = 40
    BASE_DOWNLOAD_VIEW_TEXT_START_X = 40
    BASE_DOWNLOAD_VIEW_TEXT_Y_OFFSET = 45
    BASE_DOWNLOAD_VIEW_SPEED_X_OFFSET = 180
    BASE_DOWNLOAD_VIEW_SIZE_X_OFFSET = 450
    BASE_DOWNLOAD_VIEW_ETA_X_OFFSET = 700
    BASE_DOWNLOAD_VIEW_TEXT_SPACING = 30  # Base spacing between text elements
    BASE_DOWNLOAD_VIEW_MIN_TEXT_SPACING = 20  # Minimum spacing between text elements
    BASE_DOWNLOAD_VIEW_MAX_TEXT_SPACING = 50  # Maximum spacing between text elements
    
    DOWNLOAD_VIEW_START_Y = int(BASE_DOWNLOAD_VIEW_START_Y * SCALE_FACTOR)
    DOWNLOAD_VIEW_ITEM_HEIGHT = int(BASE_DOWNLOAD_VIEW_ITEM_HEIGHT * SCALE_FACTOR)
    DOWNLOAD_VIEW_SPACING = int(BASE_DOWNLOAD_VIEW_SPACING * SCALE_FACTOR)
    DOWNLOAD_VIEW_PROGRESS_BAR_HEIGHT = int(BASE_DOWNLOAD_VIEW_PROGRESS_BAR_HEIGHT * SCALE_FACTOR)
    DOWNLOAD_VIEW_SIDE_PADDING = int(BASE_DOWNLOAD_VIEW_SIDE_PADDING * SCALE_FACTOR)
    DOWNLOAD_VIEW_INNER_PADDING = int(BASE_DOWNLOAD_VIEW_INNER_PADDING * SCALE_FACTOR)
    DOWNLOAD_VIEW_TEXT_PADDING = int(BASE_DOWNLOAD_VIEW_TEXT_PADDING * SCALE_FACTOR)
    DOWNLOAD_VIEW_TEXT_START_X = int(BASE_DOWNLOAD_VIEW_TEXT_START_X * SCALE_FACTOR)
    DOWNLOAD_VIEW_TEXT_Y_OFFSET = int(BASE_DOWNLOAD_VIEW_TEXT_Y_OFFSET * SCALE_FACTOR)
    DOWNLOAD_VIEW_SPEED_X_OFFSET = int(BASE_DOWNLOAD_VIEW_SPEED_X_OFFSET * SCALE_FACTOR)
    DOWNLOAD_VIEW_SIZE_X_OFFSET = int(BASE_DOWNLOAD_VIEW_SIZE_X_OFFSET * SCALE_FACTOR)
    DOWNLOAD_VIEW_ETA_X_OFFSET = int(BASE_DOWNLOAD_VIEW_ETA_X_OFFSET * SCALE_FACTOR)
    DOWNLOAD_VIEW_TEXT_SPACING = int(BASE_DOWNLOAD_VIEW_TEXT_SPACING * SCALE_FACTOR)
    DOWNLOAD_VIEW_MIN_TEXT_SPACING = int(BASE_DOWNLOAD_VIEW_MIN_TEXT_SPACING * SCALE_FACTOR)
    DOWNLOAD_VIEW_MAX_TEXT_SPACING = int(BASE_DOWNLOAD_VIEW_MAX_TEXT_SPACING * SCALE_FACTOR)

    # Navigation constants
    VISIBLE_DOWNLOADS = 5
    MAX_CONCURRENT_DOWNLOADS = 4
    CARDS_PER_ROW = 3
    CARDS_PER_PAGE = 9  # 3x3 grid
    GAMES_PER_PAGE = 10
    
    # Scroll bar settings (scaled)
    BASE_SCROLL_BAR_WIDTH = 12
    # BASE_SCROLL_BAR_HEIGHT = SCREEN_HEIGHT - 200
    BASE_SCROLL_BAR_HEIGHT = VISIBLE_DOWNLOADS * (BASE_DOWNLOAD_VIEW_ITEM_HEIGHT + DOWNLOAD_VIEW_SPACING) - DOWNLOAD_VIEW_SPACING
    BASE_SCROLL_BAR_X_OFFSET = 20
    BASE_SCROLL_BAR_Y_OFFSET = BASE_DOWNLOAD_VIEW_START_Y
    BASE_SCROLL_BAR_MIN_THUMB_HEIGHT = 30
    
    SCROLL_BAR_WIDTH = int(BASE_SCROLL_BAR_WIDTH * SCALE_FACTOR)
    SCROLL_BAR_HEIGHT = int(BASE_SCROLL_BAR_HEIGHT * SCALE_FACTOR)
    SCROLL_BAR_X_OFFSET = int(BASE_SCROLL_BAR_X_OFFSET * SCALE_FACTOR)
    SCROLL_BAR_Y_OFFSET = int(BASE_SCROLL_BAR_Y_OFFSET * SCALE_FACTOR)
    SCROLL_BAR_MIN_THUMB_HEIGHT = int(BASE_SCROLL_BAR_MIN_THUMB_HEIGHT * SCALE_FACTOR)
    # Resource paths
    FONT_SIZE = 16
    
    # Animation timings
    LOADING_ANIMATION_SPEED = 100  # milliseconds per frame
    IMAGE_LOAD_DELAY = 500  # milliseconds to wait before loading new image
    
    # Network settings
    DOWNLOAD_CHUNK_SIZE = 8192
    TIMEOUT = 10  # seconds
    
    # UI constants
    MAX_TITLE_LENGTH = 50
    PROGRESS_BAR_HEIGHT = 20
    CARD_WIDTH = 200
    CARD_HEIGHT = 150
    CARD_MARGIN = 20

    def reload_key_mapping(cls, settings_path: Optional[str] = None):
        """Reload controller button mapping from settings.json."""
        path = settings_path or os.path.join(cls.ASSETS_DIR, 'settings.json')
        try:
            with open(path, 'r') as f:
                buttons = json.load(f).get('keyMapping', {})
            cls.CONTROLLER_BUTTON_A = buttons.get('CONTROLLER_BUTTON_A', cls.CONTROLLER_BUTTON_A)
            cls.CONTROLLER_BUTTON_B = buttons.get('CONTROLLER_BUTTON_B', cls.CONTROLLER_BUTTON_B)
            cls.CONTROLLER_BUTTON_X = buttons.get('CONTROLLER_BUTTON_X', cls.CONTROLLER_BUTTON_X)
            cls.CONTROLLER_BUTTON_Y = buttons.get('CONTROLLER_BUTTON_Y', cls.CONTROLLER_BUTTON_Y)
            cls.CONTROLLER_BUTTON_L = buttons.get('CONTROLLER_BUTTON_L', cls.CONTROLLER_BUTTON_L)
            cls.CONTROLLER_BUTTON_R = buttons.get('CONTROLLER_BUTTON_R', cls.CONTROLLER_BUTTON_R)
            cls.CONTROLLER_BUTTON_SELECT = buttons.get('CONTROLLER_BUTTON_SELECT', cls.CONTROLLER_BUTTON_SELECT)
            cls.CONTROLLER_BUTTON_START = buttons.get('CONTROLLER_BUTTON_START', cls.CONTROLLER_BUTTON_START)
            cls.CONTROLLER_BUTTON_MENU = buttons.get('CONTROLLER_BUTTON_MENU', getattr(cls, 'CONTROLLER_BUTTON_MENU', 8))
            cls.CONTROLLER_BUTTON_UP = buttons.get('CONTROLLER_BUTTON_UP', cls.CONTROLLER_BUTTON_UP)
            cls.CONTROLLER_BUTTON_DOWN = buttons.get('CONTROLLER_BUTTON_DOWN', cls.CONTROLLER_BUTTON_DOWN)
            cls.CONTROLLER_BUTTON_LEFT = buttons.get('CONTROLLER_BUTTON_LEFT', cls.CONTROLLER_BUTTON_LEFT)
            cls.CONTROLLER_BUTTON_RIGHT = buttons.get('CONTROLLER_BUTTON_RIGHT', cls.CONTROLLER_BUTTON_RIGHT)
        except Exception:
            # On failure, keep existing mapping
            pass

    @classmethod
    def update_screen_size(cls, width, height):
        """Update screen size and recalculate all scaled dimensions"""
        cls.SCREEN_WIDTH = width
        cls.SCREEN_HEIGHT = height
        cls.SCALE_X = width / cls.BASE_SCREEN_WIDTH
        cls.SCALE_Y = height / cls.BASE_SCREEN_HEIGHT
        cls.SCALE_FACTOR = min(cls.SCALE_X, cls.SCALE_Y)
        
        # Update all scaled dimensions
        for attr_name in dir(cls):
            if attr_name.startswith('BASE_'):
                scaled_attr_name = attr_name[5:]  # Remove 'BASE_' prefix
                if hasattr(cls, scaled_attr_name):
                    base_value = getattr(cls, attr_name)
                    if isinstance(base_value, (int, float)):
                        setattr(cls, scaled_attr_name, int(base_value * cls.SCALE_FACTOR))

    @classmethod
    def get_font_path(cls):
        """Find a suitable font file"""
        font_files = [
            os.path.join(cls.FONTS_DIR, cls.FONT_NAME),
            # Add more fallback fonts if needed
        ]
        
        for font_path in font_files:
            if os.path.exists(font_path):
                return font_path
        
        return None 
