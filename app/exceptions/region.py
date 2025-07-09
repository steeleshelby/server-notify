class RegionException(Exception):
    def __init__(self, invalid_region: str):
        super().__init__(f"\n\n{invalid_region} - This is not a server region\n\nAvailable regions: EU, US, AS, SA, AF, OC, RU, CN, JP, KR, ME, IN")
