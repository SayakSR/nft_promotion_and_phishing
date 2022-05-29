import os

def create_directory(fetch_keyword,datestamp,timestamp):

    try:
        keyword_dir=f'raw_output/{fetch_keyword}'
    except:
        pass
    try:
        date_dir=f'raw_output/{fetch_keyword}/{datestamp}'
    except Exception as e:
        pass
    try:
        time_dir=f'raw_output/{fetch_keyword}/{datestamp}/{timestamp}'
    except:
        pass
    