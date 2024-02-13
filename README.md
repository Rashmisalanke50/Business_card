# Business Card Information Extraction Tool
This Python script, powered by Streamlit, facilitates the extraction and management of business card information. Users can upload images of business cards, and the script employs EasyOCR for text extraction. Extracted data is then stored in a MySQL database for easy access and manipulation.
## Features
### Image Upload and Extraction
- Users can upload images of business cards using the provided interface.
- Utilizes EasyOCR to extract text from uploaded images, capturing key details such as name, email, phone number, etc.
- Extracted information is displayed to users for verification before saving.
### Database Storage and Management
- Extracted information is stored in a MySQL database, ensuring persistence and easy retrieval.
- Users can view, edit, and delete stored card data directly from the application interface.
- Provides a seamless experience for managing business card information efficiently.
### Interactive Interface
- Streamlit offers an interactive interface, allowing users to interact with the application effortlessly.
- The user-friendly design ensures a smooth user experience, even for those unfamiliar with technical tools.
## Installation
1. Clone the repository to your local machine:
2. Install the required dependencies:
3. Set up a MySQL database and configure the connection details in the script.
4. Run the Python script using Streamlit:
## Usage
1. Launch the Streamlit application by running the script.
2. Upload an image of a business card using the provided interface.
3. Click on the "Extract and Save Card Data" button to extract information and store it in the database.
4. Explore the stored card data, edit or delete entries as needed.
## Dependencies
- Streamlit
- base64
- PIL
- mysql-connector
- re
- easyocr
- pandas
- sqlalchemy
## Contributing
Contributions are welcome! If you have any suggestions, bug fixes, or feature implementations, feel free to open an issue or submit a pull request.
