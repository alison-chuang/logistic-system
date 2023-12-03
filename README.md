# Project Overview - logistic-system

## Technologies Used

- **Programming Language:** Python (Flask)
- **Database:** MySQL
- **Cache:** Redis

## Features

1. **Query API:**
   - Show delivery status info of the order.
   - endpoint : /query
   - Query String : ?sno={sno}
   - Response : 
        ```
        {
            "sno": "3",
            "tracking_status": "Delivered"
            "estimated_delivery": "2023-12-02",
            "current_location": {
                "address": "桃園市中壢區中央西路三段150號",
                "location_id": 3,
                "title": "桃園物流中心"
            },
            "details": [
                {
                    "date": "2023-12-02",
                    "id": 52,
                    "location_id": 1,
                    "location_title": "花蓮物流中心",
                    "status": "Created"
                } .....
            ],
            "recipient": {
                "address": "澎湖縣馬公市中正路200號",
                "id": 1248,
                "name": "李大同",
                "phone": "096678901"
            }
        }
        ```

2. **Fake API:**
   - Generate new fake order and tracking_status data. (Can not generate fake status for existing order.)
   - endpoint : /fake
   - Query String : ?num={number of records}, limit to 100, default to 10 
   - Response :
        ```
        {
            "data": [
                {
                    "details": [
                        {
                            "location_id": 15,
                            "order_sno": 64,
                            "tracking_status": "Created"
                        },
                        {
                            "location_id": 15,
                            "order_sno": 64,
                            "tracking_status": "Package Received"
                        },
                        {
                            "location_id": 1,
                            "order_sno": 64,
                            "tracking_status": "In Transit"
                        } ....
                    ],
                    "sno": 64,
                    "tracking_status": {
                        "location_id": 19,
                        "order_sno": 64,
                        "tracking_status": "In Transit"
                    }
                }
            ]
        }
        ```

3. **Scheduled Report Generation:**
   - Utilizes cron jobs to generate reports at 00:00, 08:00, 16:00 daily.
   - The reports are stored in S3.

## Caching Mechanism

- **Caching Strategy:**
  - Caching is implemented using string storage.
  
- **Cache Expiry:**
  - Cache items expire after 4 hours. The decision is based on the assumption that the frequency of updates for shipping status might not be higher than every four hours.

- **Update Policy:**
  - The cache would not be updated, for the fake data is currently static. 
  - If an `update_tracking_status` API exists in this project, the cache would be updated when refreshing the database status.

# Deployment

### Requirement

- Python 3.10.13
- PM2: For background execution
    ```bash
    sudo apt install nodejs
    sudo apt install npm
    sudo npm install -g pm2
    ```

- Nginx: For reverse proxy to the app
    ```bash
    # set config `/etc/nginx/sites-available/logistic.conf`
    server {
        listen 80;
        server_name;

        location / {
            proxy_pass http://127.0.0.1:3000;
        }
    }
    ```
    ```
    cd ../sites-enabled/
    ln -s ../sites-available/logistic.conf
    ```
- MySQL 
    ```bash
    docker pull mysql
    docker run -itd --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD={passwd} mysql
    ```
- Redis
     ```bash
    docker pull redis
    docker run --name redis -d -p 6379:6379 redis
    ```

### Deployment
1. Clone the project code
    ```bash
    git clone git@github.com:alison-chuang/logistic-system.git
    ```
1. Navigate to the project directory
    ```bash
    cd logistic-system
    pip install -r requirements.txt
    ```
1. Background execution using PM2
    ```bash
    pm2 start main.py --name logistic-system
    ```

### Database Migration
1. Navigate to the `alembic` directory
    ```bash
    cd alembic
    ```
2. Run migration
    ```bash
    alembic upgrade head
    ======
    Output: 
    INFO  [alembic.runtime.migration] Context impl MySQLImpl.
    INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
    INFO  [alembic.runtime.migration] Running upgrade  -> 56bfc7c60323, create recipients table
    INFO  [alembic.runtime.migration] Running upgrade 56bfc7c60323 -> fa805950e08e, create order table
    INFO  [alembic.runtime.migration] Running upgrade fa805950e08e -> a8ee2b918a7a, create location table
    INFO  [alembic.runtime.migration] Running upgrade a8ee2b918a7a -> 953f9e952811, create tracking_status table
    ```

### Mock Data
1. Export Python path
    ```bash
    cd logistic-system
    export PYTHONPATH=$(pwd)
    ```
2. Run data generator
    ```bash
    python gen_location.py && python gen_recipient.py && python gen_order.py && python gen_tracking_status.py
    ```
