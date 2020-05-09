import csv
from webpreview import web_preview
from webpreview import OpenGraph

md = []
with open('ritagli.csv') as csvfile:
    reader = csv.reader(csvfile)
    # skip header
    next(reader, None)
    for row in reader:
        md.append('<!--'+str(row)+'-->')
        og = OpenGraph(row[1],['article:author','article:published_time'])
        if og.published_time:
            md.append('On '+og.published_time)
        title,desc,img = web_preview(row[1])
        md.append('**'+title+'**')
        md.append(desc)
        if img:
            md.append("<img alt='"+title+"' src='"+img+"'</img>")

with open("ritagli.MD", "w") as ritagli:
    for r in md:
        ritagli.write(r+'\n')