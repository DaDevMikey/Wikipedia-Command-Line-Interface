from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()

class OutputFormatter:
    @staticmethod
    def format_search_results(results):
        """Format search results as a table"""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Title", style="cyan")
        table.add_column("Snippet")
        
        for i, result in enumerate(results, 1):
            snippet = result['snippet'].replace('<span class="searchmatch">', '').replace('</span>', '')
            table.add_row(str(i), result['title'], snippet)
        
        return table
    
    @staticmethod
    def format_article(article):
        """Format article content with markdown-like styling"""
        text = f"# {article['title']}\n\n"
        text += article['extract']
        return Markdown(text)
    
    @staticmethod
    def format_links(links):
        """Format external links as a table"""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("URL", style="cyan")
        
        for i, link in enumerate(links, 1):
            table.add_row(str(i), link['*'])
        
        return table
    
    @staticmethod
    def format_images(images):
        """Format image list as a table"""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("#", style="dim", width=4)
        table.add_column("Title", style="cyan")
        
        for i, image in enumerate(images, 1):
            table.add_row(str(i), image['title'])
        
        return table
