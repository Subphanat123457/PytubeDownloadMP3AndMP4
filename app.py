from pytube import YouTube
import os

def download_mp3(url, download_path, audio_quality='128kbps'):
    audio = YouTube(url, on_progress_callback=progress_function)
    audio = audio.streams.filter(only_audio=True, abr=audio_quality).first()
    out_file = audio.download(output_path=download_path)
    base, ext = os.path.splitext(out_file)
    new_file = os.path.join(download_path, os.path.basename(base) + '.mp3')
    os.rename(out_file, new_file)
    return new_file

def download_mp4(url, download_path, resolution='highest'):
    video = YouTube(url, on_progress_callback=progress_function)
    if resolution == 'highest':
        video = video.streams.get_highest_resolution()
    else:
        video = video.streams.filter(res=resolution).first()
    out_file = video.download(output_path=download_path)
    return out_file

def get_available_audio_qualities(url):
    audio = YouTube(url)
    return [stream.abr for stream in audio.streams.filter(only_audio=True)]

def get_available_video_resolutions(url):
    video = YouTube(url)
    return [stream.resolution for stream in video.streams.filter(only_video=True)]

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(f"Downloading... {percentage:.2f}% done", end='\r')

if __name__ == '__main__':
    url = input('Enter the YouTube video URL: ')
    choice = input('Download mp3 or mp4? ')
    download_path = 'downloads'
    os.makedirs(download_path, exist_ok=True)
    
    if choice == 'mp3':
        available_audio_qualities = get_available_audio_qualities(url)
        print("Available audio qualities:")
        for index, quality in enumerate(available_audio_qualities, start=1):
            print(f"{index}. {quality}")
        selected_quality = int(input("Enter the number corresponding to the desired audio quality: ")) - 1
        print(download_mp3(url, download_path, available_audio_qualities[selected_quality]))
    elif choice == 'mp4':
        available_video_resolutions = get_available_video_resolutions(url)
        print("Available video resolutions:")
        for index, resolution in enumerate(available_video_resolutions, start=1):
            print(f"{index}. {resolution}")
        selected_resolution = int(input("Enter the number corresponding to the desired video resolution: ")) - 1
        print(download_mp4(url, download_path, available_video_resolutions[selected_resolution]))
    else:
        print("Invalid choice. Please enter 'mp3' or 'mp4'.")
