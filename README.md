# social-media-scraper
scrape scrape scrape instagram scrape scrape scrape

Chromedriver is for Chrome version 80. Update as needed. 

# How to use

`pip install selenium`, `pip install progressbar`

`python main.py username password genre`

Input your instagram `username`, `password`, and `genre` of the tags to search. 

Current supported genres are `gaming`, `food`, `rand`, and `travel`. If no tag genre is specified or an unsupport genre is input, it will default to search the #instagram tag. This uses the search by likes method since they are few paid promotion labels outside of the #ad tag. 

If `ad` is passed in as the tag genre, it will search by the paid promotion method. 

# Methods 


`related_tags_search_by_likes(tag, num_likes)`

 * Searches a genre of 8 hashtags and all related hashtags. There are roughly 10 related hashtags per tag. 
 * Visits the top 9 photos per hastag. 
 * Returns any array of users who posted top tagged posts with a minimum specified number of likes. 
 * Use `num_likes` to specify the minimum number of likes you want each user's post. Should be around 1000 in order to get quality posts which meet the minumum number of likes. 


 `related_tags_search_paid_promo(tag)`

 * Searches the #ad hashtag for posts with have `paid promotion` labelled. 
 * Visits 1024 photos. 
 * Returns an array of users who post have the `paid promotion` label. 


# Output 

A `.csv` file for each tag searched. The naming convention is `date-tag.csv`. 


# Debug 

Sometimes the headless chromedriver doesn't quit properly. Call `killall chromedriver.exe` to close all chromedriver instances. 