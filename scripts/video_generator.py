
import os
from gtts import gTTS
from moviepy.editor import VideoFileClip, ImageClip, concatenate_videoclips, AudioFileClip
import requests
from bs4 import BeautifulSoup

class VideoGenerator:
    def __init__(self, script):
        self.script = script
        self.output_dir = "web/static/generated_videos"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_video(self):
        audio_clips = []
        image_files = []

        for section, content in self.script['script'].items():
            if isinstance(content, dict) and 'content' in content:
                text = content['content']
                # Generate audio
                tts = gTTS(text=text, lang='en')
                audio_file = os.path.join(self.output_dir, f"{section}.mp3")
                tts.save(audio_file)
                audio_clips.append(AudioFileClip(audio_file))

                # Fetch image
                image_file = self._fetch_image(content.get('visual_description', text))
                if image_file:
                    image_files.append(image_file)

        if not audio_clips or not image_files:
            raise Exception("Could not generate audio or find images.")

        # Create video from images and audio
        video_clips = []
        for i, audio_clip in enumerate(audio_clips):
            image_clip = ImageClip(image_files[i % len(image_files)]).set_duration(audio_clip.duration)
            video_clips.append(image_clip.set_audio(audio_clip))

        final_video = concatenate_videoclips(video_clips)
        output_path = os.path.join(self.output_dir, "final_video.mp4")
        final_video.write_videofile(output_path, fps=24)

        return output_path

    def _fetch_image(self, query):
        try:
            url = f"https://www.google.com/search?q={query}&tbm=isch"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all('img')

            for img in img_tags:
                img_url = img.get('src')
                if img_url and img_url.startswith('http'):
                    img_data = requests.get(img_url).content
                    image_path = os.path.join(self.output_dir, f"{query.split()[0]}.jpg")
                    with open(image_path, 'wb') as handler:
                        handler.write(img_data)
                    return image_path
        except Exception as e:
            print(f"Error fetching image: {e}")
            return None
