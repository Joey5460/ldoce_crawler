#!/usr/bin/python
# -*- coding: utf-8 -*-
import mechanize
import cookielib
from bs4 import BeautifulSoup
import re

#Browser
br = mechanize.Browser()

#Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# Want debugging messages?
#br.set_debug_http(True)
#br.set_debug_redirects(True)
#br.set_debug_responses(True)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc25 Firefox/3.0.1')]
def get_urls(alpha):
    basic_url = 'http://www.ldoceonline.com/browse/english/'
    filename=alpha+".url"
    idx_url = basic_url + alpha +'/'
    r = br.open(idx_url)
    html = r.read()
    #print html
    #print br.response().read()
    soup = BeautifulSoup(html, "html5lib")
    innerDiv = soup.find(attrs={'class': "page_content"})
    links = innerDiv.find_all("a", href=re.compile("^http"))
    for link in links:
	if link.find("span"):
	    #print link
	    sublink = link['href']
	    r = br.open(sublink)
	    html = r.read()
	    soup = BeautifulSoup(html, "html5lib")
	    inner_ul = soup.find(attrs={'class': "browse_results"})
	    word_links = inner_ul.find_all("a", href=re.compile("^http"))
	    with open (filename,'a') as fd_url:
		for link in word_links:
		    #text=link.find("span")
		    #print text.string.encode('utf-8').strip()
		    print>>fd_url, link['href']

def url_filtering(filename):
    with open (filename,'r') as fd:
	ln = filename.split('.')
        fn_filed = ln[0]+'_filtered.url'
	with open (fn_filed,'w') as fd_filed:
	    for ln in fd:
		obj = re.match(r'(.*)[-](.*)', ln)
		if not obj:
		    #without newline
		    print>>fd_filed, ln[:-1]

def get_vocabulary(filename):
    with open(filename) as fd:
        for ln in fd:
            print ln
            r = br.open(ln)
            html = r.read()
            soup = BeautifulSoup(html, "html5lib")
            pagetitle=soup.find(attrs={'class':"pagetitle"})
            
            dictlinks=soup.find_all(attrs={'class':"dictlink"})
            for dictlink in dictlinks:
		freq_hd = dictlink.find(attrs={'class':"frequent Head"})

                if freq_hd:
		    word_level = freq_hd.find(attrs={'class': "tooltip LEVEL"})
		    word_freq = freq_hd.find_all(attrs={'class': "FREQ"})
		    
		    #print word_level['title'], word_level.string
		    word_property=[pagetitle.string]
		    if word_level:
			word_property.append(word_level['title'])
			word_property.append(word_level.string)

		    if word_freq:
			for v in word_freq:
			    word_property.append(v.string)

		    if len(word_property)>1:
			#print '[%s]' % ', '.join(map(encode('utf-8'), word_property))
			poses =  freq_hd.find_all(attrs={'class':"POS"})
			if poses:
			    for pos in poses:
				word_property.append(pos.get_text())
			with open("core_vocabulary.lm", 'a') as fd_cv:        
                            print>>fd_cv, ' '.join(p.encode('utf-8').strip() for p in word_property) 

if __name__ == '__main__':
    alphabet=['r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for alpha in alphabet:
	get_urls(alpha)
	url_filtering(alpha+'.url')
	get_vocabulary(alpha+'_filtered.url')
