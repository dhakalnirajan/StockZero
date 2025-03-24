# StockZero RL Chess Engine - Deployment Documentation

This document provides a comprehensive, production-ready guide for deploying the StockZero RL chess engine web application on a Linux server environment.

## 1. Production Environment Stack (Recommended)

* **Cloud Server Instance:**
  * **Provider:** AWS (EC2), Google Cloud Platform (Compute Engine), Azure VMs, DigitalOcean, etc. Choose a provider and instance type suitable for your expected traffic and performance needs. **For optimal performance, select GPU-enabled instances (highly recommended for StockZero inference).**
  * **Operating System:** Ubuntu Server (latest LTS version) or CentOS/RHEL (stable and production-proven Linux distributions).

* **Web Server:** Nginx (high-performance and widely used web server)

* **WSGI Application Server:** Gunicorn (Python WSGI server - production grade, handles concurrency and process management)

* **Database:** PostgreSQL (robust, scalable, and production-ready relational database)

* **Cache Backend:** Redis (in-memory data structure store - for high-performance caching)

* **Python:** Python 3.9 or later (for performance and security updates)

* **Virtual Environment:** `venv` (Python's built-in virtual environment tool) or Conda (for isolated Python environment and dependency management)

* **Systemd:** Systemd for service management (auto-start, monitoring) of Gunicorn and other services.

* **HTTPS:** Let's Encrypt (free, automated, and open certificate authority) for enabling HTTPS.

* **Logging and Monitoring Tools (Optional but Highly Recommended for Production):**
  * Log Aggregation and Analysis: ELK Stack (Elasticsearch, Logstash, Kibana), Graylog, Splunk, etc.
  * Server and Application Performance Monitoring (APM): Prometheus, Grafana, New Relic, Datadog, etc.

## 2. Detailed Deployment Steps (Production Walkthrough)

**Step 1: Provision and Harden the Server**

1. **Provision a Cloud Server Instance:** Create a new server instance on your chosen cloud provider. Select a GPU-enabled instance type if you plan to utilize GPU acceleration (recommended).
2. **Secure Server Access:**
    * **SSH Keys:** Configure SSH key-based authentication and disable password-based SSH login for increased security.
    * **Firewall:** Configure a firewall (e.g., `ufw` on Ubuntu, `firewalld` on CentOS) to restrict access to essential ports only (SSH, HTTP, HTTPS, and any necessary database/Redis ports from trusted networks).
3. **Update System Packages:** Update the server's package lists and install security updates immediately after provisioning:

    ```bash
    sudo apt-get update && sudo apt-get upgrade -y  # Ubuntu example
    ```

**Step 2: Install Base Software Stack (Python, pip, virtualenv, PostgreSQL, Redis)**

1. **Install Python and pip:** Ensure Python 3.9+ and `pip` are installed. You may need to install `python3-dev` package as well.
2. **Install virtualenv:** `sudo apt-get install -y virtualenv`
3. **Install PostgreSQL and Redis:** Use `setup_server.sh` script (provided in the StockZero project) or follow distribution-specific instructions to install and initialize PostgreSQL and Redis servers. Secure PostgreSQL and Redis instances appropriately following security best practices.
4. **Install CUDA and cuDNN (if using GPU):** Install NVIDIA drivers, CUDA Toolkit, and cuDNN libraries compatible with your TensorFlow version and server OS, if you plan to use GPU acceleration. Refer to NVIDIA and TensorFlow documentation.

**Step 3: Deploy StockZero Project Files**

1. **Clone from GitHub:** Clone your StockZero project repository to your server (e.g., into `/home/stockzero_user/stockzero_project/`).
2. **Create Virtual Environment:** Create and activate a virtual environment in your project directory:

    ```bash
    cd /home/stockzero_user/stockzero_project
    virtualenv venv
    source venv/bin/activate
    ```

3. **Install Dependencies:** Install Python dependencies using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

4. **Place Model Weights:** Ensure your trained model weights file (e.g., `StockZero-{year}-{month-day}.weights.h5`) is in the `stockzero/models/` directory within your server project.
5. **Configure `.env` File:** Create a `.env` file in the `stockzero/` root directory and set all necessary production environment variables, including database credentials, Redis URL, Django `SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, etc.

**Step 4: Configure Django for Production**

1. **Set `DEBUG = False` and `SECRET_KEY`:**  **Absolutely ensure** `DEBUG = False` is set in `stockzero/stockzero/settings.py` for production. Set a strong, unique, and securely stored `SECRET_KEY` via environment variable in your `.env` file.
2. **Configure `ALLOWED_HOSTS`:**  Set `ALLOWED_HOSTS` in `settings.py` to your server's domain name(s) or IP addresses using environment variables.
3. **Database Configuration:** Verify PostgreSQL database settings in `settings.py` match your production database setup (using environment variables for credentials is best practice).
4. **Redis Configuration:** Verify Redis cache settings in `settings.py` are correct for your Redis server address and port (use environment variables for connection details).
5. **Static File Setup:** Run `./manage.sh collectstatic` to collect static files into `STATIC_ROOT` for efficient serving by Nginx.

**Step 5: Configure Gunicorn and Systemd**

1. **Configure Gunicorn:** Create a Gunicorn systemd service file (e.g., `/etc/systemd/system/stockzero_gunicorn.service`) to manage the Gunicorn WSGI server. Example service configuration is provided in the `DEPLOYMENT_DOC.md` section of the README.md.
2. **Enable and Start Gunicorn:** Enable and start the Gunicorn service using `systemctl`:

    ```bash
    sudo systemctl enable stockzero_gunicorn.service
    sudo systemctl start stockzero_gunicorn.service
    sudo systemctl status stockzero_gunicorn.service # Verify Gunicorn status for any errors
    ```

**Step 6: Configure Nginx as Reverse Proxy and Web Server**

1. **Create Nginx Server Block:** Create an Nginx server block configuration file (e.g., `/etc/nginx/sites-available/stockzero`) to act as a reverse proxy for Gunicorn and serve static files. Example Nginx configuration is provided in the `DEPLOYMENT_DOC.md` section of the README.md. **Important:** Set `server_name` to your actual domain name or server IP.
2. **Enable Nginx Configuration:** Create a symbolic link to enable the configuration:

    ```bash
    sudo ln -s /etc/nginx/sites-available/stockzero /etc/nginx/sites-enabled/
    ```

3. **Test and Restart Nginx:** Test Nginx configuration and restart the Nginx service:

    ```bash
    sudo nginx -t
    sudo systemctl restart nginx
    ```

**Step 7: Enable HTTPS with Let's Encrypt (Highly Recommended)**

1. **Install `certbot`:**  Install the `certbot` tool for Let's Encrypt: `sudo apt-get install -y certbot python3-certbot-nginx`
2. **Obtain SSL Certificate:** Run `certbot` to automatically obtain and install an SSL certificate for your domain. Replace `your_domain.com` with your actual domain name:

    ```bash
    sudo certbot --nginx -d your_domain.com
    ```

    `certbot` will automatically configure Nginx to use HTTPS and set up certificate renewal.

**Step 8: Finalize and Test Production Deployment**

1. **Access via HTTPS:** Access your StockZero web application using `https://your_domain.com` in your browser.
2. **Thorough Testing:** Perform thorough testing of all features, API endpoints, user interface, PGN game recording, AI engine performance, and error handling in your production environment.
3. **Security Audits:** Conduct security audits or penetration testing to identify and address potential security vulnerabilities in your deployment configuration.
4. **Monitoring Setup:** Implement server and application monitoring tools to track performance, identify errors, and proactively address issues in your production environment.
5. **Log Rotation and Management:** Set up log rotation (e.g., using `logrotate` or systemd journald) to manage log file sizes and prevent disk space exhaustion over time.

## 3. Production Best Practices Checklist

* [x] **HTTPS Enabled:** Secure all communication with HTTPS using Let's Encrypt or similar.
* [x] **`DEBUG = False`:**  Ensure `DEBUG` is set to `False` in `settings.py` for production performance and security.
* [x] **Strong `SECRET_KEY`:** Use a strong, unique, and securely stored `SECRET_KEY` environment variable.
* [x] **`ALLOWED_HOSTS` Configured:**  Restrict `ALLOWED_HOSTS` to your server's domain name(s).
* [x] **PostgreSQL Database:**  Use PostgreSQL as the production database. Configure securely.
* [x] **Redis Caching:**  Utilize Redis for caching with a persistent Redis server.
* [x] **Static File Serving (Whitenoise/Nginx):** Configure Django to serve static files efficiently in production using Whitenoise and/or Nginx.
* [x] **Gunicorn WSGI Server:** Use Gunicorn as the production WSGI application server.
* [x] **Nginx Reverse Proxy:** Configure Nginx as a reverse proxy in front of Gunicorn.
* [x] **Systemd Service Management:**  Use systemd to manage Gunicorn service for auto-start and monitoring.
* [x] **Rate Limiting (API Throttling):** Implement rate limiting for API endpoints.
* [x] **Production Logging:** Configure comprehensive logging to files and monitor logs regularly.
* [ ] **GPU Utilization Verified (If Applicable):**  If using GPU server, confirm GPU utilization is active during inference.
* [ ] **Database Backups:** Implement regular database backups.
* [ ] **Security Hardening:** Implement server and application security hardening measures (firewall, security updates, input validation, etc.).
* [ ] **Monitoring System:** Set up server and application monitoring for performance and error tracking.

This production-grade deployment documentation should provide a detailed and comprehensive guide for deploying the StockZero RL chess engine web application to a real-world production environment. Remember to customize these steps based on your specific infrastructure, security requirements, and scalability needs. Thorough testing and monitoring are crucial after deployment. Good luck!
