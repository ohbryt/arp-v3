"""
ARP v3 — Multimodal Embedding Module (Gemini Embedding 2)

Based on: Google Gemini Embedding 2 (2026-03-10)
- Text, Image, Video, Audio, PDF unified embedding
- MRL (Martyoshka Representation Learning): 3072/1536/768 dims
- 100+ languages, direct audio processing (no transcription)

Requirements:
    pip install google-genai
"""

import os
from dataclasses import dataclass
from typing import Optional, Union

@dataclass
class EmbeddingResult:
    """Result from Gemini Embedding 2."""
    values: list[float]
    dimension: int
    model: str
    task_type: str

class MultimodalEmbedder:
    """
    Gemini Embedding 2 wrapper for ARP v3.
    
    Supports:
    - Text (up to 8,192 tokens)
    - Images (PNG, JPEG, up to 6 per request)
    - Video (MP4, MOV, up to 120 seconds)
    - Audio (direct processing, no transcription)
    - PDF (direct processing)
    
    MRL dimensions: 3072 (precise), 1536 (balanced), 768 (fast)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY", "")
        self.client = None
        self.model = "gemini-embedding-2-preview"
        
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except ImportError:
                print("  ⚠️ google-genai not installed. Run: pip install google-genai")
            except Exception as e:
                print(f"  ⚠️ Failed to initialize Gemini: {e}")
    
    def is_available(self) -> bool:
        """Check if Gemini Embedding 2 is available."""
        return self.client is not None
    
    def embed_text(
        self,
        text: str,
        dimension: int = 3072,
        task_type: str = "RETRIEVAL_DOCUMENT"
    ) -> Optional[EmbeddingResult]:
        """Embed text content."""
        if not self.is_available():
            return None
        
        try:
            result = self.client.models.embed_content(
                model=self.model,
                contents=text,
                config={
                    "task_type": task_type,
                    "output_dimension": dimension,
                }
            )
            
            return EmbeddingResult(
                values=result.embeddings[0].values,
                dimension=dimension,
                model=self.model,
                task_type=task_type
            )
        except Exception as e:
            print(f"  ⚠️ Embed failed: {e}")
            return None
    
    def embed_image(self, image_path: str, dimension: int = 3072) -> Optional[EmbeddingResult]:
        """Embed image(s)."""
        if not self.is_available():
            return None
        
        try:
            from google.genai import types
            
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            result = self.client.models.embed_content(
                model=self.model,
                contents=[
                    types.Content(
                        parts=[
                            types.Part.from_bytes(
                                data=image_data,
                                mime_type="image/png" if image_path.endswith(".png") else "image/jpeg"
                            )
                        ]
                    )
                ],
                config={
                    "task_type": "RETRIEVAL_DOCUMENT",
                    "output_dimension": dimension,
                }
            )
            
            return EmbeddingResult(
                values=result.embeddings[0].values,
                dimension=dimension,
                model=self.model,
                task_type="image"
            )
        except Exception as e:
            print(f"  ⚠️ Image embed failed: {e}")
            return None
    
    def embed_pdf(self, pdf_path: str, dimension: int = 3072) -> Optional[EmbeddingResult]:
        """Embed PDF document."""
        if not self.is_available():
            return None
        
        try:
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()
            
            result = self.client.models.embed_content(
                model=self.model,
                contents=[
                    {"mime_type": "application/pdf", "data": pdf_data}
                ],
                config={
                    "task_type": "RETRIEVAL_DOCUMENT",
                    "output_dimension": dimension,
                }
            )
            
            return EmbeddingResult(
                values=result.embeddings[0].values,
                dimension=dimension,
                model=self.model,
                task_type="pdf"
            )
        except Exception as e:
            print(f"  ⚠️ PDF embed failed: {e}")
            return None
    
    def embed_audio(self, audio_path: str, dimension: int = 3072) -> Optional[EmbeddingResult]:
        """Embed audio directly (no transcription needed)."""
        if not self.is_available():
            return None
        
        try:
            with open(audio_path, "rb") as f:
                audio_data = f.read()
            
            mime_type = "audio/mp3" if audio_path.endswith(".mp3") else "audio/wav"
            
            result = self.client.models.embed_content(
                model=self.model,
                contents=[
                    {"mime_type": mime_type, "data": audio_data}
                ],
                config={
                    "task_type": "RETRIEVAL_DOCUMENT",
                    "output_dimension": dimension,
                }
            )
            
            return EmbeddingResult(
                values=result.embeddings[0].values,
                dimension=dimension,
                model=self.model,
                task_type="audio"
            )
        except Exception as e:
            print(f"  ⚠️ Audio embed failed: {e}")
            return None
    
    def batch_embed(
        self,
        items: list[dict],
        dimension: int = 3072
    ) -> list[Optional[EmbeddingResult]]:
        """Batch embed multiple items of mixed types."""
        results = []
        
        for item in items:
            item_type = item.get("type", "text")
            
            if item_type == "text":
                results.append(self.embed_text(item["content"], dimension))
            elif item_type == "image":
                results.append(self.embed_image(item["path"], dimension))
            elif item_type == "pdf":
                results.append(self.embed_pdf(item["path"], dimension))
            elif item_type == "audio":
                results.append(self.embed_audio(item["path"], dimension))
            else:
                results.append(None)
        
        return results


# ─── RAG (Retrieval-Augmented Generation) Helper ─────────────────────────────

class SimpleVectorStore:
    """Simple in-memory vector store for RAG."""
    
    def __init__(self, embedder: MultimodalEmbedder):
        self.embedder = embedder
        self.items = []  # {"embedding": [], "content": str, "source": str}
    
    def add_text(self, text: str, source: str = "unknown"):
        """Add text to the store."""
        result = self.embedder.embed_text(text)
        if result:
            self.items.append({
                "embedding": result.values,
                "content": text,
                "source": source
            })
    
    def add_pdf(self, pdf_path: str, source: str = "unknown"):
        """Add PDF to the store."""
        result = self.embedder.embed_pdf(pdf_path)
        if result:
            self.items.append({
                "embedding": result.values,
                "content": f"[PDF: {source}]",
                "source": source
            })
    
    def cosine_similarity(self, a: list[float], b: list[float]) -> float:
        """Calculate cosine similarity."""
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        return dot / (norm_a * norm_b + 1e-10)
    
    def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Search for most similar items."""
        query_result = self.embedder.embed_text(query)
        if not query_result:
            return []
        
        scored = []
        for item in self.items:
            sim = self.cosine_similarity(query_result.values, item["embedding"])
            scored.append({
                "content": item["content"],
                "source": item["source"],
                "similarity": sim
            })
        
        scored.sort(key=lambda x: x["similarity"], reverse=True)
        return scored[:top_k]
