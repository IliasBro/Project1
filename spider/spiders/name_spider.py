import scrapy

class NameSpider(scrapy.Spider):
    name = "name_spider"
    start_urls = [
        "https://www.beliebte-vornamen.de/26104-2010er-jahre.htm",
        "https://www.beliebte-vornamen.de/3780-2000er-jahre.htm",
        "https://www.beliebte-vornamen.de/3747-1900er-jahre.htm",
        "https://www.beliebte-vornamen.de/3741-1890er-jahre.htm",
        "https://www.beliebte-vornamen.de/3764-1920er-jahre.htm",
        "https://www.beliebte-vornamen.de/3752-1910er-jahre.htm",
        "https://www.beliebte-vornamen.de/3768-1940er-jahre.htm",
        "https://www.beliebte-vornamen.de/3766-1930er-jahre.htm",
        "https://www.beliebte-vornamen.de/3772-1960er-jahre.htm",
        "https://www.beliebte-vornamen.de/3770-1950er-jahre.htm",
        "https://www.beliebte-vornamen.de/3774-1970er-jahre.htm",
        "https://www.beliebte-vornamen.de/3776-1980er-jahre.htm",
        "https://www.beliebte-vornamen.de/3778-1990er-jahre.htm"
    ]

    def parse(self, response):
        # Example parsing logic:
        # Adjust selectors based on the actual HTML structure of the pages.
        for row in response.css("table tr"):
            name = row.css("td:nth-child(1)::text").get()
            popularity = row.css("td:nth-child(2)::text").get()
            if name and popularity:
                yield {
                    "name": name.strip(),
                    "popularity": int(popularity.strip().replace(".", ""))  # Remove thousand separators if any
                }
