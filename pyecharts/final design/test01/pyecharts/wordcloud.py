from pyecharts.charts import WordCloud
import jieba

txt = open("E:\毕设\data\city-new3.txt", encoding='utf-8').read()

words = jieba.lcut(txt)
counts = {}
for word in words:
    if len(word) == 1:
        continue
    else:
        counts[word] = counts.get(word, 0) + 1

items = list(counts.items())
items.sort(key=lambda x: x[1], reverse=True)

wordcloud = WordCloud()
wordcloud.add("",data_pair=items,word_size_range=[10,50],mask_image="E:\毕设\p1.jpg", width="800",height="800")
wordcloud.set_global_opts()
wordcloud.render("E:\\final design\\test01\\templates\wordcloud.html")