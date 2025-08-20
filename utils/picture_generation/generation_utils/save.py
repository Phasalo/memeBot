import uuid
from datetime import datetime
from typing import Union
from PIL import Image
from moviepy import VideoFileClip, CompositeVideoClip
from config.const import TEMP_DIR


def unique_name(prefix: str = 'photo', extension: str = '.png') -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:16]
    return f"{prefix}_{timestamp}_{unique_id}{extension}"


def save_media(media: Union[Image.Image, VideoFileClip, CompositeVideoClip], prefix: str = 'media'):
    if isinstance(media, Image.Image):
        save_path = TEMP_DIR / unique_name(prefix=prefix + '_image', extension='.png')
        media.save(save_path, format='PNG')
    elif isinstance(media, (VideoFileClip, CompositeVideoClip)):
        save_path = TEMP_DIR / unique_name(prefix=prefix + '_video', extension='.mp4')
        media.write_videofile(save_path)
    else:
        raise TypeError(f"Unsupported media type: {type(media)}")
    return save_path
