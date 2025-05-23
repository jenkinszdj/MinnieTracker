# Minnie Tracker - Dog Event Logger

Minnie Tracker is a simple web application to log your dog's daily events, such as when they last went out, peed, or pooped. It uses Flask for the backend, SQLite for data storage, and runs in a Docker container.

## Prerequisites

- Docker Desktop (for Windows/Mac) or Docker Engine (for Linux) installed and running.

## How to Run

1.  **Clone the Repository:**
    If you've obtained this as a set of files, ensure they are all in a single directory. If it's a git repository, clone it:
    ```bash
    # git clone <repository-url>
    # cd <repository-directory>
    ```

2.  **Build the Docker Image:**
    Open a terminal in the directory containing the `Dockerfile` and other application files. Run the following command to build the Docker image:
    ```bash
    docker build -t dog-tracker-app .
    ```

3.  **Run the Docker Container:**
    Once the image is built, run the container with the following command:
    ```bash
    docker run -d -p 5000:5000 -v dogtrackerdata:/app --name dog-tracker-container dog-tracker-app:latest
    ```
    -   `-d`: Runs the container in detached mode (in the background).
    -   `-p 5000:5000`: Maps port 5000 on your host machine to port 5000 in the container.
    -   `-v dogtrackerdata:/app`: Mounts a named volume called `dogtrackerdata` to the `/app` directory inside the container. This is crucial for persisting the `dog_log.db` SQLite database, so your data isn't lost when the container stops or is removed. Docker will create this volume automatically if it doesn't exist.
    -   `--name dog-tracker-container`: Assigns a memorable name to your container.
    -   `dog-tracker-app:latest`: Specifies the image to use.

4.  **Access the Application:**
    Open your web browser and navigate to:
    [http://localhost:5000](http://localhost:5000)

## How to Stop the Container

To stop the application, run:
```bash
docker stop dog-tracker-container
```

## How to Restart the Container

If you have previously stopped the container, you can restart it with:
```bash
docker start dog-tracker-container
```
Your data will persist because of the volume mapping.

## Technology Stack

-   **Backend:** Python, Flask
-   **Database:** SQLite
-   **Containerization:** Docker
