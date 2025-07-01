# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 19:58:04 2024

@author: KIRAN
"""

# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import csv
import os
from datetime import datetime

# File paths
BOOKS_FILE = 'books.csv'
MEMBERS_FILE = 'members.csv'
TRANSACTIONS_FILE = 'transactions.csv'

# Ensure CSV files exist
def ensure_csv_files():
    if not os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['Title', 'Author', 'ISBN', 'Publication Date'])
            writer.writeheader()
    if not os.path.exists(MEMBERS_FILE):
        with open(MEMBERS_FILE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['Member ID', 'Name'])
            writer.writeheader()
    if not os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Member ID', 'ISBN', 'Action', 'Date'])

# Load data
def load_books():
    return pd.read_csv(BOOKS_FILE, encoding='utf-8')

def load_members():
    return pd.read_csv(MEMBERS_FILE, encoding='utf-8')

def log_transaction(member_id, isbn, action):
    with open(TRANSACTIONS_FILE, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([member_id, isbn, action, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

# App UI
ensure_csv_files()
st.title("📚 Library Management System")

menu = st.sidebar.selectbox("Choose Option", [
    "📖 View Books",
    "➕ Add Book",
    "👤 Add Member",
    "📦 Issue Book",
    "📬 Return Book",
    "📊 Reports"
])

if menu == "📖 View Books":
    st.subheader("All Books")
    st.dataframe(load_books())

elif menu == "➕ Add Book":
    st.subheader("Add New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    isbn = st.text_input("ISBN")
    pub_date = st.date_input("Publication Date")
    if st.button("Add Book"):
        with open(BOOKS_FILE, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['Title', 'Author', 'ISBN', 'Publication Date'])
            writer.writerow({
                'Title': title,
                'Author': author,
                'ISBN': isbn,
                'Publication Date': pub_date
            })
        st.success("✅ Book added successfully!")

elif menu == "👤 Add Member":
    st.subheader("Add New Member")
    member_id = st.text_input("Member ID")
    name = st.text_input("Member Name")
    if st.button("Add Member"):
        with open(MEMBERS_FILE, 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['Member ID', 'Name'])
            writer.writerow({'Member ID': member_id, 'Name': name})
        st.success("✅ Member added!")

elif menu == "📦 Issue Book":
    st.subheader("Issue Book")
    books = load_books()
    members = load_members()
    if books.empty or members.empty:
        st.warning("Books or members list is empty.")
    else:
        member_id = st.selectbox("Select Member", members['Member ID'])
        isbn = st.selectbox("Select Book ISBN", books['ISBN'])
        if st.button("Issue Book"):
            log_transaction(member_id, isbn, 'issue')
            st.success(f"✅ Book {isbn} issued to Member {member_id}.")

elif menu == "📬 Return Book":
    st.subheader("Return Book")
    member_id = st.text_input("Member ID")
    isbn = st.text_input("Book ISBN")
    if st.button("Return Book"):
        log_transaction(member_id, isbn, 'return')
        st.success(f"✅ Book {isbn} returned by Member {member_id}.")

elif menu == "📊 Reports":
    st.subheader("Transaction Reports")
    if os.path.exists(TRANSACTIONS_FILE):
        df = pd.read_csv(TRANSACTIONS_FILE, encoding='utf-8')
        st.dataframe(df)
        if not df.empty:
            st.bar_chart(df['Action'].value_counts())
    else:
        st.info("No transactions yet.")

