import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog
import shutil
import json
import os
import math
import librosa
import math

from tensorflow import keras
import json
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
#import matplotlib.pyplot as plt
import random
from collections import Counter
from sklearn.preprocessing import LabelEncoder
from tkinter import messagebox

from tkinter import *
from PIL import ImageTk, Image
import os

testMenu="";

def load_data(data_path):
    with open(data_path,"r") as f:
        data=json.load(f)
        #convert lists to arrays
        X=np.array(data["mfcc"])
        y=np.array(data["labels"])
        return X,y
def predictButton():
    data_path = "C:\\Users\\Leroy Chiyangwa\\Documents\\python_templates\\deploy\\music"
    json_path = "C:\\Users\\Leroy Chiyangwa\\Documents\\python_templates\\deploy\\deploy_9.json"
    sample_rate = 22050  # sample rate
    track_duration = 30  # duration of track in seconds
    samples_per_track = sample_rate * track_duration

    def save_mfcc(data_path, json_path, num_mfcc=13, n_fft=2048, hop_length=512, num_segments=1):
        myLabels = [
            "blues",
            "classical",
            "country",
            "disco",
            "hiphop",
            "jazz",
            "metal",
            "pop",
            "reggae",
            "rock"
        ]
        data = {
            "mapping": [],
            "labels": [],
            "mfcc": []
        }
        samples_per_segment = int(samples_per_track / num_segments)
        num_mfcc_vectors_per_segment = math.ceil(samples_per_segment / hop_length)
        for i, (dirpath, dirnames, filenames) in enumerate(os.walk(data_path)):
            print('looping files', i, 'length', len(filenames))
            if dirpath is not data_path:
                semantic_label = dirpath.split("/")[-1]
                data["mapping"].append(semantic_label)
                for f in filenames:
                    file_path = os.path.join(dirpath, f)
                    print('hanzi print file names', i)
                    signal, sr = librosa.load(file_path, sr=sample_rate)  # Use a different variable name here
                    for d in range(num_segments):
                        # calculate start and finish for current segment
                        start = samples_per_segment * d
                        finish = start + samples_per_segment
                        # extract mfcc
                        mfcc = librosa.feature.mfcc(y=signal[start:finish], sr=sr, n_mfcc=num_mfcc, n_fft=n_fft,
                                                    hop_length=hop_length)
                        mfcc = mfcc.T
                        # store only mfcc feature with the expected number of vectors
                        if len(mfcc) == num_mfcc_vectors_per_segment:
                            data["mfcc"].append(mfcc.tolist())
                            # data["labels"].append(i - format(file_path, d + 1))
                            # data["labels"].append(str(i) + "-" + str(file_path) + "-" + str(d + 1))
                            # data["labels"].append(os.path.basename(os.path.dirname(file_path)))
                            data["labels"].append(myLabels[d])
        data["labels"].append("rock")

        with open(json_path, "w") as fp:
            json.dump(data, fp, indent=4)

    save_mfcc(data_path, json_path, num_segments=9)
    # DATA_PATH2 = "C:\\Users\\Leroy Chiyangwa\\Documents\\python_templates\\Data\\data_9.json"
    DATA_PATH2 = "C:\\Users\\Leroy Chiyangwa\\Documents\\python_templates\\deploy\\deploy_9.json"
    X, y = load_data(DATA_PATH2)

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)
    print(y)
    X = X[..., np.newaxis]

    model = keras.models.load_model("C:\\Users\\Leroy Chiyangwa\\final_cnn_model2.h5")
    prediction = model.predict(X)
    # Convert predictions to labels
    predicted_labels = label_encoder.inverse_transform(prediction.argmax(axis=1))



    label_counts = Counter(predicted_labels)

    most_common_label = label_counts.most_common(1)[0][0]
    variable_value.set(most_common_label)
    print(most_common_label)
    messagebox.showinfo("Predicted Value", most_common_label)
    print('')
