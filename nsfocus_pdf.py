# -*- coding:utf-8 -*-

import re
import os
import time
import urllib2

from multiprocessing import Pool

__author__ = 'JiangHE'

"""
Get qyjs and zjsj pdf from NSFOCUS
"""


# Create time   : 2016-06-02 14:26:04
# Last modified : 2016-06-06 19:44:27
#########################################################

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def mkdir(rpath):
    """
    mkdir to save files
    """
    rpath = rpath.strip()
    is_dir_exists = os.path.exists(rpath)
    if is_dir_exists is False:
        os.makedirs(rpath)


class NsPDF(object):
    """
    num:        number of items have download
    firstPage:  the first page number(default 1)
    curPage:    the current page number(increase 1 everytime)
    totalPage:  number of total pages(3)
    totalFiles: number of total item(41)
    outOfRange: if curPage>totalPage
    paths:      directory to save files
    user_agent: to construct headers
    headers:    need in http Request header
    baseUrl:    http://www.nsfocus.com.cn
    htmlExt:    string .html
    option:     1 for qyjs, others for zjsj
    subUrl:     one of item below decide by option
    subUrl_qyjs:    /research/qyjs
    subUrl_zjsj:    /research/down
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
        self.referer = 'http://www.nsfocus.com.cn'
        self.headers = {'User-Agent': self.user_agent, 'Referer': self.referer}
        self.baseUrl = 'http://www.nsfocus.com.cn'
        self.subUrl_qyjs = '/research/qyjs'
        self.subUrl_zjsj = '/research/down'
        self.htmlExt = '.html'
        if option == 1:
            self.subUrl = self.subUrl_qyjs
        else:
            self.subUrl = self.subUrl_zjsj

    def fetch_html(self):
        """
        :return: html source of current page
        """
        if self.curPage == self.firstPage:
            page_url = self.baseUrl + self.subUrl + self.htmlExt
        else:
            page_url = self.baseUrl + self.subUrl + '_' + str(self.curPage) + self.htmlExt
        self.curPage += 1
        self.referer = page_url
        self.headers = {'User-Agent': self.user_agent, 'Referer': self.referer}
        """
        use print() if there is only one item to print
        """
        print('\nRequest from %s...' % page_url)
        try:
            request = urllib2.Request(page_url, headers=self.headers)
            response = urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            if hasattr(e, 'code'):
                print(e.code)
            if hasattr(e, 'reason'):
                print(e.reason)
            return None
        except urllib2.URLError as e:
            if hasattr(e, 'code'):
                print(e.code)
            if hasattr(e, 'reason'):
                print(e.reason)
            return None
        else:
            return response.read().decode('utf-8')

    def get_total_num(self):
        """
        get total page number and item number (from the bottom of page)
        """
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
        """
        :param html: html source
        :return: resource urls and  their titles
        """
        pattern_title = '<li>.*?<a\s*title="(.*?)"\s*target.*?href="(.*?)">'
        pattern = re.compile(pattern_title, re.S)
        title_url_pairs = re.findall(pattern, html)
        print 'Page', str(self.curPage - 1), 'has', str(len(title_url_pairs)), 'pdf files.'
        if title_url_pairs is not None:
            print title_url_pairs
            return title_url_pairs
        else:
            return None

    def filter_resource_urls_2(self, html):
        """
        :param html: html source
        :return: resource urls and their titles(containing data)
        """
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
        """
        :param title_url_pair: resource url and it's title
        """
        filename = self.paths + '/' + title_url_pair[0] + '.pdf'
        url = self.baseUrl + title_url_pair[1][2:]
        # print isinstance(title_url_pair[0], unicode)
        # print sys.getdefaultencoding()
        # print repr(title_url_pair[0])
        # print title_url_pair[0].decode('utf-8').encode('utf-8')
        print str(title_url_pair[0].encode('utf-8')) + '.pdf'
        try:
            pdf = urllib2.urlopen(url)
        except urllib2.URLError as e:
            if hasattr(e, 'code'):
                print(e.code)
            if hasattr(e, 'reason'):
                print(e.reason)
        except IOError as e:
            if hasattr(e, 'code'):
                print(e.code)
            if hasattr(e, 'reason'):
                print(e.reason)
        else:
            self.num += 1
            data = pdf.read()
            with open(filename, 'wb') as f:
                f.write(data)

    def get_pdf_one_by_one(self, num):
        """
        :param num: number of items(on a single page) excepted to download
        """
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
        """
        download pdf files on a single page
        """
        html_content = self.fetch_html()
        if html_content is not None:
            title_url_pairs = self.filter_resource_urls(html_content)
            if title_url_pairs is not None:
                print('Downloading there pdf files...')
                [self.save_pdf(pair) for pair in title_url_pairs]
                print 'Spider has download', str(self.num), 'pdf files.'
            if self.curPage - 1 == self.totalPage:
                if self.num != self.totalFiles:
                    print('\nThere are %d file cannot download' % (self.totalFiles - self.num))
                    # else:
                    #     self.outOfRange = True
                    #     print 'Out of Page Range!'

    def get_pdf_use_multiprocess(self):
        """
        use multiprocess to divide out work simultaneously
        """
        html_content = self.fetch_html()
        if html_content is not None:
            title_url_pairs = self.filter_resource_urls(html_content)
            if title_url_pairs is not None:
                pool = Pool()
                pool.map(self.save_pdf, title_url_pairs)


if __name__ == '__main__':
    agent = 'Mozilla/4.5'
    # agent = ''
    """
    Download qyjs
    """
    # path = 'D:\\Hij\\Desktop\\NS_QYJS'
    # spider = NsPDF(path, agent)

    """
    Download zjsj
    """
    path = 'D:\\Hij\\Desktop\\NS_ZJSJ'
    spider = NsPDF(path, agent, 0)

    mkdir(spider.paths)

    start_time = time.time()

    # 3 method to download files
    #########################################################
    """
    Download files one by one
    """
    # spider.get_pdf_one_by_one(2)

    # while spider.outOfRange is False:
    # 	spider.get_pdf_by_page()

    """
    Download files on the first page
    """
    spider.get_pdf_by_page()
    # spider.get_pdf_use_multiprocess()

    """
    Download all the files
    """
    # if spider.get_total_num() is True:
    #     while spider.curPage <= spider.totalPage:
    #         spider.get_pdf_by_page()
    # else:
    #     print 'Can not get response from server, Check Network Connection...'
    #########################################################

    end_time = time.time()
    print('\nIt spends %.2f seconds.' % (end_time - start_time))
