# Chat Web Server - Flask Web App 


![Python Version](https://img.shields.io/badge/python-3.9-blue.svg)
![Flask Version](https://img.shields.io/badge/flask-2.0-orange.svg)

Chat Web server is a simple Flask web application for real-time chat. It allows users to sign up, log in, and send messages in a chat room. Messages are persisted using either JSON file or MongoDB, making it easy to choose the storage method that suits your needs.

## Features

- User Signup: New users can create an account by providing their email, username, and password.

- User Login: Registered users can log in using their username or email along with the password.

- Real-time Chat: Users can send and receive messages in real-time within the chat room.

- Message Deletion: Users can delete their own messages, and the chat updates instantly for all participants.

- XSS Protection: The application is protected against Cross-Site Scripting (XSS) attacks using custom escape functions.


## Getting Started

### Prerequisites

- Python 3.x
- Flask
- MongoDB or JSON File

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ishanoshada/Chat-Web-Server.git
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up MongoDB (optional):
   - If you prefer to use MongoDB as the message storage method, make sure you have MongoDB installed and running on your machine. Update the `MONGODB_URI` variable in the `app.py` file with your MongoDB connection string.

## Usage

1. Run the Flask app:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000/` to access the chat app.

3. Sign up or log in to start using the chat room.

## Folder Structure

```
Chat-Web-server/
│
├── app.py
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   └── navbar.html
│
├── data/
│   ├── user_data.json
│   └── chats.json
│
├── requirements.txt
├── README.md
└── .gitignore
```
## Screenshots

![Screenshot](https://raw.githubusercontent.com/Ishanoshada/Ishanoshada/main/ss/IMG_20230729_003714.jpg)

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## Acknowledgments

- Thanks to the Flask and MongoDB communities for providing excellent resources and documentation.
- Inspiration for this project came from the need for a simple and secure real-time chat application.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**OneOne is impressive** 🚀 Give it a ⭐️ if you liked it! Thanks for stopping by! For more projects, visit [GitHub Profile](https://github.com/ishanoshada).
