import requests
import json
import os


def cleanHTML(html):
  tracks = html.split('tracks = ')[1] # Split of first half of HTML
  tracks = tracks.split('buildPlaylist = $.each(tracks, function(key, value)')[0] # Split off second half of HTML
  tracks = tracks[:-14] # Get rid of trailing apostrophe
  tracks = tracks.replace("""[
                        {
                          "track": 1,
                          "name": "welcome",
                          "chapter_link_dropbox": "https://file.tokybook.com/upload/welcome-you-to-tokybook.mp3",
                          "duration": "8",
                          "chapter_id": "0",
                          "post_id": "0",
                          },""", '[') # Get rid of leading welcome audio that is not needed

  return tracks


def main():
  inputLink = input('Enter https://tokybook.com/ link here: ')

  # Get HTML and clean it ot get track list
  response = requests.get(str(inputLink))
  html = response.text
  html = cleanHTML(html)

  # Load tracks
  tracks = json.loads(html)

  # Creat sub-folder
  bookName = tracks[0]['name'].split(' - ')[0]
  currentDirectory = os.getcwd()
  finalDirectory = os.path.join(currentDirectory, f'{bookName}')
  if not os.path.exists(finalDirectory):
    os.makedirs(finalDirectory)

  # Download to file
  for i, x in enumerate(tracks):
      # Create download link
      directory = str(x['chapter_link_dropbox'])
      directory = directory.replace('\/', '/')
      directory = directory.replace(' - ', '%20-%20')
      lnk = 'https://files01.tokybook.com/audio/' + directory

      # Download mp3 and write to file
      doc = requests.get(lnk)
      with open(f'{bookName}/{x["name"]}.mp3', 'wb') as f:
          f.write(doc.content)

      print(f'{i} of {len(tracks)}... Section [{x["name"]}] downloaded')

      
main()