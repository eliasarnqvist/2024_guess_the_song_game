import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib.request
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import os
import re
import numpy as np
import matplotlib.pyplot as plt

# %% SETTINGS

# Do you want to load the data from the playlist? (True)
get_playlist_data = True
# Do you want to generate spotify codes for the tracks? (True)
get_spotify_codes = True
# Do you want to read a json data file? (False)
read_json_data = False
# Do you want to make the card pdf? (True)
make_card_pdf = True
# Do you want to make the info pdf? (True)
make_info_pdf = True

# Playlist link from spotify
playlist_link = "https://open.spotify.com/playlist/4lCC0gzm1KsEai2Zjwnj4d?si=06f96c84ca434194"
# Playlist folder name
playlist_name = "song_guess_playlist_2"
# Text in corner of cards
card_text = "playlist_2"

# %% ADVANCED SETTINGS

# From your Spotify user API
SPOTIPY_CLIENT_ID='write your id here'
SPOTIPY_CLIENT_SECRET='write your secret here'
SPOTIPY_REDIRECT_URI='http://example.com'

# File structure
os.makedirs(playlist_name, exist_ok=True)
card_file_name = playlist_name + '/' + playlist_name + '.pdf'
data_file_name = playlist_name + '/' + playlist_name + '_data.json'
image_folder_name = playlist_name + '/' + playlist_name + '_images'
os.makedirs(image_folder_name, exist_ok=True)
info_file_name = playlist_name + '/' + playlist_name + '_info.pdf'
plot_file_name = playlist_name + '/' + playlist_name + '_plot.svg'

# Paper size settings
rows, cols = 7, 3
page_width, page_height = A4
cell_width = page_width / cols
cell_height = page_height / rows

# %% GET PLAYLIST DATA FROM SPOTIFY

if get_playlist_data == True:
    # Spotipy object with correct credentials
    spotify = spotipy.Spotify(client_credentials_manager=
                              SpotifyClientCredentials(
                                  client_id=SPOTIPY_CLIENT_ID,
                                  client_secret=SPOTIPY_CLIENT_SECRET))
    
    def get_playlist_uri(playlist_link):
        return playlist_link.split("/")[-1].split("?")[0]
    
    playlist_dictionary = {}
    
    playlist_uri = get_playlist_uri(playlist_link)
    # Get track information from the playlist
    print("Getting playlist track information")
    tracks = []
    new_track_package = [0]
    this_offset = 0
    while True:
        track_pack = spotify.playlist_tracks(playlist_uri, limit=100, 
                                             offset=this_offset)["items"]
        if len(track_pack) == 0:
            break
        tracks = tracks + track_pack
        this_offset += 100
        print("First " + str(this_offset) + " tracks have been read")
    
    number_of_tracks = len(tracks)
    print("Finished reading " + str(number_of_tracks) + " tracks")
    this_track_number = 0
    print("Gathering Spotify image codes")
    for track in tracks:
        # Get track name
        name = track["track"]["name"]
        # Get track artists
        artist_dict = track["track"]["artists"]
        artist_list = []
        for artist in artist_dict:
            artist_name = artist["name"]
            artist_list.append(artist_name)
        artists_str = ", ".join(artist_list)
        # Get album release year
        album_date = track["track"]["album"]["release_date"]
        album_year = album_date[:4]
        # Get track uri
        uri = track["track"]["uri"]
        
        if get_spotify_codes == True:
            # Make spotify code image
            url = "https://scannables.scdn.co/uri/plain/svg/FFFFFF/black/640/" + uri
            urllib.request.urlretrieve(url, image_folder_name + "/" + 
                                       str(this_track_number) + ".svg")
            
            # Show a progress indicator
            fraction_complete = int(round(this_track_number/number_of_tracks * 100))
            if number_of_tracks <= 20:
                print('Finished image: ' + str(this_track_number) + '/' + 
                      str(number_of_tracks) + ', ' + str(fraction_complete) + '%')
            elif number_of_tracks > 20 and number_of_tracks < 50:
                if this_track_number % 5 == 0:
                    print('Finished image: ' + str(this_track_number) + '/' + 
                          str(number_of_tracks) + ', ' + str(fraction_complete) + '%')
            elif number_of_tracks >= 50:
                if this_track_number % 10 == 0:
                    print('Finished image: ' + str(this_track_number) + '/' + 
                          str(number_of_tracks) + ', ' + str(fraction_complete) + '%')
        
        playlist_dictionary[this_track_number] = {"name":name, 
                                                  "artists":artists_str, 
                                                  "year":album_year, 
                                                  "uri":uri}
        
        this_track_number += 1
    
    # Save the playlist data in a json file
    with open(data_file_name, 'w') as json_file:
        json.dump(playlist_dictionary, json_file, indent=4)

# %% MAYBE READ THE JSON FILE INSTEAD

if read_json_data == True:
    with open(data_file_name, 'r') as json_file:
        playlist_dictionary = json.load(json_file)

# %% CREATE THE PDF WITH THE CARDS

