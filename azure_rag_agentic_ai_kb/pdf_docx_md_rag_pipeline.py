"""
===============================================================================
FOCUSED RAG PIPELINE: .MD, .PDF, & .DOCX EXTRACTION WITH VISION CAPTIONING
===============================================================================
Demonstrates format-aware extraction for:
1. Markdown (.md) AST Header-based Chunking
2. Word (.docx) Paragraph & Table Extraction
3. PDF (.pdf) Layout Extraction + Embedded Figure GPT-4o Vision Captioning
===============================================================================
"""

import os
import re
import json
from typing import List, Dict, Any

class DocumentChunk:
    def __init__(self, file_name: str, file_type: str, content: str, header_path: str = "", has_image: bool = False):
        self.file_name = file_name
        self.file_type = file_type
        self.content = content
        self.header_path = header_path
        self.has_image = has_image

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_name": self.file_name,
            "file_type": self.file_type,
            "header_path": self.header_path,
            "content": self.content,
            "has_embedded_images": self.has_image
        }


class MarkdownProcessor:
    @staticmethod
    def process_markdown(file_name: str, md_content: str) -> List[DocumentChunk]:
        """Splits markdown content along headers (# H1, ## H2, ### H3)."""
        chunks = []
        sections = re.split(r'\n(?=#+ )', md_content)
        
        for idx, sec in enumerate(sections):
            if not sec.strip():
                continue
                
            lines = sec.strip().split('\n')
            header_match = re.match(r'^(#+)\s+(.*)', lines[0])
            header_path = header_match.group(2) if header_match else f"Section_{idx+1}"
            
            chunks.append(DocumentChunk(
                file_name=file_name,
                file_type="md",
                content=sec.strip(),
                header_path=header_path,
                has_image=False
            ))
            
        return chunks


class PDFVisionProcessor:
    @staticmethod
    def process_pdf_with_vision(file_name: str, pdf_text: str, mock_figure_caption: str) -> List[DocumentChunk]:
        """
        Simulates Azure AI Document Intelligence Layout parsing + GPT-4o Vision captioning
        for embedded images inside PDF pages.
        """
        chunks = []
        
        # Inject GPT-4o Vision caption into chunk content
        enriched_content = f"{pdf_text}\n\n[FIGURE_CAPTION: {mock_figure_caption}]"
        
        chunks.append(DocumentChunk(
            file_name=file_name,
            file_type="pdf",
            content=enriched_content,
            header_path="Page_1_Layout",
            has_image=True
        ))
        
        return chunks


class DocxProcessor:
    @staticmethod
    def process_docx(file_name: str, paragraphs: List[str], tables: List[str]) -> List[DocumentChunk]:
        """Combines Word document paragraphs and markdown tables into structured chunks."""
        chunks = []
        
        text_block = "\n\n".join(paragraphs)
        table_block = "\n\n".join(tables)
        full_content = f"{text_block}\n\n### Document Tables\n{table_block}"
        
        chunks.append(DocumentChunk(
            file_name=file_name,
            file_type="docx",
            content=full_content,
            header_path="Main_Document",
            has_image=False
        ))
        
        return chunks


def main():
    print("=========================================================================")
    print("🚀 Running Focused .MD, .PDF, and .DOCX RAG Extraction & Chunking Pipeline")
    print("=========================================================================\n")

    # 1. Process Markdown File
    sample_md = """# Architecture Overview
This document specifies the enterprise cloud design.

## Storage Services
We use Azure Blob Storage for raw objects and BigQuery for data warehousing.

```python
def connect():
    return "Connected to Azure"
```
"""
    md_chunks = MarkdownProcessor.process_markdown("architecture_spec.md", sample_md)
    print(f"[*] Processed Markdown File: {len(md_chunks)} chunks generated.")
    for c in md_chunks:
        print(f"    - Chunk Header: '{c.header_path}' ({len(c.content)} chars)")

    # 2. Process PDF File with Embedded Vision Captioning
    sample_pdf_text = "Executive Financial Summary: Q3 Enterprise Revenue expanded by 18%."
    vision_caption = "Architecture diagram depicting Azure AI Search HNSW index connected to Azure OpenAI GPT-4o Agent."
    pdf_chunks = PDFVisionProcessor.process_pdf_with_vision("q3_report.pdf", sample_pdf_text, vision_caption)
    print(f"\n[*] Processed PDF File with Vision OCR: {len(pdf_chunks)} chunks generated.")
    print(f"    - Content Preview:\n{pdf_chunks[0].content}")

    # 3. Process DOCX File
    doc_paras = ["Section 1: Service Level Agreement (SLA).", "Availability target is set to 99.99%."]
    doc_tables = ["| Service | SLA |\n| --- | --- |\n| Azure AI Search | 99.9% |"]
    docx_chunks = DocxProcessor.process_docx("sla_agreement.docx", doc_paras, doc_tables)
    print(f"\n[*] Processed DOCX File: {len(docx_chunks)} chunks generated.")
    print(f"    - Content Preview:\n{docx_chunks[0].content}")

    print("\n=========================================================================")
    print("✅ All .MD, .PDF, and .DOCX Document Extractions Completed Successfully!")
    print("=========================================================================")


if __name__ == "__main__":
    main()
