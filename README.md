Secure Vault – File Encryption & Decryption Web App
Secure Vault is a sleek, browser-based application built using Python (Flask) and C, allowing users to encrypt and decrypt .txt files using a hybrid cryptographic method that combines Caesar Cipher and Matrix Transposition techniques.

-----> 🌟 Features
🔒 Encrypt & Decrypt .txt Files
Upload a file, select a key (1–25), and choose the mode — the app will return the processed file instantly.

⚙️ C-based Cryptographic Engine
The core logic is written in C for performance and compiled on the fly by the Flask backend.

🖥️ Interactive UI
A clean, responsive interface using HTML, CSS, and Bootstrap 5 — optimized for both desktop and mobile.

🚀 Fast & Lightweight
No database or third-party storage involved. Everything is processed in memory or local files.

📂 Downloadable Result
After processing, you can instantly download the encrypted/decrypted file.

-----> 🔧 How It Works
User uploads a .txt file.

Chooses a key (1–25) and mode (encrypt or decrypt).

Flask saves the file and compiles cipher.c (if not already compiled).

The backend executes the compiled C program with the file, key, and mode.

The result is shown on the frontend and made available for download.

-----> 🔐 Encryption Logic (C Code)
Caesar Cipher: Each character is shifted by the given key.

Matrix Transposition:

Text is placed row-wise in a matrix with width equal to the key.

Transposition is performed by reading the matrix column-wise.

The decryption reverses both steps in the correct order.

-----> ✅ Example
Upload a file: message.txt

Key: 4

Mode: Encrypt

The app will:

Apply Caesar Cipher with key = 4

Perform matrix transposition (columns = 4)

Generate a processed file ready for download.

-----> ⚠️ Limitations
Only .txt files are allowed.

Key must be an integer between 1–25.

Runs best in a Windows environment (uses cipher.exe, modify if you're on Linux/Mac).

-----> 🧠 Educational Purpose
This project demonstrates:

Web integration with native C programs

Backend logic and secure file handling in Flask

Frontend interactions using modern UI components


