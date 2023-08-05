# Standard library
import json
import re
from hashlib import md5


class Launchpad:
    """
    A collection of actions that can be performed against the Launchpad
    API, coupled with simple authentication logic.

    At the time of writing, this is basically about building snaps
    and building images.
    """

    system_codenames = {"16": "xenial", "18": "bionic"}
    board_architectures = {
        "raspberrypi2": {
            "core16": {"arch": "armhf", "subarch": "raspi2"},
            "core18": {"arch": "armhf", "subarch": "raspi3"},
            "classic16.04": {"arch": "armhf", "subarch": "raspi3"},
            "classic18.04": {"arch": "armhf", "subarch": "raspi3"},
        },
        "raspberrypi3": {
            "core16": {"arch": "armhf", "subarch": "raspi3"},
            "core18": {"arch": "armhf", "subarch": "raspi3"},
            "classic16.04": {"arch": "armhf", "subarch": "raspi3"},
            "classic18.04": {"arch": "armhf", "subarch": "raspi3"},
            "classic6418.04": {"arch": "arm64", "subarch": "raspi3"},
        },
        "raspberrypi4": {
            "core18": {"arch": "armhf", "subarch": "raspi3"},
            "classic18.04": {"arch": "armhf", "subarch": "raspi3"},
            "classic6418.04": {"arch": "arm64", "subarch": "raspi3"},
        },
        "intelnuc": {
            "core16": {"arch": "amd64", "subarch": ""},
            "core18": {"arch": "amd64", "subarch": ""},
        },
        "snapdragon": {
            "core16": {"arch": "arm64", "subarch": "snapdragon"},
            "core18": {"arch": "arm64", "subarch": "snapdragon"},
        },
        "cm3": {
            "core16": {"arch": "armhf", "subarch": "cm3"},
            "core18": {"arch": "armhf", "subarch": "raspi3"},
        },
    }

    def __init__(self, username, token, secret, session):
        """
        This requires a session object because in the normal use-case
        we will be passing through a `talisker.session.get_session()`
        """

        self.username = username
        self.session = session
        self.session.headers["Accept"] = "application/json"
        self.session.headers["Authorization"] = (
            f'OAuth oauth_version="1.0", '
            f'oauth_signature_method="PLAINTEXT", '
            f"oauth_consumer_key={username}, "
            f'oauth_token="{token}", '
            f'oauth_signature="&{secret}"'
        )

    def _request(self, path, method="GET", params={}, data={}):
        """
        Makes a raw HTTP request and returns the response.
        """

        url = f"https://api.launchpad.net/devel/{path}"

        response = self.session.request(method, url, params=params, data=data)
        response.raise_for_status()

        return response

    def build_image(self, board, system, snaps):
        """
        `board` is something like "raspberrypi3",
        `system` is something like "classic6418.04"
        """

        system_year = re.match(r"^[^\d]+(?:64)?(\d{2})(\.\d{2})?$", system)[1]
        codename = self.system_codenames[system_year]
        arch_info = self.board_architectures[board][system]
        project = "ubuntu-core"

        if system.startswith("classic"):
            project = "ubuntu-cpc"

        metadata = {"subarch": arch_info["subarch"], "extra_snaps": snaps}

        data = {
            "ws.op": "requestBuild",
            "pocket": "Updates",
            "archive": "https://api.launchpad.net/1.0/ubuntu/+archive/primary",
            "distro_arch_series": (
                "https://api.launchpad.net/1.0/ubuntu/"
                f"{codename}/{arch_info['arch']}"
            ),
            "metadata_override": json.dumps(metadata),
        }

        return self._request(
            path=(
                f"~{self.username.replace('.', '')}/"
                f"+livefs/ubuntu/{codename}/{project}"
            ),
            method="post",
            data=data,
        )

    def get_collection_entries(self, path, params=None):
        """
        Return collection items from the API
        """

        collection = self._request(path=path, params=params)

        return collection.json().get("entries", [])

    def get_snap_by_store_name(self, snap_name):
        """
        Return an Snap from the Launchpad API by store_name
        """

        snaps = self.get_collection_entries(
            path="+snaps",
            params={
                "ws.op": "findByStoreName",
                "owner": f"/~{self.username}",
                "store_name": snap_name,
            },
        )

        # The Launchpad API only allows to find by snaps by store_name
        # but we are only interested in the first one
        if snaps and snaps[0]["store_name"] == snap_name:
            return snaps[0]

        return None

    def get_snap(self, name):
        """
        Return a Snap from the Launchpad API by name
        """

        return self._request(
            path=f"~{self.username}/+snap/{name}", method="GET"
        ).json()

    def create_snap(self, snap_name, git_url, macaroon):
        """
        Create an ISnap in Launchpad
        """

        lp_snap_name = md5(git_url.encode("UTF-8")).hexdigest()

        data = {
            "ws.op": "new",
            "owner": f"/~{self.username}",
            "name": lp_snap_name,
            "store_name": snap_name,
            "git_repository_url": git_url,
            "git_path": "HEAD",
            "auto_build_archive": "/ubuntu/+archive/primary",
            "auto_build_pocket": "Updates",
            "processors": [
                "/+processors/amd64",
                "/+processors/arm64",
                "/+processors/armhf",
                "/+processors/i386",
                "/+processors/ppc64el",
                "/+processors/s390x",
            ],
            "store_series": "/+snappy-series/16",
            "store_channels": ["edge"],
            "store_upload": "true",
            "auto_build": "false",
        }

        self._request(path="+snaps", method="POST", data=data)

        # Authorize uploads to the store from this user
        data = {"ws.op": "completeAuthorization", "root_macaroon": macaroon}

        self._request(
            path=f"~{self.username}/+snap/{lp_snap_name}/",
            method="POST",
            data=data,
        )

        return True

    def is_snap_building(self, snap_name):
        """
        Return True is the snap is being build in Launchpad
        """
        lp_snap = self.get_snap_by_store_name(snap_name)
        request = self._request(
            path=lp_snap["pending_builds_collection_link"][32:]
        )
        return request.json()["total_size"] > 0

    def cancel_snap_builds(self, snap_name):
        """
        Cancel the builds if it is either pending or in progress.
        """
        lp_snap = self.get_snap_by_store_name(snap_name)
        builds = self.get_collection_entries(
            path=lp_snap["pending_builds_collection_link"][32:]
        )

        data = {"ws.op": "cancel"}

        for build in builds:
            self._request(
                path=build["self_link"][32:], method="POST", data=data
            )

        return True

    def build_snap(self, snap_name):
        """
        Create a new build for a Snap
        """

        lp_snap = self.get_snap_by_store_name(snap_name)
        channels = lp_snap.get("auto_build_channels")

        data = {
            "ws.op": "requestBuilds",
            "archive": lp_snap["auto_build_archive_link"],
            "pocket": lp_snap["auto_build_pocket"],
        }

        if channels:
            data["channels"] = channels

        self._request(path=lp_snap["self_link"][32:], method="POST", data=data)

        return True

    def get_snap_builds(self, snap_name):
        """
        Return list of builds from a Snap from the Launchpad API
        """
        lp_snap = self.get_snap_by_store_name(snap_name)
        builds = self.get_collection_entries(
            # Remove first part of the URL
            lp_snap["builds_collection_link"][32:]
        )

        return sorted(builds, key=lambda x: x["datecreated"], reverse=True)

    def get_snap_build(self, snap_name, build_id):
        """
        Return a Snap Build from the Launchpad API
        """
        lp_snap = self.get_snap_by_store_name(snap_name)

        return self._request(
            path=f"~{self.username}/+snap/{lp_snap['name']}/+build/{build_id}",
            method="GET",
        ).json()

    def get_snap_build_log(self, snap_name, build_id):
        """
        Return the log content of a snap build
        """
        build = self.get_snap_build(snap_name, build_id)

        response = self.session.request("GET", build["build_log_url"])
        response.raise_for_status()

        return response.text

    def delete_snap(self, snap_name):
        """
        Delete an ISnap in Launchpad
        """

        lp_snap = self.get_snap_by_store_name(snap_name)

        self._request(path=lp_snap["self_link"][32:], method="DELETE")

        return True
