from datetime import datetime
import os

def user_media_image_path(instance, filename):
    today = datetime.now()
    #  profile_images/2025/08/10/user_23/filename.jpg
    'profile_images',
    return os.path.join(
        str(today.year),
        str(today.month),
        str(today.day),
        f'user_{instance.user.id}',
        filename
    )