"""Command-line interface for DocuMind AI."""

import os
import sys
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.tree import Tree

from documind_ai.core.analyzer import AIAnalyzer
from documind_ai.core.converter import DocumentConverter
from documind_ai.core.extractor import KnowledgeExtractor
from documind_ai.core.models import ProcessingConfig
from documind_ai.utils.file_utils import ensure_dir, get_output_path

console = Console()


def print_banner():
    """Print application banner."""
    banner = """
[bold cyan]╔══════════════════════════════════════════════════════════╗[/bold cyan]
[bold cyan]║[/bold cyan]  [bold white]🧠 DocuMind AI[/bold white]                                         [bold cyan]║[/bold cyan]
[bold cyan]║[/bold cyan]  [dim]Intelligent Document Conversion & Knowledge Extraction[/dim]  [bold cyan]║[/bold cyan]
[bold cyan]╚══════════════════════════════════════════════════════════╝[/bold cyan]
    """
    console.print(banner)


@click.group(invoke_without_command=True)
@click.option('--version', is_flag=True, help='Show version information')
@click.pass_context
def cli(ctx, version):
    """🧠 DocuMind AI - Intelligent Document Conversion & Knowledge Extraction"""
    if version:
        console.print("[bold cyan]DocuMind AI[/bold cyan] version [bold]1.0.0[/bold]")
        return
    
    if ctx.invoked_subcommand is None:
        print_banner()
        console.print("\n[dim]Use --help for available commands[/dim]\n")


@cli.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('-o', '--output', 'output_dir', type=click.Path(), 
              help='Output directory')
