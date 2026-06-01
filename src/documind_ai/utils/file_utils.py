"""File utility functions."""

import re
from pathlib import Path
from typing import Optional, Union


def get_file_extension(file_path: Union[str, Path]) -> str:
    """Get file extension.
    
    Args:
        file_path: Path to file
        
    Returns:
        File extension with dot
    """
    return Path(file_path).suffix.lower()


def sanitize_filename(filename: str, max_length: int = 100) -> str:
    """Sanitize filename for safe use.
    
    Args:
        filename: Original filename
        max_length: Maximum length
        
    Returns:
        Sanitized filename
    """
    # Remove or replace unsafe characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove control characters
    sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', sanitized)
    
    # Limit length
    if len(sanitized) > max_length:
        name, ext = Path(sanitized).stem, Path(sanitized).suffix
        sanitized = name[:max_length - len(ext)] + ext
    
    # Remove leading/trailing dots and spaces
    sanitized = sanitized.strip('. ')
    
    # Ensure not empty
    if not sanitized:
        sanitized = 'unnamed'
    
    return sanitized


def ensure_dir(path: Union[str, Path]) -> Path:
    """Ensure directory exists.
    
    Args:
        path: Directory path
        
    Returns:
        Path object
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_output_path(
    input_path: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    suffix: str = '.md',
) -> Path:
    """Get output file path.
    
    Args:
        input_path: Input file path
        output_dir: Output directory
        suffix: Output file suffix
        
    Returns:
        Output file path
    """
    input_path = Path(input_path)
    
    if output_dir:
        output_dir = ensure_dir(output_dir)
        output_name = sanitize_filename(input_path.stem) + suffix
        return output_dir / output_name
    else:
        return input_path.parent / (sanitize_filename(input_path.stem) + suffix)


def format_file_size(size_bytes: int) -> str:
    """Format file size to human readable.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def find_files(
    directory: Union[str, Path],
    patterns: list[str],
    recursive: bool = True,
) -> list[Path]:
    """Find files matching patterns.
    
    Args:
        directory: Search directory
        patterns: File patterns to match
        recursive: Search recursively
        
    Returns:
        List of matching file paths
    """
    directory = Path(directory)
    matches = []
    
    if recursive:
        for pattern in patterns:
            matches.extend(directory.rglob(pattern))
    else:
        for pattern in patterns:
            matches.extend(directory.glob(pattern))
    
    return sorted(set(matches))


def get_unique_filename(path: Union[str, Path]) -> Path:
    """Get unique filename by appending number if exists.
    
    Args:
        path: Desired file path
        
    Returns:
        Unique file path
    """
    path = Path(path)
    
    if not path.exists():
        return path
    
    counter = 1
    while True:
        new_name = f"{path.stem}_{counter}{path.suffix}"
        new_path = path.parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1
