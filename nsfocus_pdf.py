import re
import os
# import sys
import time
import urllib2

# -*- coding:utf-8 -*-

__author__ = 'JiangHE'

"""
Get qyjs and zjsj pdf from NSFOCUS
"""


# Create time   : 2016-06-02 14:26:04
# Last modified : 2016-06-02 23:29:00
#########################################################

# reload(sys)
# sys.setdefaultencoding('utf-8')


def mkdir(rpath):
    rpath = rpath.strip()
    is_dir_exists = os.path.exists(rpath)
    if is_dir_exists is False:
        os.makedirs(rpath)


class NsPDF(object):
    """
    option: 1 for qyjs, others for zjsj
    """

    def __init__(self, paths, user_agent, option=1):
        self.num = 0
        self.firstPage = 1
        self.curPage = self.firstPage
        self.totalPage = 0
        self.totalFiles = 0
        self.outOfRange = False
        self.paths = paths
        self.user_agent = user_agent
        self.headers = {'User-Agent': self.user_agent}
        self.baseUrl = 'http://www.nsfocus.com.cn'
        self.subUrl_qyjs = '/research/qyjs'
        self.subUrl_zjsj = '/research/down'
        self.htmlExt = '.html'
        if option == 1:
            self.subUrl = self.subUrl_qyjs
        else:
            self.subUrl = self.subUrl_zjsj

    def fetch_html(self):
        if self.curPage == self.firstPage:
            page_url = self.baseUrl + self.subUrl + self.htmlExt
        else:
            page_url = self.baseUrl + self.subUrl + '_' + str(self.curPage) + self.htmlExt
        self.curPage += 1
        print '\nRequest from %s...' % page_url
        try:
            request = urllib2.Request(page_url, headers=self.headers)
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            if hasattr(e, 'code'):
                print e.code,
            if hasattr(e, 'reason'):
                print e.reason
            return None
        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                print e.code,
            if hasattr(e, 'reason'):
                print e.reason
            return None
        else:
            return response.read().decode('utf-8')

    def get_total_num(self):
        html = spider.fetch_html()
        self.curPage -= 1
        """
        If the network is not connect,
        html is not None, but not the response from server,
        pages_pattern can not find
        """
        if html is not None:
            pages_pattern = re.compile('<span\s*class="arial\s*color">(.*?)</span>')
            pages = re.findall(pages_pattern, html)
            if pages is not None:
                page_num = pages[0].split('/')
                self.totalPage = int(page_num.pop())
                self.totalFiles = int(pages[1])
                return True
            else:
                return False

    def filter_resource_urls(self, html):
        title_pattern = re.compile('<a\s*title="(.*?)"\s*target')
        url_pattern = re.compile('<a\s*title.*?target.*?href="(.*?)">')
        titles = re.findall(title_pattern, html)
        urls = re.findall(url_pattern, html)
        print 'Page', str(self.curPage - 1), 'has', str(len(urls)), 'pdf files.'
        if len(titles) == len(urls) and titles is not None:
            title_url_pairs = zip(titles, urls)
            return title_url_pairs
        else:
            return None

    def filter_resource_urls_2(self, html):
        date_pattern = re.compile('<span>(\d{4}-\d{2}-\d{2})</span>')
        title_pattern = re.compile('<a\s*title="(.*?)"\s*target')
        url_pattern = re.compile('<a\s*title.*?target.*?href="(.*?)">')
        dates = re.findall(date_pattern, html)
        titles = re.findall(title_pattern, html)
        urls = re.findall(url_pattern, html)
        # filenames = [ date + '-' + title for date in dates for title in titles]
        print 'Page', str(self.curPage - 1), 'has', str(len(urls)), 'pdf files.'
        if len(titles) == len(urls) == len(dates) and titles is not None:
            files = zip(dates, titles)
            filenames = [files[i][0] + '-' + files[i][1] for i in range(len(files))]
            title_url_pairs = zip(filenames, urls)
            return title_url_pairs
        else:
            return None

    """
    def set_filename_and_valid_url(self, title_url_pair):
        url = self.baseUrl + title_url_pair[1][2:]
        filename = self.path + '/' + title_url_pair[0] + '.pdf'
        return url, filename
    """

    def save_pdf(self, title_url_pair):
        filename = self.paths + '/' + title_url_pair[0] + '.pdf'
        url = self.baseUrl + title_url_pair[1][2:]
        # print isinstance(title_url_pair[0], unicode)
        # print sys.getdefaultencoding()
        # print repr(title_url_pair[0])
        # print title_url_pair[0].decode('utf-8').encode('utf-8')
        print str(title_url_pair[0].encode('utf-8')) + '.pdf'
        try:
            pdf = urllib2.urlopen(url)
        except urllib2.URLError, e:
            if hasattr(e, 'code'):
                print e.code,
            if hasattr(e, 'reason'):
                print e.reason
        except IOError, e:
            if hasattr(e, 'code'):
                print e.code,
            if hasattr(e, 'reason'):
                print e.reason
        else:
            self.num += 1
            data = pdf.read()
            with open(filename, 'wb') as f:
                f.write(data)

    def get_pdf_one_by_one(self, num):
        html_content = self.fetch_html()
        if html_content is not None:
            title_url_pairs = self.filter_resource_urls(html_content)
            if title_url_pairs is not None:
                if num > len(title_url_pairs):
                    num = len(title_url_pairs)
                for i in range(num):
                    self.save_pdf(title_url_pairs[i])
                print 'Spider has downloaded', str(self.num), 'pdf files.'

    def get_pdf_by_page(self):
        html_content = self.fetch_html()
        if html_content is not None:
            title_url_pairs = self.filter_resource_urls(html_content)
            if title_url_pairs is not None:
                print 'Downloading there pdf files...'
                [self.save_pdf(pair) for pair in title_url_pairs]
                print 'Spider has download', str(self.num), 'pdf files.'
            if self.curPage - 1 == self.totalPage:
                if self.num != self.totalFiles:
                    print '\nThere are %d file cannot download' % (self.totalFiles - self.num)
                    # else:
                    # 	self.outOfRange = True
                    # 	print 'Out of Page Range!'


if __name__ == '__main__':
    agent = 'Mozilla/4.5'
    # agent = ''
    """
    Download qyjs
    """
    # path = '\\NS_QYJS'
    # spider = NsPDF(path, agent)

    """
    Download zjsj
    """
    path = '.\\NS_ZJSJ'
    spider = NsPDF(path, agent, 0)

    mkdir(spider.paths)

    start_time = time.time()

    """
    Download files one by one
    """
    # spider.get_pdf_one_by_one(2)

    # while spider.outOfRange is False:
    # 	spider.get_pdf_by_page()

    """
    Download files on the first page
    """
    # spider.get_pdf_by_page()

    """
    Download all the files
    """
    if spider.get_total_num() is True:
        while spider.curPage <= spider.totalPage:
            spider.get_pdf_by_page()
    else:
        print 'Can not get response from server, Check Network Connection...'

    end_time = time.time()
    print '\nIt spends %.2f seconds.' % (end_time - start_time)
