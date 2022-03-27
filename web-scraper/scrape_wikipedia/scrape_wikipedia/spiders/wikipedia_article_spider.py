import scrapy

parent_node = 'test'

class WikipediaSpider(scrapy.Spider):
    name = "wikipedia_page"
    start_urls = [
        'https://en.wikipedia.org/wiki/Astrobiology'
    ]
    download_delay = 1

    def parse(self, response):
        #Get everything in the content section of the article
        content = response.css('#content')
        for element in content.css('a, h2'): #Get all links and h2 elements
            if element.css('h2'):
                #If the spider has reached the first h2 element
                #we have finished crawlind the introduction section
                break
            if element.css('a::attr(href)').get() is None: #If there is no link, skip
                continue
            node_link = None
            link_href = element.css('a::attr(href)').get() #Get the href attribute of the link
            if link_href[0] == '#':
                #This skips links to sections in this same page
                continue
            elif link_href[0:5] == 'File:' or link_href.split('/')[2][0:5] == 'File:':
                #This skips linked files
                continue
            elif link_href.split('/')[1] != 'wiki':
                #Skip all external links
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
                node_link = 'https://en.wikipedia.org/wiki/' + relative_address
                yield {
                    #Yield this list with the node name and direct address
                    'list': [node_name, node_link]
                }
            elif link_href.split('/')[2][0:8] == 'Timeline':
                #This handles all the timelines
                continue #Skipping this for now, need to determine how to parse timelines, if at all
                relative_address = link_href.split('/')[2]
                node_name = ''
                #Clean up the relative address to get a meaningful and machine readable name for the node
                #This removes the words "Timeline_of" from the relative address
                for i, s in enumerate(relative_address.split('_')[2:len(relative_address)]):
                    if i != 0:
                        node_name += '_'
                    node_name += s
                node_link = 'https://en.wikipedia.org/wiki/' + relative_address
                yield {
                    #Yield this list with the node name and direct address
                    'timeline': [node_name, node_link]
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
                node_link = 'https://en.wikipedia.org/wiki/' + relative_address
                yield {
                    #Yield this list with the node name and direct address
                    'outline': [node_name, node_link]
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
                relative_address = link_href.split('/')[2]
                if '#' in relative_address: #If there is an in-page reference in the link, the node name is the maing page only
                    node_name = relative_address.split('#')[0]
                else: #Else the relative address is the node name (no need to clean it up)
                    node_name = relative_address
                node_link = 'https://en.wikipedia.org/wiki/' + relative_address
                yield {
                    #Yield this list with the node name and direct address
                    'article': [node_name, node_link, (parent_node, 1, node_name)]
                }
            #if node_link is not None:
            #    yield scrapy.Request(node_link, callback=self.parseSecondary, cb_kwargs=dict(parent_node=node_name))