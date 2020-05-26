
def get_embed_from_url(url):
    import re

    # Youtube
    youtubeRegex = r"""
        ^(?:https?://)?                        
        (?:www\.)?                              
        (?:youtube\.com/watch\?v=|youtu\.be/|youtube.com/embed/)
        ([-_A-Za-z0-9]{10}[AEIMQUYcgkosw048])                             
    """
    ytm = re.search(youtubeRegex, url, re.VERBOSE)
    if ytm is not None:
        return {
            "provider": "youtube",
            "contentType": "video",
            "contentID": ytm.group(1)
        }

    # Twitter
    tweetRegex = r"""
        (?:twitter\.com)\/
        (?:.*)\/
        (?:status(?:es)?)\/
        ([^\/\?]+)
    """
    twt = re.search(tweetRegex, url, re.VERBOSE)
    if twt is not None:
        return {
            "provider": "twitter",
            "contentType": "tweet",
            "contentID": twt.group(1)
        }

    # Twitter
    twitterProfileRegex = r"""
        (?:twitter\.com)\/
        (.*)
    """
    twt = re.search(twitterProfileRegex, url, re.VERBOSE)
    if twt is not None:
        return {
            "provider": "twitter",
            "contentType": "profile",
            "contentID": twt.group(1)
        }

    # Instagram
    instagramRegex = r"""
        (?:https?:\/\/www\.)?instagram\.com\/p\/(\w+)\/?
    """
    instaPost = re.search(instagramRegex, url, re.VERBOSE)
    if instaPost is not None:
        return {
            "provider": "instagram",
            "contentType": "post",
            "contentID": instaPost.group(1)
        }

    return None
