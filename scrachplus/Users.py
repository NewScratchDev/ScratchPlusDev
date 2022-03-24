import requests
import json
from .UserProfiles import YourUserProfile, AnotherUserProfile
from .Project import YourProject, AnotherProject


class YourUser:
    def __init__(self, data, client):
        self.id = data["id"]
        self.username = data["username"]
        self.joined_timestamp = data["history"]["joined"]
        self.scratchteam = data["scratchteam"]
        self.profile = YourUserProfile(data["profile"], self)
        self._client = client
        self._headers = {
            "x-csrftoken": self._client.csrf_token,
            "X-Token": self._client.token,
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken="
                      + self._client.csrf_token
                      + ";scratchlanguage=en;scratchsessionsid="
                      + self._client.session_id
                      + ";",
            "referer": "https://scratch.mit.edu/users/" + self.username + "/",
        }

    def get_projects(self, all=False, limit=20, offset=0):
        if all:
            projects = []
            offset = 0
            while True:
                res = requests.get(
                    "https://api.scratch.mit.edu/users/"
                    + self.username
                    + "/projects/"
                    + "?limit=40&offset="
                    + str(offset)
                ).json()
                projects += res
                if len(res) != 40:
                    break
                offset += 40
            for x, i in enumerate(projects):
                projects[x].update({
                    "author": self.username
                })
            return [
                YourProject(i, self._client) if i["author"]["username"] == self._client.username else AnotherProject(i,
                                                                                                                     self._client)
                for i in projects]
        else:

            projects = requests.get(
                "https://api.scratch.mit.edu/users/"
                + self.username
                + "/projects/"
                + "?limit="
                + str(limit)
                + "&offset="
                + str(offset)
            ).json(),
            for x, i in enumerate(projects):
                projects[x].update({
                    "author": self.username
                })
            return [
                YourProject(i, self._client) if i["author"]["username"] == self._client.username else AnotherProject(i,
                                                                                                                     self._client)
                for i in projects]

    def get_curating(self, all=False, limit=20, offset=0):
        if all:
            studios = []
            offset = 0
            while True:
                res = requests.get(
                    "https://api.scratch.mit.edu/users/"
                    + self.username
                    + "/studios/curate"
                    + "?limit=40&offset="
                    + str(offset)
                ).json()
                studios += res
                if len(res) != 40:
                    break
                offset += 40
            return list(map(self._client._to_studio, studios))
        else:
            return list(
                map(
                    self._client._to_studio,
                    requests.get(
                        "https://api.scratch.mit.edu/users/"
                        + self.username
                        + "/studios/curate/"
                        + "?limit="
                        + str(limit)
                        + "&offset="
                        + str(offset)
                    ).json(),
                )
            )

    def get_favorites(self, all=False, limit=20, offset=0):
        if all:
            projects = []
            offset = 0
            while True:
                res = requests.get(
                    "https://api.scratch.mit.edu/users/"
                    + self.username
                    + "/favorites/"
                    + "?limit=40&offset="
                    + str(offset)
                ).json()
                projects += res
                if len(res) != 40:
                    break
                offset += 40
            for x, i in enumerate(projects):
                projects[x]["author"] = self.username
            return [
                YourProject(i, self._client) if i["author"]["username"] == self._client.username else AnotherProject(i,
                                                                                                                     self._client)
                for i in projects]

        else:
            return list(
                map(
                    self._client._to_project,
                    {
                        **requests.get(
                            "https://api.scratch.mit.edu/users/"
                            + self.username
                            + "/favorites/"
                            + "?limit="
                            + str(limit)
                            + "&offset="
                            + str(offset)
                        ).json(),
                        **{
                            "author": self.username
                        }}
                )
            )

    def get_followers(self, all=False, limit=20, offset=0):
        if all:
            users = []
            offset = 0
            while True:
                res = requests.get(
                    "https://api.scratch.mit.edu/users/"
                    + self.username
                    + "/followers/"
                    + "?limit=40&offset="
                    + str(offset)
                ).json()
                users += res
                if len(res) != 40:
                    break
                offset += 40
            return list(map(self._client._to_user, users))
        else:
            return list(
                map(
                    self._client._to_user,
                    requests.get(
                        "https://api.scratch.mit.edu/users/"
                        + self.username
                        + "/followers/"
                        + "?limit="
                        + str(limit)
                        + "&offset="
                        + str(offset)
                    ).json(),
                )
            )

    def get_following(self, all=False, limit=20, offset=0):
        if all:
            users = []
            offset = 0
            while True:
                res = requests.get(
                    "https://api.scratch.mit.edu/users/"
                    + self.username
                    + "/following/"
                    + "?limit=40&offset="
                    + str(offset)
                ).json()
                users += res
                if len(res) != 40:
                    break
                offset += 40
            return list(map(self._client._to_user, users))
        else:
            return list(
                map(
                    self._client._to_user,
                    requests.get(
                        "https://api.scratch.mit.edu/users/"
                        + self.username
                        + "/following/"
                        + "?limit="
                        + str(limit)
                        + "&offset="
                        + str(offset)
                    ).json(),
                )
            )

    def get_message_count(self):
        return requests.get(
            "https://api.scratch.mit.edu/users/" + self.username + "/messages/count/"
        ).json()["count"]

    def post_comment(self, content, parent_id="", commentee_id=""):
        data = {
            "commentee_id": commentee_id,
            "content": content,
            "parent_id": parent_id,
        }
        requests.post(
            "https://scratch.mit.edu/site-api/comments/user/" + self.username + "/add/",
            headers=self._headers,
            data=json.dumps(data),
        )

    def report(self, field):

        data = {"selected_field": field}
        requests.post(
            "https://scratch.mit.edu/site-api/users/all/" + self.username + "/report/",
            headers=self._headers,
            data=json.dumps(data),
        )

    def toggle_commenting(self):

        requests.post(
            "https://scratch.mit.edu/site-api/comments/user/"
            + self.username
            + "/toggle-comments/",
            headers=self._headers,
        )

    def follow(self):
        return requests.put(
            "https://scratch.mit.edu/site-api/users/followers/"
            + self.username
            + "/add/?usernames="
            + self._client.username,
            headers=self._headers,
        ).json()

    def unfollow(self):
        return requests.put(
            "https://scratch.mit.edu/site-api/users/followers/"
            + self.username
            + "/remove/?usernames="
            + self._client.username,
            headers=self._headers,
        ).json()


