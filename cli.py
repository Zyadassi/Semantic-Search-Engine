"""
CLI interface for semantic search
"""
import click
import sys
from pathlib import Path
from core.search import SemanticSearch
from core.indexer import DocumentIndexer
from utils.logger import logger

# Initialize search engine
search_engine = SemanticSearch()
indexer = DocumentIndexer()

@click.group()
def cli():
    """Semantic Search Engine - Index and search your documents"""
    pass

@cli.command()
@click.argument('directory', type=click.Path(exists=True))
@click.option('--extensions', '-e', multiple=True, default=['md', 'txt'], 
              help='File extensions to index (without dot)')
def index(directory, extensions):
    """Index all documents in a directory"""
    click.echo(f"🗂️  Indexing directory: {directory}")
    
    # Add dots to extensions
    exts = [f".{ext}" if not ext.startswith('.') else ext for ext in extensions]
    
    try:
        results = indexer.index_directory(directory, exts)
        
        click.echo("\n✅ Indexing complete!")
        click.echo(f"   📄 Files indexed: {results['indexed']}")
        click.echo(f"   ❌ Failed: {results['failed']}")
        
        if results['files']:
            click.echo("\n   Indexed files:")
            for f in results['files']:
                click.echo(f"   - {f}")
    
    except FileNotFoundError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('query', nargs=-1, required=True)
@click.option('--top-k', '-k', default=5, help='Number of results to return')
@click.option('--threshold', '-t', default=0.1, help='Minimum similarity threshold')
@click.option('--filter', '-f', default=None, help='Filter by filename')
def search(query, top_k, threshold, filter):
    """Search indexed documents"""
    query_text = ' '.join(query)
    click.echo(f"🔍 Searching for: '{query_text}'")
    click.echo(f"   (top {top_k} results, threshold: {threshold})\n")
    
    try:
        if filter:
            results = search_engine.search_with_filter(
                query_text, filename_filter=filter, top_k=top_k
            )
        else:
            results = search_engine.search(query_text, top_k, threshold)
        
        if not results:
            click.echo("❌ No results found")
            return
        
        click.echo(f"✅ Found {len(results)} results:\n")
        
        for i, result in enumerate(results, 1):
            click.echo(f"{i}. [Similarity: {result['similarity']}]")
            click.echo(f"   File: {result['metadata']['filename']}")
            click.echo(f"   {result['text'][:150]}...")
            click.echo()
    
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)

@cli.command()
def stats():
    """Show indexing statistics"""
    try:
        stats_data = indexer.get_stats()
        click.echo("📊 Index Statistics:")
        click.echo(f"   Total chunks indexed: {stats_data['total_chunks']}")
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.confirmation_option(prompt='Are you sure you want to clear the index?')
def clear():
    """Clear all indexed documents"""
    try:
        indexer.clear_index()
        click.echo("✅ Index cleared successfully")
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
