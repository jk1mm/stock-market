import importlib

AVAILABLE_INDEX = ["SP500"]


class IndexView(object):
    """
    Analysis on market indexes.

    Parameters
    ----------
    index: str
        The market index of interest for analysis. Currently supports the indexes in AVAILABLE_INDEX.

    """

    def __init__(self, index: str):

        # Check availability of index
        if (index_name := index.upper()) not in AVAILABLE_INDEX:
            raise Warning(
                f"Please select from the available indexes: {AVAILABLE_INDEX}"
            )

        # Extract specified index data
        data = getattr(importlib.import_module("stock_market.data"), index_name)

        # Self stores
        self.data = data
        self.sector_list = list(set(data["Sector"]))

        # Value from property
        self._summary = None

        # TODO: Add category differentiation
        # TODO: Count categories
        # TODO: Valuation based on sampling of different industries?
