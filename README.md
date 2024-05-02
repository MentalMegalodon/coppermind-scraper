# coppermind-scraper
A simple script for scraping the coppermind and outputting the summary of a specified book to a .txt file. Usage:
`python scraper.py <relativeUrl> <fileName>`
Relative Url is the url without the `https://coppermind.net` at the beginning. For example, `/wiki/Summary:The_Way_of_Kings` for The Way of Kings. A `.txt` will be appended to whatever filename you input, and the output file will go into an output directory. So far this has only been tested for the 6 Stormlight books. If you notice any issues, please open an issue and I'll look at it.
