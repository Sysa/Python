import urllib.request
import bs4



url = ("http://m-sestra.ru/books/item/f00/s00/z0000018/st180.shtml")
#opening page
page = urllib.request.urlopen(url)
#prettifying to text
content = bs4.BeautifulSoup(page, "lxml")
#making as string to operate with wildcards
content = str(content)
cutted = content.partition('<!--chapter_begin-->')[2].partition('<!--chapter_end-->')[0]

#adding full path to pics:
substr = "pic"
insertURL = "http://m-sestra.ru/books/item/f00/s00/z0000018/"
#cut and insert urls
idx = cutted.index(substr)
cutted = cutted[:idx] + insertURL + cutted[idx:]
#output result
print(cutted)

