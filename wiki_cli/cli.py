import click
import asyncio
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import WordCompleter
import os
from .config import Config
from .api import WikiAPI
from .formatters import OutputFormatter, console
from .image_converter import ASCIIConverter
from rich.panel import Panel

# Ensure cache directory exists
os.makedirs(Config.CACHE_DIR, exist_ok=True)

class WikiCLI:
    def __init__(self):
        self.formatter = OutputFormatter()
        self.current_article = None
        self.search_results = []
        self.session = PromptSession(
            history=FileHistory(Config.HISTORY_FILE),
            completer=WordCompleter(['search', 'view', 'image', 'images', 'links', 'open', 'help', 'clear', 'about', 'exit'])
        )
    
    async def run(self):
        console.print(Panel.fit("Welcome to Wiki-CLI", style="bold magenta"))
        console.print("Type 'help' for available commands\n")
        
        while True:
            try:
                command = await self.session.prompt_async("wiki> ")
                await self.handle_command(command)
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            except Exception as e:
                console.print(f"[red]Error: {str(e)}[/red]")
    
    async def handle_command(self, command):
        if not command:
            return
        
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd == 'exit':
            raise EOFError
        
        commands = {
            'search': self.cmd_search,
            'view': self.cmd_view,
            'image': self.cmd_image,
            'images': self.cmd_images,
            'links': self.cmd_links,
            'open': self.cmd_open,
            'help': self.cmd_help,
            'clear': self.cmd_clear,
            'about': self.cmd_about
        }
        
        if cmd in commands:
            await commands[cmd](args)
        elif cmd.isdigit():
            await self.handle_number(int(cmd))
        else:
            console.print("[red]Unknown command. Type 'help' for available commands.[/red]")
    
    async def cmd_search(self, args):
        if not args:
            console.print("[red]Usage: search <query>[/red]")
            return
        
        query = ' '.join(args)
        async with WikiAPI() as api:
            results = await api.search(query)
            self.search_results = results
            console.print(self.formatter.format_search_results(results))
            console.print("\n[cyan]Type a number to view an article[/cyan]")
    
    async def handle_number(self, number):
        """Handle numeric input for selecting search results"""
        if not self.search_results:
            console.print("[red]No search results to select from. Try searching first.[/red]")
            return
        
        if 1 <= number <= len(self.search_results):
            result = self.search_results[number - 1]
            await self.view_article(result['title'])
        else:
            console.print("[red]Invalid selection number.[/red]")

    async def view_article(self, title):
        """View a specific article"""
        async with WikiAPI() as api:
            article = await api.get_article(title)
            self.current_article = article
            console.print(self.formatter.format_article(article))

    async def cmd_view(self, args):
        if not args:
            console.print("[red]Usage: view <article title>[/red]")
            return
        title = ' '.join(args)
        await self.view_article(title)

    async def cmd_links(self, args):
        if not self.current_article:
            console.print("[red]No article currently viewed. Use 'view' or search first.[/red]")
            return
        
        if 'extlinks' in self.current_article:
            console.print(self.formatter.format_links(self.current_article['extlinks']))
        else:
            console.print("[yellow]No external links found in this article.[/yellow]")

    async def cmd_images(self, args):
        if not self.current_article:
            console.print("[red]No article currently viewed. Use 'view' or search first.[/red]")
            return
        
        if 'images' in self.current_article:
            console.print(self.formatter.format_images(self.current_article['images']))
            console.print("\n[cyan]Use 'image <number>' to view an image[/cyan]")
        else:
            console.print("[yellow]No images found in this article.[/yellow]")

    async def cmd_image(self, args):
        if not args or not args[0].isdigit():
            console.print("[red]Usage: image <number>[/red]")
            return
        
        if not self.current_article or 'images' not in self.current_article:
            console.print("[red]No article with images currently viewed.[/red]")
            return

        number = int(args[0])
        images = self.current_article['images']
        
        if 1 <= number <= len(images):
            image = images[number - 1]
            async with WikiAPI() as api:
                url = await api.get_image_info(image['title'])
                if url:
                    ascii_art = ASCIIConverter.image_to_ascii(url)
                    console.print(ascii_art)
                else:
                    console.print("[red]Could not load image.[/red]")
        else:
            console.print("[red]Invalid image number.[/red]")

    async def cmd_help(self, args):
        help_text = """
        Available commands:
        - search <query>: Search Wikipedia articles
        - view <title>: View a specific article
        - <number>: View article from search results
        - images: List images in current article
        - image <number>: View ASCII art of an image
        - links: Show external links for current article
        - clear: Clear the screen
        - help: Show this help message
        - exit: Exit the application
        """
        console.print(Panel(help_text, title="Wiki-CLI Help", border_style="cyan"))

    async def cmd_clear(self, args):
        console.clear()

    async def cmd_about(self, args):
        about_text = """
        Wiki-CLI - A command-line interface for Wikipedia
        Version 1.0.0
        
        Browse Wikipedia articles directly from your terminal!
        """
        console.print(Panel(about_text, title="About Wiki-CLI", border_style="magenta"))

    async def cmd_open(self, args):
        if not self.current_article:
            console.print("[red]No article currently viewed.[/red]")
            return
        
        title = self.current_article['title'].replace(' ', '_')
        url = f"https://{Config.DEFAULT_LANGUAGE}.wikipedia.org/wiki/{title}"
        console.print(f"[cyan]Article URL: {url}[/cyan]")

@click.command()
def main():
    """Wikipedia Command Line Interface"""
    cli = WikiCLI()
    asyncio.run(cli.run())

if __name__ == '__main__':
    main()