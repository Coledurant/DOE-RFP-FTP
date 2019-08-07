from classes import RSSParser

def sort_rss_parse(rss_parser_class, sort_by_dict):

    rss_dict = rss_parser_class.parse()

    valid_rss_items = []


    for rss_item in rss_dict:

        bool_dict = []

        for sort_by_tag, sort_by_value in sort_by_dict.items():

            try:

                if sort_by_value in rss_item.get(sort_by_tag):

                    bool_dict.append(True)
                else:
                    bool_dict.append(False)

            except TypeError:
                bool_dict.append(False)

        if False not in bool_dict:
            valid_rss_items.append(rss_item)

    return valid_rss_items
