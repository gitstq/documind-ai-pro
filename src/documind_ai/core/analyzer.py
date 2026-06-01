"""AI analysis module for document content."""

import json
import time
from typing import Dict, List, Optional

import tiktoken
from openai import AsyncOpenAI, OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from documind_ai.core.models import (
    AIAnalyzer as AIAnalyzerProtocol,
    AnalysisResult,
    Entity,
    ProcessingConfig,
)


class AIAnalyzer:
    """Analyze document content using AI."""

    def __init__(self, config: Optional[ProcessingConfig] = None):
        """Initialize analyzer.
        
        Args:
            config: Processing configuration
        """
        self.config = config or ProcessingConfig()
        self.client: Optional[OpenAI] = None
        self.async_client: Optional[AsyncOpenAI] = None
        
        if self.config.ai_enabled and self.config.api_key:
            self._init_client()

    def _init_client(self) -> None:
        """Initialize OpenAI client."""
        client_kwargs = {
            "api_key": self.config.api_key,
        }
        
        if self.config.api_base:
            client_kwargs["base_url"] = self.config.api_base
        
        self.client = OpenAI(**client_kwargs)
        self.async_client = AsyncOpenAI(**client_kwargs)
        
        # Initialize tokenizer
        try:
            self.tokenizer = tiktoken.encoding_for_model(self.config.ai_model)
        except KeyError:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def _count_tokens(self, text: str) -> int:
        """Count tokens in text.
        
        Args:
            text: Input text
            
        Returns:
            Token count
        """
        if hasattr(self, 'tokenizer'):
            return len(self.tokenizer.encode(text))
        return len(text) // 4  # Rough estimate

    def _split_content(self, content: str, max_tokens: int = 4000) -> List[str]:
        """Split content into chunks.
        
        Args:
            content: Document content
            max_tokens: Maximum tokens per chunk
            
        Returns:
            List of content chunks
        """
        chunks = []
        current_chunk = []
        current_tokens = 0
        
        # Split by paragraphs
        paragraphs = content.split('\n\n')
        
        for para in paragraphs:
            para_tokens = self._count_tokens(para)
            
            if current_tokens + para_tokens > max_tokens:
                if current_chunk:
                    chunks.append('\n\n'.join(current_chunk))
                current_chunk = [para]
                current_tokens = para_tokens
            else:
                current_chunk.append(para)
                current_tokens += para_tokens
        
        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))
        
        return chunks

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def _call_ai(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 2000,
    ) -> Dict:
        """Call AI API with retry logic.
        
        Args:
            messages: Chat messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            API response
        """
        if not self.client:
            raise RuntimeError("AI client not initialized")
        
        response = self.client.chat.completions.create(
            model=self.config.ai_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        return {
            "content": response.choices[0].message.content,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
        }

    def analyze(self, content: str) -> AnalysisResult:
        """Analyze document content.
        
        Args:
            content: Document content
            
        Returns:
            Analysis result
        """
        start_time = time.time()
        
        if not self.config.ai_enabled or not self.client:
            return AnalysisResult(
                success=False,
                errors=["AI analysis not enabled or client not initialized"],
            )
        
        # Split content into manageable chunks
        chunks = self._split_content(content)
        
        results = {
            "summaries": [],
            "key_points": [],
            "topics": [],
            "entities": [],
            "sentiments": [],
        }
        
        total_tokens = {"prompt": 0, "completion": 0}
        
        # Analyze each chunk
        for i, chunk in enumerate(chunks):
            try:
                chunk_result = self._analyze_chunk(chunk, i + 1, len(chunks))
                
                if chunk_result.get("summary"):
                    results["summaries"].append(chunk_result["summary"])
                
                results["key_points"].extend(chunk_result.get("key_points", []))
                results["topics"].extend(chunk_result.get("topics", []))
                results["entities"].extend(chunk_result.get("entities", []))
                results["sentiments"].append(chunk_result.get("sentiment", "neutral"))
                
                if "usage" in chunk_result:
                    total_tokens["prompt"] += chunk_result["usage"].get("prompt_tokens", 0)
                    total_tokens["completion"] += chunk_result["usage"].get("completion_tokens", 0)
                    
            except Exception as e:
                return AnalysisResult(
                    success=False,
                    errors=[f"Analysis failed for chunk {i+1}: {str(e)}"],
                )
        
        # Combine results
        final_summary = self._combine_summaries(results["summaries"]) if results["summaries"] else None
        
        # Get unique topics
        all_topics = list(set(results["topics"]))
        
        # Aggregate entities
        entity_map = {}
        for entity_data in results["entities"]:
            name = entity_data.get("name", "").lower()
            if name in entity_map:
                entity_map[name]["confidence"] = max(
                    entity_map[name]["confidence"],
                    entity_data.get("confidence", 0)
                )
            else:
                entity_map[name] = entity_data
        
        entities = [
            Entity(
                name=e["name"],
                entity_type=e.get("type", "unknown"),
                confidence=e.get("confidence", 0.5),
            )
            for e in entity_map.values()
        ]
        
        # Determine overall sentiment
        sentiment = self._aggregate_sentiments(results["sentiments"])
        
        processing_time = time.time() - start_time
        
        return AnalysisResult(
            success=True,
            summary=final_summary,
            key_points=list(set(results["key_points"]))[:20],  # Top 20 unique key points
            topics=all_topics[:15],  # Top 15 topics
            sentiment=sentiment,
            entities=entities,
            processing_time=processing_time,
            token_usage=total_tokens,
        )

    def _analyze_chunk(
        self,
        chunk: str,
        chunk_num: int,
        total_chunks: int,
    ) -> Dict:
        """Analyze a single chunk.
        
        Args:
            chunk: Content chunk
            chunk_num: Current chunk number
            total_chunks: Total number of chunks
            
        Returns:
            Analysis results for chunk
        """
        system_prompt = """You are an expert document analyst. Analyze the provided text and extract key information.

Respond in JSON format with the following structure:
{
    "summary": "Brief summary of this section (2-3 sentences)",
    "key_points": ["point 1", "point 2", ...],
    "topics": ["topic 1", "topic 2", ...],
    "entities": [
        {"name": "Entity Name", "type": "person|organization|location|product|technology|other", "confidence": 0.9}
    ],
    "sentiment": "positive|negative|neutral"
}

Be concise and accurate."""

        user_prompt = f"""Analyze this document section ({chunk_num}/{total_chunks}):

{chunk}

Provide your analysis in the requested JSON format."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        
        response = self._call_ai(messages, temperature=0.3, max_tokens=1500)
        
        # Parse JSON response
        content = response["content"]
        
        # Extract JSON from markdown code block if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        result = json.loads(content.strip())
        result["usage"] = response.get("usage", {})
        
        return result

    def _combine_summaries(self, summaries: List[str]) -> str:
        """Combine multiple summaries into one.
        
        Args:
            summaries: List of summaries
            
        Returns:
            Combined summary
        """
        if len(summaries) == 1:
            return summaries[0]
        
        # If too many summaries, combine them iteratively
        combined_text = "\n\n".join([f"Section {i+1}: {s}" for i, s in enumerate(summaries)])
        
        system_prompt = """Combine these section summaries into a coherent overall summary of the entire document.
Provide a concise summary in 3-5 sentences."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": combined_text},
        ]
        
        try:
            response = self._call_ai(messages, temperature=0.3, max_tokens=300)
            return response["content"].strip()
        except Exception:
            # Fallback: just join summaries
            return "\n\n".join(summaries)

    def _aggregate_sentiments(self, sentiments: List[str]) -> str:
        """Aggregate sentiment scores.
        
        Args:
            sentiments: List of sentiment labels
            
        Returns:
            Overall sentiment
        """
        if not sentiments:
            return "neutral"
        
        counts = {"positive": 0, "negative": 0, "neutral": 0}
        for s in sentiments:
            counts[s.lower()] = counts.get(s.lower(), 0) + 1
        
        return max(counts, key=counts.get)

    def generate_questions(self, content: str, num_questions: int = 5) -> List[str]:
        """Generate questions from content.
        
        Args:
            content: Document content
            num_questions: Number of questions to generate
            
        Returns:
            List of questions
        """
        if not self.client:
            return []
        
        system_prompt = f"""Generate {num_questions} insightful questions that can be answered from the provided text.
The questions should cover different aspects and depths of understanding.

Respond with a JSON array of questions."""

        # Use first chunk for question generation
        chunks = self._split_content(content, max_tokens=3000)
        if not chunks:
            return []
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": chunks[0]},
        ]
        
        try:
            response = self._call_ai(messages, temperature=0.5, max_tokens=500)
            content = response["content"]
            
            # Extract JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            questions = json.loads(content.strip())
            return questions if isinstance(questions, list) else []
            
        except Exception:
            return []

    def extract_action_items(self, content: str) -> List[str]:
        """Extract action items from content.
        
        Args:
            content: Document content
            
        Returns:
            List of action items
        """
        if not self.client:
            return []
        
        system_prompt = """Extract all action items, tasks, todos, or follow-up items from the text.
Include who should do what and by when if specified.

Respond with a JSON array of action items."""

        chunks = self._split_content(content, max_tokens=3000)
        if not chunks:
            return []
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": chunks[0]},
        ]
        
        try:
            response = self._call_ai(messages, temperature=0.3, max_tokens=500)
            content = response["content"]
            
            # Extract JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            items = json.loads(content.strip())
            return items if isinstance(items, list) else []
            
        except Exception:
            return []
