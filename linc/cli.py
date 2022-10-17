from pathlib import Path

import typer

from linc.core import convert_to_nc

app = typer.Typer(
    name="linc CLI",
    help="Converts raw lidar files (Licel format) to NC with a configuration file",
)


@app.command(no_args_is_help=True)
def main(
    source_path: list[Path] = typer.Argument(..., dir_okay=False, readable=True),
    output_path: Path = typer.Option(..., "--output", "-o", file_okay=True),
    config_file: Path = typer.Option(
        None,
        "--config",
        "-c",
    ),
):
    convert_to_nc(source_path, output_file=output_path, config_file=config_file)


if __name__ == "__main__":
    app()
