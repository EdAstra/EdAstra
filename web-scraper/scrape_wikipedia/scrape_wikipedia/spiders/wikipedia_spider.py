import scrapy

class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    start_urls = [
        'https://en.wikipedia.org/wiki/Wikipedia:Contents/Outlines'
    ]
    download_delay = 5

    def parse(self, response):
        #Get all the links in the contents of this page
        for link in response.css('.contentsPage__section a'):
            if link.css('a::attr(href)').get() is None: #If there is no link, skip
                continue
            node_link = None
            link_href = link.css('a::attr(href)').get() #Get the href attribute of the link
            if '#' in link_href:
                #This skips links to sections in this same page
                continue
            elif link_href[0:5] == 'File:':
                #This skips linked files in this page
                #This mostly (entirely?) consists of map image files in the Geography section
                continue
            elif link_href.split('/')[1] != 'wiki':
                #There are currently no pages on the contents/outline page that meet this criteria
                #But this is still here to help handle errors if such pages are introduced in the future
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
            else:
                #The only thing left is direct links to pages
                #We skip these here as they will be handled within the lower level outlines
                #This code is just a placeholder in case this becomes useful in the future
                pass
            if node_link is not None:
                yield scrapy.Request(node_link, callback=self.parseSecondary, cb_kwargs=dict(parent_node=node_name))


    def parseSecondary(self, response, parent_node):
        #Get all the links in the contents of this page
        for link in response.css('#mw-content-text a'):
            if link.css('a::attr(href)').get() is None: #If there is no link, skip
                continue
            node_link = None
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
                    'list': [node_name, node_link, (parent_node, 1, node_name)]
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
                    'timeline': [node_name, node_link, (parent_node, 1, node_name)]
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
                    'outline': [node_name, node_link, (parent_node, 1, node_name)]
                }
            else:
                #This handles all the rest of the links
                #These should all be articles
                #In this case, the relative address is the node name (no need to clean it up)
                relative_address = link_href.split('/')[2]
                node_name = relative_address
                node_link = 'https://en.wikipedia.org/wiki/' + relative_address
                yield {
                    #Yield this list with the node name and direct address
                    'article': [node_name, node_link, (parent_node, 1, node_name)]
                }

    def parsePage(self, response, parent_node):
        #Get all the links in the contents of this page
        for link in response.css('#mw-content-text a'):
            if link.css('a::attr(href)').get() is None: #If there is no link, skip
                continue
            node_link = None
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
                    'list': [node_name, node_link, (parent_node, 1, node_name)]
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
                    'timeline': [node_name, node_link, (parent_node, 1, node_name)]
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
                    'outline': [node_name, node_link, (parent_node, 1, node_name)]
                }
            else:
                #This handles all the rest of the links
                #These should all be articles
                #In this case, the relative address is the node name (no need to clean it up)
                relative_address = link_href.split('/')[2]
                node_name = relative_address
                node_link = 'https://en.wikipedia.org/wiki/' + relative_address
                yield {
                    #Yield this list with the node name and direct address
                    'article': [node_name, node_link, (parent_node, 1, node_name)]
                }
