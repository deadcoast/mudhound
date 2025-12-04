# MUDHOUND - Design Specification v1.1

> Batch URL extraction from keyword searches via terminal interface

---

## 1. PROJECT IDENTITY

```text
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                                                                          ║
║        ██▄  ▄██ ██  ██ ████▄  ██  ██ ▄████▄ ██  ██ ███  ██ ████▄         ║
║        ██ ▀▀ ██ ██  ██ ██  ██ ██████ ██  ██ ██  ██ ██ ▀▄██ ██  ██        ║
║        ██    ██ ▀████▀ ████▀  ██  ██ ▀████▀ ▀████▀ ██   ██ ████▀         ║
║                                                                          ║
║                 [ Fetch URLs. Filter Noise. Hunt Data. ]                 ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

| Attribute       | Value                                           |
|-----------------|-------------------------------------------------|
| **Name**        | MudHound                                        |
| **Binary**      | `mh`                                            |
| **Version**     | 1.0.0                                           |
| **Python**      | >=3.10                                          |
| **License**     | MIT                                             |
| **CLI Engine**  | Typer                                           |
| **Search Core** | duckduckgo-search (primary), extensible         |

---

## 2. ARCHITECTURE OVERVIEW

### 2.1 Modular Layer Stack

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PRESENTATION LAYER                             │
│ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────────┐   │
│ │ UIRenderer│ │FrameEngine│ │ThemeEngine│ │LayoutMgr  │ │AnimationEngine│   │
│ └───────────┘ └───────────┘ └───────────┘ └───────────┘ └───────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              INTERACTION LAYER                              │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│ │   Prompts   │ │    Menus    │ │ Validators  │ │      Confirmations      │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                               COMMAND LAYER                                 │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│ │   search    │ │   config    │ │   export    │ │        [plugin]         │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                                CORE LAYER                                   │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│ │SearchEngine │ │ ResultStore │ │  Logging    │ │      ConfigManager      │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                               ADAPTER LAYER                                 │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│ │ DuckDuckGo  │ │   Google*   │ │    Bing*    │ │       [custom]*         │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────────────────┘ │
│                              * = future adapters                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Directory Structure

```text
mudhound/
├── __init__.py
├── __main__.py                 # Entry: `python -m mudhound`
├── cli/
│   ├── __init__.py
│   ├── app.py                  # Typer application root
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── search.py           # mh search <query>
│   │   ├── config.py           # mh config [get|set|list]
│   │   ├── export.py           # mh export [json|csv|txt]
│   │   └── history.py          # mh history [list|clear|replay]
│   └── callbacks.py            # Global option callbacks
├── ui/
│   ├── __init__.py
│   ├── renderer.py             # Core rendering engine
│   ├── frames.py               # Box/border primitives
│   ├── layout.py               # Terminal dimension management
│   ├── theme.py                # Color + glyph definitions
│   ├── animation/
│   │   ├── __init__.py
│   │   ├── engine.py           # Animation controller
│   │   ├── frames.py           # Frame sequence management
│   │   ├── timing.py           # Timing/easing functions
│   │   └── schemes.py          # Color scheme definitions
│   ├── components/
│   │   ├── __init__.py
│   │   ├── banner.py           # ASCII art header (animated)
│   │   ├── logo.py             # Compact logo (animated)
│   │   ├── menu.py             # Interactive menus
│   │   ├── prompt.py           # Input prompts
│   │   ├── table.py            # Data tables
│   │   ├── progress.py         # Progress/spinner
│   │   ├── status.py           # Status messages
│   │   └── confirm.py          # Y/N confirmations
│   └── glyphs.py               # Symbol registry (no emojis)
├── core/
│   ├── __init__.py
│   ├── engine.py               # Search orchestration
│   ├── result.py               # Result data models
│   ├── store.py                # Result persistence
│   ├── config.py               # Configuration management
│   └── exceptions.py           # Custom exceptions
├── adapters/
│   ├── __init__.py
│   ├── base.py                 # Abstract adapter interface
│   ├── duckduckgo.py           # DuckDuckGo implementation
│   └── registry.py             # Adapter discovery/loading
├── assets/
│   ├── __init__.py
│   ├── manager.py              # Asset loading/caching
│   ├── animated/
│   │   ├── rainbow-banner/
│   │   │   ├── dark-rainbow-banner.ansi
│   │   │   ├── light-rainbow-banner.ansi
│   │   │   ├── rainbow-banner.ansi
│   │   │   └── white-banner.ansi
│   │   └── rainbow-logo/
│   │       ├── dark-rainbow-logo.ansi
│   │       ├── light-rainbow-logo.ansi
│   │       ├── rainbow-logo.ansi
│   │       └── white-logo.ansi
│   └── static/
│       ├── banner-large.ansi
│       └── banner-minimal.ansi
├── logging/
│   ├── __init__.py
│   ├── handler.py              # Custom log handler
│   ├── formatter.py            # Styled log formatter
│   └── levels.py               # Custom log levels
├── utils/
│   ├── __init__.py
│   ├── terminal.py             # Terminal utilities
│   ├── text.py                 # Text manipulation
│   └── validators.py           # Input validation
└── data/
    ├── config.default.toml     # Default configuration
    └── themes/
        ├── default.toml
        ├── minimal.toml
        └── hacker.toml
```

---

## 3. ANIMATION SYSTEM SPECIFICATION

### 3.1 Animation Engine Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ANIMATION ENGINE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────┐      ┌─────────────┐      ┌─────────────────────────┐     │
│   │FrameLoader  │─────>│ FrameBuffer │─────>│     RenderController    │     │
│   └─────────────┘      └─────────────┘      └─────────────────────────┘     │
│          │                    │                         │                   │
│          ▼                    ▼                         ▼                   │
│   ┌─────────────┐      ┌─────────────┐      ┌─────────────────────────┐     │
│   │ ColorScheme │      │TimingEngine │      │    TerminalOutput       │     │
│   └─────────────┘      └─────────────┘      └─────────────────────────┘     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

ANIMATION FLOW:
1. FrameLoader reads ANSI frame files from assets/animated/
2. ColorScheme applies color transforms based on active scheme
3. FrameBuffer holds pre-rendered frames in memory
4. TimingEngine controls frame timing and transitions
5. RenderController outputs frames to terminal with cursor management
```

### 3.2 Color Schemes

