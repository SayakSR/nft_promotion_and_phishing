
def url_activity(url):
    import requests
    try:
        r = requests.head(url)
        status_code=r.status_code
        if status_code!=404:
            status_code=200

        return status_code
    except requests.ConnectionError as e:
        print(e)
        print("Failed to connect")
        return 404
