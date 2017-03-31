# Pop-a-Bias
## Alyssa Cox, Yuxi Wu, Regina Widjaya

### How to run our software
- In the command line, cd into the directory acrwyw122
- Type into the command line: "python3 bias_buster_flask.py"
- Navigate to port 5001 in the browser on the machine. Our web app should pop up. 
- Run article links to test. 

### Our Proposal
In this past election, citizens from opposing sides of the political spectrum have accused each other of spreading bias and lies to the general public. With the ascent of Donald Trump—and his inflammatory, often factually dubious rhetoric—to the presidential seat, the divide has only been exacerbated, and news media have become one of the primary targets of greatest criticism for alleged bias and lies. Distrust in the mainstream media has grown so severe that even the previously unthinkable notion of “alternative facts” is now used by some to further justify the (supposed) dangers of media bias. As UChicago students, we want to make sure that we are getting the whole story when we read the news, and that includes reading what the other side has to say. 

We propose to create a Chrome extension that, when a user visits a website with a political bias, (1) sends a pop-up to the page alerting the user that what they are reading might contain bias and (2) suggests to the user an article on the same issue from a different media with opposing or center political affiliation, thus providing the user with opportunity to do comparative reading and understand the issue from multiple different point of views. 
  
We intend to scrape bias rating data on a number of political websites from the AllSides news bias ratings (here). Based on the website that the user is on (and consequently, the data we scrape), we will suggest a website or websites that have approximately a mirror bias rating.  For example, if a user is viewing a liberal-biased page with a certain degree of slant, we’d suggest a conservative-biased page with a similar degree of bias, and vice versa. We also intend to scrape keywords from the article being read by the user and recommend specific articles from the suggested websites that are related to the original topic (using a web crawler similar to the one we made in PA2). 

### New Tools
- Chrome extension technology
- CSS (to make a nice-looking pop-up box)
- JavaScript (for pop-ups and changing page HTML/CSS)
- Algorithm for matching mirror-ranked websites 

### Data Sources
- AllSides news bias ratings 
- Data from a given user start page

### Work Required
- Gather data by scraping AllSides using BeautifulSoup
- Clean data
- Build relational database
- Create mirror-rank matching function/algorithm
- Build scraper for user site
- Build web crawler that takes mirror-ranked pages as starting URLs and returns articles with keywords matching that of the original user site
- Use Javascript to create a pop-up with a warning and the results from the crawler 
- Build Chrome extension incorporating the pop-up on pages with URLs found in our database
