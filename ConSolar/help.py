from rich import print
import click
@click.command()
@click.option('--help', '-h', is_flag=True, help='Show help message')
def main(help):
    if help:
        print("""this is your help message place.""")

if __name__ == "__main__":
    main()