# 🛠 Password Manager (In Progress)

A simple password manager built in **Python** that uses **cryptography (Fernet)** for encryption.  
Currently runs in the terminal and saves encrypted passwords locally.  

## Current Features
- Encrypts and decrypts passwords using **Fernet** (AES-128 encryption)
- Generates strong random passwords with customizable options
- Saves passwords in an encrypted text file
- Supports adding, viewing, and deleting passwords
- Uses a master password for access

## In Progress
- Building a **GUI** using **Tkinter** and **ttkbootstrap**
- Migrating from text file storage to a **SQLite database**
- Adding **search**, **username**, and **notes** fields
- Implementing **auto clipboard clear** for better security
- Improving key management (replacing hardcoded master password with PBKDF2-derived key)

## Learning Goals
- Apply SQL concepts to manage encrypted data efficiently
- Practice database integration with Python (`sqlite3`)
- Build a user-friendly interface for password management
- Strengthen understanding of encryption and data security

## Technologies
- Python 3
- cryptography (Fernet)
- os, random, string
- (WIP) tkinter, ttkbootstrap
- (Planned) sqlite3 database integration

## File Overview
- `main.py` → backend and CLI logic
- `key.key` → encryption key file (auto-generated)
- `password.txt` → encrypted vault file (I will remove this .txt file soon cause I learned SQL)
- `README.md` → project info and progress log

---

### 👨‍💻 Author
Developed by Gab Talavera  
**Goal:** Learn how encryption, databases, and GUI design work together in real applications.
