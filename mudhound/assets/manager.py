"""Asset management system for loading and caching ANSI frame files."""

import glob
from pathlib import Path
from typing import Dict, List, Optional

from mudhound.core.exceptions import AnimationError


# Global cache for loaded assets
CACHE: Dict[str, List[str]] = {}


class AssetManager:
    """Manages loading and caching of ANSI frame files for animations."""
    
    def __init__(self, assets_dir: Optional[Path] = None):
        """Initialize the AssetManager.
        
        Args:
            assets_dir: Path to the assets directory. If None, uses the default
                       location relative to this module.
        """
        if assets_dir is None:
            # Default to the assets directory in the package
            self.assets_dir = Path(__file__).parent
        else:
            self.assets_dir = Path(assets_dir)
        
        self.animated_dir = self.assets_dir / "animated"
        self.static_dir = self.assets_dir / "static"
    
    def _strip_metadata(self, content: str) -> str:
        """Strip metadata header from ANSI frame file.
        
        Metadata headers are separated from content by a line containing "---".
        All lines before and including the separator are removed.
        
        Args:
            content: Raw file content with potential metadata header
            
        Returns:
            Content with metadata header stripped
        """
        lines = content.split('\n')
        
        # Find the separator line
        separator_index = -1
        for i, line in enumerate(lines):
            if line.strip() == '---':
                separator_index = i
                break
        
        # If separator found, return content after it
        if separator_index >= 0:
            return '\n'.join(lines[separator_index + 1:])
        
        # No separator found, return original content
        return content
    
    def _load_animated_asset(self, asset_name: str, pattern: str) -> List[str]:
        """Load animated asset frames using glob pattern matching.
        
        Args:
            asset_name: Name of the asset for caching (e.g., "rainbow-banner")
            pattern: Glob pattern to match frame files (e.g., "rainbow-banner/*.txt")
            
        Returns:
            List of frame contents (strings)
            
        Raises:
            AnimationError: If no frames are found
        """
        # Check cache first
        cache_key = f"animated:{asset_name}"
        if cache_key in CACHE:
            return CACHE[cache_key]
        
        # Build full pattern path
        pattern_path = self.animated_dir / pattern
        
        # Find all matching files
        frame_files = sorted(glob.glob(str(pattern_path)))
        
        if not frame_files:
            raise AnimationError(f"No frames found for pattern: {pattern}")
        
        # Load and parse each frame
        frames = []
        for frame_file in frame_files:
            try:
                with open(frame_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Strip metadata header
                    frame_content = self._strip_metadata(content)
                    frames.append(frame_content)
            except Exception as e:
                raise AnimationError(f"Failed to load frame {frame_file}: {e}")
        
        # Cache the frames
        CACHE[cache_key] = frames
        
        return frames
    
    def _load_static_asset(self, asset_name: str) -> str:
        """Load a static asset file.
        
        Args:
            asset_name: Name of the static asset file (e.g., "banner.txt")
            
        Returns:
            Content of the static asset
            
        Raises:
            AnimationError: If the static asset cannot be loaded
        """
        # Check cache first
        cache_key = f"static:{asset_name}"
        if cache_key in CACHE:
            # Static assets are cached as single-item lists for consistency
            return CACHE[cache_key][0]
        
        asset_path = self.static_dir / asset_name
        
        try:
            with open(asset_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Strip metadata if present
                content = self._strip_metadata(content)
                # Cache as single-item list
                CACHE[cache_key] = [content]
                return content
        except Exception as e:
            raise AnimationError(f"Failed to load static asset {asset_name}: {e}")
    
    def get_banner_frames(self, scheme: str = "rainbow") -> List[str]:
        """Get banner frames for the specified color scheme.
        
        Args:
            scheme: Color scheme name (e.g., "rainbow", "dark-rainbow", "light-rainbow")
            
        Returns:
            List of banner frame contents
        """
        try:
            # Try to load animated frames
            pattern = f"{scheme}-banner/*.txt"
            return self._load_animated_asset(f"{scheme}-banner", pattern)
        except AnimationError:
            # Fall back to static banner
            try:
                static_banner = self._load_static_asset("banner.txt")
                # Return the cached list directly
                return CACHE["static:banner.txt"]
            except AnimationError:
                # If even static fallback fails, return a minimal banner
                # Cache the minimal banner too
                cache_key = "minimal:banner"
                if cache_key not in CACHE:
                    CACHE[cache_key] = [self._get_minimal_banner()]
                return CACHE[cache_key]
    
    def get_logo_frames(self, scheme: str = "rainbow") -> List[str]:
        """Get logo frames for the specified color scheme.
        
        Args:
            scheme: Color scheme name (e.g., "rainbow", "dark-rainbow", "light-rainbow")
            
        Returns:
            List of logo frame contents
        """
        try:
            # Try to load animated frames
            pattern = f"{scheme}-logo/*.txt"
            return self._load_animated_asset(f"{scheme}-logo", pattern)
        except AnimationError:
            # Fall back to static logo
            try:
                static_logo = self._load_static_asset("logo.txt")
                # Return the cached list directly
                return CACHE["static:logo.txt"]
            except AnimationError:
                # If even static fallback fails, return a minimal logo
                # Cache the minimal logo too
                cache_key = "minimal:logo"
                if cache_key not in CACHE:
                    CACHE[cache_key] = [self._get_minimal_logo()]
                return CACHE[cache_key]
    
    def _get_minimal_banner(self) -> str:
        """Get a minimal text-only banner as last resort fallback.
        
        Returns:
            Minimal banner string
        """
        return "MUDHOUND"
    
    def _get_minimal_logo(self) -> str:
        """Get a minimal text-only logo as last resort fallback.
        
        Returns:
            Minimal logo string
        """
        return "[MH]"
    
    def clear_cache(self):
        """Clear the asset cache."""
        CACHE.clear()