```python
class ColorScheme(Enum):
    """
    Defines available color schemes for animated elements.
    Each scheme maps to a set of ANSI frame files.
    """
    RAINBOW = "rainbow"           # Full spectrum cycling
    DARK_RAINBOW = "dark-rainbow" # Muted/darker rainbow
    LIGHT_RAINBOW = "light-rainbow" # Bright/pastel rainbow
    WHITE = "white"               # Monochrome white
    THEME = "theme"               # Use current theme colors

COLOR_SCHEME_FRAMES = {
    ColorScheme.RAINBOW: [
        "rainbow-frame-01.ansi",
        "rainbow-frame-02.ansi",
        "rainbow-frame-03.ansi",
        "rainbow-frame-04.ansi",
        "rainbow-frame-05.ansi",
        "rainbow-frame-06.ansi",
    ],
    ColorScheme.DARK_RAINBOW: [
        "dark-rainbow-frame-01.ansi",
        "dark-rainbow-frame-02.ansi",
        "dark-rainbow-frame-03.ansi",
        "dark-rainbow-frame-04.ansi",
        "dark-rainbow-frame-05.ansi",
        "dark-rainbow-frame-06.ansi",
    ],
    # ... etc
}
```

### 3.3 Animation Configuration

```toml
# Animation settings in config.toml

[animation]
enabled = true
default_scheme = "rainbow"        # rainbow | dark-rainbow | light-rainbow | white | theme
banner_animation = true
logo_animation = true
frame_rate = 10                   # FPS for animations
transition_duration = 0.15        # Seconds between color transitions
idle_animation = false            # Animate during idle states
on_completion = "flash"           # none | flash | pulse | fade

[animation.banner]
style = "animated"                # animated | static | minimal | none
scheme = "rainbow"                # Override default scheme for banner
loop = true                       # Continuous loop or single pass
duration = 0.0                    # 0 = infinite, >0 = seconds to display

[animation.logo]
style = "animated"
scheme = "rainbow"
position = "inline"               # inline | header | footer
```

### 3.4 Frame Timing System

```python
class TimingEngine:
    """
    Controls animation timing with support for various easing functions.
    """
    
    EASING_FUNCTIONS = {
        "linear":      lambda t: t,
        "ease_in":     lambda t: t * t,
        "ease_out":    lambda t: 1 - (1 - t) ** 2,
        "ease_in_out": lambda t: 2 * t * t if t < 0.5 else 1 - (-2 * t + 2) ** 2 / 2,
        "bounce":      lambda t: 1 - abs(math.cos(t * math.pi * 2.5)) * (1 - t),
    }
    
    def __init__(
        self,
        frame_rate: int = 10,
        easing: str = "linear",
        loop: bool = True
    ):
        self.frame_rate = frame_rate
        self.frame_duration = 1.0 / frame_rate
        self.easing_fn = self.EASING_FUNCTIONS[easing]
        self.loop = loop
        self._running = False
        self._current_frame = 0
    
    def start(self) -> None:
        """Begin animation playback."""
        self._running = True
        self._start_time = time.monotonic()
    
    def stop(self) -> None:
        """Stop animation playback."""
        self._running = False
    
    def get_current_frame(self, total_frames: int) -> int:
        """Calculate current frame index based on elapsed time."""
        if not self._running:
            return 0
        
        elapsed = time.monotonic() - self._start_time
        progress = (elapsed / self.frame_duration) % total_frames
        
        if not self.loop and elapsed >= total_frames * self.frame_duration:
            self._running = False
            return total_frames - 1
        
        return int(progress)
```

### 3.5 Terminal Animation Rendering

```python
class AnimationRenderer:
    """
    Handles terminal-specific animation rendering with cursor management.
    """
    
    def __init__(self, timing: TimingEngine):
        self.timing = timing
        self._last_frame = -1
        self._frame_height = 0
    
    def render_frame(self, frame: str, clear_previous: bool = True) -> None:
        """
        Render a single animation frame to terminal.
        
        RENDERING STRATEGY:
        1. Save cursor position
        2. If clearing: move up by frame height, clear lines
        3. Print new frame
        4. Store frame height for next clear
        """
        if clear_previous and self._frame_height > 0:
            # Move cursor up and clear previous frame
            sys.stdout.write(f"\033[{self._frame_height}A")  # Move up
            sys.stdout.write("\033[J")  # Clear from cursor down
        
        # Render new frame
        sys.stdout.write(frame)
        sys.stdout.flush()
        
        # Track frame height for next render
        self._frame_height = frame.count('\n') + 1
    
    def animate(
        self,
        frames: list[str],
        duration: float = 0.0,
        on_complete: Callable[[], None] | None = None
    ) -> None:
        """
        Run animation loop.
        
        Args:
            frames: List of ANSI frame strings
            duration: Seconds to run (0 = until stopped)
            on_complete: Callback when animation ends
        """
        self.timing.start()
        start = time.monotonic()
        
        try:
            while self.timing._running:
                frame_idx = self.timing.get_current_frame(len(frames))
                
                if frame_idx != self._last_frame:
                    self.render_frame(frames[frame_idx])
                    self._last_frame = frame_idx
                
                if duration > 0 and (time.monotonic() - start) >= duration:
                    break
                
                time.sleep(self.timing.frame_duration / 2)
        
        except KeyboardInterrupt:
            pass
        finally:
            self.timing.stop()
            if on_complete:
                on_complete()
```

