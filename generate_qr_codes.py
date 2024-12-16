import csv
import qrcode
import os

# Path to the CSV file containing user data
csv_file_path = 'authorized_users.csv'

# Directory to save generated QR codes
output_directory = 'qr_codes/'

# Create the directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Function to read the CSV file and generate QR codes
def generate_qr_codes_from_csv():
    # Open the CSV file for reading
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = row['USER_ID']  # Access the 'USER_ID' column

            # Generate QR code for the user ID
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(user_id)
            qr.make(fit=True)
            
            # Create QR code image
            qr_image = qr.make_image(fill='black', back_color='white')
            
            # Save the QR code image with the user ID as the file name
            qr_image.save(f"{output_directory}{user_id}.png")

    print("QR codes generated successfully!")


# Run the function to generate QR codes
generate_qr_codes_from_csv()
