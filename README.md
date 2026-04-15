# \# Playlist Vibe Builder

# 

# \## Chosen Problem

# This app solves the Playlist Vibe Builder problem. It lets the user sort a playlist of songs by either energy score or duration so the playlist can be organized by mood or listening time.

# 

# \## Chosen Algorithm

# I used \*\*Merge Sort\*\*.

# 

# I chose Merge Sort because it is a reliable divide-and-conquer sorting algorithm that works well on lists of song records. It also fits this project well because its steps are easy to visualize: the list is split into smaller parts, then merged back together in sorted order. This makes it easier for a user to follow how the playlist changes over time.

# 

# \## Demo

# !\[App Screenshot](screenshot.png)

# 

# \## Problem Breakdown \& Computational Thinking

# 

# \### Decomposition

# \- Read the playlist data entered by the user

# \- Let the user choose a sorting key

# \- Break the playlist into smaller halves

# \- Compare songs while merging them back together

# \- Display the sorted playlist and the sorting steps

# 

# \### Pattern Recognition

# \- The same process repeats: split the list, compare values, and merge in order

# \- During merging, the algorithm repeatedly checks which song should come first based on the selected key

# 

# \### Abstraction

# \- The app shows the important parts: song title, artist, energy, duration, and sorting steps

# \- The app hides low-level implementation details that the user does not need to see

# 

# \### Algorithm Design

# Input → user enters or edits songs and chooses a sort key

# Process → the app uses Merge Sort to reorder the songs

# Output → the app shows the sorted playlist and the recorded sorting steps

# 

# \### Flowchart

# Start

# ↓

# Load playlist

# ↓

# Choose sorting key

# ↓

# Run Merge Sort

# ↓

# Record comparisons and merges

# ↓

# Display sorted playlist

# ↓

# End

# 

# \## Steps to Run

# 1\. Make sure Python is installed

# 2\. Install dependencies with:

# &#x20;  `pip install -r requirements.txt`

# 3\. Run the program with:

# &#x20;  `python app.py`

# 4\. Open the local Gradio link in the browser

# 

# \## Hugging Face Link

# Add your Hugging Face Space link here after deployment.

# 

# \## Testing

# I tested the app with:

# \- normal playlists with different energy and duration values

# \- songs already in sorted order

# \- songs in reverse order

# \- songs with equal values

# \- invalid input formats

# 

# Expected result:

# \- the playlist should be sorted correctly by the selected key

# \- the app should show sorting steps clearly

# \- invalid input should give a helpful error message

# 

# Actual result:

# \- the app sorted the songs correctly

# \- the interface displayed the sorted playlist and steps

# \- invalid input was handled with an error message

# 

# \## Author \& AI Acknowledgment

# Author: Jayden Junagadala

# 

# I used AI tools to help me understand the project requirements, generate starter code ideas, and improve documentation. I reviewed and edited the final work before submitting it.

