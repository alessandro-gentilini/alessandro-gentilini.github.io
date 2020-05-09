import csv
from webpreview import web_preview
from webpreview import OpenGraph

lines = []
with open('ritagli.MD') as ritagli:
     lines = ritagli.readlines()

md = []
with open('ritagli.csv') as csvfile:
    reader = csv.reader(csvfile)
    # skip header
    next(reader, None)
    for row in reader:
        id = "<!--"+str(row)+"-->\n"
        if id in lines:
            continue
        md.append(id)
        og = OpenGraph(row[1],['article:author','article:published_time'])
        if og.published_time:
            md.append('On '+og.published_time+'\n')
        title,desc,img = web_preview(row[1])
        md.append('[**'+title+'**]('+row[1]+')\n')
        md.append(desc+'\n')
        if img:
            md.append("\n<img alt='"+title+"' src='"+img+"' width='400'>")
        md.append('\n')

with open("ritagli.MD", "w") as ritagli:
    for r in lines:
        ritagli.write(r)    
    for r in md:
        ritagli.write(r)
