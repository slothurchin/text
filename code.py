import streamlit as st
import json
from pathlib import Path

# File to store blog posts
BLOG_FILE = Path("blog_posts.json")
PUBLIC_URL = "https://slothurchin.streamlit.app"  # Updated public URL

def load_posts():
    return json.loads(BLOG_FILE.read_text()) if BLOG_FILE.exists() else []

def save_posts(posts):
    BLOG_FILE.write_text(json.dumps(posts, indent=4))

def display_posts(posts):
    for post in reversed(posts):
        st.markdown(f"### {post['title']}")
        st.write(f"*By {post['author']} on {post['date']}*")
        st.write(post['content'])
        st.markdown("---")

def main():
    st.set_page_config(page_title="The Blog")
    st.title("📝 The Blog")
    
    menu = ["Home", "New Post", "Manage Posts"]
    choice = st.sidebar.selectbox("Menu", menu)
    posts = load_posts()
    
    if choice == "Home":
        st.subheader("Recent Blog Posts")
        display_posts(posts) if posts else st.write("No posts available yet.")
    
    elif choice == "New Post":
        st.subheader("Create a New Blog Post")
        title, author, content, date = st.text_input("Title"), st.text_input("Author"), st.text_area("Content"), st.date_input("Date")
        
        if st.button("Publish") and all([title, author, content]):
            posts.append({"title": title, "author": author, "content": content, "date": str(date)})
            save_posts(posts)
            st.success("Blog post published!")
            st.experimental_rerun()
        elif st.button("Publish"):
            st.warning("Please fill in all fields.")
    
    elif choice == "Manage Posts":
        st.subheader("Manage Your Blog Posts")
        if posts:
            for i, post in enumerate(posts):
                st.markdown(f"### {post['title']}")
                st.write(f"*By {post['author']} on {post['date']}*")
                st.write(post['content'])
                if st.button(f"Delete {post['title']}", key=f"delete_{i}"):
                    posts.pop(i)
                    save_posts(posts)
                    st.experimental_rerun()
        else:
            st.write("No posts available to manage.")

if __name__ == "__main__":
    main()
