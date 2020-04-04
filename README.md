# social-media-scraper
scrape scrape scrape

Chromedriver is for Chrome version 80. Update as needed. 

# How to use

`pip install selenium`

`python ./selenium_driver.py`


# Methods 


`related_tags_search_by_likes(tag, pics_per_tag, num_likes)`

 * Searches hashtags and all related hashtags. 
 * Returns any array of users who posted top tagged posts with a minimum specified number of likes. 
 * Use `pics_per_tag` to specify how many users per tag to collect. 
 * Use `num_likes` to specify the minimum number of likes you want each user's post. Should be around 9 in order to get quality posts which meet the minumum number of likes. 

 `related_tags_search_paid_promo(tag, pics_per_tag)`

 * Searches hashtags and all related hashtags. 
 * Returns any array of users who specify their post is a paid promotion. 
 * Use `pics_per_tag` to specify how many users per tag to collect. Should be a higher number because there are not that many paid promotions per tag. 
