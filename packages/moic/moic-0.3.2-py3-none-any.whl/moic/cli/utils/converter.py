import re

from rich.syntax import Syntax


class Jira2Markdown:

    HEAD_COLORS = [
        "dodger_blue3",
        "dodger_blue2",
        "dodger_blue1",
        "deep_sky_blue3",
        "deep_sky_blue2",
        "deep_sky_blue1",
        "bright_blue",
    ]

    def __init__(self, raw_content):
        self.raw_content = raw_content
        self._parse()

    def render(self):
        in_block = False
        document = self.converted.split("\r\n")
        rendered_document = []
        block = ""
        block_style = ""
        for line in document:
            if line.startswith("```") and not in_block:
                in_block = True
                block_style = line.replace("```", "").replace("\r\n", "")
            elif line.startswith("```") and in_block:
                in_block = False
                rendered_document.append(Syntax(block, block_style, line_numbers=False))
                block = ""
                block_style = ""
            else:
                if in_block:
                    block = block + line + "\n"
                else:
                    rendered_document.append(self._render(line))

        return rendered_document

    def _render(self, line):

        # Links
        matches = re.findall(r"(\[(.*?)\](\(?.*\)?))", line)
        for match in matches:
            if not match[2]:
                line = line.replace(match[0], f"[grey70]{match[1]}[/grey70]")
            else:
                line = line.replace(match[0], f"[blue]{match[1]}[/blue] | [grey70]{match[2]}[/grey70]")
        # *strong*
        matches = re.findall(r"(\*\*(.*?)\*\*)", line)
        for match in matches:
            line = line.replace(match[0], f"[bold]{match[1]}[/bold]")
        # _emphasis_
        matches = re.findall(r"(__(.*?)__)", line)
        for match in matches:
            line = line.replace(match[0], f"[italic]{match[1]}[/italic]")
        # ??citation?? / -deleted- / +inserted+ / ^superscript^ / ~subscript~
        matches = re.findall(r"(\*(.*?)\*)", line)
        for match in matches:
            line = line.replace(match[0], f"[underline]{match[1]}[/underline]")

        # {{monospaced}}
        matches = re.findall(r"(`(.*?)`)", line)
        for match in matches:
            line = line.replace(match[0], f"[dim]{match[1]}[/dim]")

        # quote
        matches = re.findall(r"(> (.*?))", line)
        for match in matches:
            line = line.replace(match[0], f"[bold blue]| Note: [/][italic]{match[1]}[/italic]")

        # HEADINDS
        matches = re.findall(r"(#+ (.*))", line)
        for match in matches:
            level = len(re.search(r"^(#+) .*$", match[0])[1])
            line = line.replace(match[0], f"[bold {Jira2Markdown.HEAD_COLORS[level - 1]}]{match[1]}[/]")

        # Text Breaks
        line = line.replace("----", "---")

        # Lists
        matches = re.findall(r"^( *\*) (.*)", line)
        for match in matches:
            line = f"{match[0].replace('*', '•')} {match[1]}"

        return line

    def _parse(self):
        self.converted = self.raw_content
        # Lists
        matches = re.findall(r"(\*{2,} (.*?\r\n))", self.converted)
        for match in matches:
            level = len(re.search(r"(\*+) ", match[0])[1])
            self.converted = self.converted.replace(match[0], "  " * (level - 1) + f"* {match[1]}")

        # *strong*
        matches = re.findall(r"\*(((?!\r|\*).)+?)\*", self.converted)
        for match in matches:
            self.converted = self.converted.replace(match[0], f"*{match[0]}*")
        # _emphasis_
        matches = re.findall(r"_(((?!\r).)+?)_", self.converted)
        for match in matches:
            self.converted = self.converted.replace(match[0], f"_{match[0]}_")
        # ??citation??
        matches = re.findall(r"(\?\?(((?!\r).)+?)\?\?)", self.converted)
        for match in matches:
            self.converted = self.converted.replace(match[0], f"*{match[1]}*")
        # -deleted- / +inserted+ / ^superscript^ / ~subscript~
        matches = re.findall(r"(-(((?!\r|/|-).)+?)-)", self.converted)
        for match in matches:
            self.converted = self.converted.replace(match[0], f"*{match[1]}*")

        matches = re.findall(r"(\+(((?!\r).)+?)\+)", self.converted)
        for match in matches:
            self.converted = self.converted.replace(match[0], f"*{match[1]}*")

        matches = re.findall(r"(\^(((?!\r).)+?)\^)", self.converted)
        for match in matches:
            self.converted = self.converted.replace(match[0], f"*{match[1]}*")

        matches = re.findall(r"(~(((?!\r).)+?)~)", self.converted)
        for match in matches:
            self.converted = self.converted.replace(match[0], f"*{match[1]}*")

        # {{monospaced}}
        matches = re.findall(r"({{(((?!\r).)+?)}})", self.converted)
        for match in matches:
            self.converted = self.converted.replace(match[0], f"`{match[1]}`")

        # quote
        matches = re.findall(r"({quote}(.+?){quote})", self.converted, re.DOTALL)
        for match in matches:
            quote = match[1]
            if not quote.startswith("\r\n"):
                quote = f"\r\n{quote}"
            self.converted = self.converted.replace(match[0], f"```{quote}```\r\n")
        matches = re.findall(r"(bq. (.*?)\r)", self.converted)
        for match in matches:
            self.converted = self.converted.replace(match[0], f"> {match[1]}\r\n")

        # HEADINDS
        matches = re.findall(r"(h[0-9]\. (.*?))\r\n", self.converted)
        for match in matches:
            level = re.search(r"h([0-9])\.", match[0])[1]
            md_heading = "#" * int(level) + f" {match[1]}"
            self.converted = self.converted.replace(match[0], md_heading)

        # Text Breaks
        self.converted = self.converted.replace("----", "---")

        # Links
        matches = re.findall(r"(\[(.*?)\])", self.converted)
        for match in matches:
            if "|" in match[1]:
                self.converted = self.converted.replace(
                    match[0], f"[{match[1].split('|')[0]}]({match[1].split('|')[1]})"
                )

        # Code Blocks
        matches = re.findall(r"({code:*(.*?)}(.*?){code})", self.converted, re.DOTALL)
        for match in matches:
            self.converted = self.converted.replace(match[0], f"```{match[1]}\r\n{match[2]}```")
