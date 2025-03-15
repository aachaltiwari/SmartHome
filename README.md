# Smart Home Management System

## Overview
This project is a **Smart Home Management System** built using **Django** and **Django Rest Framework (DRF)**. The system manages **users, rooms, sensors, Wi-Fi details, notifications, and smart bulbs**. It includes **RFID-based door access control**, sensor data storage, and group permission-based access control.

The project features an **admin dashboard** with **group-wise permission-based access** to manage users and IoT devices.

## Features
- **User Authentication**: Custom user model using Django's `AbstractUser`.
- **IoT Device Management**: Manages **sensors, bulbs, RFID doors, and Wi-Fi**.
- **Real-time Sensor Data**: Stores **sensor readings** with timestamps.
- **Notification System**: Sends and stores notifications for users.
- **Admin Dashboard**: Manage all entities using Django Admin Panel.
- **Permission-Based Access Control**: Group-wise data restrictions.

## Project Setup
Follow the steps below to set up and run the project.

### Step 1: Create a Virtual Environment
```sh
python -m venv venv
```

Activate the virtual environment:
- **Windows**:
  ```sh
  venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```sh
  source venv/bin/activate
  ```

### Step 2: Install Dependencies
```sh
pip install -r requirements.txt
```

### Step 3: Apply Migrations
```sh
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create a Superuser (Admin)
```sh
python manage.py createsuperuser
```

### Step 5: Run the Server
```sh
python manage.py runserver
```

## Models Explanation
### `models.py`
The database structure consists of:
1. **User**: Custom user model.
2. **UserProfile**: Stores user phone numbers.
3. **RFID**: Manages door access.
4. **WiFi**: Stores Wi-Fi credentials.
5. **Notification**: Stores user notifications.
6. **Room**: Represents a physical room.
7. **Sensor**: Stores sensor readings.
8. **Bulb**: Represents smart bulbs in rooms.
9. **SensorValueStore**: Logs sensor data over time.

### `views.py`
Handles API requests for:
- User authentication
- Managing IoT devices
- Retrieving sensor data
- Controlling smart bulbs

### `sensor.py`
Handles **sensor data processing** and **real-time updates**.

## Admin Site
A powerful **Django Admin Panel** is included to manage users, sensors, Wi-Fi, rooms, and notifications.

### Permission-based Access
The system uses **group-wise access control**:
- **Admin**: Full access
- **Staff**: Read/write access
- **Users**: Restricted access to their data

## API Endpoints
| Endpoint            | Method | Description                  |
|--------------------|--------|------------------------------|
| `/api/users/`       | GET    | Get list of users            |
| `/api/rooms/`       | GET    | Get list of rooms            |
| `/api/sensors/`     | GET    | Get list of sensors          |
| `/api/notifications/` | GET  | Get user notifications       |
| `/api/rfid/`       | POST   | Update RFID door status      |
| `/api/bulbs/`       | PATCH  | Change bulb color/status     |

