"""Spotify client.

Reference:
    https://developer.spotify.com/documentation/web-api/reference-beta
"""

from typing import Any, Dict, List

import requests

import spotifier.scopes as S
import spotifier.status_codes as C
from spotifier.oauth import SpotifyAuthorizationCode, SpotifyScopeError

AnyDict = Dict[str, Any]


class SpotifyClientError(Exception):
    pass


class SpotifyResponseError(Exception):
    pass


class Spotify:
    def __init__(self, oauth: SpotifyAuthorizationCode, auto_refresh: bool = True):
        """Spotify client.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta
        """
        self._oauth = oauth
        self._auto_refresh = auto_refresh

        if self._oauth.token is None:
            raise ValueError("Authenticate first.")

    def remove_albums_user(self, ids: List[str]):
        """Remove one or more albums from the current user's 'Your Music' library.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-remove-albums-user
        """
        if 50 < len(ids):
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_LIBRARY_MODIFY]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/albums"

        data: AnyDict = {
            "ids": ",".join(ids),
        }

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.delete(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.remove_albums_user(ids)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def remove_tracks_user(self, ids: List[str]):
        """Remove one or more tracks from the current user's 'Your Music' library.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-remove-tracks-user
        """
        if 50 < len(ids):
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_LIBRARY_MODIFY]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/tracks"

        data: AnyDict = {
            "ids": ",".join(ids),
        }

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.delete(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.remove_tracks_user(ids)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def save_tracks_user(self, ids: List[str]):
        """Save one or more tracks to the current user's 'Your Music' library.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-save-tracks-user
        """
        if 50 < len(ids):
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_LIBRARY_MODIFY]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/tracks"

        data: AnyDict = {
            "ids": ",".join(ids),
        }

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.put(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.save_tracks_user(ids)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def check_users_saved_albums(self, ids: List[str]):
        """Check if one or more albums is already saved in the current Spotify user's 'Your Music' library.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-check-users-saved-albums
        """
        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_LIBRARY_READ]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/albums/contains"

        params: AnyDict = {
            "ids": ",".join(ids),
        }

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.check_users_saved_albums(ids)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def save_albums_user(self, ids: List[str]):
        """Save one or more albums to the current user's 'Your Music' library.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-save-albums-user
        """
        if 50 < len(ids):
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_LIBRARY_MODIFY]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/albums"

        data: AnyDict = {
            "ids": ",".join(ids),
        }

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.put(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.save_albums_user(ids)
        if r.status_code != C.RESPONSE_CREATED:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_users_saved_tracks(self, limit: int = None, offset: int = None, market: str = None):
        """Get a list of the songs saved in the current Spotify user's 'Your Music' library.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-users-saved-tracks
        """
        if limit is not None and not (1 <= limit <= 50):
            raise SpotifyClientError
        if offset is not None and offset < 0:
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_LIBRARY_READ]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/tracks"

        params: AnyDict = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if market is not None:
            params["market"] = market

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_users_saved_tracks(limit, offset, market)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def check_users_saved_tracks(self, ids: List[str]):
        """Check if one or more tracks is already saved in the current Spotify user's 'Your Music' library.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-check-users-saved-tracks
        """
        if 50 < len(ids):
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_LIBRARY_READ]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/tracks/contains"

        params: AnyDict = {
            "ids": ",".join(ids),
        }

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.check_users_saved_tracks(ids)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_users_saved_albums(self, limit: int = None, offset: int = None, market: str = None):
        """Get a list of the albums saved in the current Spotify user's 'Your Music' library.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-users-saved-albums
        """
        if limit is not None and not (1 <= limit <= 50):
            raise SpotifyClientError
        if offset is not None and offset < 0:
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_LIBRARY_READ]):
            raise SpotifyScopeError

        url = "GET https://api.spotify.com/v1/me/albums"

        params: AnyDict = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if market is not None:
            params["market"] = market

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_users_saved_albums(limit, offset, market)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_users_saved_shows(self, limit: int = None, offset: int = None):
        """Get a list of shows saved in the current Spotify user's library. Optional parameters can be used to limit the
        number of shows returned.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-users-saved-shows
        """
        if limit is not None and not (1 <= limit <= 50):
            raise SpotifyClientError
        if offset is not None and offset < 0:
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_LIBRARY_READ]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/shows"

        params: AnyDict = {
            "limit": limit,
            "offset": offset,
        }
        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_users_saved_shows(limit, offset)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def remove_shows_user(self, ids: List[str], market: str = None):
        """Delete one or more shows from current Spotify user's library.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-remove-shows-user
        """
        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_LIBRARY_MODIFY]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/shows"

        data: AnyDict = {
            "ids": ",".join(ids),
        }
        if market is not None:
            data["market"] = market

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.delete(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.remove_shows_user(ids, market)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def check_users_saved_shows(self, ids: List[str]):
        """Check if one or more shows is already saved in the current Spotify user's library.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-check-users-saved-shows
        """
        if 50 < len(ids):
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_LIBRARY_READ]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/shows/contains"

        params: AnyDict = {
            "ids": ",".join(ids),
        }

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.check_users_saved_shows(ids)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def save_shows_user(self, ids: List[str]):
        """Save one or more shows to current Spotify user's library.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-save-shows-user
        """
        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_LIBRARY_MODIFY]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/shows"

        data: AnyDict = {
            "ids": ",".join(ids),
        }

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.put(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.save_shows_user(ids)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_a_show(self, id: str, market: str = None):
        """Get Spotify catalog information for a single show identified by its unique Spotify ID.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-a-show
        """
        url = f"https://api.spotify.com/v1/shows/{id}"

        params: AnyDict = {}
        if market is not None:
            params["market"] = market

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_a_show(id, market)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_multiple_shows(self, ids: List[str], market: str = None):
        """Get Spotify catalog information for several shows based on their Spotify IDs.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-multiple-shows
        """
        if 50 < len(ids):
            raise SpotifyClientError

        url = "https://api.spotify.com/v1/shows"

        params: AnyDict = {
            "ids": ",".join(ids),
        }
        if market is not None:
            params["market"] = market

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_multiple_shows(ids, market)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_a_shows_episodes(self, id: str, limit: int = None, offset: int = None, market: str = None):
        """Get Spotify catalog information about an show's episodes. Optional parameters can be used to limit the number
        of episodes returned.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-a-shows-episodes
        """
        if limit is not None and not (1 <= limit <= 50):
            raise SpotifyClientError
        if offset is not None and offset < 0:
            raise SpotifyClientError

        url = f"https://api.spotify.com/v1/shows/{id}/episodes"

        params: AnyDict = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if market is not None:
            params["market"] = market

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_a_shows_episodes(id, limit, offset, market)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def replace_playlists_tracks(self, playlist_id: str, uris: List[str]):
        """Replace all the tracks in a playlist, overwriting its existing tracks. This powerful request can be useful
        for replacing tracks, re-ordering existing tracks, or clearing the playlist.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-replace-playlists-tracks
        """
        if 100 < len(uris):
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.PLAYLIST_MODIFY_PUBLIC]):
            raise SpotifyScopeError

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        data: AnyDict = {}
        if uris is not None:
            data["uris"] = ",".join(uris)

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.put(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.replace_playlists_tracks(playlist_id, uris)
        if r.status_code != C.RESPONSE_CREATED:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_list_users_playlists(self, user_id: str, limit: int = None, offset: int = None):
        """Get a list of the playlists owned or followed by a Spotify user.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-list-users-playlists
        """
        if limit is not None and not (1 <= limit <= 50):
            raise SpotifyClientError
        if offset is not None and not (0 <= offset <= 100000):
            raise SpotifyClientError

        url = f"https://api.spotify.com/v1/users/{user_id}/playlists"

        params: AnyDict = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_list_users_playlists(user_id, limit, offset)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def change_playlist_details(
        self,
        playlist_id: str,
        name: str = None,
        public: bool = None,
        collaborative: bool = None,
        description: str = None,
    ):
        """Change a playlist's name and public/private state. (The user must, of course, own the playlist.)

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-change-playlist-details
        """
        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.PLAYLIST_MODIFY_PUBLIC]):
            raise SpotifyScopeError

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

        data: AnyDict = {}
        if name is not None:
            data["name"] = name
        if public is not None:
            data["public"] = public
        if collaborative is not None:
            data["collaborative"] = collaborative
        if description is not None:
            data["description"] = description

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.put(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.change_playlist_details(playlist_id, name, public, collaborative, description)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def upload_custom_playlist_cover(self, playlist_id: str, image_path: str):
        """Replace the image used to represent a specific playlist.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-upload-custom-playlist-cover
        """
        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.UGC_IMAGE_UPLOAD]):
            raise SpotifyScopeError

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/images"

        files = {"file": open(image_path, "rb")}

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "image/jpeg",
        }

        r = requests.put(url, files=files, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.upload_custom_playlist_cover(playlist_id, image_path)
        if r.status_code != C.RESPONSE_ACCEPTED:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def reorder_playlists_tracks(
        self, playlist_id: str, range_start: int, insert_before: int, range_length: int = None, snapshot_id: str = None
    ):
        """Reorder a track or a group of tracks in a playlist.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-reorder-playlists-tracks
        """
        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.PLAYLIST_MODIFY_PUBLIC]):
            raise SpotifyScopeError

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        data: AnyDict = {
            "range_start": range_start,
            "insert_before": insert_before,
        }
        if range_length is not None:
            data["range_length"] = range_length
        if snapshot_id is not None:
            data["snapshot_id"] = snapshot_id

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.put(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.reorder_playlists_tracks(playlist_id, range_start, insert_before, range_length, snapshot_id)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def add_tracks_to_playlist(self, playlist_id: str, uris: List[str] = None, position: int = None):
        """Add one or more tracks to a user's playlist.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-add-tracks-to-playlist
        """
        if uris is not None and 100 < len(uris):
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.PLAYLIST_MODIFY_PUBLIC]):
            raise SpotifyScopeError

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        data: AnyDict = {}
        if uris is not None:
            data["uri"] = ",".join(uris)
        if position is not None:
            data["position"] = position

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.post(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.add_tracks_to_playlist(playlist_id, uris, position)
        if r.status_code != C.RESPONSE_CREATED:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_playlist_tracks(
        self,
        playlist_id: str,
        fields: List[str] = None,
        limit: int = None,
        offset: int = None,
        market: str = None,
        additional_types: List[str] = None,
    ):
        """Get full details of the tracks of a playlist owned by a Spotify user.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-playlists-tracks
        """
        if limit is not None and not (1 <= limit <= 100):
            raise SpotifyClientError
        if offset is not None and offset < 0:
            raise SpotifyClientError

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        params: AnyDict = {}
        if fields is not None:
            params["fields"] = ",".join(fields)
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if market is not None:
            params["market"] = market
        if additional_types is not None:
            params["additional_types"] = ",".join(additional_types)

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_playlist_tracks(playlist_id, fields, limit, offset, market, additional_types)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_playlist_cover(self, playlist_id: str):
        """Get the current image associated with a specific playlist.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-playlist-cover
        """
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/images"

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_playlist_cover(playlist_id)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def remove_tracks_playlist(self, playlist_id: str, tracks: List[str], snapshot_id: str = None):
        """Remove one or more tracks from a user's playlist.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-remove-tracks-playlist
        """
        if 100 < len(tracks):
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.PLAYLIST_MODIFY_PUBLIC]):
            raise SpotifyScopeError

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        data: AnyDict = {
            "tracks": tracks,
        }
        if snapshot_id is not None:
            data["snaphot_id"] = snapshot_id

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.delete(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.remove_tracks_playlist(playlist_id, tracks, snapshot_id)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_a_list_of_current_users_playlists(self, limit: int = None, offset: int = None):
        """Get a list of the playlists owned or followed by the current Spotify user.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-a-list-of-current-users-playlists
        """
        if limit is not None and not (1 <= limit <= 50):
            raise SpotifyClientError
        if offset is not None and not (0 <= offset <= 100000):
            raise SpotifyClientError

        url = "https://api.spotify.com/v1/me/playlists"

        params: AnyDict = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_a_list_of_current_users_playlists(limit, offset)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_playlist(
        self, playlist_id: str, fields: List[str] = None, market: str = None, additional_types: List[str] = None
    ):
        """Get a playlist owned by a Spotify user.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-playlist
        """
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"

        params: AnyDict = {}
        if fields is not None:
            params["fields"] = ",".join(fields)
        if market is not None:
            params["market"] = market
        if additional_types is not None:
            params["additional_types"] = ",".join(additional_types)

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_playlist(playlist_id, fields, market, additional_types)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def create_playlist(
        self, user_id: str, name: str, public: bool = None, collaborative: bool = None, description: str = None
    ):
        """Create a playlist for a Spotify user. (The playlist will be empty until you add tracks.)

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-create-playlist
        """
        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.PLAYLIST_MODIFY_PUBLIC]):
            raise SpotifyScopeError

        url = f"https://api.spotify.com/v1/users/{user_id}/playlists"

        data: AnyDict = {
            "name": name,
        }
        if public is not None:
            data["public"] = public
        if collaborative is not None:
            data["collaborative"] = collaborative
        if description is not None:
            data["description"] = description

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.post(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.create_playlist(user_id, name, public, collaborative, description)
        if r not in (C.RESPONSE_OK, C.RESPONSE_CREATED):
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_multiple_albums(self, ids: List[str], market: str = None):
        """Get Spotify catalog information for multiple albums identified by their Spotify IDs.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-multiple-albums
        """
        if 20 < len(ids):
            raise SpotifyClientError

        url = "https://api.spotify.com/v1/albums"

        params: AnyDict = {
            "ids": ",".join(ids),
        }
        if market is not None:
            params["market"] = market

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_multiple_albums(ids, market)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_an_album(self, id: str, market: str = None):
        """Get Spotify catalog information for a single album.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-an-album
        """
        url = f"https://api.spotify.com/v1/albums/{id}"

        params: AnyDict = {}
        if market is not None:
            params["market"] = market

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_an_album(id, market)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_an_albums_tracks(self, id: str, limit: int = None, offset: int = None, market: str = None):
        """Get Spotify catalog information about an album's tracks. Optional parameters can be used to limit the number
        of tracks returned.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-an-albums-tracks
        """
        if limit is not None and not (1 <= limit <= 50):
            raise SpotifyClientError
        if offset is not None and offset < 0:
            raise SpotifyClientError

        url = f"https://api.spotify.com/v1/albums/{id}/tracks"

        params: AnyDict = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if market is not None:
            params["market"] = market

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_an_albums_tracks(id, limit, offset, market)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_several_tracks(self, ids: List[str], market: str = None):
        """Get Spotify catalog information for multiple tracks based on their Spotify IDs.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-several-tracks
        """
        if 50 < len(ids):
            raise SpotifyClientError

        url = "https://api.spotify.com/v1/tracks"

        params: AnyDict = {
            "ids": ",".join(ids),
        }
        if market is not None:
            params["market"] = market

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_several_tracks(ids, market)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_audio_analysis(self, id: str):
        """Get a detailed audio analysis for a single track identified by its unique Spotify ID.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-audio-analysis
        """
        url = f"https://api.spotify.com/v1/audio-analysis/{id}"

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_audio_analysis(id)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_audio_features(self, id: str):
        """Get audio feature information for a single track identified by its unique Spotify ID.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-audio-features
        """
        url = f"https://api.spotify.com/v1/audio-features/{id}"

        params: AnyDict = {}

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_audio_features(id)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_track(self, id: str, market: str = None):
        """Get Spotify catalog information for a single track identified by its unique Spotify ID.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-track
        """
        url = f"https://api.spotify.com/v1/tracks/{id}"

        params: AnyDict = {}
        if market is not None:
            params["market"] = market

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_track(id, market)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_several_audio_features(self, ids: List[str]):
        """Get audio features for multiple tracks based on their Spotify IDs.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-several-audio-features
        """
        if 100 < len(ids):
            raise SpotifyClientError

        url = "https://api.spotify.com/v1/audio-features"

        params: AnyDict = {
            "ids": ",".join(ids),
        }

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_several_audio_features(ids)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def skip_users_playback_to_next_track(self, device_id: str = None):
        """Skips to next track in the user's queue.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-skip-users-playback-to-next-track
        """
        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_MODIFY_PLAYBACK_STATE]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/player/next"

        data: AnyDict = {}
        if device_id is not None:
            data["device_id"] = device_id

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.post(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.skip_users_playback_to_next_track(device_id)
        if r.status_code != C.RESPONSE_NO_CONTENT:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def set_repeat_mode_on_users_playback(self, state: str, device_id: str = None):
        """Set the repeat mode for the user's playback. Options are repeat-track, repeat-context, and off.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-set-repeat-mode-on-users-playback
        """
        if state not in ("track", "context", "off"):
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_MODIFY_PLAYBACK_STATE]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/player/repeat"

        data: AnyDict = {
            "state": state,
        }
        if device_id is not None:
            data["device_id"] = device_id

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.put(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.set_repeat_mode_on_users_playback(state, device_id)
        if r.status_code != C.RESPONSE_NO_CONTENT:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def transfer_a_users_playback(self, device_ids: List[str], play: bool = None):
        """Transfer playback to a new device and determine if it should start playing.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-transfer-a-users-playback
        """
        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_MODIFY_PLAYBACK_STATE]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/player"

        data: AnyDict = {
            "device_ids": device_ids,
        }
        if play is not None:
            data["play"] = play

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.put(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.transfer_a_users_playback(device_ids, play)
        if r.status_code != C.RESPONSE_NO_CONTENT:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_the_users_currently_playing_track(self, market: str, additional_types: List[str] = None):
        """Get the object currently being played on the user's Spotify account.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-the-users-currently-playing-track
        """
        if not (
            self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_READ_CURRENTLY_PLAYING])
            or self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_READ_PLAYBACK_STATE])
        ):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/player/currently-playing"

        params: AnyDict = {
            "market": market,
        }
        if additional_types is not None:
            params["additional_types"] = ",".join(additional_types)

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_the_users_currently_playing_track(market, additional_types)
        if r.status_code == C.RESPONSE_NO_CONTENT:
            return None
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_information_about_the_users_current_playback(self, market: str = None, additional_types: List[str] = None):
        """Get information about the user's current playback state, including track or episode, progress, and active
        device.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-information-about-the-users-current-playback
        """
        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_READ_PLAYBACK_STATE]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/player"

        params: AnyDict = {}
        if market is not None:
            params["market"] = market
        if additional_types is not None:
            params["additional_types"] = additional_types

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_information_about_the_users_current_playback(market, additional_types)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def seek_to_position_in_currently_playing_track(self, position_ms: int, device_id: str = None):
        """Seeks to the given position in the user's currently playing track.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-seek-to-position-in-currently-playing-track
        """
        if position_ms < 0:
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_MODIFY_PLAYBACK_STATE]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/player/seek"

        data: AnyDict = {
            "position_ms": position_ms,
        }
        if device_id is not None:
            data["device_id"] = device_id

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.put(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.seek_to_position_in_currently_playing_track(position_ms, device_id)
        if r.status_code != C.RESPONSE_NO_CONTENT:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def skip_users_playback_to_previous_track(self, device_id: str = None):
        """Skips to previous track in the user's queue.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-skip-users-playback-to-previous-track
        """
        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_MODIFY_PLAYBACK_STATE]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/player/previous"

        data: AnyDict = {}
        if device_id is not None:
            data["device_id"] = device_id

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.post(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.skip_users_playback_to_previous_track(device_id)
        if r.status_code != C.RESPONSE_NO_CONTENT:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def start_a_users_playback(
        self,
        device_id: str = None,
        context_uri: str = None,
        uris: List[str] = None,
        offset: Any = None,
        position_ms: int = None,
    ):
        """Start a new context or resume current playback on the user's active device.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-start-a-users-playback
        """
        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_MODIFY_PLAYBACK_STATE]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/player/queue"

        params: AnyDict = {}
        if device_id is not None:
            params["device_id"] = device_id

        data: AnyDict = {}
        if context_uri is not None:
            data["context_uri"] = context_uri
        if uris is not None:
            data["uris"] = uris
        if offset is not None:
            data["offset"] = offset
        if position_ms is not None:
            data["position_ms"] = position_ms

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.put(url, params=params, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.start_a_users_playback(device_id, context_uri, uris, offset, position_ms)
        if r.status_code != C.RESPONSE_NO_CONTENT:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def pause_a_users_playback(self, device_id: str = None):
        """Pause playback on the user's account.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-pause-a-users-playback
        """
        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_MODIFY_PLAYBACK_STATE]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/player/pause"

        data: AnyDict = {}
        if device_id is not None:
            data["device_id"] = device_id

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.put(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.pause_a_users_playback(device_id)
        if r.status_code != C.RESPONSE_NO_CONTENT:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def set_volume_for_users_playback(self, volume_percent: int, device_id: str = None):
        """Set the volume for the user's current playback device.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-set-volume-for-users-playback
        """
        if not (0 <= volume_percent <= 100):
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_MODIFY_PLAYBACK_STATE]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/player/volume"

        data: AnyDict = {
            "volume_percent": volume_percent,
        }
        if device_id is not None:
            data["device_id"] = device_id

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.put(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.set_volume_for_users_playback(volume_percent, device_id)
        if r.status_code != C.RESPONSE_NO_CONTENT:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_recently_played(self, limit: int = None, after: int = None, before: int = None):
        """Get tracks from the current user's recently played tracks. Note: Currently doesn't support podcast episodes.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-recently-played
        """
        if limit is not None and not (1 <= limit <= 50):
            raise SpotifyClientError
        if after is not None and before is not None:
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_READ_RECENTLY_PLAYED]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/player/recently-played"

        params: AnyDict = {}
        if limit is not None:
            params["limit"] = limit
        if after is not None:
            params["after"] = after
        if before is not None:
            params["before"] = before

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_recently_played(limit, after, before)
        if r.status_code != C.RESPONSE_NO_CONTENT:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_a_users_available_devices(self):
        """Get information about a user's available devices.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-a-users-available-devices
        """
        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_READ_PLAYBACK_STATE]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/player/devices"

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_a_users_available_devices()
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def toggle_shuffle_for_users_playback(self, state: bool, device_id: str = None):
        """Toggle shuffle on or off for user's playback.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-toggle-shuffle-for-users-playback
        """
        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_MODIFY_PLAYBACK_STATE]):
            raise SpotifyScopeError

        url = f"https://api.spotify.com/v1/me/player/shuffle"

        data: AnyDict = {
            "state": state,
        }
        if device_id is not None:
            data["device_id"] = device_id

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.put(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.toggle_shuffle_for_users_playback(state, device_id)
        if r.status_code != C.RESPONSE_NO_CONTENT:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def add_to_queue(self, uri: str, device_id: str = None):
        """Add an item to the end of the user's current playback queue.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-add-to-queue
        """
        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_MODIFY_PLAYBACK_STATE]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/player/queue"

        data: AnyDict = {
            "uri": uri,
        }
        if device_id is not None:
            data["device_id"] = device_id

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.post(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.add_to_queue(uri, device_id)
        if r.status_code != C.RESPONSE_NO_CONTENT:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_categories(self, country: str = None, locale: str = None, limit: int = None, offset: int = None):
        """Get a list of categories used to tag items in Spotify (on, for example, the Spotify player's "Browse" tab).

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-categories
        """
        if limit is not None and not (1 <= limit <= 50):
            raise SpotifyClientError
        if offset is not None and offset < 0:
            raise SpotifyClientError

        url = "https://api.spotify.com/v1/browse/categories"

        params: AnyDict = {}
        if country is not None:
            params["country"] = country
        if locale is not None:
            params["locale"] = locale
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_categories(country, locale, limit, offset)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_a_category(self, category_id: str, country: str = None, locale: str = None):
        """Get a single category used to tag items in Spotify (on, for example, the Spotify player's "Browse" tab).

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-a-category
        """
        url = f"https://api.spotify.com/v1/browse/categories/{category_id}"

        params: AnyDict = {}
        if country is not None:
            params["country"] = country
        if locale is not None:
            params["locale"] = locale

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_a_category(category_id, country, locale)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_a_categories_playlists(self, category_id: str, country: str = None, limit: int = None, offset: int = None):
        """Get a list of Spotify playlists tagged with a particular category.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-a-categories-playlists
        """
        if limit is not None and not (1 <= limit <= 50):
            raise SpotifyClientError
        if offset is not None and offset < 0:
            raise SpotifyClientError

        url = f"https://api.spotify.com/v1/browse/categories/{category_id}/playlists"

        params: AnyDict = {}
        if country is not None:
            params["country"] = country
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_a_categories_playlists(category_id, country, limit, offset)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_recommendations(
        self,
        seed_artists: str = None,
        seed_genres: str = None,
        seed_tracks: str = None,
        limit: int = None,
        market: str = None,
        **kwargs: Dict[str, Any],
    ):
        """Recommendations are generated based on the available information for a given seed entity and matched against
        similar artists and tracks. If there is sufficient information about the provided seeds, a list of tracks will
        be returned together with pool size details.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-recommendations
        """
        if limit is not None and not (1 <= limit <= 100):
            raise SpotifyClientError

        url = "https://api.spotify.com/v1/recommendations"

        params: AnyDict = {
            "seed_artists": seed_artists,
            "seed_genres": seed_genres,
            "seed_tracks": seed_tracks,
        }
        if limit is not None:
            params["limit"] = limit
        if market is not None:
            params["market"] = market
        if kwargs is not None:
            # TODO: Support "min_*", "max_*", "target_*"
            params.update(kwargs)

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_recommendations(seed_artists, seed_genres, seed_tracks, limit, market, **kwargs)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_recommendation_genres(self):
        """Retrieve a list of available genres seed parameter values for recommendations.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-recommendation-genres
        """
        url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_recommendation_genres()
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_new_releases(self, country: str = None, limit: int = None, offset: int = None):
        """Get a list of new album releases featured in Spotify (shown, for example, on a Spotify player's "Browse" tab).

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-new-releases
        """
        if limit is not None and not (1 <= limit <= 50):
            raise SpotifyClientError
        if offset is not None and offset < 0:
            raise SpotifyClientError

        url = "https://api.spotify.com/v1/browse/new-releases"

        params: AnyDict = {}
        if country is not None:
            params["country"] = country
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_new_releases(country, limit, offset)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_featured_playlists(
        self, country: str = None, locale: str = None, timestamp: int = None, limit: int = None, offset: int = None
    ):
        """Get a list of Spotify featured playlists (shown, for example, on a Spotify player's 'Browse' tab).

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-featured-playlists
        """
        if limit is not None and not (1 <= limit <= 50):
            raise SpotifyClientError
        if offset is not None and offset < 0:
            raise SpotifyClientError

        url = f""

        params: AnyDict = {}
        if country is not None:
            params["country"] = country
        if locale is not None:
            params["locale"] = locale
        if timestamp is not None:
            params["timestamp"] = timestamp
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_featured_playlists(country, locale, timestamp, limit, offset)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def endpoint_get_users_profile(self, user_id: str):
        """Get public profile information about a Spotify user.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-users-profile
        """
        url = f"https://api.spotify.com/v1/users/{user_id}"

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.endpoint_get_users_profile(user_id)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_current_users_profile(self):
        """Get detailed profile information about the current user (including the current user's username).

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-current-users-profile
        """
        url = "https://api.spotify.com/v1/me"

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, headers=headers)
        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_current_users_profile()
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def check_current_user_follows(self, type: str, ids: List[str]):
        """Check to see if the current user is following one or more artists or other Spotify users.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-check-current-user-follows
        """
        if type not in ("artist", "user"):
            raise SpotifyClientError
        if 50 < len(ids):
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_FOLLOW_READ]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/following/contains"

        params: AnyDict = {
            "type": type,
            "ids": ",".join(ids),
        }

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.check_current_user_follows(type, ids)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def check_if_user_follows_playlist(self, playlist_id: str, ids: List[str]):
        """Check to see if one or more Spotify users are following a specified playlist.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-check-if-user-follows-playlist
        """
        if 5 < len(ids):
            raise SpotifyClientError

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/followers/contains"

        params: AnyDict = {}
        if ids is not None:
            params["ids"] = ",".join(ids)

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.check_if_user_follows_playlist(playlist_id, ids)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def follow_artists_users(self, type: str, ids: List[str]):
        """Add the current user as a follower of one or more artists or other Spotify users.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-follow-artists-users
        """
        if type not in ("artist", "user"):
            raise SpotifyClientError
        if 50 < len(ids):
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_FOLLOW_MODIFY]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/following"

        data: AnyDict = {
            "type": type,
            "ids": ids,
        }

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.put(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.follow_artists_users(type, ids)
        if r.status_code != C.RESPONSE_NO_CONTENT:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def follow_playlist(self, playlist_id: str, public: bool = None):
        """Add the current user as a follower of a playlist.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-follow-playlist
        """
        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_FOLLOW_MODIFY]):
            raise SpotifyScopeError

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/followers"

        data: AnyDict = {}
        if public is not None:
            data["public"] = public

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.put(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.follow_playlist(playlist_id, public)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_followed(self, type: str, limit: int = None, after: str = None):
        """Get the current user's followed artists.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-followed
        """
        if type not in ("artist"):
            raise SpotifyClientError
        if limit is not None and not (1 <= limit <= 50):
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_FOLLOW_MODIFY, S.USER_FOLLOW_READ]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/following"

        params: AnyDict = {
            "type": type,
        }
        if limit is not None:
            params["limit"] = limit
        if after is not None:
            params["after"] = after

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_followed(type, limit, after)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def unfollow_artists_users(self, type: str, ids: List[str]):
        """Remove the current user as a follower of one or more artists or other Spotify users.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-unfollow-artists-users
        """
        if type not in ("artist", "user"):
            raise SpotifyClientError
        if 50 < len(ids):
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_FOLLOW_MODIFY]):
            raise SpotifyScopeError

        url = "https://api.spotify.com/v1/me/following"

        data: AnyDict = {
            "type": type,
            "ids": ",".join(ids),
        }

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.delete(url, data=data, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.unfollow_artists_users(type, ids)
        if r.status_code != C.RESPONSE_NO_CONTENT:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def unfollow_playlist(self, playlist_id: str):
        """Remove the current user as a follower of a playlist.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-unfollow-playlist
        """
        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.PLAYLIST_MODIFY_PUBLIC]):
            raise SpotifyScopeError

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/followers"

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.delete(url, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.unfollow_playlist(playlist_id)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_multiple_artists(self, ids: List[str]):
        """Get Spotify catalog information for several artists based on their Spotify IDs.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-multiple-artists
        """
        if 50 < len(ids):
            raise SpotifyClientError

        url = "https://api.spotify.com/v1/artists"

        params: AnyDict = {
            "ids": ",".join(ids),
        }

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_multiple_artists(ids)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_an_artist(self, id: str):
        """Get Spotify catalog information for a single artist identified by their unique Spotify ID.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-an-artist
        """
        url = f"https://api.spotify.com/v1/artists/{id}"

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_an_artist(id)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_an_artists_albums(
        self, id: str, include_groups: str = None, market: str = None, limit: int = None, offset: int = None
    ):
        """Get Spotify catalog information about an artist's albums. Optional parameters can be specified in the query
        string to filter and sort the response.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-an-artists-albums
        """
        if limit is not None and not (1 <= limit <= 50):
            raise SpotifyClientError
        if offset is not None and offset < 0:
            raise SpotifyClientError

        url = f"https://api.spotify.com/v1/artists/{id}/albums"

        params: AnyDict = {}
        if include_groups is not None:
            params["include_groups"] = include_groups
        if market is not None:
            params["market"] = market
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_an_artists_albums(id, include_groups, market, limit, offset)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_an_artists_top_tracks(self, id: str, market: str):
        """Get Spotify catalog information about an artist's top tracks by country.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-an-artists-top-tracks
        """
        url = f"https://api.spotify.com/v1/artists/{id}/top-tracks"

        params: AnyDict = {
            "market": market,
        }

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_an_artists_top_tracks(id, market)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_an_artists_related_artists(self, id: str):
        """Get Spotify catalog information about artists similar to a given artist. Similarity is based on analysis of
        the Spotify community's listening history.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-an-artists-related-artists
        """
        url = f"https://api.spotify.com/v1/artists/{id}/related-artists"

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
        if r.status_code != C.RESPONSE_OK:
            return self.get_an_artists_related_artists(id)
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def search(
        self, q: str, type: str, market: str = None, limit: int = None, offset: int = None, include_external: str = None
    ):
        """Get Spotify Catalog information about albums, artists, playlists, tracks, shows or episodes that match a
        keyword string.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-search
        """
        if limit is not None and not (1 <= limit <= 50):
            raise SpotifyClientError
        if offset is not None and not (0 <= offset <= 2000):
            raise SpotifyClientError
        if include_external is not None and include_external not in ("audio"):
            raise SpotifyClientError

        url = "https://api.spotify.com/v1/search"

        params: AnyDict = {
            "q": q,
            "type": type,
        }
        if market is not None:
            params["market"] = market
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if include_external is not None:
            params["include_external"] = include_external

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.search(q, type, market, limit, offset, include_external)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_an_episode(self, id: str, market: str = None):
        """Get Spotify catalog information for a single episode identified by its unique Spotify ID.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-an-episode
        """
        url = f"https://api.spotify.com/v1/episodes/{id}"

        params: AnyDict = {}
        if market is not None:
            params["market"] = market

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_an_episode(id, market)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_multiple_episodes(self, ids: List[str], market: str = None):
        """Get Spotify catalog information for several episodes based on their Spotify IDs.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-multiple-episodes
        """
        if 50 < len(ids):
            raise SpotifyClientError

        url = f"https://api.spotify.com/v1/episodes"

        params: AnyDict = {
            "ids": ",".join(ids),
        }
        if market is not None:
            params["market"] = market

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_multiple_episodes(ids, market)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()

    def get_users_top_artists_and_tracks(
        self, type: str, limit: int = None, offset: int = None, time_range: str = None
    ):
        """Get the current user's top artists or tracks based on calculated affinity.

        Reference:
            https://developer.spotify.com/documentation/web-api/reference-beta/#endpoint-get-users-top-artists-and-tracks
        """
        if type not in ("artists", "tracks"):
            raise SpotifyClientError
        if limit is not None and not (1 <= limit <= 50):
            raise SpotifyClientError
        if offset is not None and offset < 0:
            raise SpotifyClientError
        if time_range is not None and time_range not in ("long_term", "medium_term", "short_term"):
            raise SpotifyClientError

        if not self._oauth.is_scopes_subset(self._oauth.scopes, [S.USER_TOP_READ]):
            raise SpotifyScopeError

        url = f"https://api.spotify.com/v1/me/top/{type}"

        params: AnyDict = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if time_range is not None:
            params["time_range"] = time_range

        headers = {
            "Authorization": f"Bearer {self._oauth.token['access_token']}",  # type: ignore
            "Content-Type": "application/json",
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code == C.RESPONSE_UNAUTHORIZED:
            if not self._auto_refresh:
                return None
            self._oauth.refresh_token()
            return self.get_users_top_artists_and_tracks(type, limit, offset, time_range)
        if r.status_code != C.RESPONSE_OK:
            raise SpotifyResponseError(r.json()["message"])

        return r.json()
