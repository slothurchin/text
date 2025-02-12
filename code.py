import streamlit as st
import json
import os

# File to store blog posts
BLOG_FILE = "blog_posts.json"
PUBLIC_URL = "https://slothurchin.streamlit.app"  # Public URL for search engines

def load_posts():
    if os.path.exists(BLOG_FILE):
        with open(BLOG_FILE, "r") as file:
            return json.load(file)
    return []

def save_posts(posts):
    with open(BLOG_FILE, "w") as file:
        json.dump(posts, file, indent=4)

def main():
    st.set_page_config(page_title="Simple Blog Platform")
    st.title("📝 The Blog")
    
    menu = ["Home", "New Post", "Manage Posts"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Home":
        st.subheader("Recent Blog Posts")
        posts = load_posts()
        if posts:
            for post in reversed(posts):
                st.markdown(f"### {post['title']}")
                st.write(f"*By {post['author']} on {post['date']}*\n")
                st.write(post['content'])
                st.markdown("---")
        else:
            st.write("No posts available yet.")
    
    elif choice == "New Post":
        st.subheader("Create a New Blog Post")
        title = st.text_input("Title")
        author = st.text_input("Author")
        content = st.text_area("Content")
        date = st.date_input("Date")
        
        if st.button("Publish"):
            if title and author and content:
                new_post = {"title": title, "author": author, "content": content, "date": str(date)}
                posts = load_posts()
                posts.append(new_post)
                save_posts(posts)
                st.success("Blog post published!")
            else:
                st.warning("Please fill in all fields.")
    
    elif choice == "Manage Posts":
        st.subheader("Manage Your Blog Posts")
        posts = load_posts()
        if posts:
            for i, post in enumerate(posts):
                st.markdown(f"### {post['title']}")
                st.write(f"*By {post['author']} on {post['date']}*\n")
                st.write(post['content'])
                if st.button(f"Delete {post['title']}", key=i):
                    del posts[i]
                    save_posts(posts)
                    st.experimental_rerun()
        else:
            st.write("No posts available to manage.")

if __name__ == "__main__":
    main()
