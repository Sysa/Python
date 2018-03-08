import urllib.request
import bs4

def main_page_download():
    
    url = ("http://m-sestra.ru/books/item/f00/s00/z0000018/index.shtml")
    #opening page
    page = urllib.request.urlopen(url)
    #prettifying to text
    content = bs4.BeautifulSoup(page, "lxml")
    #making as string to operate with wildcards
    content = str(content)
    cutted = content.partition('google_ad_section_start -->')[2].partition('<!-- Rating@Mail.ru counter')[0]
    with open('book.html', 'a', encoding='utf-8') as the_file:
            the_file.write(cutted)

def book_download(start_page, end_page):
    #000->182
    for page_num in range(start_page, end_page):
        url = ("http://m-sestra.ru/books/item/f00/s00/z0000018/st" + "{0:0>3}".format(page_num) + ".shtml")
        #opening page
        page = urllib.request.urlopen(url)
        #prettifying to text
        content = bs4.BeautifulSoup(page, "lxml")
        #making as string to operate with wildcards
        content = str(content)
        cutted = content.partition('<!--chapter_begin-->')[2].partition('<!--chapter_end-->')[0]

        #adding full path to pics:
        try:
            cutted = cutted.replace("pic","http://m-sestra.ru/books/item/f00/s00/z0000018/pic")
        except Exception as identifier:
            pass
        #save and append the output            
        with open('book.html', 'a', encoding='utf-8') as the_file:
            the_file.write(cutted)

if __name__ == '__main__':
    main_page_download()
    book_download(000, 183)
    #book_download(000, 3)