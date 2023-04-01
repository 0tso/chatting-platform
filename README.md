# **chatting-platform**

### a web platform for direct one-on-one chatting

## Core functionality
* Registering and logging into the service with a username & password combination
* Finding and opening a chat with other users by searching their usernames
* Real-time chat conversations with:
	* A saved chat history
	* The possibility to delete and edit previous messages
	* Dynamically changing user status markers such as "online", "writing a message", "offline"
* Viewing a list of the users you've searched and chatted with previously

## Installation

1. Clone the repository
```sh
git clone https://github.com/0tso/chatting-platform.git
```
2. Create a virtual environment in the cloned repository:
```sh
python3 -m venv .venv
```
3. Open the virtual environment and install the dependencies:
```sh
source ./.venv/bin/activate
pip install -r requirements.txt
```
4. Create a PostreSQL database with a privileged user and set them up as the environment variables specified in `db.py` (for example using `python-dotenv` and a `.env` file)
5. Execute the `schema.sql` file within the created database, for example using a similar command:
```sh
sudo -u postgres psql DB_NAME < schema.sql
```

### Running the application

To run the application on a development server, execute the following command inside the virtual environment:
```sh
flask run
```