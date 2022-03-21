import scrapy

class WikipediaListSpider(scrapy.Spider):
    name = "wikipedia_list"
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_wars_of_independence'
    ]

    def parse(self, response):
        #Get all the links in the contents of this page
        for link in response.css('#mw-content-text a'):
            if link.css('a::attr(href)').get() == None:
                continue
            link_href = link.css('a::attr(href)').get() #Get the href attribute of the link
            if '#' in link_href:
                #This skips links to sections in this same page
                continue
            elif link_href[0:5] == 'File:' or link_href.split('/')[2][0:4] == 'File':
                #This skips linked files in this page
                continue
            elif link_href.split('/')[1] != 'wiki':
                #This skips external links
                continue
            elif link_href.split('/')[2][0:4] == 'List':
                #This handles all the lists
                relative_address = link_href.split('/')[2]
                node_name = ''
                #Clean up the relative address to get a meaningful and machine readable name for the node
                #This removes the words "Lists_of" from the relative address
                #Also removes the word "topic" or "topics" which is at the end of a few of the addresses
                for i, s in enumerate(relative_address.split('_')[2:len(relative_address)]):
                    if 'topic' in s:
                        continue
                    if i != 0:
                        node_name += '_'
                    node_name += s
                yield {
                    #Yield this list with the node name and direct address
                    'list': [node_name, 'https://en.wikipedia.org/wiki/' + relative_address]
                }
            elif link_href.split('/')[2][0:8] == 'Timeline':
                #This handles all the timelines
                relative_address = link_href.split('/')[2]
                node_name = ''
                #Clean up the relative address to get a meaningful and machine readable name for the node
                #This removes the words "Timeline_of" from the relative address
                for i, s in enumerate(relative_address.split('_')[2:len(relative_address)]):
                    if i != 0:
                        node_name += '_'
                    node_name += s
                yield {
                    #Yield this list with the node name and direct address
                    'timeline': [node_name, 'https://en.wikipedia.org/wiki/' + relative_address]
                }
            elif link_href.split('/')[2][0:7] == 'Outline':
                #This handles all the outlines
                relative_address = link_href.split('/')[2]
                node_name = ''
                #Clean up the relative address to get a meaningful and machine readable name for the node
                #This removes the words "Outline_of" from the relative address
                for i, s in enumerate(relative_address.split('_')[2:len(relative_address)]):
                    if i != 0:
                        node_name += '_'
                    node_name += s
                yield {
                    #Yield this list with the node name and direct address
                    'outline': [node_name, 'https://en.wikipedia.org/wiki/' + relative_address]
                }
            elif link_href.split('/')[2][0:8] == 'Category' or link_href.split('/')[2][0:6] == 'Portal':
                #Skipping Categories and Portals
                #Though this information can be useful, it seems there
                #...is quite a great deal of redundancy between categories/portals, and outlines
                #...(NEEDSCONFIRMATION): There is little point of including these since we already
                #........................are using the outlines
                continue
            elif link_href.split('/')[2][0:8] == 'Template' or link_href.split('/')[2][0:9] == 'Wikipedia':
            	#Template links are for Wikipedia editing purposes
            	#Links starting with Wikipedia are Top-level contents, outlines, etc.
            	continue
            else:
                #This handles all the rest of the links
                #These should all be articles
                #In this case, the relative address is the node name (no need to clean it up)
                relative_address = link_href.split('/')[2]
                node_name = relative_address
                yield {
                    #Yield this list with the node name and direct address
                    'article': [node_name, 'https://en.wikipedia.org/wiki/' + relative_address]
                }