@click.option('--no-ai', is_flag=True, help='Disable AI analysis')
@click.option('--model', default='gpt-4o-mini', help='AI model to use')
@click.option('--api-key', envvar='OPENAI_API_KEY', help='OpenAI API key')
@click.option('--api-base', envvar='OPENAI_API_BASE', help='OpenAI API base URL')
@click.option('--extract-kg', is_flag=True, help='Extract knowledge graph')
@click.option('--questions', is_flag=True, help='Generate questions')
@click.option('--actions', is_flag=True, help='Extract action items')
@click.option('--max-pages', type=int, help='Maximum pages to process')
def convert(
    input_path: str,
    output_dir: Optional[str],
    no_ai: bool,
    model: str,
    api_key: Optional[str],
    api_base: Optional[str],
    extract_kg: bool,
    questions: bool,
    actions: bool,
    max_pages: Optional[int],
):
    """Convert document to Markdown with AI analysis."""
    print_banner()
    
    input_path = Path(input_path)
    
    # Setup configuration
    config = ProcessingConfig(
        ai_enabled=not no_ai,
        ai_model=model,
        api_key=api_key,
        api_base=api_base,
        generate_summary=True,
        extract_entities=True,
        build_knowledge_graph=extract_kg,
        generate_questions=questions,
        extract_action_items=actions,
        max_pages=max_pages,
    )
    
    # Determine output directory
    if output_dir:
        output_dir = Path(output_dir)
    else:
        output_dir = input_path.parent / 'documind_output'
    
    ensure_dir(output_dir)
    
    # Process files
    if input_path.is_dir():
        files = list(input_path.rglob('*'))
        files = [f for f in files if f.is_file()]
    else:
        files = [input_path]
    
    console.print(f"\n[bold]Processing {len(files)} file(s)...[/bold]\n")
    
    # Initialize components
    converter = DocumentConverter(config)
    analyzer = AIAnalyzer(config) if config.ai_enabled else None
    extractor = KnowledgeExtractor() if extract_kg else None
    
    results = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        
        for file_path in files:
            task_id = progress.add_task(f"Processing {file_path.name}...", total=None)
            
            try:
                # Convert document
                output_path = output_dir / f"{file_path.stem}.md"
                result = converter.convert(file_path, output_path)
                
                if not result.success:
                    console.print(f"[red]✗[/red] {file_path.name}: {result.errors[0]}")
                    continue
                
                analysis_result = None
                
                # AI Analysis
                if analyzer and config.ai_enabled:
                    progress.update(task_id, description=f"Analyzing {file_path.name}...")
                    analysis_result = analyzer.analyze(result.content)
                    
                    # Save analysis
                    if analysis_result.success:
                        analysis_path = output_dir / f"{file_path.stem}_analysis.json"
                        import json
                        analysis_data = {
                            "summary": analysis_result.summary,
                            "key_points": analysis_result.key_points,
                            "topics": analysis_result.topics,
                            "sentiment": analysis_result.sentiment,
                            "entities": [
                                {"name": e.name, "type": e.entity_type}
                                for e in analysis_result.entities
                            ],
                            "token_usage": analysis_result.token_usage,
                        }
                        analysis_path.write_text(
                            json.dumps(analysis_data, indent=2, ensure_ascii=False),
                            encoding='utf-8'
                        )
                
                # Knowledge Graph Extraction
                if extractor and config.build_knowledge_graph:
                    progress.update(task_id, description=f"Extracting knowledge from {file_path.name}...")
                    kg = extractor.extract(result.content, analysis_result)
                    
                    # Save knowledge graph
                    kg_path = output_dir / f"{file_path.stem}_knowledge.json"
                    kg_path.write_text(
                        json.dumps(kg.to_dict(), indent=2, ensure_ascii=False),
                        encoding='utf-8'
                    )
                
                # Generate questions
                if analyzer and config.generate_questions:
                    progress.update(task_id, description=f"Generating questions for {file_path.name}...")
                    questions_list = analyzer.generate_questions(result.content)
                    if questions_list:
                        questions_path = output_dir / f"{file_path.stem}_questions.txt"
                        questions_path.write_text(
                            '\n'.join(f"{i+1}. {q}" for i, q in enumerate(questions_list)),
                            encoding='utf-8'
                        )
                
                # Extract action items
                if analyzer and config.extract_action_items:
                    progress.update(task_id, description=f"Extracting actions from {file_path.name}...")
                    action_items = analyzer.extract_action_items(result.content)
                    if action_items:
                        actions_path = output_dir / f"{file_path.stem}_actions.txt"
                        actions_path.write_text(
                            '\n'.join(f"- {a}" for a in action_items),
                            encoding='utf-8'
                        )
                
                results.append({
                    'file': file_path.name,
                    'success': True,
                    'type': result.document_type.value,
                    'pages': result.metadata.page_count,
                    'words': len(result.content.split()),
                })
                
                console.print(f"[green]✓[/green] {file_path.name}")
                
            except Exception as e:
                console.print(f"[red]✗[/red] {file_path.name}: {str(e)}")
                results.append({
                    'file': file_path.name,
                    'success': False,
                    'error': str(e),
                })
            
            progress.remove_task(task_id)
    
    # Print summary
    console.print("\n" + "=" * 60)
    console.print("[bold]Processing Summary[/bold]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("File", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Status", style="bold")
    table.add_column("Details", style="dim")
    
    for result in results:
        if result['success']:
            details = f"{result.get('words', 0)} words"
            if result.get('pages'):
                details += f", {result['pages']} pages"
            table.add_row(
                result['file'],
                result.get('type', 'unknown'),
                "[green]✓ Success[/green]",
                details
            )
        else:
            table.add_row(
                result['file'],
                "-",
                "[red]✗ Failed[/red]",
                result.get('error', 'Unknown error')[:50]
            )
    
    console.print(table)
    console.print(f"\n[bold]Output directory:[/bold] {output_dir}")


@cli.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('-o', '--output', type=click.Path(), help='Output file path')
@click.option('--format', 'output_format', 
              type=click.Choice(['json', 'cypher', 'rdf']), 
              default='json', help='Output format')
