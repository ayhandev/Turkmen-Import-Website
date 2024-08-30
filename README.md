# TURKMEN IMPORT

**TURKMEN IMPORT** is an e-commerce platform specializing in electronics, offering a wide range of products including phones, headphones, and other gadgets. Users can browse, filter, and purchase products through an intuitive shopping cart system. Orders are sent directly to the site administrator's email for processing.

## Key Features
- Advanced product search and filtering
- Seamless shopping cart integration
- Secure order processing with email notifications to the admin
- User registration and authentication

## How to Run the Project

To run the project locally:

1. **Install Dependencies:**  
   Run the following command to install all required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Apply Migrations:**  
   Ensure the database is up to date by applying migrations:
   ```bash
   python manage.py migrate
   ```

3. **Start the Server:**  
   Launch the development server:
   ```bash
   python manage.py runserver
   ```

4. **Access the Site:**  
   Open your web browser and go to http://127.0.0.1:8000/ to view the site.

# Deployment
For deployment on a live server, ensure proper configuration of the database, static files, and email settings in settings.py


# Contact
For any inquiries or support, please visit [Ayhan's Website.](https://ayhan008.pythonanywhere.com/)
