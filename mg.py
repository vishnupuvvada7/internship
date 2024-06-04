import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
bg_color = '#283046'  # Replace with your actual color

# Open and resize the image
img = Image.open("CAS.jpeg")
img = img.resize((50, 50))  # Adjust the size as needed
cas_image = ImageTk.PhotoImage(img)

# Create a frame to hold the image and heading
top_frame = tk.Frame(root, bg=bg_color, width=30, height=5)
top_frame.pack(side="top", expand=True, fill="both")

# Create a label to display the image inside the frame
# Adjust padx to move the image closer to the center
image_label = tk.Label(top_frame, image=cas_image, bg=bg_color)
image_label.pack(side="left", padx=(20, 0))  # Left padding of 20 pixels

# Create the heading label inside the frame
# Adjust padx to give some space after the image
# Use anchor='w' to align the text to the left
heading_label = tk.Label(top_frame, text="CAS AUDIT TOOL", font=("Arial", 18, "bold"), bg=bg_color, fg="white", anchor='w')
heading_label.pack(side="left", padx=(0, 20))  # Right padding of 20 pixels

root.mainloop()
