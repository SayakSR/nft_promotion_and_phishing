openSquat
====
![alt text](https://raw.githubusercontent.com/atenreiro/opensquat/master/screenshots/openSquat_logo.png)

What is openSquat
-------------

openSquat is an opensource Intelligence (OSINT) security tool to identify **cyber squatting** threats to specific companies or domains, such as:

*   Phishing campaigns
*   Domain squatting
*   Typo squatting
*   Bitsquatting
*   IDN homograph attacks
*   Doppenganger domains
*   Other brand/domain related scams

It does support some key features such as:

*   Automatic newly registered domain updating (once a day)
*   Levenshtein distance to calculate word similarity
*   Fetches active and known phishing domains (Phishing Database project)
*   IDN homograph attack detection
*   Integration with VirusTotal
*   Integration with Quad9 DNS service
*   Use different levels of confidence threshold to fine tune
*   Save output into different formats (txt, JSON and CSV)
*   Can be integrated with other threat intelligence tools and DNS sinkholes

This is an opensource project so everyone's welcomed to contribute.

Screenshot / Video Demo
-------------
![alt text](https://raw.githubusercontent.com/atenreiro/opensquat/master/screenshots/openSquat.PNG)

Check the 40 seconds [Demo Video](https://asciinema.org/a/361931) (v1.95)


Demo / Forks
------------
*   [Phishy Domains](https://phishydomains.com) for a simple web version of the openSquat.
*   [openSquat Bot](https://telegram.me/opensquat_bot) for a simple Telegram bot.

Note: Both forks do not contain all openSquat features.


How to Install
------------

```bash
    git clone https://github.com/atenreiro/opensquat
    pip install -r requirements.txt
```
Make sure you have **Python 3.6+** and **pip3** in your environment

How to Update
------------
To update your current version, just type the following commands inside the openSquat directory:
```bash
    git pull
    pip install -r requirements.txt
```
The "pip install" is just to make sure no new libs were added with the new upgrade. 


Usage Examples
------------
Edit the "keywords.txt" with your customised keywords to hunt.

```bash
    # Lazy run with default options
    python opensquat.py

    # for all the options
    python opensquat.py -h
    
    # Search for generic terms used in phishing campaigns (can lead to false positives)
    python opensquat.py -k generic.txt

    # With DNS validation (quad9)
    python opensquat.py --dns
    
    # Subdomain search
    python opensquat.py --subdomains
    
    # Check for domains with open ports 80/443
    python opensquat.py --portcheck

    # With Phishing validation (Phishing Database)
    python opensquat.py --phishing phish_results.txt

    # Save output as JSON
    python opensquat.py -o example.json -t json

    # Save output as CSV
    python opensquat.py -o example.csv -t csv

    # Conduct a certificate transparency (ct) hunt
    python opensquat.py --ct

    # Period search - registrations from the last month (default: day)
    python opensquat.py -p month

    # Tweak confidence level. The lower values bring more false positives
    # (0: very high, 1: high (default), 2: medium, 3: low, 4: very low
    python opensquat.py -c 2

    # All validations options
    python opensquat.py --phishing phishing_domains.txt --dns --ct --subdomains --portcheck 
```

To Do / Roadmap
-------------
*   ~~Integration with VirusTotal (VT) for subdomains validation~~
*   Integratration with VirusTotal (VT) for malware detection
*   ~~Use certificate transparency~~
*   ~~Homograph detection~~ done
*   ~~Improve code quality from B to A grade (codacy)~~
*   ~~PEP8 compliance~~
*   AND logical condition for keywords search (e.g: goole+login) - Thanks to Steff T.
*   Add documentation

Feature Request
-------------
To request for a new feature, create a "new issue" and describe the feature and potential use cases. If something similar already exists, you can upvote the "issue" and contribute to the discussions.

Changelog
-------------
*   Check the [CHANGELOG](https://github.com/atenreiro/opensquat/blob/master/CHANGELOG) file.

Authors
-------------
Project founder
*   Andre Tenreiro [(LinkedIn)](https://www.linkedin.com/in/andretenreiro/)
*   [andre@cert.mz](mailto:andre@cert.mz)

Contributors
*   Please check the contributors page on GitHub

How to help
-------------
You can help this project in many ways:
*   Providing your time and coding skills to enhance the project
*   Build a decent but simple [project webpage](https://opensquat.com)
*   Provide access to OSINT feeds
*   Open new issues with new suggestions, ideas, bug report or feature requests
*   Spread this project within your network
*   Share your story how have you been using the openSquat and what impact it brought to you
*   Make a project logo
