import re
import jieba
import streamlit as st
import streamlit_echarts
from bs4 import BeautifulSoup
from pyecharts.charts import Line, Pie, Radar, WordCloud
from pyecharts.charts import Bar, Scatter
from collections import Counter
import requests
from pyecharts import options as opts
from pyecharts.globals import ThemeType


def crawl(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.get_text()

  # 使用正则表达式去除HTML标签
    content = re.sub(r'<.*?>', '',  content)
    # 去除标点符号和多余空格
    content = re.sub(r'[^\w\s]', '',  content)
    # 去除文本中所有的标点符号及空格只保留中文汉字
    content = re.sub(r'[^\u4e00-\u9fa5]', '',  content)
    # 自定义停用词列表
    stopwords = [ '一个', '以及', '我们', '你们', '他们', '它们', '关系', '感觉', '特别','第一','只是','这是','做出','第一章', '第二章', '两个', '指出', '年月日', '全体', '提高', '一种','一直','一时','一边', '一起', '一转眼', '关于', '需要', '以为', '上来', '上述','下来','下面','这时', '这样', '进而', '进行', '那个', '那里', '针对', '问题','随着','通过', '可以', '自己', '代码','输出','输入', '使用', '例如', '结果']
    # 对文本进行分词
    words = jieba.cut(content)
    # 统计词频
    word_count = { }
    for word in words:
        if word not in stopwords and len(word) > 1:
            word_count[word] = word_count.get(word, 0) + 1

    # 过滤长度为1或者词频为1的词
    word_counts = { word: count for word, count in word_count.items() if count > 1 }
    top_word = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]

    wordcloud_chart = (
        WordCloud()
        .add("", [list(word) for word in top_word], word_size_range=[20, 60])
        .set_global_opts(title_opts=opts.TitleOpts(title=" "))
    )

    bar_chart = (
        Bar()
        .add_xaxis([word[0] for word in top_word])
        .add_yaxis("频率",[word[1] for word in top_word])
        .set_global_opts(title_opts=opts.TitleOpts(title=' '))
    )

    line_chart = (
        Line()
        .add_xaxis([word[0] for word in top_word])
        .add_yaxis("频率",[word[1] for word in top_word])
        .set_global_opts(title_opts=opts.TitleOpts(title=" "))
    )

    scatter_chart = (
        Scatter()
        .add_xaxis([word[0] for word in top_word])
        .add_yaxis("频率",[word[1] for word in top_word])
        .set_global_opts(title_opts=opts.TitleOpts(title=" "))
    )


    labels = []
    frequencies = []
    for word, freq in top_word:
        labels.append(word)
        frequencies.append(freq)

    pie_chart = (
          Pie(init_opts=opts.InitOpts(width="800px", height="600px"))
        .add("", top_word)
        .set_global_opts(title_opts=opts.TitleOpts(title=" "))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )

    radar_chart = (
        Radar(init_opts=opts.InitOpts(width="700px", height="500px"))
    .add_schema(schema=[
        opts.RadarIndicatorItem(name=label, max_=max(frequencies)) for label in labels ])
    .add("频率", [frequencies], linestyle_opts=opts.LineStyleOpts(width=1))
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title=" "))
    )

    donut_chart = (
        Pie()
        .add(
            series_name="",
            data_pair=[list(z) for z in zip([word[0] for word in top_word], [word[1] for word in top_word])],
            radius=["40%", "55%"],
            label_opts=opts.LabelOpts(position="outside", formatter="{b}: {d}%"),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title=" "))
    )

    bar2_chart = (
        Bar()
        .add_xaxis([word[0] for word in top_word])
        .add_yaxis("频率", [word[1] for word in top_word])
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title=" "))
    )

    return wordcloud_chart, bar_chart, line_chart, scatter_chart, pie_chart,radar_chart, donut_chart, bar2_chart


def main():
    st.title("Web Crawler and Data Visualization")
    st.sidebar.title("Options")
    url = st.text_input("Enter the URL:")
    chart_options = ["Word Cloud", "Bar Chart", "Line Chart", "Scatter Chart", "Pie Chart", "Radar Chart",
                     "Donut Chart", "Reversed Bar Chart"]
    selected_chart = st.sidebar.selectbox("Select Chart", chart_options)
    if st.sidebar.button("Crawl") or url:
        wordcloud_chart, bar_chart, line_chart, scatter_chart, pie_chart, radar_chart, donut_chart, bar2_chart = crawl(
            url)

    if selected_chart == "Word Cloud":
        st.subheader("Word Cloud")
        streamlit_echarts.st_pyecharts(
            wordcloud_chart,
            theme=ThemeType.DARK
        )

    elif selected_chart == "Bar Chart":
        st.subheader("Bar Chart")
        streamlit_echarts.st_pyecharts(
            bar_chart,
            theme=ThemeType.DARK
        )

    elif selected_chart == "Line Chart":
        st.subheader("Line Chart")
        streamlit_echarts.st_pyecharts(
            line_chart,
            theme=ThemeType.DARK
        )

    elif selected_chart == "Scatter Chart":
        st.subheader("Scatter Chart")
        streamlit_echarts.st_pyecharts(
            scatter_chart,
            theme=ThemeType.DARK
        )
    elif selected_chart == "Pie Chart":
        st.subheader("Pie Chart")
        streamlit_echarts.st_pyecharts(
            pie_chart,
            theme=ThemeType.DARK
        )
    elif selected_chart == "Radar Chart":
        st.subheader("Radar Chart")
        streamlit_echarts.st_pyecharts(
            radar_chart,
            theme=ThemeType.DARK
        )

    elif selected_chart == "Donut Chart":
        st.subheader("Donut Chart")
        streamlit_echarts.st_pyecharts(
            donut_chart,
            theme=ThemeType.DARK
        )
    elif selected_chart == "Reversed Bar Chart":
        st.subheader("Reversed Bar Chart")
        streamlit_echarts.st_pyecharts(
            bar2_chart,
            theme=ThemeType.DARK
        )


if __name__ == '__main__':
    main()
