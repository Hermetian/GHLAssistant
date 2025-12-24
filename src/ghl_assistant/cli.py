"""GHL Assistant CLI - Main entry point."""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer(
    name="ghl",
    help="GoHighLevel automation assistant - CLI tools, templates, and wizards",
    no_args_is_help=True,
)
console = Console()

# Sub-command groups
auth_app = typer.Typer(help="Authentication commands")
tdlc_app = typer.Typer(help="10DLC registration commands")
templates_app = typer.Typer(help="Workflow template commands")
browser_app = typer.Typer(help="Browser automation and traffic capture")

app.add_typer(auth_app, name="auth")
app.add_typer(tdlc_app, name="10dlc")
app.add_typer(templates_app, name="templates")
app.add_typer(browser_app, name="browser")


# ============================================================================
# Auth Commands
# ============================================================================


@auth_app.command("login")
def auth_login():
    """Authenticate with GoHighLevel via OAuth."""
    console.print(
        Panel(
            "[yellow]OAuth login not yet implemented.[/yellow]\n\n"
            "For now, set your API credentials in a .env file:\n"
            "  GHL_API_KEY=your_api_key\n"
            "  GHL_LOCATION_ID=your_location_id",
            title="Authentication",
        )
    )


@auth_app.command("status")
def auth_status():
    """Check current authentication status."""
    from dotenv import dotenv_values

    config = dotenv_values(".env")

    table = Table(title="GHL Authentication Status")
    table.add_column("Setting", style="cyan")
    table.add_column("Status", style="green")

    api_key = config.get("GHL_API_KEY")
    location_id = config.get("GHL_LOCATION_ID")

    table.add_row("API Key", "Set" if api_key else "[red]Not set[/red]")
    table.add_row("Location ID", location_id if location_id else "[red]Not set[/red]")

    console.print(table)


# ============================================================================
# 10DLC Commands
# ============================================================================


@tdlc_app.command("status")
def tdlc_status():
    """Check 10DLC registration status for your account."""
    console.print(
        Panel(
            "[yellow]10DLC status check requires API integration.[/yellow]\n\n"
            "Run [bold]ghl 10dlc guide[/bold] for registration help.",
            title="10DLC Status",
        )
    )


@tdlc_app.command("guide")
def tdlc_guide():
    """Interactive guide for 10DLC registration."""
    console.print()
    console.print(
        Panel(
            "[bold cyan]10DLC Registration Guide[/bold cyan]\n\n"
            "10DLC (10-Digit Long Code) is required for business SMS in the US.\n"
            "Without proper registration, your messages may be filtered or blocked.",
            title="What is 10DLC?",
        )
    )

    console.print()
    table = Table(title="Registration Steps")
    table.add_column("Step", style="cyan", width=8)
    table.add_column("Action", style="white")
    table.add_column("Status", style="yellow", width=12)

    table.add_row("1", "Register your Brand with The Campaign Registry (TCR)", "Required")
    table.add_row("2", "Register your Campaign (what you're texting about)", "Required")
    table.add_row("3", "Wait for carrier approval (1-7 days)", "Required")
    table.add_row("4", "Link approved campaign to your GHL number", "Required")

    console.print(table)

    console.print()
    console.print(
        Panel(
            "[bold]Common Rejection Reasons:[/bold]\n\n"
            "1. Business name doesn't match EIN records exactly\n"
            "2. Website doesn't match business name\n"
            "3. Vague campaign description\n"
            "4. Missing opt-in/opt-out language\n"
            "5. Sample messages don't match campaign type\n\n"
            "[dim]Run with Claude Code for interactive assistance:[/dim]\n"
            "[bold green]/ghl-10dlc[/bold green]",
            title="Troubleshooting",
        )
    )


# ============================================================================
# Template Commands
# ============================================================================


@templates_app.command("list")
def templates_list():
    """List available workflow templates."""
    table = Table(title="Available Workflow Templates")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("Category", style="yellow")
    table.add_column("Description")

    # Placeholder templates - will be loaded from templates/ directory
    templates = [
        ("lead-nurture", "Lead Nurture Sequence", "Sales", "5-touch follow-up for new leads"),
        ("appt-reminder", "Appointment Reminder", "Calendar", "SMS/email reminders before appointments"),
        ("review-request", "Review Request", "Reputation", "Ask for reviews after service"),
        ("new-lead-notify", "New Lead Notification", "Alerts", "Notify team of new leads"),
    ]

    for tid, name, cat, desc in templates:
        table.add_row(tid, name, cat, desc)

    console.print(table)
    console.print("\n[dim]Use [bold]ghl templates import <id>[/bold] to import a template[/dim]")


@templates_app.command("import")
def templates_import(template_id: str):
    """Import a workflow template to your GHL account."""
    console.print(f"[yellow]Template import not yet implemented: {template_id}[/yellow]")
    console.print("[dim]This will require API integration with your GHL account.[/dim]")


# ============================================================================
# Browser Commands
# ============================================================================