def delete_files_in_folder():
    # Specify the directory path to delete files from
    directory_path = "C:\\Users\\Leroy Chiyangwa\\Documents\\python_templates\\deploy\\music\\music"

    # Confirm with the user before deleting
    #confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete all files in the folder?")

    #if confirmation:
    #try:
            # Iterate over all the files and folders in the directory
    for root, dirs, files in os.walk(directory_path):
            for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)  # Delete the file
            for folder in dirs:
                    folder_path = os.path.join(root, folder)
                    shutil.rmtree(folder_path)  # Delete the folder recursively

            #messagebox.showinfo("Success", "All files and folders have been deleted!")
        #except Exception as e:
            #messagebox.showerror("Error", str(e))
    #else:
        #print('failed')
        #messagebox.showinfo("Canceled", "Deletion operation canceled.")
def upload_wav_file():
    delete_files_in_folder()
    # Open file dialog to select a WAV file
    file_path = filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav")])

    if file_path:
        # Specify the destination directory to save the file
        destination_directory = "C:\\Users\\Leroy Chiyangwa\\Documents\\python_templates\\deploy\\music\\music"

        # Copy the file to the destination directory
        shutil.copy(file_path, destination_directory)

        print("File uploaded successfully!")

def new_file_clicked():
    print("The New File menu was clicked!")
def handle_navbar_click(title):
    print("The navbar was clicked!",title)
    if(title=="Test"):
        print("Home")
        #newWindow = tk.Toplevel(window)
        newWindow  = tk.Tk()

        newWindow.title("Music Upload")
        newWindow.geometry("400x400")
        variable_value = tk.StringVar()
        upload_button = tk.Button(newWindow, text="Upload WAV File", command=upload_wav_file)
        upload_button.pack()

        delete_button = tk.Button(newWindow, text="Predidct Music Genre", command=predictButton)
        delete_button.pack()
        #label = tk.Label(newWindow, textvariable=variable_value)
        #label.pack()

        window_width = 800
        window_height = 600
        window.geometry(f"{window_width}x{window_height}")



window = tk.Tk()

#=========================

# Create a menubar.
menubar = tk.Menu()

# Create the navbar frame
navbar_frame = tk.Frame(window, bg="gray", height=50)
navbar_frame.pack(fill=tk.X)

# Create the navbar titles
titles = ["Home", "Test", "Services", "Logout"]
for title in titles:
    label = tk.Label(navbar_frame, text=title, padx=10, pady=10, bg="gray", fg="white")
    label.pack(side=tk.LEFT)
    label.bind("<Button-1>", lambda event, title=title: handle_navbar_click(title))





# Insert the menubar in the main window.
file_menu = tk.Menu(menubar, tearoff=False, bg="lightgrey", fg="black", font=("Arial", 10))

# Append the menu to the menubar.
file_menu.add_command(
    label="New",
    accelerator="Ctrl+N",
    command=new_file_clicked
)
file_menu.add_command(label="New")
file_menu.add_command(label="Open")
file_menu.add_command(label="Save")


menubar.add_cascade(menu=file_menu, label="File")



window.config(menu=menubar)

#===========================

variable_value = tk.StringVar()
#upload_button = tk.Button(window, text="Upload WAV File", command=upload_wav_file)
#upload_button.pack()

#delete_button = tk.Button(window, text="Predidct Music Genre",command=predictButton)
#delete_button.pack()


#label = tk.Label(window, textvariable=variable_value)
#.pack()



#window_width = 800
#window_height = 600
#window.geometry(f"{window_width}x{window_height}")

label = tk.Label(window, textvariable="Metrics").pack()

img1 = ImageTk.PhotoImage(Image.open("accuracy_test.jpg"))
panel1 = tk.Label(window, image=img1)
panel1.pack(side="left", padx=10, pady=10)

# Load the second image
img2 = ImageTk.PhotoImage(Image.open("metrics_test.jpg"))
panel2 = tk.Label(window, image=img2)
panel2.pack(side="left", padx=10, pady=10)

window.mainloop()