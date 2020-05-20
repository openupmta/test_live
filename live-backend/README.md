Live-Backend Documentation
-----------------------------------

# 1. Project Structure
This project consists of the following components:
- __app__

    This is the main component of the project, it consists of all main sub-modules of the project. These modules are used to handle data, manage connections from client.
    - modules
        - common
        - load_planning
        - port
        - region
        - vehicle
        - vessel
    - settings
    - umls
    - utils
    - apis.py
    - app.py
- __manage.py__
- __README.md__
- __requirements.txt__
- __.gitignore__

# 2. Start the Development Server
## 2.1. Minimum Requirements (main libraries)
- flask
- flask-restplus
- flask-excel
- flask-sqlalchemy

## 2.2. Test Source Code

- Install miniconda, download [here](https://docs.conda.io/en/latest/miniconda.html).

    E.g, For Linux distribution:
    
    ```bash
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh
    ```

- Create conda environment and activate it:

    ```bash
    conda activate
    conda install python=3.6
    ```

- Install required dependencies:

    ```bash
    sudo apt-get install libmysqlclient-dev
    sudo apt install unixodbc-dev
    pip install -r requirements.txt
    ```

- Run project:
    ```bash
    python manage.py
    ```

**Notes**: To run project in the background, you should use [**`tmux`**](https://gist.github.com/ladin157/d2f6bfa09df584ec13f3f6e2055952b7) to manage processes. 

# 3. Tips
- Install all dependencies in Linux distribution before installing the packages to avoiding errors during installation.
- If you get any trouble while installing a dependency, install it separately using conda.
    ```bash
    conda install <package_name>
    ``` 
- Each service is running under `tmux` process.

# 4. Stat The Production Server Ubuntu 16.04 LTS Using Docker
##### 4.1 Unzip sourcecode.zip to /opt folder
- After unzip you will see:
```
- /opt/live-backend
- /opt/live-carwler
- /opt/live-frontend
- /opt/logwin_full.sql
```

- Install mysql database and import data
```bash
$ sudo apt-get install mysql-server
$ systemctl status mysql
$ mysql_secure_installation
$ mysqladmin -u root -p 
mysql> source /opt/logwin_full.sql
mysql> use logwin
mysql> GRANT ALL ON *.* TO root@'%' IDENTIFIED BY 'Mysql PASSWORD';
mysql> flush privileges;
mysql> exit
```

- Change database configuration:

    Goto /opt/live-backend/app/settings/config.py and change:
    
        username to your mysql database username
        
        password to your mysql database password
        
        ip.address to your mysql database ip.address
        
        port to your mysql database port
    
    Do the same with file /opt/live-crawler/settings/config.py
    

##### 4.2 Install Docker
```bash
$ sudo apt-get install curl
$ curl --fail --silent --show-error --location https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
$ sudo apt-get update
$ sudo apt-get install -y docker-ce
$ sudo systemctl status docker
$ sudo usermod -aG docker ${USER}
```

##### 4.3 Install Docker Compose
```bash
$ sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
```

- Check Docker compose is installed
```bash
$ docker-compose --version
```

##### 4.4 Test docker compose

- Run backend service
```bash
$ cd /opt/live-backend
$ docker-compose build
$ docker-compose up
```

##### 4.5 Create startup with server
- Create file in /etc/systemd/system/livebackend.service
- Your livebackend.service file should look like this:

```bash
[Unit]
Description=Docker Compose Application Service
Requires=docker.service
After=docker.service

[Service]
WorkingDirectory=/opt/live-backend
ExecStart=/usr/local/bin/docker-compose up
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0
Restart=on-failure
StartLimitIntervalSec=60
StartLimitBurst=3

[Install]
WantedBy=multi-user.target
```

- Enable startup when server started
```bash
$ sudo systemctl daemon-reaload
$ sudo systemctl enable livebackend.service
$ sudo systemctl start livebackend.service
$ sudo systemctl status livebackend.service
```

- Check backend service is running
```bash
$ cd /opt/live-backend
$ docker-compose logs -f
```

##### 4.6 Install Nginx
```bash
$ sudo apt install nginx -y
$ sudo cp /opt/live-backend/default /etc/nginx/sites-enabled/default
```

- Restart services
```bash
$ sudo systemctl restart mysql
$ sudo systemctl restart livebackend
```

- Well Done your host is IPv4 or domain of server: 
  - http://<your.domain>
  - http://<your.ip.address>
