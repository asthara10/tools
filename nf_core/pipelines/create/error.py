from textwrap import dedent

from textual.app import ComposeResult
from textual.containers import Center
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Markdown, Static


class ExistError(Screen):
    """A screen to show the final text and exit the app - when an error ocurred."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Markdown(
            dedent(
                """
                # Pipeline exists
                """
            )
        )
        yield Static(
            rf"\n[green]{' ' * 40},--.[grey39]/[green],-."
            + r"\n[blue]        ___     __   __   __   ___     [green]/,-._.--~\\"
            + r"\n[blue]|\ | |__  __ /  ` /  \ |__) |__      [yellow]   }  {"
            + r"\n[blue]   | \| |       \__, \__/ |  \ |___     [green]\`-._,-`-,"
            + r"\n[green]                                       `._,._,'\n",
            id="logo",
        )

        completed_text_markdown = f"""
        A pipeline '`{self.parent.TEMPLATE_CONFIG.outdir + "/" + self.parent.TEMPLATE_CONFIG.org + "-" + self.parent.TEMPLATE_CONFIG.name}`' already exists.
        Please select a different name or `force` the creation of the pipeline to override the existing one.
        """

        yield Markdown(dedent(completed_text_markdown))
        yield Center(
            Button("Close App", id="close_app", variant="success"),
            classes="cta",
        )