### 3.6 ANSI Frame File Format

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ ANSI FRAME FILE SPECIFICATION                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ FILE EXTENSION: .ansi                                                       │
│ ENCODING: UTF-8                                                             │
│                                                                             │
│ STRUCTURE:                                                                  │
│ ─────────────────────────────────────────────────────────────               │
│ # MUDHOUND ANSI FRAME                                                       │
│ # scheme: rainbow                                                           │
│ # frame: 1                                                                  │
│ # width: 76                                                                 │
│ # height: 3                                                                 │
│ ---                                                                         │
│ [ANSI escape sequences + ASCII art content]                                 │
│                                                                             │
│ EXAMPLE:                                                                    │
│ ─────────────────────────────────────────────────────────────               │
│ # MUDHOUND ANSI FRAME                                                       │
│ # scheme: rainbow                                                           │
│ # frame: 1                                                                  │
│ # width: 76                                                                 │
│ # height: 3                                                                 │
│ ---                                                                         │
│ \033[38;5;196m██▄  ▄██\033[38;5;208m ██  ██\033[38;5;226m ████▄ ...         │
│ \033[38;5;196m██ ▀▀ ██\033[38;5;208m ██  ██\033[38;5;226m ██  ██ ...        │
│ \033[38;5;196m██    ██\033[38;5;208m ▀████▀\033[38;5;226m ████▀ ...         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 3.7 Rainbow Color Cycling Definition

```python
RAINBOW_COLORS_256 = [
    196,  # Red
    208,  # Orange
    226,  # Yellow
    46,   # Green
    51,   # Cyan
    21,   # Blue
    129,  # Purple
    201,  # Magenta
]

DARK_RAINBOW_COLORS_256 = [
    88,   # Dark Red
    130,  # Dark Orange
    136,  # Dark Yellow
    22,   # Dark Green
    23,   # Dark Cyan
    18,   # Dark Blue
    54,   # Dark Purple
    90,   # Dark Magenta
]

LIGHT_RAINBOW_COLORS_256 = [
    210,  # Light Red
    216,  # Light Orange
    228,  # Light Yellow
    120,  # Light Green
    123,  # Light Cyan
    111,  # Light Blue
    183,  # Light Purple
    219,  # Light Magenta
]

def generate_rainbow_frame(
    base_art: str,
    color_offset: int,
    scheme: ColorScheme
) -> str:
    """
    Generate a single rainbow frame by applying color offset to base ASCII art.
    
    ALGORITHM:
    1. Parse base ASCII art into character segments
    2. For each segment, calculate color index: (segment_index + offset) % len(colors)
    3. Wrap segment with ANSI color escape sequence
    4. Join segments into complete frame
    """
    colors = {
        ColorScheme.RAINBOW: RAINBOW_COLORS_256,
        ColorScheme.DARK_RAINBOW: DARK_RAINBOW_COLORS_256,
        ColorScheme.LIGHT_RAINBOW: LIGHT_RAINBOW_COLORS_256,
    }.get(scheme, RAINBOW_COLORS_256)
    
    # Implementation...
```

---

## 4. UI FRAMEWORK SPECIFICATION

### 4.1 Frame System

The frame system provides consistent ASCII borders that adapt to terminal width.

#### 4.1.1 Border Character Sets

```python
BORDER_SETS = {
    "double": {
        "tl": "╔", "tr": "╗", "bl": "╚", "br": "╝",
        "h": "═", "v": "║",
        "lj": "╠", "rj": "╣", "tj": "╦", "bj": "╩", "x": "╬"
    },
    "single": {
        "tl": "┌", "tr": "┐", "bl": "└", "br": "┘",
        "h": "─", "v": "│",
        "lj": "├", "rj": "┤", "tj": "┬", "bj": "┴", "x": "┼"
    },
    "bold": {
        "tl": "┏", "tr": "┓", "bl": "┗", "br": "┛",
        "h": "━", "v": "┃",
        "lj": "┣", "rj": "┫", "tj": "┳", "bj": "┻", "x": "╋"
    },
    "rounded": {
        "tl": "╭", "tr": "╮", "bl": "╰", "br": "╯",
        "h": "─", "v": "│",
        "lj": "├", "rj": "┤", "tj": "┬", "bj": "┴", "x": "┼"
    },
    "ascii": {
        "tl": "+", "tr": "+", "bl": "+", "br": "+",
        "h": "-", "v": "|",
        "lj": "+", "rj": "+", "tj": "+", "bj": "+", "x": "+"
    }
}
```

#### 4.1.2 Frame Rendering Protocol

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ FRAME ANATOMY                                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ╔═══════════════════════════════════════════════════╗  <- top_border      │
│   ║ TITLE                                       [TAG] ║  <- header_row      │
│   ╠═══════════════════════════════════════════════════╣  <- divider         │
│   ║                                                   ║                     │
│   ║  Content area with padding                        ║  <- content_rows    │
│   ║                                                   ║                     │
│   ╠═══════════════════════════════════════════════════╣  <- divider         │
│   ║ STATUS: Ready                           [1/10]    ║  <- footer_row      │
│   ╚═══════════════════════════════════════════════════╝  <- bottom_border   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 4.1.3 Dynamic Resize Handling

```python
class LayoutManager:
    """
    Manages terminal dimensions and triggers re-renders on resize.
    
    RESIZE STRATEGY:
    1. Poll terminal size on each render call
    2. Compare against cached dimensions
    3. If changed: recalculate all frame widths, re-wrap content
    4. Emit resize event to registered components
    5. Pause animations during resize, resume after
    
    MINIMUM DIMENSIONS:
    - Width:  60 columns (graceful degradation below)
    - Height: 10 rows (scroll mode activated below)
    """
    
    MIN_WIDTH = 60
    MIN_HEIGHT = 10
    PADDING_H = 2  # Left + right padding inside frames
    PADDING_V = 1  # Top + bottom padding inside frames
    
    def __init__(self):
        self._cached_size: tuple[int, int] = (0, 0)
        self._resize_callbacks: list[Callable] = []
        self._animation_engine: AnimationEngine | None = None
    
    def get_content_width(self) -> int:
        """Returns usable width inside frame borders."""
        term_width = shutil.get_terminal_size().columns
        return max(term_width - 4, self.MIN_WIDTH - 4)
    
    def on_resize(self) -> None:
        """Handle terminal resize event."""
        new_size = shutil.get_terminal_size()
        if (new_size.columns, new_size.lines) != self._cached_size:
            # Pause animations during resize
            if self._animation_engine:
                self._animation_engine.pause()
            
            self._cached_size = (new_size.columns, new_size.lines)
            
            for callback in self._resize_callbacks:
                callback(new_size.columns, new_size.lines)
            
            # Resume animations
            if self._animation_engine:
                self._animation_engine.resume()
```

### 4.2 Glyph Registry (Emoji-Free)

```python
GLYPHS = {
    # Status Indicators
    "success":    "[+]",
    "error":      "[!]",
    "warning":    "[~]",
    "info":       "[*]",
    "debug":      "[.]",
    "pending":    "[?]",
    
    # Progress
    "spinner":    ["|", "/", "-", "\\"],
    "progress":   ["░", "▒", "▓", "█"],
    "bullet":     ">>",
    "arrow":      "->",
    "pointer":    ">",
    
    # Selection
    "selected":   "[x]",
    "unselected": "[ ]",
    "radio_on":   "(*)",
    "radio_off":  "( )",
    "cursor":     ">>>",
    
    # Decorative
    "divider":    "---",
    "ellipsis":   "...",
    "check":      "[OK]",
    "cross":      "[XX]",
    "dot":        ".",
    
    # Data Flow
    "input":      "<<<",
    "output":     ">>>",
    "pipe":       "|",
    "chain":      ">>>"
}
```

#### 4.2.1 Frame Rendering Protocol

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ FRAME ANATOMY                                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ╔═══════════════════════════════════════════════════╗  <- top_border      │
│   ║ TITLE                                       [TAG] ║  <- header_row      │
│   ╠═══════════════════════════════════════════════════╣  <- divider         │
│   ║                                                   ║                     │
│   ║  Content area with padding                        ║  <- content_rows    │
│   ║                                                   ║                     │
│   ╠═══════════════════════════════════════════════════╣  <- divider         │
│   ║ STATUS: Ready                           [1/10]    ║  <- footer_row      │
│   ╚═══════════════════════════════════════════════════╝  <- bottom_border   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Theme Engine

#### 4.3.1 Color Palette Structure

```toml
# themes/default.toml

[meta]
name = "MudHound Default"
version = "1.0"

[palette]
# Primary colors (ANSI 256 or hex)
primary = "cyan"
secondary = "white"
accent = "yellow"

# Semantic colors
success = "green"
error = "red"
warning = "yellow"
info = "blue"
muted = "bright_black"

# Frame colors
border = "cyan"
border_accent = "bright_cyan"
header_bg = "default"
header_fg = "bright_white"

# Content colors
text = "white"
text_dim = "bright_black"
highlight = "bright_yellow"
url = "bright_blue"

# Animation colors (overrides default scheme)
[palette.animation]
use_scheme = true              # false = use palette colors instead
scheme = "rainbow"             # Override animation scheme
```

#### 4.3.2 Theme Application Protocol

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ THEME APPLICATION HIERARCHY                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   1. Component requests style by semantic name: "success"                   │
│   2. Theme resolves semantic name to palette color                          │
│   3. Palette color maps to terminal escape code                             │
│   4. Renderer wraps text with escape sequences                              │
│                                                                             │
│   FALLBACK CHAIN:                                                           │
│   Component Style -> Theme Override -> Default Theme -> Raw Text            │
│                                                                             │
│   ANIMATION OVERRIDE:                                                       │
│   If animation.use_scheme = false:                                          │
│     Animation colors derived from palette.primary/secondary/accent          │
│   Else:                                                                     │
│     Animation uses specified color scheme                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. COMPONENT SPECIFICATIONS

### 5.1 Banner Component (Animated)

```text
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║        ██▄  ▄██ ██  ██ ████▄  ██  ██ ▄████▄ ██  ██ ███  ██ ████▄         ║
║        ██ ▀▀ ██ ██  ██ ██  ██ ██████ ██  ██ ██  ██ ██ ▀▄██ ██  ██        ║
║        ██    ██ ▀████▀ ████▀  ██  ██ ▀████▀ ▀████▀ ██   ██ ████▀         ║
║                                                                          ║
║                 [ Fetch URLs. Filter Noise. Hunt Data. ]                 ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝

VARIANTS:
- animated:  Rainbow color cycling (default)
- static:    Single color scheme
- minimal:   Single-line version name only
- none:      No banner (headless mode)

ANIMATION BEHAVIOR:
- Colors cycle horizontally across characters
- Frame rate: 10 FPS default
- Scheme: Configurable (rainbow/dark-rainbow/light-rainbow/white)
- Respects terminal width, scales down if needed
```

### 5.2 Logo Component (Animated)

```text
         ▄▄        
██▄  ▄██ ██ ██  ██ 
██ ▀▀ ██ ██ ██████ 
██    ██ ██ ██  ██ 
         ▀▀        

USAGE:
- Inline display during operations
- Header/footer decoration
- Progress indicator accent

POSITIONS:
- inline:   Within content flow
- header:   Fixed at top
- footer:   Fixed at bottom
- floating: Absolute positioning
```

### 5.3 Footer and Goodbye Component

```text
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║     ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄     ║
║     ██  MUDHOUND v1.0.0  ████████████████████████████████████████████████     ║
║     ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀     ║
║                                                       Closing Application     ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║ > sys::Goodbye!                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

VARIANTS:
- full:    Complete ASCII art with `Closing Application` Confirmation prompt and `sys::Goodbye!`
- compact: fits as a signoff signature
- minimal: No Large ASCII Logo Splash
```

### 5.3 Menu Component

```text
╔══════════════════════════════════════════════════════════════════════════════╗
║  MAIN MENU                                                          [ESC]    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║    >>> [ 1 ] New Search                                                      ║
║        [ 2 ] Search History                                                  ║
║        [ 3 ] Export Results                                                  ║
║        [ 4 ] Configuration                                                   ║
║        ─────────────────────────────────────                                 ║
║        [ Q ] Quit                                                            ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  [*] Use arrow keys or number to select                          [1/5]       ║
╚══════════════════════════════════════════════════════════════════════════════╝

BEHAVIOR:
- Arrow keys navigate cursor (>>>)
- Number keys direct-select
- Enter confirms selection
- ESC returns to parent / exits
- Mouse support: optional, off by default
```

### 5.4 Prompt Component

```text
╔══════════════════════════════════════════════════════════════════════════════╗
║  SEARCH QUERY                                                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║    Enter keywords to search:                                                 ║
║                                                                              ║
║    >>> python web scraping libraries_                                        ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  [*] Press ENTER to search | CTRL+C to cancel                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

VARIANTS:
- text:     Free-form text input
- number:   Numeric input with validation
- choice:   Select from predefined options
- path:     File/directory path with completion
- confirm:  Y/N binary choice
```

### 5.5 Table Component

```text
╔═════════════════════════════════════════════════════════════════════════════╗
║  SEARCH RESULTS                                              [47 URLs]      ║
╠═════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║    #   │ URL                                             │ Source           ║
║   ─────┼─────────────────────────────────────────────────┼──────────────────║
║    001 │ https://docs.python.org/3/library/              │ DuckDuckGo       ║
║    002 │ https://realpython.com/python-web-scraping/     │ DuckDuckGo       ║
║    003 │ https://scrapy.org/                             │ DuckDuckGo       ║
║    004 │ https://www.crummy.com/software/BeautifulSo...  │ DuckDuckGo       ║
║    005 │ https://selenium-python.readthedocs.io/         │ DuckDuckGo       ║
║        │                                                 │                  ║
║    ... │ (42 more results)                               │                  ║
║                                                                             ║
╠═════════════════════════════════════════════════════════════════════════════╣
║  [*] Scroll: j/k | Export: e | Filter: / | Quit: q              [1-5/47]    ║
╚═════════════════════════════════════════════════════════════════════════════╝

FEATURES:
- Column auto-sizing based on content
- URL truncation with ellipsis (configurable max)
- Keyboard navigation (j/k, PgUp/PgDn)
- Inline filtering with /pattern
- Selection mode for batch operations
```

### 5.6 Progress Component

```text
╔══════════════════════════════════════════════════════════════════════════════╗
║  SEARCHING                                                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║    Query: "python web scraping"                                              ║
║    Engine: DuckDuckGo                                                        ║
║                                                                              ║
║    [████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░]  47%                ║
║                                                                              ║
║    [*] Fetching page 3 of 5...                                               ║
║    [+] 47 URLs collected                                                     ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  [*] Press CTRL+C to cancel                                      [00:03]     ║
╚══════════════════════════════════════════════════════════════════════════════╝

VARIANTS:
- bar:          Standard progress bar
- spinner:      Indeterminate spinner animation
- counter:      Numeric counter (X/Y)
- transfer:     Bytes transferred display
- rainbow:      Progress bar with rainbow coloring
```

### 5.7 Status/Log Component

```text
╔══════════════════════════════════════════════════════════════════════════════╗
║  ACTIVITY LOG                                                   [VERBOSE]    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║    12:34:01  [+] Search initiated: "python libraries"                        ║
║    12:34:02  [*] Connecting to DuckDuckGo API...                             ║
║    12:34:03  [+] Page 1: 10 results                                          ║
║    12:34:04  [+] Page 2: 10 results                                          ║
║    12:34:05  [~] Rate limit detected, backing off 2s...                      ║
║    12:34:07  [+] Page 3: 10 results                                          ║
║    12:34:08  [!] Connection timeout on page 4, retrying...                   ║
║    12:34:10  [+] Page 4: 10 results                                          ║
║    12:34:11  [+] Search complete: 40 URLs collected                          ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  [+] = success  [*] = info  [~] = warn  [!] = error            [9 events]    ║
╚══════════════════════════════════════════════════════════════════════════════╝

LOG LEVELS:
- TRACE:   Granular debug info (hidden by default)
- DEBUG:   Developer diagnostics
- INFO:    Standard operation messages
- WARN:    Non-fatal issues
- ERROR:   Operation failures
- FATAL:   Unrecoverable errors
```

### 5.8 Confirmation Component

```text
╔══════════════════════════════════════════════════════════════════════════════╗
║  CONFIRM ACTION                                                     [!]      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║    [~] You are about to clear all search history.                            ║
║                                                                              ║
║        This action cannot be undone.                                         ║
║        47 searches will be permanently deleted.                              ║
║                                                                              ║
║    ─────────────────────────────────────────────────────────────────         ║
║                                                                              ║
║                     [ YES ]          [ NO ]                                  ║
║                                      ^^^^^                                   ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  [*] Y/N or arrow keys to select                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

VARIANTS:
- yesno:      Binary Y/N (default NO)
- yesno_yes:  Binary Y/N (default YES)  
- destructive: Requires typing confirmation word
- timed:      Auto-cancels after timeout
```

### 5.9 Validation Display

```text
╔══════════════════════════════════════════════════════════════════════════════╗
║  INPUT VALIDATION                                                   [!]      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║    Enter maximum results (1-500):                                            ║
║                                                                              ║
║    >>> 9999_                                                                 ║
║                                                                              ║
║    [!] ERROR: Value must be between 1 and 500                                ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  [*] Enter valid number to continue                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

VALIDATION TYPES:
- range:      Numeric range enforcement
- pattern:    Regex pattern matching
- length:     String length constraints
- enum:       Allowed value set
- custom:     User-defined validator function
```

---

## 6. CLI COMMAND SPECIFICATION

### 6.1 Command Tree

```text
mh
├── search <query>          # Execute keyword search
│   ├── --max, -m           # Maximum results (default: 50)
│   ├── --engine, -e        # Search engine adapter (default: duckduckgo)
│   ├── --region, -r        # Region code (default: wt-wt)
│   ├── --safesearch, -s    # Safe search level (off|moderate|strict)
│   ├── --time, -t          # Time filter (d|w|m|y)
│   ├── --output, -o        # Output file path
│   ├── --format, -f        # Output format (json|csv|txt|urls)
│   ├── --quiet, -q         # Suppress UI, output only
│   └── --interactive, -i   # Interactive mode with live filtering
│
├── config                  # Configuration management
│   ├── list                # Show all config values
│   ├── get <key>           # Get specific config value
│   ├── set <key> <value>   # Set config value
│   ├── reset               # Reset to defaults
│   └── edit                # Open config in $EDITOR
│
├── export                  # Export stored results
│   ├── --format, -f        # Export format
│   ├── --output, -o        # Output path
│   ├── --search-id         # Specific search ID
│   └── --all               # Export all stored searches
│
├── history                 # Search history management
│   ├── list                # Show recent searches
│   ├── show <id>           # Show specific search results
│   ├── replay <id>         # Re-run a previous search
│   ├── delete <id>         # Delete specific search
│   └── clear               # Clear all history
│
├── interactive             # Launch interactive TUI mode
│
└── version                 # Show version information
```

### 6.2 Command Examples

```bash
# Basic search
mh search "python web scraping"

# Search with options
mh search "machine learning" --max 100 --format json --output results.json

# Quiet mode for scripting
mh search "api endpoints" -q -f urls > urls.txt

# Interactive mode
mh search "data science" --interactive

# Pipe-friendly
echo "search term" | mh search --stdin

# Configuration
mh config set default.max_results 100
mh config set theme hacker
mh config set animation.scheme dark-rainbow
mh config list

# History
mh history list --limit 10
mh history replay 42
mh history clear --confirm
```

### 6.3 Global Options

```text
--verbose, -v       Increase output verbosity (stackable: -vvv)
--quiet, -q         Suppress all non-essential output
--no-color          Disable ANSI color codes
--no-animation      Disable all animations
--theme, -T         Override theme for this session
--config, -c        Use alternate config file
--help, -h          Show help for command
```

---

## 7. LOGGING SYSTEM SPECIFICATION

### 7.1 Log Handler Architecture

```python
class StyledLogHandler(logging.Handler):
    """
    Custom log handler that routes messages through the UI renderer.
    
    FEATURES:
    - Timestamps with configurable format
    - Level-based glyph prefixes
    - Color coding per level
    - Frame-aware output (respects current UI context)
    - File output mirroring (optional)
    - Animation-safe (pauses animations during log output)
    """
    
    LEVEL_STYLES = {
        "TRACE":   {"glyph": "[.]", "color": "muted"},
        "DEBUG":   {"glyph": "[.]", "color": "muted"},
        "INFO":    {"glyph": "[*]", "color": "info"},
        "SUCCESS": {"glyph": "[+]", "color": "success"},
        "WARNING": {"glyph": "[~]", "color": "warning"},
        "ERROR":   {"glyph": "[!]", "color": "error"},
        "FATAL":   {"glyph": "[X]", "color": "error"},
    }
```

### 7.2 Log Output Formats

```text
INLINE (default for operations):
[+] 12:34:56 | Search complete: 47 results

BOXED (for summaries):
┌─────────────────────────────────────────────────────────────────────┐
│ [+] SEARCH COMPLETE                                                 │
├─────────────────────────────────────────────────────────────────────┤
│     Query:    "python web scraping"                                 │
│     Results:  47 URLs                                               │
│     Time:     3.2 seconds                                           │
│     Engine:   DuckDuckGo                                            │
└─────────────────────────────────────────────────────────────────────┘

STREAM (for live operations):
12:34:56.123 [*] Initiating search...
12:34:56.456 [*] Connecting to DuckDuckGo...
12:34:57.001 [+] Page 1: 10 results
12:34:57.523 [+] Page 2: 10 results
...
```

### 7.3 Log File Format

```text
# ~/.mudhound/logs/mudhound.log

2025-12-03T12:34:56.123Z | INFO    | engine.search | Search initiated: query="python"
2025-12-03T12:34:56.456Z | DEBUG   | adapter.ddg   | Request: GET https://duckduckgo.com/...
2025-12-03T12:34:57.001Z | INFO    | engine.search | Page 1 complete: 10 results
2025-12-03T12:34:57.523Z | WARNING | adapter.ddg   | Rate limit approaching, adding delay
2025-12-03T12:35:00.001  | ERROR   | adapter.ddg   | Request failed: ConnectionTimeout
2025-12-03T12:35:00.002Z | INFO    | adapter.ddg   | Retry 1/3 in 2 seconds
```

---

## 8. ADAPTER INTERFACE SPECIFICATION

### 8.1 Base Adapter Protocol

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterator, Optional

@dataclass
class SearchResult:
    """Individual search result."""
    url: str
    title: str
    snippet: str
    source: str
    rank: int
    metadata: dict = field(default_factory=dict)

@dataclass  
class SearchOptions:
    """Search configuration options."""
    max_results: int = 50
    region: str = "wt-wt"
    safesearch: str = "moderate"
    time_limit: Optional[str] = None  # d, w, m, y

class SearchAdapter(ABC):
    """
    Abstract base class for search engine adapters.
    
    All adapters must implement this interface to be registered
    with the adapter registry.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique adapter identifier."""
        pass
    
    @property
    @abstractmethod
    def display_name(self) -> str:
        """Human-readable name."""
        pass
    
    @abstractmethod
    def search(
        self, 
        query: str, 
        options: SearchOptions
    ) -> Iterator[SearchResult]:
        """
        Execute search and yield results.
        
        Must be a generator for streaming support.
        """
        pass
    
    @abstractmethod
    def validate_options(self, options: SearchOptions) -> list[str]:
        """
        Validate options for this adapter.
        
        Returns list of validation error messages (empty = valid).
        """
        pass
    
    def on_rate_limit(self) -> float:
        """
        Called when rate limit detected.
        
        Returns: seconds to wait before retry
        """
        return 2.0
```

### 8.2 Adapter Registry

```python
class AdapterRegistry:
    """
    Discovers and manages search adapters.
    
    DISCOVERY:
    1. Built-in adapters (mudhound.adapters.*)
    2. Plugin adapters (mudhound_adapter_* packages)
    3. User adapters (~/.mudhound/adapters/*.py)
    """
    
    _adapters: dict[str, Type[SearchAdapter]] = {}
    
    @classmethod
    def register(cls, adapter_cls: Type[SearchAdapter]) -> None:
        """Register an adapter class."""
        instance = adapter_cls()
        cls._adapters[instance.name] = adapter_cls
    
    @classmethod
    def get(cls, name: str) -> SearchAdapter:
        """Get adapter instance by name."""
        if name not in cls._adapters:
            raise AdapterNotFoundError(name)
        return cls._adapters[name]()
    
    @classmethod
    def list_available(cls) -> list[str]:
        """List all registered adapter names."""
        return list(cls._adapters.keys())
```

---

## 9. CONFIGURATION SPECIFICATION

### 9.1 Config File Location

```text
Priority (first found wins):
1. --config <path>                       # CLI override
2. $MUDHOUND_CONFIG                      # Environment variable
3. ./mudhound.toml                       # Current directory
4. ~/.config/mudhound/config.toml        # XDG standard
5. ~/.mudhound/config.toml               # Legacy location
6. (internal defaults)                   # Fallback
```

### 9.2 Config Schema

```toml
# mudhound.toml

[general]
default_engine = "duckduckgo"
default_max_results = 50
default_format = "urls"
history_enabled = true
history_max_entries = 100

[ui]
theme = "default"
banner = "animated"          # animated | static | minimal | none
color_enabled = true
unicode_enabled = true       # false = ASCII fallback
confirm_destructive = true

[animation]
enabled = true
default_scheme = "rainbow"   # rainbow | dark-rainbow | light-rainbow | white | theme
frame_rate = 10              # FPS
transition_duration = 0.15   # Seconds between color shifts
idle_animation = false       # Animate during idle states
on_completion = "flash"      # none | flash | pulse | fade

[animation.banner]
style = "animated"
scheme = "rainbow"
loop = true
duration = 0.0               # 0 = infinite

[animation.logo]
style = "animated"
scheme = "rainbow"
position = "inline"

[search]
default_region = "wt-wt"
default_safesearch = "moderate"
timeout_seconds = 30
retry_count = 3
retry_delay = 2.0

[export]
default_path = "~/Downloads"
include_metadata = false
url_only_mode = true

[logging]
level = "INFO"
file_enabled = true
file_path = "~/.mudhound/logs/mudhound.log"
file_max_size = "10MB"
file_backup_count = 5

[adapters.duckduckgo]
backend = "auto"             # auto | html | lite
proxy = ""
```

---

## 10. DATA MODELS

### 10.1 Core Models

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum

class SearchStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class SearchQuery:
    """Represents a search request."""
    id: str
    query: str
    engine: str
    options: SearchOptions
    created_at: datetime
    status: SearchStatus = SearchStatus.PENDING

@dataclass
class SearchSession:
    """Complete search session with results."""
    query: SearchQuery
    results: list[SearchResult] = field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    
    @property
    def duration(self) -> Optional[float]:
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None
    
    @property
    def result_count(self) -> int:
        return len(self.results)
```

### 10.2 Storage Schema

```text
~/.mudhound/
├── config.toml              # User configuration
├── history.db               # SQLite: search history
├── cache/                   # Temporary result cache
│   └── <session_id>.json
├── exports/                 # Default export location
└── logs/
    ├── mudhound.log
    └── mudhound.log.1       # Rotated logs
```

---

## 11. ERROR HANDLING SPECIFICATION

### 11.1 Exception Hierarchy

```python
class MudHoundError(Exception):
    """Base exception for all MudHound errors."""
    pass

class ConfigError(MudHoundError):
    """Configuration-related errors."""
    pass

class AdapterError(MudHoundError):
    """Search adapter errors."""
    pass

class AdapterNotFoundError(AdapterError):
    """Requested adapter not available."""
    pass

class RateLimitError(AdapterError):
    """Rate limit exceeded."""
    retry_after: float

class NetworkError(AdapterError):
    """Network connectivity issues."""
    pass

class ValidationError(MudHoundError):
    """Input validation failures."""
    field: str
    message: str

class ExportError(MudHoundError):
    """Export operation failures."""
    pass

class AnimationError(MudHoundError):
    """Animation system errors."""
    pass
```

### 11.2 Error Display Format

```text
╔══════════════════════════════════════════════════════════════════════════════╗
║  [!] ERROR                                                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║    NetworkError: Connection timeout                                          ║
║                                                                              ║
║    The search engine did not respond within 30 seconds.                      ║
║                                                                              ║
║    SUGGESTIONS:                                                              ║
║    >> Check your internet connection                                         ║
║    >> Try again in a few moments                                             ║
║    >> Use --timeout to increase wait time                                    ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  [*] Run with -v for detailed error information                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 12. ASSET MANAGEMENT SPECIFICATION

### 12.1 Asset Manager

```python
class AssetManager:
    """
    Manages loading, caching, and serving of static and animated assets.
    
    RESPONSIBILITIES:
    1. Load ANSI frame files from disk
    2. Cache loaded assets in memory
    3. Provide frame sequences for animations
    4. Handle missing asset fallbacks
    """
    
    ASSET_ROOT = Path(__file__).parent / "assets"
    CACHE: dict[str, list[str]] = {}
    
    @classmethod
    def get_banner_frames(cls, scheme: ColorScheme) -> list[str]:
        """Load banner frames for given color scheme."""
        cache_key = f"banner:{scheme.value}"
        
        if cache_key not in cls.CACHE:
            frames = cls._load_animated_asset("rainbow-banner", scheme)
            cls.CACHE[cache_key] = frames
        
        return cls.CACHE[cache_key]
    
    @classmethod
    def get_logo_frames(cls, scheme: ColorScheme) -> list[str]:
        """Load logo frames for given color scheme."""
        cache_key = f"logo:{scheme.value}"
        
        if cache_key not in cls.CACHE:
            frames = cls._load_animated_asset("rainbow-logo", scheme)
            cls.CACHE[cache_key] = frames
        
        return cls.CACHE[cache_key]
    
    @classmethod
    def _load_animated_asset(
        cls, 
        asset_name: str, 
        scheme: ColorScheme
    ) -> list[str]:
        """Load all frames for an animated asset."""
        asset_dir = cls.ASSET_ROOT / "animated" / asset_name
        frames = []
        
        # Load frame files in order
        frame_pattern = f"{scheme.value}-*.ansi"
        for frame_file in sorted(asset_dir.glob(frame_pattern)):
            frames.append(cls._parse_ansi_file(frame_file))
        
        if not frames:
            # Fallback to static asset
            return [cls._get_static_fallback(asset_name)]
        
        return frames
    
    @classmethod
    def _parse_ansi_file(cls, path: Path) -> str:
        """Parse ANSI frame file, stripping header metadata."""
        content = path.read_text(encoding="utf-8")
        
        # Skip header lines until ---
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.strip() == "---":
                return "\n".join(lines[i + 1:])
        
        return content
```

### 12.2 Asset Directory Structure

```text
mudhound/assets/
├── __init__.py
├── manager.py
├── animated/
│   ├── rainbow-banner/
│   │   ├── rainbow-frame-01.ansi
│   │   ├── rainbow-frame-02.ansi
│   │   ├── rainbow-frame-03.ansi
│   │   ├── rainbow-frame-04.ansi
│   │   ├── rainbow-frame-05.ansi
│   │   ├── rainbow-frame-06.ansi
│   │   ├── dark-rainbow-frame-01.ansi
│   │   ├── dark-rainbow-frame-02.ansi
│   │   ├── ...
│   │   ├── light-rainbow-frame-01.ansi
│   │   ├── ...
│   │   ├── white-frame-01.ansi
│   │   └── ...
│   └── rainbow-logo/
│       ├── rainbow-frame-01.ansi
│       ├── ...
│       ├── dark-rainbow-frame-01.ansi
│       ├── ...
│       ├── light-rainbow-frame-01.ansi
│       ├── ...
│       └── white-frame-01.ansi
└── static/
    ├── banner-large.ansi
    ├── banner-minimal.ansi
    └── logo-static.ansi
```

### 12.3 PNG to ANSI Conversion (Build Tool)

```python
"""
Build tool for converting PNG banner assets to ANSI frame files.

USAGE:
    python -m mudhound.tools.png_to_ansi assets/source/ assets/animated/

CONVERSION PROCESS:
1. Load PNG image
2. Sample colors at character grid positions
3. Map RGB to nearest ANSI 256 color
4. Generate escape sequences for each character block
5. Write .ansi frame file with metadata header
"""

def png_to_ansi(
    png_path: Path,
    output_path: Path,
    scheme: str,
    frame_number: int
) -> None:
    """Convert a single PNG to ANSI frame file."""
    from PIL import Image
    
    img = Image.open(png_path)
    width, height = img.size
    
    # Character block size (adjust based on terminal font aspect ratio)
    char_width = 2   # pixels per character width
    char_height = 4  # pixels per character height
    
    grid_w = width // char_width
    grid_h = height // char_height
    
    lines = []
    for y in range(grid_h):
        line = ""
        for x in range(grid_w):
            # Sample center pixel of block
            px = x * char_width + char_width // 2
            py = y * char_height + char_height // 2
            
            r, g, b, *_ = img.getpixel((px, py))
            ansi_color = rgb_to_ansi256(r, g, b)
            
            # Use block character with foreground color
            line += f"\033[38;5;{ansi_color}m█"
        
        line += "\033[0m"  # Reset at end of line
        lines.append(line)
    
    # Write with metadata header
    header = f"""# MUDHOUND ANSI FRAME
# scheme: {scheme}
# frame: {frame_number}
# width: {grid_w}
# height: {grid_h}
---
"""
    
    output_path.write_text(header + "\n".join(lines), encoding="utf-8")
```

---

## 13. EXTENSION POINTS

### 13.1 Plugin System (Future)

```text
PLUGIN DISCOVERY:
- Python packages: mudhound_plugin_*
- Entry points: mudhound.plugins
- Local plugins: ~/.mudhound/plugins/*.py

PLUGIN TYPES:
1. Adapters      - New search engines
2. Exporters     - New output formats  
3. Themes        - UI customization
4. Commands      - New CLI commands
5. Processors    - Result transformers
6. Animations    - Custom animation schemes

PLUGIN LIFECYCLE:
1. Discovery (on startup)
2. Validation (interface check)
3. Registration (add to registry)
4. Initialization (on first use)
5. Cleanup (on exit)
```

### 13.2 Hook System (Future)

```python
AVAILABLE_HOOKS = {
    "pre_search":      "Before search execution",
    "post_search":     "After search completion",
    "on_result":       "For each result received",
    "pre_export":      "Before export operation",
    "post_export":     "After export completion",
    "on_error":        "When error occurs",
    "on_startup":      "Application startup",
    "on_shutdown":     "Application shutdown",
    "on_animation":    "Animation frame rendered",
}
```

---

## 14. IMPLEMENTATION PHASES

### Phase 1: Foundation

- [ ] Project scaffolding
- [ ] UI framework (frames, layout, theme)
- [ ] Animation engine (timing, rendering)
- [ ] Asset manager and ANSI loader
- [ ] Core components (banner, prompt, status)
- [ ] Basic logging system
- [ ] Configuration management

### Phase 2: Core Functionality  

- [ ] Adapter interface
- [ ] DuckDuckGo adapter
- [ ] Search command
- [ ] Result display (table)
- [ ] Basic export (txt, urls)
- [ ] Animated banner integration

### Phase 3: Enhanced Features

- [ ] Interactive mode
- [ ] History management
- [ ] Progress/spinner components
- [ ] Menu component
- [ ] JSON/CSV export
- [ ] All color scheme variants

### Phase 4: Polish

- [ ] Multiple themes
- [ ] Validation refinement
- [ ] Error handling polish
- [ ] PNG to ANSI build tool
- [ ] Documentation
- [ ] Tests

### Phase 5: Extension (Future)

- [ ] Plugin system
- [ ] Additional adapters
- [ ] Hook system
- [ ] Custom exporters
- [ ] Custom animation schemes

---

## 15. DEPENDENCIES

```toml
# pyproject.toml

[project]
name = "mudhound"
version = "1.0.0"
requires-python = ">=3.10"

dependencies = [
    "typer>=0.12.0",
    "rich>=13.0.0",              # Terminal rendering utilities
    "duckduckgo-search>=8.0.0",  # Primary search adapter
    "httpx>=0.27.0",             # HTTP client
    "pydantic>=2.0.0",           # Data validation
    "tomli>=2.0.0",              # TOML parsing (Python <3.11)
    "tomli-w>=1.0.0",            # TOML writing
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.4.0",
    "mypy>=1.10.0",
    "pillow>=10.0.0",            # PNG to ANSI conversion tool
]

[project.scripts]
mh = "mudhound.cli.app:app"
```

---

## APPENDIX A: ASCII ART ASSETS

### A.1 Banner and Logo Variants

#### A.1.1 Animated Banner (Default)

```text
██▄  ▄██ ██  ██ ████▄  ██  ██ ▄████▄ ██  ██ ███  ██ ████▄  
██ ▀▀ ██ ██  ██ ██  ██ ██████ ██  ██ ██  ██ ██ ▀▄██ ██  ██ 
██    ██ ▀████▀ ████▀  ██  ██ ▀████▀ ▀████▀ ██   ██ ████▀  

COLOR SCHEMES:
- rainbow:       Full spectrum cycling (196->208->226->46->51->21->129->201)
- dark-rainbow:  Muted spectrum (88->130->136->22->23->18->54->90)
- light-rainbow: Bright/pastel (210->216->228->120->123->111->183->219)
- white:         Monochrome (255)

ANIMATION:
- Colors shift horizontally by 1 position per frame
- 6-8 frames per complete cycle
- 10 FPS default
```

#### A.1.2 Animated Logo (Compact)

```text
         ▄▄        
██▄  ▄██ ██ ██  ██ 
██ ▀▀ ██ ██ ██████ 
██    ██ ██ ██  ██ 
         ▀▀        

USAGE:
- Progress indicator decoration
- Inline status markers
- Header/footer accents
```

#### A.1.3 Large Stylized (Static)

```text
@@@@@@@@@@   @@@  @@@  @@@@@@@   @@@  @@@   @@@@@@   @@@  @@@  @@@  @@@  @@@@@@@   
@@@@@@@@@@@  @@@  @@@  @@@@@@@@  @@@  @@@  @@@@@@@@  @@@  @@@  @@@@ @@@  @@@@@@@@  
@@! @@! @@!  @@!  @@@  @@!  @@@  @@!  @@@  @@!  @@@  @@!  @@@  @@!@!@@@  @@!  @@@  
!@! !@! !@!  !@!  @!@  !@!  @!@  !@!  @!@  !@!  @!@  !@!  @!@  !@!!@!@!  !@!  @!@  
@!! !!@ @!@  @!@  !@!  @!@  !@!  @!@!@!@!  @!@  !@!  @!@  !@!  @!@ !!@!  @!@  !@!  
!@!   ! !@!  !@!  !!!  !@!  !!!  !!!@!!!!  !@!  !!!  !@!  !!!  !@!  !!!  !@!  !!!  
!!:     !!:  !!:  !!!  !!:  !!!  !!:  !!!  !!:  !!!  !!:  !!!  !!:  !!!  !!:  !!!  
:!:     :!:  :!:  !:!  :!:  !:!  :!:  !:!  :!:  !:!  :!:  !:!  :!:  !:!  :!:  !:!  
:::     ::   ::::: ::   :::: ::  ::   :::  ::::: ::  ::::: ::   ::   ::   :::: ::  
 :      :     : :  :   :: :  :    :   : :   : :  :    : :  :   ::    :   :: :  :   
```

#### A.1.4 Compact Stylized

```text
░█▄█░█░█░█▀▄░█░█░█▀█░█░█░█▀█░█▀▄
░█░█░█░█░█░█░█▀█░█░█░█░█░█░█░█░█
░▀░▀░▀▀▀░▀▀░░▀░▀░▀▀▀░▀▀▀░▀░▀░▀▀░
```

#### A.1.5 Minimal (Inline)

```text
[ MUDHOUND v1.0.0 ]
```

- can be applied to most ASCII logos, or banners on the bottom left most line.

> EXAMPLE:

```text
░█▄█░█░█░█▀▄░█░█░█▀█░█░█░█▀█░█▀▄
░█░█░█░█░█░█░█▀█░█░█░█░█░█░█░█░█
░▀░▀░▀▀▀░▀▀░░▀░▀░▀▀▀░▀▀▀░▀░▀░▀▀░
[ MUDHOUND v1.0.0 ]
```

### A.2 Decorative Elements

```text
Section Dividers:
════════════════════════════════════════════════════════════════════════════════
────────────────────────────────────────────────────────────────────────────────
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀

Corners:
╔═  ═╗     ┌─  ─┐     ╭─  ─╮
║    ║     │    │     │    │
╚═  ═╝     └─  ─┘     ╰─  ─╯

Arrows (spacing-safe):
>>> -> => >> 
<<< <- <= << 
```

---

## APPENDIX B: EXTERNAL ASSET REFERENCES

### B.1 Source PNG Assets (Development Only)

```text
Location: assets/source/ (not distributed)

rainbow-banner/
├── dark-rainbow-banner.png
├── light-rainbow-banner.png
├── rainbow-banner.png
└── white-banner.png

rainbow-logo/
├── dark-rainbow-logo.png
├── light-rainbow-logo.png
├── rainbow-logo.png
└── white-logo.png

BUILD PROCESS:
1. Source PNGs created in image editor
2. Build tool converts PNG -> ANSI frames
3. ANSI files committed to assets/animated/
4. Source PNGs excluded from distribution
```

---

*Document Version: 1.1.0*
*Last Updated: 2025-12-03*
*Author: MudHound Design Team*
