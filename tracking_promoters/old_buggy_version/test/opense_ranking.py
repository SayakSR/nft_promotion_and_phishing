import cloudscraper

def get_slug_url(slug):
    from re import T
    from opensea import OpenseaAPI
    import ast

    api = OpenseaAPI(apikey="c99e72a93cfe488bb66a6c4b33bd80f6")
    collection_metadata = api.collection(collection_slug=slug) # Opensea metadata that is returned is a dictionary

    try:
        url=collection_metadata["collection"]["primary_asset_contracts"][0]["external_link"]
        return url
    except:
        print("No URLs")



scraper=cloudscraper.create_scraper(browser="chrome")
html = scraper.get("https://opensea.io/rankings?search%5BsortAscending%5D=true&search%5BsortBy%5D=TOTAL_VOLUME&chain=ethereum&sortBy=total_volume").text

nfts=[]
urls=[]

for i in range(1000):
    # nft_name=html.split('"name":"')[i].split('"')[0]
    nft_name=html.split('"slug":"')[i].split('"')[0]
    if i==0:
        pass
    else:
        print(nft_name)
        nfts.append(nft_name)



# for i in nfts:
#     print(f"Getting URL for {i}")
#     url=get_slug_url(i)
#     urls.append(url)

# print(urls)

