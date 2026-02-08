# Matcha
Our Matcha is a full-stack web application designed to help people find partners through smart technology. Built with Flask and Vue 3, the application manages the entire process from account verification to the final meeting.

> **Note**: The stable production code is located in the 42-submission branch. The main branch is mainly left for tracking the development process and workflow.

## System Architecture
The project is built on a containerized micro-service architecture to ensure high availability and environment parity.
### Core Technology Stack
**Backend:** Flask (Python) following a Repository Pattern (DAL) for clean database interactions.
**Frontend:** Vue.js 3 with TypeScript and SCSS, optimized for modern browsers (Chrome/Firefox).
**Database:** PostgreSQL for relational data management with manual query optimization
**Real-time:** Socket.IO for instant messaging and live notifications.


###  Infrastructure
**Nginx:** Reverse proxy handling SSL termination and request routing.
* **Redis:** High-speed caching for real-time presence and session management.
**GeoIP:** MaxMind GeoLite2 for automated localization.


## Features

### 1. Account & Security
**Secure Registration:** Registration requires unique email verification via a dedicated link.
**Data Protection:** Passwords are cryptographically hashed; plain-text storage was forbidden.
**Input Sanitization:** Robust protection against SQL injection and XSS (HTML/JS injection).



> Registration and Authentication Flow

![alt text](https://github.com/EVBLOOD/Matcha/blob/main/screenshots/Login.png)

![alt text](https://github.com/EVBLOOD/Matcha/blob/main/screenshots/Register.png)

![alt text](https://github.com/EVBLOOD/Matcha/blob/main/screenshots/Email_confirmation.png)

![alt text](https://github.com/EVBLOOD/Matcha/blob/main/screenshots/Profile_Setup.png)

![alt text](https://github.com/EVBLOOD/Matcha/blob/main/screenshots/Forgot_password.png)

![alt text](https://github.com/EVBLOOD/Matcha/blob/main/screenshots/Resend_email.png)


![alt text](https://github.com/EVBLOOD/Matcha/blob/main/screenshots/Reset_your_password.png)


![alt text](https://github.com/EVBLOOD/Matcha/blob/main/screenshots/password_successfully.png)


### 2. Discovery & Matching
**Smart Suggestions:** Profiles are prioritized based on geographic proximity, shared interests (tags), and "fame rating".
**Advanced Research:** Comprehensive search filtering by age range, fame, location, and multiple tags.
**Profile Management:** Users manage bios, reusable interest tags, and up to 5 pictures.



> Discovery Dashboard and Search Filters
![alt text](https://github.com/EVBLOOD/Matcha/blob/main/screenshots/Home_Page.png)

![alt text](https://github.com/EVBLOOD/Matcha/blob/main/screenshots/Home_Page_Map.png)

![alt text](https://github.com/EVBLOOD/Matcha/blob/main/screenshots/Suggestions.png)

![alt text](https://github.com/EVBLOOD/Matcha/blob/main/screenshots/Suggestions-filter.png)

![alt text](https://github.com/EVBLOOD/Matcha/blob/main/screenshots/Suggestions-sort.png)

### 3. Interaction Layer
**Real-time Chat:** Instant messaging enabled between users with a mutual "like".
**Live Notifications:** Real-time alerts for profile views, likes, and messages.
**Safety Controls:** Features to block users or report "fake accounts".

> Interaction, Notifs and Messages

![alt text](https://github.com/EVBLOOD/Matcha/blob/main/screenshots/Profile_second.png)

![alt text](https://github.com/EVBLOOD/Matcha/blob/main/screenshots/chat.png)

![alt text](https://github.com/EVBLOOD/Matcha/blob/main/screenshots/Notifications.png)



> **Note**: To see more of our UI, feel free to check screenshots folder in the root of our repository.



## Bonus

The project includes several advanced features beyond the mandatory scope:
**OmniAuth:** Social authentication strategies for streamlined login.
**Interactive Map:** Precise user localization via an integrated JavaScript map.
**Advanced Media:** Enhanced photo management and gallery features.
**Audio/Video Chat:** Real-time audio and video calls for connected users.
**Event Planning:** Tools to schedule and organize real-life dates for matches.


> Video Call Interface

![alt text](https://github.com/EVBLOOD/Matcha/blob/main/screenshots/Calling.png)

![alt text](https://github.com/EVBLOOD/Matcha/blob/main/screenshots/Incoming_call.png)

![alt text](https://github.com/EVBLOOD/Matcha/blob/main/screenshots/accept_call.png)

## Deployment
The project uses a `Makefile` to simplify the project running.

### Production Environment
The production setup includes SSL (self-signed for local testing), optimized assets, and automatic database health checks.

```bash
git checkout 42-submission
# Then create a .env file based on .env.example
# Then RUN
make
```

### Development Environment

For active development with hot-reloading and debug tools:

```bash
cd project
# Then create a .env file based on .env.example
# Then RUN
make dev
```