if make_card_pdf == True:
    print("Creating track cards")
    # Create PDF
    c = canvas.Canvas(card_file_name, pagesize=A4)
    
    # List of SVG files
    svg_files = [f for f in sorted(os.listdir(image_folder_name)) if f.endswith(".svg")]
    svg_files = sorted(svg_files, key=lambda x: int(x.split('.')[0]))
    
    def draw_grid():
        # Draw grid lines for any page page
        c.setDash(3, 3)
        for r in range(rows + 1):
            y = page_height - r * cell_height
            c.line(0, y, page_width, y)
        for cl in range(cols + 1):
            x = cl * cell_width
            c.line(x, 0, x, page_height)
        c.setDash()
    
    max_idx = len(svg_files)
    pdf_page_counter = 0
    # Layout
    for idx, svg_file in enumerate(svg_files):
        page_idx = idx // (rows * cols)
        idx_on_page = idx % (rows * cols)
        row = idx_on_page // cols
        col = idx_on_page % cols
    
        # Start a new page if needed
        if idx_on_page == 0:
            draw_grid()
    
        # Load and render SVG
        svg_path = os.path.join(image_folder_name, svg_file)
        drawing = svg2rlg(svg_path)
        scale_x = cell_width / drawing.width
        scale_y = cell_height / drawing.height
        scale = min(scale_x, scale_y) - 0.05
        drawing.width *= scale
        drawing.height *= scale
        drawing.scale(scale, scale)
    
        image_height = drawing.height
        image_width = drawing.width
    
        x_pos = col * cell_width + cell_width / 2 - image_width / 2
        y_pos = page_height - row * cell_height - cell_height / 2 - image_height / 2
    
        renderPDF.draw(drawing, c, x_pos, y_pos)
        
        c.setFont("Helvetica", 8)
        x_text = col * cell_width + 4 * mm
        y_text = page_height - (row + 1) * cell_height + 4 * mm
        c.drawString(x_text, y_text, card_text)
        
        card_number_text = str(idx)
        text_width = c.stringWidth(card_number_text, "Helvetica", 8)
        x_text = (col + 1) * cell_width - text_width - 4 * mm
        c.drawString(x_text, y_text, card_number_text)
        
        # Check if we need to make a new page
        if idx_on_page % (rows * cols) == rows * cols - 1 or idx == max_idx - 1:
            c.showPage()
            draw_grid()
            
            # Back of paper with information text
            if idx != max_idx - 1:
                start_idx = idx + 1 - rows * cols
            else:
                start_idx = idx - idx % (rows * cols)
            end_idx = idx
            
            for jdxx, jdx in enumerate(range(start_idx, end_idx + 1)):
                # jdx is same range idx, jdxx is only on one page (0 to rows*cols)
                # print(jdx, jdxx)
                
                track_name = playlist_dictionary[jdx]["name"]
                track_name = re.sub(r'\[.*?\]', '', track_name)
                artists_name = playlist_dictionary[jdx]["artists"]
                track_year = playlist_dictionary[jdx]["year"]
                
                text = '» ' + track_name + '\n» ' + artists_name + '\n» ' + track_year
                
                row = jdxx // cols
                col = jdxx % cols
                
                # Add text
                text_x_pos = page_width - (col + 1) * cell_width + 4 * mm
                text_y_pos = page_height - row * cell_height - 7 * mm
                c.setFont("Helvetica", 12)
                text_width_limit = cell_width - 8 * mm
                wrapped_text = c.beginText(text_x_pos, text_y_pos)
                wrapped_text.setFont("Helvetica", 12)
                for line in text.split("\n"):
                    for word in line.split():
                        if wrapped_text.getX() + c.stringWidth(word, "Helvetica", 12) > text_x_pos + text_width_limit:
                            wrapped_text.textLine("")
                        wrapped_text.textOut(word + " ")
                    wrapped_text.textLine("")
                c.drawText(wrapped_text)
            
            c.showPage()
    
    # Save PDF
    c.save()

# %% GENERATE INFORMATION ABOUT THE TRACKS IN THE PLAYLIST

if make_info_pdf == True:
    print("Generating information about tracks")
    plt.close('all')
    inch_to_mm = 25.4
    color = plt.cm.tab10
    
    min_year = 1950
    max_year = 2025
    
    # Information about release year
    fig, ax = plt.subplots(figsize=(150/inch_to_mm,55/inch_to_mm))
    year_data = np.array([int(track["year"]) for track in playlist_dictionary.values()])
    histo, ex = np.histogram(year_data, bins = max_year - min_year + 1, 
                             range = [min_year, max_year + 1])
    extended_ex = np.hstack([ex[0] - 0.5, ex[:-1], ex[-2] + 0.5])
    extended_histo = np.hstack([histo[0], histo, histo[-1]])
    # ax.step(ex[:-1], histo, where='mid', lw=1.5)
    ax.step(extended_ex, extended_histo, where='mid', lw=1.5)
    
    ax.set_ylabel('Number of tracks per year')
    ax.set_xlabel('Release year')
    
    plt.tight_layout(pad=0.5)
    plt.subplots_adjust(hspace=0, wspace=0)
    
    maximum_year = max(year_data)
    minimum_year = min(year_data)
    number_of_songs = len(year_data)
    
    plt.savefig(plot_file_name)
    
    # Make the pdf now
    c = canvas.Canvas(info_file_name, pagesize=A4)
    
    text1 = r"Playlist information"
    text2 = ("Oldest track: " + str(minimum_year) + 
             ", newest track: " + str(maximum_year))
    text3 = ("Number of tracks: " + str(number_of_songs))
    text_x = page_width / 2
    text_y = page_height * 3 / 4
    c.setFont("Helvetica", 18)
    c.drawCentredString(text_x, text_y, text1)
    c.setFont("Helvetica", 12)
    c.drawCentredString(text_x, text_y - 20 * mm, text2)
    c.drawCentredString(text_x, text_y - 30 * mm, text3)
    
    drawing = svg2rlg(plot_file_name)
    # scale 
    # drawing.width *= scale
    # drawing.height *= scale
    # drawing.scale(scale, scale)

    image_height = drawing.height
    image_width = drawing.width

    x_pos = (page_width - image_width) / 2
    y_pos = (page_height - image_height) / 2

    renderPDF.draw(drawing, c, x_pos, y_pos)

    c.save()
    plt.close(fig)

# %% FINISHED

print("Finished")
