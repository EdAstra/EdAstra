import scrapy

def handleListLinks(link_href):
    #This handles all the lists
    relative_address = link_href.split('/')[2]
    node_name = ''
    #Clean up the relative address to get a meaningful and machine readable name for the node
    #This removes the words "Lists_of" from the relative address
    #Also removes the word "topic" or "topics" which is at the end of a few of the addresses
    if '#' in relative_address: #If there is an in-page reference in the link, the node name is the maing page only
        relative_address = relative_address.split('#')[0]
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
    if '#' in relative_address: #If there is an in-page reference in the link, the node name is the maing page only
        relative_address = relative_address.split('#')[0]
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
    if '#' in relative_address: #If there is an in-page reference in the link, the node name is the maing page only
        relative_address = relative_address.split('#')[0]
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

def getNodeFromLink(link_href):
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
    elif link_href.split('/')[2][0:9] == 'Category:' or link_href.split('/')[2][0:7] == 'Portal:':
        #Skipping Categories and Portals
        #Though this information can be useful, it seems there
        #...is quite a great deal of redundancy between categories/portals, and outlines
        #...(NEEDSCONFIRMATION): There is little point of including these since we already
        #........................are using the outlines
        pass
    elif link_href.split('/')[2][0:9] == 'Template:' or link_href.split('/')[2][0:10] == 'Wikipedia:':
        #Template links are for Wikipedia editing purposes
        #Links starting with Wikipedia are Top-level contents, outlines, etc.
        pass
    elif link_href.split('/')[2][0:8] == 'Special:' or link_href.split('/')[2][0:5] == 'Help:' or link_href.split('/')[2][0:4] == 'ISBN':
        #Special links have to do mostly with project maintenance
        #https://en.wikipedia.org/wiki/Help:Special_page
        #Help pages are...help pages for Wikipedia
        #ISBN links all lead to the same ISBN identifiers page
        #https://en.wikipedia.org/wiki/International_Standard_Book_Number
        pass
    elif link_href.split('/')[2][0:7] == 'List_of' or link_href.split('/')[2][0:8] == 'Lists_of':
        pass #Skipping this for now, need to determine how to parse lists, if at all
        #link_type = 'list'
        #node_name, node_link = handleListLinks(link_href)
    elif link_href.split('/')[2][0:11] == 'Timeline_of':
        pass #Skipping this for now, need to determine how to parse timelines, if at all
        #link_type = 'timeline'
        #node_name, node_link = handleTimelineLinks(link_href)
    elif link_href.split('/')[2][0:10] == 'Outline_of':
        link_type = 'outline'
        node_name, node_link = handleOutlineLinks(link_href)
    else:
        link_type = 'article'
        node_name, node_link = handleArticleLinks(link_href)

    return link_type, node_name, node_link


class WikipediaSpider(scrapy.Spider):
    name = "wikipedia_subset"
    start_urls = [
        'https://en.wikipedia.org/wiki/Outline_of_academic_disciplines'
    ]

    custom_settings = {
        #Autothrottle the spider to avoid overtaxing the Wikipedia servers
        #https://docs.scrapy.org/en/latest/topics/autothrottle.html
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 3,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1
    }

    def getNextRequest(self, link_type, node_name, node_link):
        if link_type == 'article':
            return scrapy.Request(node_link, callback=self.parseArticle, cb_kwargs=dict(parent_node=node_name))
        else:
            return scrapy.Request(node_link, callback=self.parseOutline, cb_kwargs=dict(parent_node=node_name))

    def parse(self, response):
        #Get all the links in the contents of this page
        for link in response.css('#mw-content-text a'):
            if link.css('a::attr(href)').get() is None:
                continue

            link_href = link.css('a::attr(href)').get()

            link_type, node_name, node_link = getNodeFromLink(link_href)

            if link_type != None:
                yield {
                    '{}'.format(link_type): [node_name, node_link]
                }
                yield self.getNextRequest(link_type, node_name, node_link)
            
    def parseOutline(self, response, parent_node):
        #Get all the links in the contents of this page
        for link in response.css('#mw-content-text a'):
            if link.css('a::attr(href)').get() is None:
                continue

            link_href = link.css('a::attr(href)').get()
            link_type, node_name, node_link = getNodeFromLink(link_href)
            
            if link_type is not None:
                yield {
                    '{}'.format(link_type): [node_name, node_link, (parent_node, 1, node_name)]
                }
                yield self.getNextRequest(link_type, node_name, node_link)

    def parseArticle(self, response, parent_node):
        #Get all links and h2 elements in the content section of the article
        for element in response.css('#content a, h2'):
            if element.css('h2'):
                #If the spider has reached the first h2 element
                #we have finished crawlind the introduction section
                break
            link = element
            if link.css('a::attr(href)').get() is None:
                continue

            link_href = link.css('a::attr(href)').get()
            link_type, node_name, node_link = getNodeFromLink(link_href)
            
            if link_type is not None:
                yield {
                    '{}'.format(link_type): [node_name, node_link, (parent_node, 1, node_name)]
                }
                #For now, end at articles, to see the size of the initial data set
                #yield self.getNextRequest(link_type, node_name, node_link)

