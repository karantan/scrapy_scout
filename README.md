
Scrapy Scout
============
Web crawler for scraping varstvo-konkurence.si


Installation
------------
Install by running: ``$ make``

Run crowlers e.g.:
``$ pipenv run scrapy crawl priglasitve``

Run crowlers in production mode:

``$ pipenv run scrapy crawl priglasitve -a mode=production``

Atm the only difference is that production mode will try to send emails.

Contribute
----------
- Issue Tracker: github.com/karantan/scrapy_scout/issues
- Source Code: github.com/karantan/scrapy_scout

Support
-------
If you are having issues, please let us know.

License
-------
The project is licensed under the MIT License.
