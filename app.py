import cv2
import os
from os.path import join

import yaml
import pandas as pd
import streamlit as st

import matplotlib.pyplot as plt

from matching.utils import shape_data

from src.drawer import Drawer
from src.typing import Content

with open("config.yml") as f:
    cfg = yaml.load(f, Loader=yaml.SafeLoader)


def main():
    st.title("Cow DataViewer")

    date = st.sidebar.selectbox("date", os.listdir(cfg["data_root"]))

    content = Content.from_str(
        (st.sidebar.selectbox("Content", Content.all(), index=0))
    )

    anns = shape_data(path=join(cfg["data_root"], date))

    if content == Content.table:
        id_queries = list(anns.keys())

        _acc1, _acc5 = 0, 0
        _num_queries = 0

        num_db, num_queries = [], []
        acc1_list, acc5_list = [], []

        for id_query in id_queries:

            acc1 = len(anns[id_query]["top1"])
            acc5 = acc1 + len(anns[id_query]["top2_5"])
            num_query = acc5 + len(anns[id_query]["top6_later"])

            acc1_list.append(100 * acc1 / num_query)
            acc5_list.append(100 * acc5 / num_query)
            num_queries.append(num_query)

            _acc1 += acc1
            _acc5 += acc5
            _num_queries += num_query

        num_db = [1 for i in range(len(num_queries))]

        table_df = pd.DataFrame(
            {
                "db": num_db,
                "query": num_queries,
                "Top1(%)": acc1_list,
                "Top5(%)": acc5_list,
            },
            index=id_queries,
        )

        st.markdown(
            f"### Result:\nTop1: {round(100 * _acc1 / _num_queries, 1)}%, Top5: {round(100 * _acc5 / _num_queries, 1)}%"
        )

        table_df.plot.bar(y=["Top1(%)", "Top5(%)"], alpha=0.8, figsize=(12, 4))
        st.pyplot()
        st.table(table_df)

    if content == Content.images:
        id_queries = list(anns.keys())
        id_query: str = st.sidebar.selectbox("ID", id_queries)
        res_type: str = st.sidebar.selectbox("Type", ["top1", "top2_5", "top6_later"])

        path_queries = list(anns[id_query][res_type].keys())
        num_query = len(path_queries)

        if num_query == 0:
            st.markdown(f"None")
            return

        if num_query == 1:
            index = 1
        else:
            index = st.sidebar.slider("Page index (1-index)", 1, num_query, value=1)

        st.markdown(f"Page: {index}/{num_query}")
        index -= 1  # convert to 0-index

        path_query = path_queries[index]
        img_query = cv2.imread(path_query)
        img_query = cv2.resize(img_query, (224, 224))

        path_db = anns[id_query][res_type][path_query]
        imgs_db = []

        assert len(path_db) == 10, "database length is not 10"

        for i, path in enumerate(path_db):

            id_db = path.split("/")[-2]
            img_db = cv2.imread(path)
            img_db = cv2.resize(img_db, (224, 224))

            if id_db == id_query:
                img_db = Drawer.draw_id(
                    img=img_db, text1=id_db, text2=f"Top{i + 1}", color1=(0, 0, 255)
                )
                img_db = Drawer.draw_rectangle(img_db)
            else:
                img_db = Drawer.draw_id(img=img_db, text1=id_db, text2=f"Top{i + 1}")

            imgs_db.append(img_db)

        st.markdown(f"### Query:")
        st.image(cv2.cvtColor(img_query, cv2.COLOR_BGR2RGB))

        st.markdown(f"### Database:")
        st.image(
            cv2.cvtColor(cv2.hconcat(imgs_db[:5]), cv2.COLOR_BGR2RGB),
            use_column_width=True,
        )
        st.image(
            cv2.cvtColor(cv2.hconcat(imgs_db[5:10]), cv2.COLOR_BGR2RGB),
            use_column_width=True,
        )


if __name__ == "__main__":
    main()
