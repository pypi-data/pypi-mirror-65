"""Main module."""
import urllib.parse
import requests


class Client:
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl

    def codon_hamming_distance(self, amino_acid_pairs):
        url = urllib.parse.urljoin(self.baseUrl, "api/CodonDistance")
        json = {
            "pairs": amino_acid_pairs
        }

        r = requests.post(url, json=json)
        return r.json()
