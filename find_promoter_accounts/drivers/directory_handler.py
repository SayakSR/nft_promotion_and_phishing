import os

def create_directory(fetch_keyword,datestamp):

    try:
        keyword_dir=f"mkdir \rraw_output\{fetch_keyword}"
        print(keyword_dir)
        os.system(keyword_dir)
        
    except Exception as e:
        print(e)
    try:
        date_dir=f'mkdir \rraw_output\{fetch_keyword}\{datestamp}'
        os.system(date_dir)
    except Exception as e:
        print(e)

    