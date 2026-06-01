"""Text utility functions."""

import re
from typing import List


def clean_text(text: str) -> str:
    """Clean and normalize text.
    
    Args:
        text: Input text
        
    Returns:
        Cleaned text
    """
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove control characters
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    
    # Normalize quotes
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")
    
    # Normalize dashes
    text = text.replace('–', '-').replace('—', '-')
    
    return text.strip()


def truncate_text(text: str, max_length: int, suffix: str = '...') -> str:
    """Truncate text to maximum length.
    
    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    truncated = text[:max_length - len(suffix)]
    return truncated.rstrip() + suffix


def count_words(text: str) -> int:
    """Count words in text.
    
    Args:
        text: Input text
        
    Returns:
        Word count
    """
    return len(text.split())


def extract_sentences(text: str) -> List[str]:
    """Extract sentences from text.
    
    Args:
        text: Input text
        
    Returns:
        List of sentences
    """
    # Simple sentence splitting
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def extract_paragraphs(text: str) -> List[str]:
    """Extract paragraphs from text.
    
    Args:
        text: Input text
        
    Returns:
        List of paragraphs
    """
    paragraphs = text.split('\n\n')
    return [p.strip() for p in paragraphs if p.strip()]


def remove_html_tags(text: str) -> str:
    """Remove HTML tags from text.
    
    Args:
        text: HTML text
        
    Returns:
        Plain text
    """
    clean = re.sub(r'<[^>]+>', '', text)
    return clean_text(clean)


def remove_urls(text: str) -> str:
    """Remove URLs from text.
    
    Args:
        text: Input text
        
    Returns:
        Text without URLs
    """
    url_pattern = r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
    return re.sub(url_pattern, '', text)


def remove_emails(text: str) -> str:
    """Remove email addresses from text.
    
    Args:
        text: Input text
        
    Returns:
        Text without emails
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.sub(email_pattern, '', text)


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text.
    
    Args:
        text: Input text
        
    Returns:
        Normalized text
    """
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    
    # Replace multiple newlines with double newline
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug.
    
    Args:
        text: Input text
        
    Returns:
        Slug
    """
    # Convert to lowercase
    text = text.lower()
    
    # Replace non-alphanumeric with hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text)
    
    # Remove leading/trailing hyphens
    text = text.strip('-')
    
    return text


def highlight_keywords(text: str, keywords: List[str], tag: str = '**') -> str:
    """Highlight keywords in text.
    
    Args:
        text: Input text
        keywords: Keywords to highlight
        tag: Tag to wrap keywords
        
    Returns:
        Text with highlighted keywords
    """
    for keyword in keywords:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        text = pattern.sub(f'{tag}\\g<0>{tag}', text)
    return text


def estimate_reading_time(text: str, wpm: int = 200) -> int:
    """Estimate reading time in minutes.
    
    Args:
        text: Input text
        wpm: Words per minute
        
    Returns:
        Reading time in minutes
    """
    word_count = count_words(text)
    return max(1, round(word_count / wpm))
