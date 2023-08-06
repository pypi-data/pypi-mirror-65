from .category import Category
from .namespace import Namespace
from .playlist import Playlist
from .project import Project
from .subscriber import Subscriber
from .user import User
from .video import Video as VideoModel
from ..core.synchable_models.feature import Feature


class Video(Feature):
    @property
    def user(self):
        return self.configure_endpoint(User)

    @property
    def namespace(self):
        return self.configure_endpoint(Namespace)

    @property
    def project(self):
        return self.configure_endpoint(Project)

    @property
    def category(self):
        return self.configure_endpoint(Category)

    @property
    def playlist(self):
        return self.configure_endpoint(Playlist)

    @property
    def subscriber(self):
        return self.configure_endpoint(Subscriber)

    @property
    def video(self):
        return self.configure_endpoint(Video)
