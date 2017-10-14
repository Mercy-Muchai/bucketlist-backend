### Bucketlist API

#### Description
A Bucketlist is a list of things that one has not done before but wants to do before dying.
This is a CRUD API that enables creating users. 
Authenticated users can then create bucketlists/goals of things they intend to do in future before they die.
It enables creating the models for the data which the bucketlist API will be manipulating. 
This is done using postgres ORM. Perform CRUD actions for bucketlists and users. 

### Development

Clone the repository: 

```git clone https://github.com/Mercy-Muchai/bucketlist-backend.git```

Navigate to the cloned repo. 

Ensure you have the following:

```
1. postgres
2. python3 & virtualenv
3. Flask
4. Postman
```
Create a database using:

``` createdb bucketlist```

Create a virtualenv and activate it. [Refer here](https://docs.python.org/3/tutorial/venv.html)

Run the following commands on your terminal to set up the environment. Alternatively, create a .env file on the root of the app and enter the following:

```
export DATABASE_URL="postgresql://localhost/bucketlist"
export APP_SETTINGS="development"
export FLASK_APP="run.py"
export SECRET="somerandomcharactersyoulike"
```

After setting up the above. Run:

```flask run```

Test the endpoints on Postman on the port the app is running on. 

#### Testing

``` python manage.py test```