class AnotherUser:
    def __init__(self, data, client):
        self.id = data["id"]
        self.username = data["username"]
        self.joined_timestamp = data["history"]["joined"]
        self.scratchteam = data["scratchteam"]
        self.profile = AnotherUserProfile(data["profile"], self)
        self._client = client
        self._headers = {
            "x-csrftoken": self._client.csrf_token,
            "X-Token": self._client.token,
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken="
                      + self._client.csrf_token
                      + ";scratchlanguage=en;scratchsessionsid="
                      + self._client.session_id
                      + ";",
            "referer": "https://scratch.mit.edu/users/" + self.username + "/",
        }

    def get_projects(self, all=False, limit=20, offset=0):
        if all:
            projects = []
            offset = 0
            while True:
                res = requests.get(
                    "https://api.scratch.mit.edu/users/"
                    + self.username
                    + "/projects/"
                    + "?limit=40&offset="
                    + str(offset)
                ).json()
                projects += res
                if len(res) != 40:
                    break
                offset += 40
            for x, i in enumerate(projects):
                projects[x].update({
                    "author": self.username
                })
            return [
                YourProject(i, self._client) if i["author"]["username"] == self._client.username else AnotherProject(i,
                                                                                                                     self._client)
                for i in projects]
        else:

            projects = requests.get(
                "https://api.scratch.mit.edu/users/"
                + self.username
                + "/projects/"
                + "?limit="
                + str(limit)
                + "&offset="
                + str(offset)
            ).json(),
            for x, i in enumerate(projects):
                projects[x].update({
                    "author": self.username
                })
            return [
                YourProject(i, self._client) if i["author"]["username"] == self._client.username else AnotherProject(i,
                                                                                                                     self._client)
                for i in projects]

    def get_curating(self, all=False, limit=20, offset=0):
        if all:
            studios = []
            offset = 0
            while True:
                res = requests.get(
                    "https://api.scratch.mit.edu/users/"
                    + self.username
                    + "/studios/curate"
                    + "?limit=40&offset="
                    + str(offset)
                ).json()
                studios += res
                if len(res) != 40:
                    break
                offset += 40
            return list(map(self._client._to_studio, studios))
        else:
            return list(
                map(
                    self._client._to_studio,
                    requests.get(
                        "https://api.scratch.mit.edu/users/"
                        + self.username
                        + "/studios/curate/"
                        + "?limit="
                        + str(limit)
                        + "&offset="
                        + str(offset)
                    ).json(),
                )
            )

    def get_favorites(self, all=False, limit=20, offset=0):
        if all:
            projects = []
            offset = 0
            while True:
                res = requests.get(
                    "https://api.scratch.mit.edu/users/"
                    + self.username
                    + "/favorites/"
                    + "?limit=40&offset="
                    + str(offset)
                ).json()
                projects += res
                if len(res) != 40:
                    break
                offset += 40
            for x, i in enumerate(projects):
                projects[x]["author"] = self.username
            return [
                YourProject(i, self._client) if i["author"]["username"] == self._client.username else AnotherProject(i,
                                                                                                                     self._client)
                for i in projects]

        else:
            return list(
                map(
                    self._client._to_project,
                    {
                        **requests.get(
                            "https://api.scratch.mit.edu/users/"
                            + self.username
                            + "/favorites/"
                            + "?limit="
                            + str(limit)
                            + "&offset="
                            + str(offset)
                        ).json(),
                        **{
                            "author": self.username
                        }}
                )
            )

    def get_followers(self, all=False, limit=20, offset=0):
        if all:
            users = []
            offset = 0
            while True:
                res = requests.get(
                    "https://api.scratch.mit.edu/users/"
                    + self.username
                    + "/followers/"
                    + "?limit=40&offset="
                    + str(offset)
                ).json()
                users += res
                if len(res) != 40:
                    break
                offset += 40
            return list(map(self._client._to_user, users))
        else:
            return list(
                map(
                    self._client._to_user,
                    requests.get(
                        "https://api.scratch.mit.edu/users/"
                        + self.username
                        + "/followers/"
                        + "?limit="
                        + str(limit)
                        + "&offset="
                        + str(offset)
                    ).json(),
                )
            )

    def get_following(self, all=False, limit=20, offset=0):
        if all:
            users = []
            offset = 0
            while True:
                res = requests.get(
                    "https://api.scratch.mit.edu/users/"
                    + self.username
                    + "/following/"
                    + "?limit=40&offset="
                    + str(offset)
                ).json()
                users += res
                if len(res) != 40:
                    break
                offset += 40
            return list(map(self._client._to_user, users))
        else:
            return list(
                map(
                    self._client._to_user,
                    requests.get(
                        "https://api.scratch.mit.edu/users/"
                        + self.username
                        + "/following/"
                        + "?limit="
                        + str(limit)
                        + "&offset="
                        + str(offset)
                    ).json(),
                )
            )

    def get_message_count(self):
        return requests.get(
            "https://api.scratch.mit.edu/users/" + self.username + "/messages/count/"
        ).json()["count"]

    def post_comment(self, content, parent_id="", commentee_id=""):
        data = {
            "commentee_id": commentee_id,
            "content": content,
            "parent_id": parent_id,
        }
        requests.post(
            "https://scratch.mit.edu/site-api/comments/user/" + self.username + "/add/",
            headers=self._headers,
            data=json.dumps(data),
        )

    def report(self, field):

        data = {"selected_field": field}
        requests.post(
            "https://scratch.mit.edu/site-api/users/all/" + self.username + "/report/",
            headers=self._headers,
            data=json.dumps(data),
        )

    def follow(self):
        return requests.put(
            "https://scratch.mit.edu/site-api/users/followers/"
            + self.username
            + "/add/?usernames="
            + self._client.username,
            headers=self._headers,
        ).json()

    def unfollow(self):
        return requests.put(
            "https://scratch.mit.edu/site-api/users/followers/"
            + self.username
            + "/remove/?usernames="
            + self._client.username,
            headers=self._headers,
        ).json()
