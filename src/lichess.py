import berserk


class MissingLichessTokenError(Exception):
    pass


class LichessAPI:
    """Lichess API convenience wrapper"""

    def __init__(self, token: str):
        session = berserk.TokenSession(token)
        self.client = berserk.Client(session=session)

    def _get_puzzle_dashboard(self, days=1) -> dict:
        """Get user puzzle dashboard

        Args:
        ----
            days (int): env variable name to check
        """
        try:
            return self.client.puzzles.get_puzzle_dashboard(days=days)
        except berserk.exceptions.ResponseError:
            return {}

    def get_puzzle_count(self, days=1) -> int:
        try:
            dashboard = self._get_puzzle_dashboard(days=days)
            return dashboard["global"]["nb"]
        except KeyError:
            return 0

    def get_user_perfs(self) -> dict:
        account = self.client.account.get()

        perfs = {}
        for mode, data in account.get("perfs").items():
            if data.get("prov"):
                continue  # inore provisional rating

            for metric, value in data.items():
                perfs[f"perfs_{mode}_{metric}"] = value

        return perfs
