"""Tests for document converter."""

import tempfile
from pathlib import Path

import pytest

from documind_ai.core.converter import DocumentConverter
from documind_ai.core.models import DocumentType, ProcessingConfig


class TestDocumentConverter:
    """Test document converter."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = ProcessingConfig()
        self.converter = DocumentConverter(self.config)

    def test_detect_document_type_pdf(self):
        """Test PDF detection."""
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            f.write(b'%PDF-1.4 fake pdf content')
            temp_path = Path(f.name)
        
        try:
            doc_type = self.converter.detect_document_type(temp_path)
            assert doc_type == DocumentType.PDF
        finally:
            temp_path.unlink()

    def test_detect_document_type_docx(self):
        """Test DOCX detection."""
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as f:
            f.write(b'PK\x03\x04 fake docx content')
            temp_path = Path(f.name)
        
        try:
            doc_type = self.converter.detect_document_type(temp_path)
            assert doc_type == DocumentType.DOCX
        finally:
            temp_path.unlink()

    def test_detect_document_type_unknown(self):
        """Test unknown file type detection."""
        with tempfile.NamedTemporaryFile(suffix='.xyz', delete=False) as f:
            f.write(b'unknown content')
            temp_path = Path(f.name)
        
        try:
            doc_type = self.converter.detect_document_type(temp_path)
            assert doc_type == DocumentType.UNKNOWN
        finally:
            temp_path.unlink()

    def test_convert_text_file(self):
        """Test text file conversion."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write("Hello, World!\n\nThis is a test document.")
            temp_path = Path(f.name)
        
        try:
            result = self.converter.convert(temp_path)
            assert result.success
            assert result.document_type == DocumentType.TXT
            assert "Hello, World!" in result.content
            assert result.metadata.word_count == 8
        finally:
            temp_path.unlink()

    def test_convert_markdown_file(self):
        """Test markdown file conversion."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("# Test Document\n\nThis is a test.")
            temp_path = Path(f.name)
        
        try:
            result = self.converter.convert(temp_path)
            assert result.success
            assert result.document_type == DocumentType.MD
            assert "# Test Document" in result.content
        finally:
            temp_path.unlink()

    def test_convert_nonexistent_file(self):
        """Test conversion of nonexistent file."""
        result = self.converter.convert("/nonexistent/file.pdf")
        assert not result.success
        assert "File not found" in result.errors[0]

    def test_clean_content(self):
        """Test content cleaning."""
        dirty_content = "Hello\n\n\n\n\nWorld"
        clean_content = self.converter._clean_content(dirty_content)
        assert "\n\n\n" not in clean_content
        assert "Hello" in clean_content
        assert "World" in clean_content


class TestFileUtils:
    """Test file utilities."""

    def test_get_file_extension(self):
        """Test file extension extraction."""
        from documind_ai.utils.file_utils import get_file_extension
        
        assert get_file_extension("test.pdf") == ".pdf"
        assert get_file_extension("test.PDF") == ".pdf"
        assert get_file_extension(Path("test.docx")) == ".docx"

    def test_sanitize_filename(self):
        """Test filename sanitization."""
        from documind_ai.utils.file_utils import sanitize_filename
        
        assert sanitize_filename("test<file>.pdf") == "test_file_.pdf"
        assert sanitize_filename("test:document.pdf") == "test_document.pdf"
        assert sanitize_filename("a" * 200 + ".pdf") != "a" * 200 + ".pdf"

    def test_ensure_dir(self):
        """Test directory creation."""
        from documind_ai.utils.file_utils import ensure_dir
        
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "nested" / "dir"
            result = ensure_dir(test_dir)
            assert result.exists()
            assert result.is_dir()

    def test_get_output_path(self):
        """Test output path generation."""
        from documind_ai.utils.file_utils import get_output_path
        
        input_path = Path("/input/test.pdf")
        output_path = get_output_path(input_path)
        assert output_path.name == "test.md"
        
        output_path = get_output_path(input_path, "/output")
        assert output_path == Path("/output/test.md")
