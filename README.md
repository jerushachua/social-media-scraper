# social-media-scraper
scrape scrape scrape

Chromedriver is for Chrome version 80. Update as needed. 

# How to use

`pip install selenium`

`python selenium_driver.py username password genre`

Input your instagram `username`, `password`, and `genre` of the tags to search. 

Current supported genres are `gaming`, `food`, `rand`, and `travel`. If no tag genre is specified, it will default to search the #instagram tag. 

# Methods 


`related_tags_search_by_likes(tag, num_likes)`

 * Searches hashtags and all related hashtags. 
 * Visits the top 9 photos per hastag. 
 * Returns any array of users who posted top tagged posts with a minimum specified number of likes. 
 * Use `num_likes` to specify the minimum number of likes you want each user's post. Should be around 1000 in order to get quality posts which meet the minumum number of likes. 


 `related_tags_search_paid_promo(tag)`

 * Searches hashtags and all related hashtags. 
 * Visits 255 photos per hashtag. This is because there aren't likely to be many paid promotion photos per tag. We need to sift through many photos before encoutering a paid promotion. 
 * Returns any array of users who specify their post is a paid promotion. 