@browser_app.command("capture")
def browser_capture(
    url: str = typer.Option(
        "https://app.gohighlevel.com/",
        "--url", "-u",
        help="Starting URL",
    ),
    profile: str = typer.Option(
        "ghl_session",
        "--profile", "-p",
        help="Browser profile name (for cookie persistence)",
    ),
    duration: int = typer.Option(
        0,
        "--duration", "-d",
        help="Capture duration in seconds (0 = until Ctrl+C)",
    ),
    output: str = typer.Option(
        None,
        "--output", "-o",
        help="Output file path for session data",
    ),
):
    """Start a browser session and capture API traffic.

    Opens a browser window where you can interact with GHL.
    All API traffic is captured for analysis.

    First run: Log in manually (session will be saved).
    Future runs: Session is restored from cookies.
    """
    import asyncio
    from .browser.agent import run_capture_session

    console.print(
        Panel(
            f"[bold cyan]Starting Browser Capture Session[/bold cyan]\n\n"
            f"URL: {url}\n"
            f"Profile: {profile}\n"
            f"Duration: {'Until Ctrl+C' if duration == 0 else f'{duration}s'}\n\n"
            "[dim]Interact with GHL in the browser window.\n"
            "All API traffic will be captured.[/dim]",
            title="Browser Agent",
        )
    )

    try:
        result = asyncio.run(
            run_capture_session(
                url=url,
                profile=profile,
                duration=duration,
                output=output,
            )
        )

        if result.get("success"):
            console.print("\n[green]Capture session completed successfully![/green]")
        else:
            console.print(f"\n[red]Capture failed: {result.get('error')}[/red]")

    except KeyboardInterrupt:
        console.print("\n[yellow]Capture interrupted[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")


@browser_app.command("analyze")
def browser_analyze(
    session_file: str = typer.Argument(..., help="Session JSON file to analyze"),
):
    """Analyze a captured session file.

    Shows API endpoints, auth tokens, and patterns found.
    """
    import json
    from pathlib import Path

    filepath = Path(session_file)
    if not filepath.exists():
        console.print(f"[red]File not found: {session_file}[/red]")
        raise typer.Exit(1)

    with open(filepath) as f:
        data = json.load(f)

    console.print(
        Panel(
            f"[bold]Session Analysis[/bold]\n\n"
            f"Profile: {data.get('profile', 'unknown')}\n"
            f"Captured: {data.get('captured_at', 'unknown')}\n"
            f"API calls: {len(data.get('api_calls', []))}\n"
            f"Screenshots: {len(data.get('screenshots', []))}",
            title="Session Info",
        )
    )

    # Show auth tokens
    auth = data.get("auth", {})
    if auth:
        console.print("\n[bold cyan]Auth Tokens Found:[/bold cyan]")
        table = Table()
        table.add_column("Token", style="cyan")
        table.add_column("Value (truncated)", style="white")

        for key, value in auth.items():
            display_val = str(value)[:60] + "..." if len(str(value)) > 60 else str(value)
            table.add_row(key, display_val)

        console.print(table)
    else:
        console.print("\n[yellow]No auth tokens found[/yellow]")

    # Show API endpoints
    api_calls = data.get("api_calls", [])
    if api_calls:
        console.print(f"\n[bold cyan]API Endpoints ({len(api_calls)}):[/bold cyan]")
        table = Table()
        table.add_column("Method", style="cyan", width=8)
        table.add_column("URL", style="white")
        table.add_column("Status", style="green", width=8)

        # Show first 20
        for call in api_calls[:20]:
            url = call.get("url", "")
            # Truncate URL for display
            if len(url) > 80:
                url = url[:77] + "..."
            table.add_row(
                call.get("method", "?"),
                url,
                str(call.get("response_status", "?")),
            )

        console.print(table)

        if len(api_calls) > 20:
            console.print(f"[dim]... and {len(api_calls) - 20} more[/dim]")


@browser_app.command("token")
def browser_token(
    profile: str = typer.Option(
        "ghl_session",
        "--profile", "-p",
        help="Browser profile to check",
    ),
):
    """Extract auth token from a saved browser session.

    Starts browser briefly to check current session and extract tokens.
    """
    import asyncio
    from .browser.agent import BrowserAgent

    async def extract_token():
        async with BrowserAgent(profile_name=profile, capture_network=True) as agent:
            # Navigate to GHL
            await agent.navigate("https://app.gohighlevel.com/")

            # Check if logged in
            if not await agent.is_logged_in():
                return {"success": False, "error": "Not logged in. Run 'ghl browser capture' first."}

            # Wait a moment for API calls
            import asyncio
            await asyncio.sleep(3)

            # Extract tokens
            tokens = agent.get_auth_tokens()
            ghl_data = agent.network.get_ghl_specific() if agent.network else {}

            return {
                "success": True,
                "tokens": tokens,
                "location_id": ghl_data.get("location_id"),
            }

    console.print(f"[dim]Checking session: {profile}[/dim]")

    try:
        result = asyncio.run(extract_token())

        if result.get("success"):
            tokens = result.get("tokens", {})
            if tokens:
                console.print("\n[bold green]Auth tokens found:[/bold green]")
                for key, value in tokens.items():
                    display_val = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
                    console.print(f"  {key}: {display_val}")

                if result.get("location_id"):
                    console.print(f"\n  location_id: {result['location_id']}")
            else:
                console.print("[yellow]No tokens captured. Try interacting with the app.[/yellow]")
        else:
            console.print(f"[red]{result.get('error')}[/red]")

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


# ============================================================================
# Main
# ============================================================================


@app.command()
def version():
    """Show version information."""
    from . import __version__

    console.print(f"GHL Assistant v{__version__}")


if __name__ == "__main__":
    app()
