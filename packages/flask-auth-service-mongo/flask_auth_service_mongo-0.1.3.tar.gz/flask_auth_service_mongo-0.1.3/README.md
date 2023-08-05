# Flask authentication service with mongo

Flask JWT authentication package with mongo.


## Installing
- Install and update using pip:
    ```shell
    $ pip3 install -U flask-auth-service-mongo
    ```

## Configuration

-   Define the following environment variables
    * (str) Key with which the token is generated
        ```
        SECRET_KEY=
        ```
    * (bool) Turn the token whitelist on or off
        ```
        WHITE_LIST_TOKEN=
        ```
    * (int) Minimum username length
        ```
        USERNAME_MIN_LENGTH=
        ```
    - (int) Minimum password length
        ```
        PASSWORD_MIN_LENGTH=
        ```
    - (int) Minutes in which the token will expire
        ```
        TOKEN_EXPIRE_MINUTES=
        ```
    - (int) Length of the password generated in the reset
        ```
        RESET_PASSWORD_LEN_GENERATOR=
        ```
    - (bool) Default value for auth.required(require_password_change)
        ```
        REQUIRE_PASSWORD_CHANGE=
        ```

## Links

- [Documentation.](https://flask-auth-service-mongo.readthedocs.io/en/latest/index.html)
