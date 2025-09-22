# Spotify QR Code Downloader

This script downloads QR codes for all tracks in your Spotify playlist. Each QR code, when scanned, will link directly to the track on Spotify.

## Setup Instructions

1. Create a Spotify Developer Account:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Log in with your Spotify account
   - Accept the terms of service

2. Create a New Application:
   - Click "Create App"
   - Fill in the application name (e.g., "Playlist QR Generator")
   - Set the redirect URI to: `https://localhost:8888/callback`
   - Save the application

3. Get Your Credentials:
   - Once your app is created, you'll see your Client ID on the dashboard
   - Click "Show Client Secret" to reveal your Client Secret
   - Copy both the Client ID and Client Secret

4. Update the Script:
   - Open `spotify_qr_downloader.py`
   - Replace `YOUR_CLIENT_ID` with your actual Client ID
   - Replace `YOUR_CLIENT_SECRET` with your actual Client Secret

5. Replace USERNAME with your own username and make sure u create a private copy of the playlist (possible in mobile and desktop app, not in browser app), as you cannot access shared playlists.

## Usage

1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Run the script:
   ```bash
   python spotify_qr_downloader.py
   ```

3. Follow the prompts:
   - The script will show a list of your playlists
   - Enter the number of the playlist you want to process
   - QR codes will be generated in the `qr_codes` directory

## Notes

- Each QR code is named after the track title
- QR codes are saved as PNG files
- When scanned, the QR codes will open the track directly in Spotify
- Make sure you have a Spotify account and are logged in
