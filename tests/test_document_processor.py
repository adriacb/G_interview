"""Tests for the document processor."""
import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from io import BytesIO

from docling.document_converter import DocumentConverter
from docling_core.types.doc import DoclingDocument
from adriacb_galtea.core.document_processor import DoclingProcessor
from docling_core.utils.file import resolve_source_to_stream


@pytest.fixture
def mock_path_stat():
    """Fixture to mock Path.stat()."""
    with patch("pathlib.Path.stat") as mock_stat:
        mock_stat.return_value = MagicMock(st_size=1234)
        yield mock_stat


@pytest.fixture
def mock_docling_document():
    """Fixture to mock a Docling document."""
    mock = MagicMock()
    mock.export_to_markdown.return_value = "Test content\n\nMore content"
    mock.pages = [MagicMock(), MagicMock()]
    return mock


@pytest.fixture
def mock_docling_result(mock_docling_document):
    """Fixture to mock a Docling conversion result."""
    mock = MagicMock()
    mock.document = mock_docling_document
    return mock


@pytest.fixture
def mock_docling_converter(mock_docling_result):
    """Fixture to mock the Docling converter."""
    with patch("docling.document_converter.DocumentConverter") as mock_class:
        mock_instance = MagicMock()
        mock_instance.convert.return_value = mock_docling_result
        mock_class.return_value = mock_instance
        mock_class.side_effect = lambda *args, **kwargs: mock_instance
        yield mock_instance


@pytest.fixture
def mock_resolve_source_to_stream():
    """Mock resolve_source_to_stream to return a BytesIO object."""
    with patch('docling_core.utils.file.resolve_source_to_stream') as mock_resolve:
        mock_resolve.return_value = BytesIO(b"test content")
        yield mock_resolve


@pytest.fixture
def document_processor(mock_docling_converter):
    """Fixture to create a document processor instance."""
    return DoclingProcessor(converter=mock_docling_converter)


def test_process_document(document_processor, mock_docling_converter, mock_docling_document, mock_path_stat, mock_resolve_source_to_stream):
    """Test processing a document."""
    # Create a temporary file path
    doc_path = "test.pdf"
    
    # Process the document
    result = document_processor.process_document(doc_path)
    
    # Check that Docling was called
    mock_docling_converter.convert.assert_called_once_with(doc_path)
    mock_docling_document.export_to_markdown.assert_called_once()
    
    # Check the result structure
    assert "content" in result
    assert "metadata" in result
    assert "chunks" in result
    
    # Check content
    assert result["content"] == "Test content\n\nMore content"
    
    # Check metadata
    assert "filename" in result["metadata"]
    assert "file_size" in result["metadata"]
    assert result["metadata"]["file_size"] == 1234  # Check mocked file size
    assert "file_type" in result["metadata"]
    assert "page_count" in result["metadata"]
    
    # Check chunks
    assert len(result["chunks"]) > 0
    assert all(isinstance(chunk, str) for chunk in result["chunks"])


def test_extract_text(document_processor, mock_docling_converter, mock_docling_document, mock_path_stat, mock_resolve_source_to_stream):
    """Test extracting text from a document."""
    doc_path = "test.pdf"
    
    text = document_processor.extract_text(doc_path)
    
    mock_docling_converter.convert.assert_called_once_with(doc_path)
    mock_docling_document.export_to_markdown.assert_called_once()
    
    assert text == "Test content\n\nMore content"


def test_get_metadata(document_processor, mock_docling_converter, mock_docling_document, mock_path_stat, mock_resolve_source_to_stream):
    """Test getting metadata from a document."""
    doc_path = "test.pdf"
    
    metadata = document_processor.get_metadata(doc_path)
    
    mock_docling_converter.convert.assert_called_once_with(doc_path)
    
    assert "filename" in metadata
    assert "file_size" in metadata
    assert metadata["file_size"] == 1234  # Check mocked file size
    assert "file_type" in metadata
    assert "page_count" in metadata
    assert metadata["page_count"] == 2


def test_chunk_splitting(document_processor):
    """Test splitting text into chunks."""
    text = "First paragraph\n\nSecond paragraph\n\nThird paragraph"
    
    chunks = document_processor._split_into_chunks(text, chunk_size=20)
    
    assert len(chunks) == 3  # Update expected number of chunks
    assert "First paragraph" in chunks[0]
    assert "Second paragraph" in chunks[1]  # Update chunk index
    assert "Third paragraph" in chunks[2]  # Update chunk index 