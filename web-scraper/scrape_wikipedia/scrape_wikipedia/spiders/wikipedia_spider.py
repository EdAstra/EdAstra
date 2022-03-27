import scrapy

def handleListLinks(link_href):
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
        return node_name, node_link
        
def handleTimelineLinks(link_href):
    #This handles all the timelines
    relative_address = link_href.split('/')[2]
    node_name = ''
    #Clean up the relative address to get a meaningful and machine readable name for the node
    #This removes the words "Timeline_of" from the relative address
    for i, s in enumerate(relative_address.split('_')[2:len(relative_address)]):
        if i != 0:
            node_name += '_'
        node_name += s
    node_link = 'https://en.wikipedia.org/wiki/' + relative_address
    return node_name, node_link

def handleOutlineLinks(link_href):
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
    return node_name, node_link

def handleArticleLinks(link_href):
    #This handles all the articles
    relative_address = link_href.split('/')[2]
    if '#' in relative_address: #If there is an in-page reference in the link, the node name is the maing page only
        node_name = relative_address.split('#')[0]
    else: #Else the relative address is the node name (no need to clean it up)
        node_name = relative_address
    node_link = 'https://en.wikipedia.org/wiki/' + relative_address
    return node_name, node_link

def getNodeFromLink(link_href, parent_node):
    link_type = None
    node_link = None
    node_name = None

    if link_href[0] == '#':
        #This skips links to sections in this same page
        pass
    elif link_href[0:5] == 'File:' or link_href.split('/')[2][0:4] == 'File':
        #This skips linked files in this page
        pass
    elif link_href.split('/')[1] != 'wiki':
        #This skips external links
        pass
    elif link_href.split('/')[2][0:8] == 'Category' or link_href.split('/')[2][0:6] == 'Portal':
        #Skipping Categories and Portals
        #Though this information can be useful, it seems there
        #...is quite a great deal of redundancy between categories/portals, and outlines
        #...(NEEDSCONFIRMATION): There is little point of including these since we already
        #........................are using the outlines
        pass
    elif link_href.split('/')[2][0:8] == 'Template' or link_href.split('/')[2][0:9] == 'Wikipedia':
        #Template links are for Wikipedia editing purposes
        #Links starting with Wikipedia are Top-level contents, outlines, etc.
        pass
    elif link_href.split('/')[2][0:7] == 'Special':
        #Special links have to do mostly with project maintenance
        #https://en.wikipedia.org/wiki/Help:Special_page
        pass
    elif link_href.split('/')[2][0:4] == 'List':
        pass #Skipping this for now, need to determine how to parse lists, if at all
        #link_type = 'list'
        #node_name, node_link = handleListLinks(link_href)
        #yield {
            #Yield this list with the node name and direct address
        #    'list': [node_name, node_link, (parent_node, 1, node_name)]
        #}
    elif link_href.split('/')[2][0:8] == 'Timeline':
        pass #Skipping this for now, need to determine how to parse timelines, if at all
        #link_type = 'timeline'
        #node_name, node_link = handleTimelineLinks(link_href)
        #yield {
            #Yield this list with the node name and direct address
        #    'timeline': [node_name, node_link, (parent_node, 1, node_name)]
        #}
    elif link_href.split('/')[2][0:7] == 'Outline':
        link_type = 'outline'
        node_name, node_link = handleOutlineLinks(link_href)
    else:
        link_type = 'article'
        node_name, node_link = handleArticleLinks(link_href)

    return link_type, node_name, node_link


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    start_urls = [
        'https://en.wikipedia.org/wiki/Wikipedia:Contents/Outlines'
    ]
    download_delay = 1

    def getNextRequest(self, link_type, node_name, node_link):
        if link_type == 'article':
            return scrapy.Request(node_link, callback=self.parseArticle, cb_kwargs=dict(parent_node=node_name))
        else:
            return scrapy.Request(node_link, callback=self.parseOutline, cb_kwargs=dict(parent_node=node_name))

    def parse(self, response):
        #Get all the links in the contents of this page
        for link in response.css('.contentsPage__section a'):
            if link.css('a::attr(href)').get() is None: #If there is no link, skip
                continue

            link_type = None
            node_link = None
            node_name = None

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
                continue #Skipping this for now, need to determine how to parse Lists, if at all
                link_type = 'list'
                node_name, node_link = handleListLinks(link_href)
                yield {
                    'list': [node_name, node_link]
                }
            elif link_href.split('/')[2][0:8] == 'Timeline':
                continue #Skipping this for now, need to determine how to parse timelines, if at all
                link_type = 'timeline'
                node_name, node_link = handleTimelineLinks(link_href)
                yield {
                    'timeline': [node_name, node_link]
                }
            elif link_href.split('/')[2][0:7] == 'Outline':
                link_type = 'outline'
                node_name, node_link = handleOutlineLinks(link_href)
                yield {
                    'outline': [node_name, node_link]
                }
            else:
                link_type = 'article'
                node_name, node_link = handleArticleLinks(link_href)
                yield {
                    'article': [node_name, node_link]
                }

            if link_type != None:
                yield self.getNextRequest(link_type, node_name, node_link)
            

    def parseOutline(self, response, parent_node):
        #Get all the links in the contents of this page
        for link in response.css('#mw-content-text a'):
            if link.css('a::attr(href)').get() is None: #If there is no link, skip
                continue

            link_href = link.css('a::attr(href)').get() #Get the href attribute of the link
            link_type, node_name, node_link = getNodeFromLink(link_href, parent_node)
            
            if link_type is not None:
                yield {
                    '{}'.format(link_type): [node_name, node_link, (parent_node, 1, node_name)]
                }
                yield self.getNextRequest(link_type, node_name, node_link)

    def parseArticle(self, response, parent_node):
        #Get everything in the content section of the article
        content = response.css('#content')
        for element in content.css('a, h2'): #Get all links and h2 elements
            if element.css('h2'):
                #If the spider has reached the first h2 element
                #we have finished crawlind the introduction section
                break
            link = element
            if link.css('a::attr(href)').get() is None: #If there is no link, skip
                continue

            link_href = link.css('a::attr(href)').get() #Get the href attribute of the link
            link_type, node_name, node_link = getNodeFromLink(link_href, parent_node)
            
            if link_type is not None:
                yield {
                    '{}'.format(link_type): [node_name, node_link, (parent_node, 1, node_name)]
                }
                yield self.getNextRequest(link_type, node_name, node_link)
