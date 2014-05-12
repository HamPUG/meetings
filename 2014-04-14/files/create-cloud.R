library(tm)
library(wordcloud)
library(RColorBrewer)

txt = Corpus(DirSource("out/"))
txt = tm_map(txt, stripWhitespace)
txt = tm_map(txt, tolower)
txt = tm_map(txt, removeWords, stopwords("english"))
txt = tm_map(txt, removePunctuation)

# brewer.pal(8,"Dark2")
col.scheme = c("#fd8d3c","#fc4e2a","#e31a1c","#bd0026","#800026")

random.seed(1)

png("final-output.png",width=1600,height=800) # create a png graphics device
wordcloud(txt,
          scale=c(10,3),
          random.order=FALSE,
          max.words=1000,
          colors=col.scheme,
          vfont=c("sans serif","bold"),
          rot.per=0,
          fixed.asp=FALSE,
          random.color=TRUE)
dev.off() # turn off the device -- i.e. write it to disk now!
