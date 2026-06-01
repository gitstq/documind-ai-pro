"""Knowledge extraction module."""

import json
import re
from typing import Dict, List, Optional, Set, Tuple

from documind_ai.core.models import (
    AnalysisResult,
    Entity,
    KnowledgeGraph,
    Relationship,
)


class KnowledgeExtractor:
    """Extract knowledge graph from document content."""

    # Common relationship patterns
    RELATIONSHIP_PATTERNS = [
        (r'(\w+)\s+(?:is|are|was|were)\s+(?:a|an|the)?\s*(\w+)', 'is_a'),
        (r'(\w+)\s+(?:has|have|had)\s+(?:a|an|the)?\s*(\w+)', 'has'),
        (r'(\w+)\s+(?:works?\s+for|employed\s+by)\s+(\w+)', 'works_for'),
        (r'(\w+)\s+(?:created?|developed?|built?)\s+(\w+)', 'created'),
        (r'(\w+)\s+(?:founded?|established?)\s+(\w+)', 'founded'),
        (r'(\w+)\s+(?:acquired?|bought?)\s+(\w+)', 'acquired'),
        (r'(\w+)\s+(?:partners?\s+with|collaborates?\s+with)\s+(\w+)', 'partners_with'),
        (r'(\w+)\s+(?:located?\s+in|based?\s+in)\s+(\w+)', 'located_in'),
        (r'(\w+)\s+(?:uses?|utilizes?)\s+(\w+)', 'uses'),
        (r'(\w+)\s+(?:produces?|manufactures?)\s+(\w+)', 'produces'),
        (r'(\w+)\s+(?:owns?|possesses?)\s+(\w+)', 'owns'),
        (r'(\w+)\s+(?:leads?|manages?)\s+(\w+)', 'leads'),
        (r'(\w+)\s+(?:invested?\s+in)\s+(\w+)', 'invested_in'),
        (r'(\w+)\s+(?:announced?|declared?)\s+(\w+)', 'announced'),
        (r'(\w+)\s+(?:supports?|backs?)\s+(\w+)', 'supports'),
    ]

    # Entity type keywords
    ENTITY_TYPE_KEYWORDS = {
        'person': ['ceo', 'founder', 'president', 'director', 'manager', 'engineer', 'developer',
                   'researcher', 'scientist', 'author', 'writer', 'artist', 'designer'],
        'organization': ['company', 'corporation', 'inc', 'ltd', 'llc', 'corp', 'startup',
                         'enterprise', 'firm', 'agency', 'institute', 'university', 'school'],
        'location': ['city', 'country', 'state', 'region', 'area', 'district', 'province',
                     'capital', 'headquarters', 'office'],
        'technology': ['software', 'platform', 'system', 'framework', 'library', 'api',
                       'algorithm', 'model', 'database', 'cloud', 'ai', 'ml'],
        'product': ['product', 'service', 'solution', 'application', 'app', 'tool',
                    'device', 'gadget', 'feature'],
    }

    def __init__(self):
        """Initialize extractor."""
        self.entity_cache: Dict[str, Entity] = {}
        self.relationship_cache: Set[str] = set()

    def extract(
        self,
        content: str,
        analysis_result: Optional[AnalysisResult] = None,
    ) -> KnowledgeGraph:
        """Extract knowledge graph from content.
        
        Args:
            content: Document content
            analysis_result: Optional AI analysis result
            
        Returns:
            Knowledge graph
        """
        self.entity_cache = {}
        self.relationship_cache = set()

        # Extract entities from analysis if available
        if analysis_result and analysis_result.entities:
            for entity in analysis_result.entities:
                self.entity_cache[entity.name.lower()] = entity

        # Extract entities from content
        self._extract_entities_from_content(content)

        # Extract relationships
        self._extract_relationships_from_content(content)

        # Build knowledge graph
        return KnowledgeGraph(
            entities=list(self.entity_cache.values()),
            relationships=list(self._get_unique_relationships()),
        )

    def _extract_entities_from_content(self, content: str) -> None:
        """Extract entities from content using pattern matching.
        
        Args:
            content: Document content
        """
        # Named entity patterns
        patterns = [
            # Capitalized words (potential proper nouns)
            (r'\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\b', 'unknown'),
            # Quoted names
            (r'"([^"]+)"', 'unknown'),
            # Parenthetical mentions
            (r'\(([A-Z][^)]+)\)', 'unknown'),
        ]

        for pattern, default_type in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                name = match.group(1) if match.groups() else match.group(0)
                name = name.strip()
                
                # Skip common false positives
                if self._is_false_positive(name):
                    continue
                
                # Determine entity type
                entity_type = self._determine_entity_type(name, content)
                
                # Add to cache
                key = name.lower()
                if key not in self.entity_cache:
                    self.entity_cache[key] = Entity(
                        name=name,
                        entity_type=entity_type,
                        confidence=0.6,
                        occurrences=[match.start()],
                    )
                else:
                    self.entity_cache[key].occurrences.append(match.start())

    def _is_false_positive(self, name: str) -> bool:
        """Check if entity name is a false positive.
        
        Args:
            name: Entity name
            
        Returns:
            True if false positive
        """
        false_positives = {
            'the', 'a', 'an', 'this', 'that', 'these', 'those',
            'and', 'or', 'but', 'if', 'then', 'else',
            'is', 'are', 'was', 'were', 'be', 'been',
            'it', 'its', 'they', 'them', 'their',
            'he', 'she', 'his', 'her', 'him',
            'you', 'your', 'we', 'our', 'us',
            'i', 'my', 'me', 'mine',
            'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'as', 'into', 'through',
            'during', 'before', 'after', 'above', 'below',
            'between', 'under', 'again', 'further',
            'then', 'once', 'here', 'there', 'when',
            'where', 'why', 'how', 'all', 'each',
            'few', 'more', 'most', 'other', 'some',
            'such', 'no', 'nor', 'not', 'only',
            'own', 'same', 'so', 'than', 'too',
            'very', 'can', 'will', 'just', 'should',
            'now', 'also', 'may', 'might', 'must',
            'shall', 'could', 'would', 'january', 'february',
            'march', 'april', 'may', 'june', 'july',
            'august', 'september', 'october', 'november', 'december',
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday', 'sunday', 'figure', 'table', 'section',
            'chapter', 'page', 'appendix',
        }
        
        return name.lower() in false_positives or len(name) < 2

    def _determine_entity_type(self, name: str, context: str) -> str:
        """Determine entity type from context.
        
        Args:
            name: Entity name
            context: Document context
            
        Returns:
            Entity type
        """
        name_lower = name.lower()
        context_lower = context.lower()
        
        # Check for keywords before the entity
        for entity_type, keywords in self.ENTITY_TYPE_KEYWORDS.items():
            for keyword in keywords:
                # Look for patterns like "keyword name" or "name, keyword"
                pattern1 = rf'\b{keyword}\s+{re.escape(name)}\b'
                pattern2 = rf'\b{re.escape(name)}\b[^.]*?\b{keyword}\b'
                
                if re.search(pattern1, context_lower) or re.search(pattern2, context_lower):
                    return entity_type
        
        # Check for common suffixes
        org_suffixes = ['inc', 'corp', 'ltd', 'llc', 'company', 'corporation', 'limited']
        if any(name_lower.endswith(f' {suffix}') or name_lower.endswith(f',{suffix}') 
               for suffix in org_suffixes):
            return 'organization'
        
        # Check for location indicators
        location_words = ['street', 'avenue', 'road', 'city', 'country', 'region']
        if any(word in context_lower[max(0, context_lower.find(name_lower) - 50):
                                     context_lower.find(name_lower) + len(name) + 50]
               for word in location_words):
            return 'location'
        
        return 'unknown'

    def _extract_relationships_from_content(self, content: str) -> None:
        """Extract relationships from content.
        
        Args:
            content: Document content
        """
        sentences = re.split(r'[.!?]+', content)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:
                continue
            
            for pattern, relation_type in self.RELATIONSHIP_PATTERNS:
                matches = re.finditer(pattern, sentence, re.IGNORECASE)
                for match in matches:
                    source = match.group(1)
                    target = match.group(2)
                    
                    # Validate entities exist
                    if (source.lower() in self.entity_cache and 
                        target.lower() in self.entity_cache):
                        
                        relationship_key = f"{source.lower()}|{relation_type}|{target.lower()}"
                        if relationship_key not in self.relationship_cache:
                            self.relationship_cache.add(relationship_key)

    def _get_unique_relationships(self) -> List[Relationship]:
        """Get unique relationships from cache.
        
        Returns:
            List of relationships
        """
        relationships = []
        for rel_key in self.relationship_cache:
            parts = rel_key.split('|')
            if len(parts) == 3:
                source, relation_type, target = parts
                relationships.append(Relationship(
                    source=source.title(),
                    target=target.title(),
                    relation_type=relation_type,
                    confidence=0.7,
                ))
        return relationships

    def build_graph_data(self, knowledge_graph: KnowledgeGraph) -> Dict:
        """Build graph data for visualization.
        
        Args:
            knowledge_graph: Knowledge graph
            
        Returns:
            Graph data dictionary
        """
        nodes = []
        edges = []
        
        # Build nodes
        for i, entity in enumerate(knowledge_graph.entities):
            nodes.append({
                "id": i,
                "label": entity.name,
                "type": entity.entity_type,
                "confidence": entity.confidence,
            })
        
        # Create entity name to index mapping
        entity_map = {e.name.lower(): i for i, e in enumerate(knowledge_graph.entities)}
        
        # Build edges
        for rel in knowledge_graph.relationships:
            source_idx = entity_map.get(rel.source.lower())
            target_idx = entity_map.get(rel.target.lower())
            
            if source_idx is not None and target_idx is not None:
                edges.append({
                    "source": source_idx,
                    "target": target_idx,
                    "label": rel.relation_type,
                    "confidence": rel.confidence,
                })
        
        return {
            "nodes": nodes,
            "edges": edges,
        }

    def export_to_cypher(self, knowledge_graph: KnowledgeGraph) -> str:
        """Export knowledge graph to Cypher query language.
        
        Args:
            knowledge_graph: Knowledge graph
            
        Returns:
            Cypher queries
        """
        queries = []
        
        # Create nodes
        for entity in knowledge_graph.entities:
            safe_name = entity.name.replace("'", "\\'")
            query = (
                f"CREATE (e:Entity {{name: '{safe_name}', "
                f"type: '{entity.entity_type}', "
                f"confidence: {entity.confidence}}})"
            )
            queries.append(query)
        
        # Create relationships
        for rel in knowledge_graph.relationships:
            safe_source = rel.source.replace("'", "\\'")
            safe_target = rel.target.replace("'", "\\'")
            query = (
                f"MATCH (a:Entity {{name: '{safe_source}'}}), "
                f"(b:Entity {{name: '{safe_target}'}}) "
                f"CREATE (a)-[:{rel.relation_type.upper()} "
                f"{{confidence: {rel.confidence}}}]->(b)"
            )
            queries.append(query)
        
        return "\n".join(queries)

    def export_to_rdf(self, knowledge_graph: KnowledgeGraph) -> str:
        """Export knowledge graph to RDF/Turtle format.
        
        Args:
            knowledge_graph: Knowledge graph
            
        Returns:
            RDF/Turtle content
        """
        lines = [
            "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .",
            "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
            "@prefix ex: <http://example.org/> .",
            "",
        ]
        
        # Define entities
        for entity in knowledge_graph.entities:
            entity_uri = f"ex:{self._to_uri_safe(entity.name)}"
            lines.append(f"{entity_uri} rdf:type ex:{entity.entity_type.title()} ;")
            lines.append(f'    rdfs:label "{entity.name}" .')
            lines.append("")
        
        # Define relationships
        for rel in knowledge_graph.relationships:
            source_uri = f"ex:{self._to_uri_safe(rel.source)}"
            target_uri = f"ex:{self._to_uri_safe(rel.target)}"
            rel_uri = f"ex:{rel.relation_type}"
            lines.append(f"{source_uri} {rel_uri} {target_uri} .")
        
        return "\n".join(lines)

    def _to_uri_safe(self, name: str) -> str:
        """Convert name to URI-safe string.
        
        Args:
            name: Entity name
            
        Returns:
            URI-safe string
        """
        return re.sub(r'[^a-zA-Z0-9]', '_', name).lower()
