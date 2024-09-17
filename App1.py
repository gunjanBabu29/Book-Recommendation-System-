import pickle
import streamlit as st
import numpy as np

# Load data
st.header('Book Recommender System')
model = pickle.load(open('artifacts/model.pkl', 'rb'))
book_names = pickle.load(open('artifacts/book_names.pkl', 'rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl', 'rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))
books_authors = pickle.load(open('artifacts/books_authors.pkl', 'rb'))


def fetch_poster_and_author(suggestion):
    book_name = []
    ids_index = []
    poster_url = []
    author_names = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name:
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]['image_url']
        poster_url.append(url)

    for name in book_name:
        author = books_authors.loc[books_authors['title'] == name, 'author'].values[0]
        author_names.append(author)

    return poster_url, author_names


def recommend_book(book_name):
    books_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)

    poster_url, author_names = fetch_poster_and_author(suggestion)

    for i in range(len(suggestion)):
        books = book_pivot.index[suggestion[i]]
        for j in books:
            books_list.append(j)

    return books_list, poster_url, author_names


selected_books = st.selectbox(
    "Type or select a book from the dropdown",
    book_names
)

if st.button('Show Recommendation'):
    recommended_books, poster_url, author_names = recommend_book(selected_books)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text(f"{recommended_books[1]} by {author_names[1]}")
        st.image(poster_url[1])
    with col2:
        st.text(f"{recommended_books[2]} by {author_names[2]}")
        st.image(poster_url[2])
    with col3:
        st.text(f"{recommended_books[3]} by {author_names[3]}")
        st.image(poster_url[3])
    with col4:
        st.text(f"{recommended_books[4]} by {author_names[4]}")
        st.image(poster_url[4])
    # with col5:
    #     st.text(f"{recommended_books[5]} by {author_names[5]}")
    #     st.image(poster_url[5])
