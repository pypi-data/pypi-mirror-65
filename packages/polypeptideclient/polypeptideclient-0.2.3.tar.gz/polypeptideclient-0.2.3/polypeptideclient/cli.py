"""Console script for polypeptideclient."""
import sys
import click
from polypeptideclient import Client


@click.command()
def main(args=None):
    client = Client('http://localhost:7071')
    response = client.codon_hamming_distance([['ala', 'met'], ['val', 'met']])
    print(response)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