def extract_kg(input_path: str, output: Optional[str], output_format: str):
    """Extract knowledge graph from document."""
    print_banner()
    
    input_path = Path(input_path)
    
    # Read content
    if input_path.suffix.lower() == '.md':
        content = input_path.read_text(encoding='utf-8')
    else:
        # Convert first
        config = ProcessingConfig()
        converter = DocumentConverter(config)
        result = converter.convert(input_path)
        if not result.success:
            console.print(f"[red]Error:[/red] {result.errors[0]}")
            sys.exit(1)
        content = result.content
    
    # Extract knowledge graph
    extractor = KnowledgeExtractor()
    kg = extractor.extract(content)
    
    # Determine output path
    if output:
        output_path = Path(output)
    else:
        output_path = input_path.parent / f"{input_path.stem}_kg.{output_format}"
    
    # Export in requested format
    if output_format == 'json':
        import json
        output_data = kg.to_dict()
        output_path.write_text(
            json.dumps(output_data, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
    elif output_format == 'cypher':
        cypher = extractor.export_to_cypher(kg)
        output_path.write_text(cypher, encoding='utf-8')
    elif output_format == 'rdf':
        rdf = extractor.export_to_rdf(kg)
        output_path.write_text(rdf, encoding='utf-8')
    
    console.print(f"\n[green]✓[/green] Knowledge graph saved to: {output_path}")
    console.print(f"[dim]Entities: {len(kg.entities)}[/dim]")
    console.print(f"[dim]Relationships: {len(kg.relationships)}[/dim]")


@cli.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--model', default='gpt-4o-mini', help='AI model to use')
@click.option('--api-key', envvar='OPENAI_API_KEY', help='OpenAI API key')
def analyze(input_path: str, model: str, api_key: Optional[str]):
    """Analyze document with AI."""
    print_banner()
    
    input_path = Path(input_path)
    
    # Setup configuration
    config = ProcessingConfig(
        ai_enabled=True,
        ai_model=model,
        api_key=api_key,
    )
    
    # Read or convert content
    if input_path.suffix.lower() in ['.md', '.txt']:
        content = input_path.read_text(encoding='utf-8')
    else:
        converter = DocumentConverter(config)
        result = converter.convert(input_path)
        if not result.success:
            console.print(f"[red]Error:[/red] {result.errors[0]}")
            sys.exit(1)
        content = result.content
    
    # Analyze
    analyzer = AIAnalyzer(config)
    
    with console.status("[bold green]Analyzing document..."):
        result = analyzer.analyze(content)
    
    if not result.success:
        console.print(f"[red]Analysis failed:[/red] {result.errors[0]}")
        sys.exit(1)
    
    # Display results
    console.print("\n" + "=" * 60)
    console.print("[bold cyan]📊 Analysis Results[/bold cyan]\n")
    
    # Summary
    if result.summary:
        console.print(Panel(
            result.summary,
            title="[bold]Summary[/bold]",
            border_style="blue"
        ))
    
    # Key Points
    if result.key_points:
        console.print("\n[bold]📝 Key Points:[/bold]")
        for i, point in enumerate(result.key_points[:10], 1):
            console.print(f"  {i}. {point}")
    
    # Topics
    if result.topics:
        console.print("\n[bold]🏷️  Topics:[/bold]")
        topics_str = ", ".join(result.topics[:15])
        console.print(f"  {topics_str}")
    
    # Sentiment
    if result.sentiment:
        sentiment_emoji = {
            'positive': '😊',
            'negative': '😔',
            'neutral': '😐',
        }.get(result.sentiment, '😐')
        console.print(f"\n[bold]💭 Sentiment:[/bold] {sentiment_emoji} {result.sentiment.title()}")
    
    # Entities
    if result.entities:
        console.print("\n[bold]👥 Key Entities:[/bold]")
        entity_table = Table(show_header=True, header_style="bold")
        entity_table.add_column("Name", style="cyan")
        entity_table.add_column("Type", style="green")
        entity_table.add_column("Confidence", style="yellow")
        
        for entity in sorted(result.entities, key=lambda e: e.confidence, reverse=True)[:10]:
            entity_table.add_row(
                entity.name,
                entity.entity_type,
                f"{entity.confidence:.2f}"
            )
        console.print(entity_table)
    
    # Token usage
    if result.token_usage:
        console.print(f"\n[dim]Token Usage: {result.token_usage}[/dim]")


@cli.command()
def config():
    """Show configuration information."""
    print_banner()
    
    console.print("\n[bold]Configuration[/bold]\n")
    
    # Environment variables
    env_vars = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', '[not set]'),
        'OPENAI_API_BASE': os.getenv('OPENAI_API_BASE', '[not set]'),
    }
    
    table = Table(show_header=True, header_style="bold")
    table.add_column("Variable", style="cyan")
    table.add_column("Value", style="green")
    
    for var, value in env_vars.items():
        # Mask API key
        if 'KEY' in var and value != '[not set]':
            value = value[:8] + '...' + value[-4:]
        table.add_row(var, value)
    
    console.print(table)
    
    console.print("\n[bold]Supported Formats:[/bold]")
    formats = [
        "PDF (.pdf)", "Word (.docx, .doc)", "Excel (.xlsx, .xls)",
        "PowerPoint (.pptx, .ppt)", "HTML (.html, .htm)",
        "Text (.txt)", "Markdown (.md)", "CSV (.csv)",
        "JSON (.json)", "XML (.xml)", "RTF (.rtf)",
        "OpenDocument (.odt, .ods, .odp)"
    ]
    
    for fmt in formats:
        console.print(f"  ✓ {fmt}")


def main():
    """Entry point."""
    cli()


if __name__ == '__main__':
    main()
