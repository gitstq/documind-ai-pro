"""
DocuMind AI - Intelligent Document Conversion and Knowledge Extraction

A powerful tool that converts documents to Markdown and uses AI to extract
insights, summarize content, and build knowledge graphs.
"""

__version__ = "1.0.0"
__author__ = "DocuMind AI Team"
__license__ = "MIT"

from documind_ai.core.converter import DocumentConverter
from documind_ai.core.analyzer import AIAnalyzer
from documind_ai.core.extractor import KnowledgeExtractor

__all__ = [
    "DocumentConverter",
    "AIAnalyzer", 
    "KnowledgeExtractor",
]
