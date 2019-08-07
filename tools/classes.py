import feedparser
class ConEdisonRFP(object):

    all_rfps = []

    def __init__(self, project_name, current_status, documents = []):

        self.project_name = project_name
        self.current_status = current_status
        self.documents = documents

        ConEdisonRFP.all_rfps.append(self)

    def __str__(self):

        return self.project_name

class ConEdisonDocument(object):

    all_documents = []

    def __init__(self, document_name, url):

        self.document_name = document_name
        self.url = url

        ConEdisonDocument.all_documents.append(self)

    def __str__(self):

        return self.document_name

class DominionRSSItem(object):

    def __init__(self, title, link, description):

        self.title = title
        self.link = link
        self.description = description

class RSSParser(object):

    '''
    Used to parse an RSS feed
    Parameters:
        feed_url (str): A url string for the RSS feed
        parse_items (list): A list of strings for the feed parser to get information on every feed item
                            that the parser returns in the entries key
                            If parse_items is left blank, it will default to None and RSSParser will
                            find all possible parse_items and use those
    '''

    all_parsers = []

    def __init__(self, title, feed_url, parse_items=None):

        self.title = title
        self.feed_url = feed_url
        self.parse_items = parse_items

        RSSParser.all_parsers.append(self)

    def parse(self):

        '''
        Parses RSS feed and returns dicts for every feed item with specified keys
        Parameters:
            self
        Returns:
            feed_item_dict_list (list): A list of dicts for every rss feed item.
                                        Keys are the rss parse 'parse_items'
        '''

        NewsFeed = feedparser.parse(self.feed_url)

        if self.parse_items is None:

            self.parse_items = [parse_item for parse_item in NewsFeed['entries'][0]]


        feed_item_dict_list = []

        for rss_item in NewsFeed['entries']:

            # Dict of every item and its corresponding value in parse_items for the one rss_item
            rss_item_info_dict = {}

            for parse_item in self.parse_items:

                # Adding the parse_item from parse_items as key and the value to feed returned to the dict above
                rss_item_info_dict[parse_item] = rss_item[parse_item]

            # Adding the rss_item dict rss_item_info_dict to the list of all rss_item dicts feed_item_dict_list
            feed_item_dict_list.append(rss_item_info_dict)

        return feed_item_dict_list

    def get_rss_div(self):

        parsed_dict_list = self.parse()

        rss_item_uls = ''

        for rss_item_dict in parsed_dict_list:

            rss_list_items = ''

            for parse_item in self.parse_items:

                parse_item_content = rss_item_dict.get(parse_item)

                parse_item_content_li = '<li class="rss_item">{0}</li>'.format(parse_item_content)

                rss_list_items += parse_item_content_li

            rss_item_list = '<ul class="rss_item_list">{0}</ul>'.format(rss_list_items)

            rss_item_uls += rss_item_list

        rss_div = '<div class="rss_feed">{0}</div>'.format(rss_item_uls)

        return rss_div
