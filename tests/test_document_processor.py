# Append root to path so we can import multimodal_advanced
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from multimodal_advanced import DocumentProcessor


class TestDocumentProcessor(unittest.TestCase):
    def test_extract_text_from_pdf(self):
        # Mock PyPDF2
        mock_pypdf2 = MagicMock()
        mock_reader = MagicMock()

        # Setup pages
        mock_page1 = MagicMock()
        mock_page1.extract_text.return_value = "Page 1 Content"

        mock_page2 = MagicMock()
        mock_page2.extract_text.return_value = "Page 2 Content"

        # reader.pages must be iterable and len() capable. List works best.
        mock_reader.pages = [mock_page1, mock_page2]

        # Setup metadata
        mock_reader.metadata = {
            "/Title": "Test PDF",
            "/Author": "Tester",
            "/CreationDate": "Today",
        }

        mock_pypdf2.PdfReader.return_value = mock_reader

        # Since PyPDF2 is imported inside the method, we need to ensure it's available in sys.modules
        # when the method runs.
        with patch.dict(sys.modules, {"PyPDF2": mock_pypdf2}):
            # Mock open
            with patch(
                "builtins.open", unittest.mock.mock_open(read_data=b"fake pdf data")
            ):
                text, metadata = DocumentProcessor.extract_text_from_pdf("dummy.pdf")

        # Verify text construction
        expected_part1 = "\n--- Page 1 ---\n"
        expected_part2 = "Page 1 Content"
        expected_part3 = "\n--- Page 2 ---\n"
        expected_part4 = "Page 2 Content"

        self.assertIn(expected_part1, text)
        self.assertIn(expected_part2, text)
        self.assertIn(expected_part3, text)
        self.assertIn(expected_part4, text)

        # Strict equality check to ensure order and no missing chars
        self.assertEqual(
            text, expected_part1 + expected_part2 + expected_part3 + expected_part4
        )

        # Verify metadata
        self.assertEqual(metadata["pages"], 2)
        self.assertEqual(metadata["title"], "Test PDF")
        self.assertEqual(metadata["author"], "Tester")


if __name__ == "__main__":
    unittest.main()
