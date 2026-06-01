"""Data models for DocuMind AI."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from enum import Enum
from pathlib import Path


class DocumentType(Enum):
    """Supported document types."""
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    XLSX = "xlsx"
    XLS = "xls"
    PPTX = "pptx"
    PPT = "ppt"
    HTML = "html"
    HTM = "htm"
    TXT = "txt"
    MD = "md"
    MARKDOWN = "markdown"
    CSV = "csv"
    JSON = "json"
    XML = "xml"
    EPUB = "epub"
    MOBI = "mobi"
    AZW = "azw"
    AZW3 = "azw3"
    RTF = "rtf"
    ODT = "odt"
    ODS = "ods"
    ODP = "odp"
    IMAGE = "image"
    UNKNOWN = "unknown"


@dataclass
class DocumentMetadata:
    """Metadata for a document."""
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    created: Optional[str] = None
    modified: Optional[str] = None
    page_count: Optional[int] = None
    word_count: Optional[int] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    encoding: Optional[str] = None


@dataclass
class ConversionResult:
    """Result of document conversion."""
    success: bool
    content: str
    document_type: DocumentType
    metadata: DocumentMetadata
    file_path: Path
    markdown_path: Optional[Path] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    processing_time: float = 0.0


@dataclass
class Entity:
    """Entity extracted from document."""
    name: str
    entity_type: str
    confidence: float
    occurrences: List[int] = field(default_factory=list)
    context: List[str] = field(default_factory=list)


@dataclass
class Relationship:
    """Relationship between entities."""
    source: str
    target: str
    relation_type: str
    confidence: float
    context: Optional[str] = None


@dataclass
class KnowledgeGraph:
    """Knowledge graph extracted from document."""
    entities: List[Entity] = field(default_factory=list)
    relationships: List[Relationship] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "entities": [
                {
                    "name": e.name,
                    "type": e.entity_type,
                    "confidence": e.confidence,
                    "occurrences": e.occurrences,
                }
                for e in self.entities
            ],
            "relationships": [
                {
                    "source": r.source,
                    "target": r.target,
                    "type": r.relation_type,
                    "confidence": r.confidence,
                }
                for r in self.relationships
            ],
        }


@dataclass
class AnalysisResult:
    """Result of AI analysis."""
    success: bool
    summary: Optional[str] = None
    key_points: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    sentiment: Optional[str] = None
    entities: List[Entity] = field(default_factory=list)
    knowledge_graph: Optional[KnowledgeGraph] = None
    questions: List[str] = field(default_factory=list)
    action_items: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    processing_time: float = 0.0
    token_usage: Dict[str, int] = field(default_factory=dict)


@dataclass
class ProcessingConfig:
    """Configuration for document processing."""
    # Conversion settings
    preserve_formatting: bool = True
    extract_images: bool = False
    ocr_enabled: bool = True
    
    # AI analysis settings
    ai_enabled: bool = True
    ai_provider: str = "openai"
    ai_model: str = "gpt-4o-mini"
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    
    # Analysis features
    generate_summary: bool = True
    extract_entities: bool = True
    build_knowledge_graph: bool = True
    generate_questions: bool = False
    extract_action_items: bool = False
    
    # Output settings
    output_dir: Optional[Path] = None
    save_markdown: bool = True
    save_analysis: bool = True
    save_knowledge_graph: bool = True
    
    # Processing limits
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    max_pages: Optional[int] = None
    timeout: int = 300
