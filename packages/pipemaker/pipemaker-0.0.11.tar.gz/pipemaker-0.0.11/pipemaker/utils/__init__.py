""" generic utilities that may be used on other projects """
import unicodedata
import re
import os
import pandas as pd


def get_name():
    """ return random name """
    # https://www.nrscotland.gov.uk/statistics-and-data/statistics/statistics-by-theme/vital-events/names
    here = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(
        f"{here}/babies-first-names-top-100-girls.csv"
    ).FirstForename.drop_duplicates()
    name = df.sample(1).iloc[0]
    return name


def slugify(value, unicode=False):
    """ convert string to standard format e.g. for use in filenames
    :param value: string to be converted
    :param unicode: allow unicode chars. if False then convert to ascii.
    :return: cleaned string

    Convert spaces to hyphens; replace chars that are not alpha with _; lower; strip.
    """
    value = str(value)
    if unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w]", "_", value).strip().lower()
    return value
