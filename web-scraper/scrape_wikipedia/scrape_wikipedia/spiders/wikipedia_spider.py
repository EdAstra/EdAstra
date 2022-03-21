import scrapy

class WikipediaSpider(scrapy.Spider):
    name = "wikipedia"
    start_urls = [
        'https://en.wikipedia.org/wiki/Wikipedia:Contents/Outlines'
    ]

    def parse(self, response):
        #Get all the links in the contents of this page
        for link in response.css('.contentsPage__section a'): 
            link_href = link.css('a::attr(href)')[0].get() #Get the href attribute of the link
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
            else:
            	#The only thing left is direct links to pages
            	#We skip these here as they will be handled within the lower level outlines
            	pass
