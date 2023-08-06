import pandas as pd
from enum import Enum
import requests
from io import BytesIO

# Remove the pandas' limit to display the whole column if it's long
pd.set_option('max_colwidth', 1)


class tables(Enum):
    # Since the file is too large, we can't have a direct link using Google drive
    refactoring="1-EHbvtr6-zGynRAwatQ48-ZagjJmk5gG"
    refactorings_in_commit_v1="16yUpL1k3Eddyghb3okL6flHbLZA_cabe"
    commit="1-BKOYtMUspW_Of6TBO_c4tEjFEjt6Mvv"
    project="1-DGgI4HdnwWdmx3hS4x7HbTmcgLJLf0W"
    keywords="10BBmp7Vx_BzANiRy4K_0L-K2xbg-Qp1O"
    clean_commits="1CX8jf7INRchSSC0meNtMZRsTOCtHUgAh"
    clean_commits_v3="10UIhWryfU8QM2X3adBhhilNg6q5v9trs"
    clean_commits_matching_keywords_v1="1oAHRU8sTXxX0B3f63yQVcilqhK-7OCFO"
    clean_commits_with_structure="1XFbhSXuKFKQxFaYx_x__314Vja6DKCf_"
    clean_commits_with_structure_v2="12QMCdj5RPPdOaNcbiF3VRnIvHEzxFnBj"
    commits_with_scores_v2="10Gwj-ZETuFhm0Uxvtzh2XOiitfvqz9mK"


def load_dataset(table):
    url = f"https://drive.google.com/u/0/uc?id={table.value}&export=download"
    file = requests.get(url).content
    dataset = pd.read_csv(BytesIO(file))
    return dataset
