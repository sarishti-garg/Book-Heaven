import streamlit as st
import pickle
import pandas as pd



def recommend(book):
    book_index = books[books['title'] == book].index[0]
    distances = similarity[book_index]
    books_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_books = []
    recommended_images = []
    recommended_links = []  # List to hold buy links
    recommended_summaries = []  # List to hold book summaries
    recommended_ratings = []  # List to hold book ratings
    
    for i in books_list:
        recommended_books.append(books.iloc[i[0]].title)  # Append only the book title
        recommended_images.append(books.iloc[i[0]].img)    # Append the image link
        recommended_links.append(books.iloc[i[0]].link)    # Append the buy link
        recommended_summaries.append(books.iloc[i[0]].description)  # Append the summary
        recommended_ratings.append(books.iloc[i[0]].rating)  # Append the rating

    return recommended_books, recommended_images, recommended_links, recommended_summaries, recommended_ratings

def render_stars(rating):
    """Convert rating into star display."""
    full_stars = int(rating)  # Full stars are the integer part
    half_stars = 1 if (rating - full_stars) >= 0.5 else 0  # Half star if 0.5 or more
    empty_stars = 5 - full_stars - half_stars  # Remaining stars

    stars_html = ''
    stars_html += '🌕' * full_stars  # Full stars
    stars_html += '🌗' * half_stars   # Half stars
    stars_html += '🌑' * empty_stars   # Empty stars

    return stars_html

# Load the data
books_dict = pickle.load(open('books_dict.pkl', 'rb'))
books = pd.DataFrame(books_dict)

similarity = pickle.load(open('books_similarity.pkl', 'rb'))

st.title('Book Recommender System')

selected_book_name = st.selectbox(
    "Select a book to get recommendations:",
    books['title'].values
)

if st.button('Recommend'):
    names, images, links, summaries, ratings = recommend(selected_book_name)
    
    # Custom CSS for tooltips and book name heights
    st.markdown(
        

        """
        <style>
        .tooltip {
            position: relative;
            display: inline-block;
            cursor: pointer;
        }
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 220px;
            background-color: black;
            color: #fff;
            text-align: left;
            border-radius: 6px;
            padding: 10px;
            position: absolute;
            z-index: 1;
            bottom: 125%; /* Position the tooltip above the text */
            left: 50%;
            margin-left: -110px; /* Center the tooltip */
            opacity: 0;
            transition: opacity 0.3s;
            max-height: 100px;  /* Set max height for the tooltip */
            overflow-y: auto;    /* Enable vertical scroll */
            overflow-x: hidden;  /* Prevent horizontal scroll */
        }
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        .book-name {
            height: 60px; /* Fixed height for book names */
            overflow-y: auto; /* Enable vertical scroll */
            overflow-x: hidden; /* Prevent horizontal scroll */
            display: block; /* Use block display for scrolling */
            max-height: 60px; /* Set max height for scrolling */
            scrollbar-width: none; /* For Firefox */
            -ms-overflow-style: -ms-autohiding-scrollbar; /* For Internet Explorer and Edge */
        }
        .book-name::-webkit-scrollbar {
            width: 0px; /* Width of the scrollbar */
        }
        .buy-now-button {
            display: flex; /* Use flex to center */
            justify-content: center; /* Center horizontally */
            align-items: center; /* Center vertically */
            margin: 5px auto; /* Center horizontally with margin */
            background-color: black; /* Black background */
            color: white; /* White text */
            padding: 2px; /* Padding around text */
            border: 2px solid white; /* White border */
            border-radius: 8px; /* Rounded corners */
            cursor: pointer; /* Pointer cursor on hover */
            width: 80%; /* Set a width for the button */
            text-decoration: none; /* No underline for link */
            font-size: 16px; /* Larger font size */
            transition: all 0.3s ease; /* Smooth transition for hover effect */
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Add shadow */
        }
        .buy-now-button:hover {
            background-color: #333; /* Darker shade of black on hover */
            transform: translateY(-2px); /* Lift effect on hover */
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3); /* Deeper shadow on hover */
        }
        .image-container {
            display: flex; /* Use flexbox for centering */
            flex-direction: column; /* Align items vertically */
            align-items: center; /* Center items horizontally */
            padding: 10px; /* Add padding around the image */
        }
        .image-container img {
            height: 200px; /* Set a fixed height for images */
            width: 130px; /* Set a fixed width for images */
            object-fit: cover; /* Ensure images cover the area without stretching */
        }
        </style>
        """, unsafe_allow_html=True
    )

    col1, col2, col3, col4, col5 = st.columns(5)
    
    for idx, (name, image, link, summary, rating) in enumerate(zip(names, images, links, summaries, ratings)):
        with eval(f'col{idx + 1}'):  # Dynamically access columns
            stars_html = render_stars(rating)  # Get stars representation
            st.markdown(f"""
                <div class="tooltip">
                    <div class="book-name">{name}</div>
                    <span class="tooltiptext">{summary}</span>
                </div>
                <div class="image-container">
                    <img src="{image}" alt="Book Image" />
                    <div style='margin-top: 5px; font-size: 14px;'>
                        {stars_html} <span style='font-size: 14px; color: gray;'>({rating})</span>
                    </div>  <!-- Display stars -->
                    <a href="{link}" target="_blank" class="buy-now-button">Buy Now</a>
                </div>
            """, unsafe_allow_html=True)

    # Disclaimer
    st.markdown("<br><div style='font-size: 18px; font-weight: bold;'>**Disclaimer:** Clicking 'Buy Now' will take you to an external website.</div>", unsafe_allow_html=True)

