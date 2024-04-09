# Social Media Sample


## Installation Steps:

1) Clone this repo from Git to your local pc.

2) Inside 'social_media_sample' create virtual environment using the following command

    ```
    $ python3 -m venv venv
    ```

3) Activate the environment using following command

    ```
    $ source venv/bin/activate
    ```

4) Install the required libraries using the following command

    ```
    $ pip3 install -r requirements.txt
    ```

5) Now go to project folder and do migrations using the folloing
    ```
    $ cd project
    $ python3 manage.py makemigrations
    $ python3 manage.py migrate
    ```



* Installation steps are completed. Now lets check how to run it.

## How To Run:

* Assuming that you have completed the installation steps, and now you are inside project folder.
* Now execute the folloing to run your project

    ```
    $ python3 manage.py runserver 0.0.0.0:8000
    ```

### Please Note:
* In this project, you need authentication token in order to access the APIs except 'Sign up' and 'Sign in/Login' API.
* To get and use the authentication token, at first you need to signin, here in response you will get an token. Now you need to use it in 'Authorization' header of other APIs as shown below.

```
Authorization : Token <your_token_here>
```