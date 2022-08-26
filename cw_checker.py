"""Codewars Challnge Checker"""
import json
from time import sleep

import requests


def user_complete_challenge(
    codewars_id: str, challenge_slug: str, delay_between_request=2
) -> bool:
    """True if user compelete kata with a slug `challenge_slug`."""
    current_page = 0

    while True:
        payload = {"page": current_page}
        response_obj = requests.get(
            f"https://www.codewars.com/api/v1/users/{codewars_id}/code-challenges/completed",
            params=payload,
        )

        if response_obj.status_code == 200:
            response = response_obj.json()
            if "success" in response.keys() and not response["success"]:
                raise ValueError("api responds with '{}'".format(response["reason"]))
            if "data" not in response.keys():
                raise ValueError(
                    "api responds payload that does not contain 'data' key"
                )

            for kata in response["data"]:
                if kata["slug"] == challenge_slug:
                    return True

            # The target kata may not be on this page.
            if current_page + 1 - response["totalPages"] <= 0:
                # Reached the end of the pages.
                return False
            current_page += 1

        elif response_obj.status_code == 404:
            raise ValueError("cannot find user or challenge")

        sleep(delay_between_request)


def user_complete_n_challenges(codewars_id: str, n: int) -> bool:
    """True if user complete more than or equal to `n` katas. False otherwise."""
    payload = {"page": 0}
    response_obj = requests.get(
        f"https://www.codewars.com/api/v1/users/{codewars_id}/code-challenges/completed",
        params=payload,
    )

    if response_obj.status_code == 200:
        response = response_obj.json()
        if "success" in response.keys() and not response["success"]:
            raise ValueError("api responds with '{}'".format(response["reason"]))
        if "data" not in response.keys():
            raise ValueError("api responds payload that does not contain 'data' key")
        if "totalItems" not in response.keys():
            raise ValueError(
                "api responds payload that does not contain 'totalItems' key"
            )

        return response["totalItems"] >= n

    elif response_obj.status_code == 404:
        raise ValueError("cannot find user or challenge")


def get_line(path):
    with open(path, "r") as f:
        content = f.read()
        for idx, line in enumerate(content.split("\n")):
            if len(line.strip()) == 0:
                continue
            if line.strip()[0] == "#":
                continue

            columns = line.strip().split(",")

            if len(columns) < 2:
                raise ValueError(f"[error] expect two or more columns in the '{path}'")

            if idx == 0 and columns[0] == "handle":
                continue

            yield (columns[0], columns[1])


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Codewars Challenge Checker")
    parser.add_argument(
        "ids_file",
        metavar="IDs-file",
        help="A CSV file containing a column for email address handle, and a column for Codewars ID.",
    )
    parser.add_argument(
        "--slug",
        metavar="kata-slug",
        help="Check if user complete a kata with a slug of 'kata-slug'",
        default="",
        type=str,
    )
    parser.add_argument(
        "--n",
        metavar="N",
        help="Check if each user complete at least N katas.",
        default=0,
        type=int,
    )
    parser.add_argument(
        "--delay",
        metavar="DELAY",
        help="A delay before issue another request",
        default=2,
        type=int,
    )

    args = parser.parse_args()

    if len(args.slug) != 0:
        try:
            result = {}
            for email_handle, codewars_id in get_line(args.ids_file):
                result[email_handle] = user_complete_challenge(
                    codewars_id=codewars_id, challenge_slug=args.slug
                )
                sleep(args.delay)
            print(json.dumps(result))
        except ValueError as e:
            print(f"[error] expect two or more columns in the '{args.ids_file}'")

    elif args.n != 0:
        try:
            result = {}
            for email_handle, codewars_id in get_line(args.ids_file):
                result[email_handle] = user_complete_n_challenges(
                    codewars_id=codewars_id, n=args.n
                )
                sleep(args.delay)
            print(json.dumps(result))
        except ValueError as e:
            print(f"[error] expect two or more columns in the '{args.ids_file}'")
