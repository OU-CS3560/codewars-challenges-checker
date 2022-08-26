# Design Specification

## Overview

User provides list of Codewars IDs and challenges slug to the program. The program reports if a user has completed the challenge or not.

## Input Data

CSV file of the user OHIO email handle and Codewars user ID. For example

```csv
emailHandle,codewars-id
bc180403,ou-bobcat
```

## API Endpoints Available

Codewars provides an API for the list of completed challenges for a user. This is avaiable at

```plain
https://www.codewars.com/api/v1/users/{user}/code-challenges/completed?page={page}
```

The documentation is available at [https://dev.codewars.com/#list-completed-challenges](https://dev.codewars.com/#list-completed-challenges).

The following is an example of making a request to the endpoint using curl.

```console
$ curl -sL https://www.codewars.com/api/v1/users/krerkkiat/code-challenges/completed\?page\=0 | jq .
{
  "totalPages": 1,
  "totalItems": 175,
  "data": [
    {
      "id": "5ae62fcf252e66d44d00008e",
      "name": "Expressions Matter ",
      "slug": "expressions-matter",
      "completedLanguages": [
        "haskell"
      ],
      "completedAt": "2021-06-20T00:22:41.457Z"
    },
    ... # output is truncated.
    {
      "id": "54ba84be607a92aa900000f1",
      "name": "Isograms",
      "slug": "isograms",
      "completedLanguages": [
        "python",
        "cpp"
      ],
      "completedAt": "2021-01-19T19:27:14.624Z"
    },
    {
      "id": "541c8630095125aba6000c00",
      "name": "Sum of Digits / Digital Root",
      "slug": "sum-of-digits-slash-digital-root",
      "completedLanguages": [
        "python",
        "cpp",
        "java",
        "haskell",
        "ruby"
      ],
      "completedAt": "2021-01-19T18:48:26.529Z"
    },
    {
      "id": "50654ddff44f800200000004",
      "name": "Multiply",
      "slug": "multiply",
      "completedLanguages": [
        "python",
        "cpp",
        "ruby",
        "haskell",
        "javascript",
        "commonlisp"
      ],
      "completedAt": "2021-01-19T16:03:19.253Z"
    }
  ]
}
```

## Justification for choosing Python

C++ was the original language. However, the unconventional method of pacakaging of the expected dependencies
are posing more problem than anticipated. The problem seems to be that the dependencies do not have `install`
command, and `packageProject` requires that all dependencies are installed.

Python will be the easiest to implement the solution with its native support of JSON and CSV data format. Python also has
strong HTTP client library (notably `requests`).

Thus, Python will be used instead of the C++ even though C++ due to time constraint.

## Expected Tools and Libraries

### HTTP Client Library

- requests

### Core data processing libraries 

- json (builtin)
- csv / manual text processing

## User Stories

*Assumptions*

- User already built the executable file for the program.

Bobcat creates a CSV file with the student OHIO email handle and corresponding Codewars user ID.
Then Bobcat runs the program and give it the CSV file along with the challenge slug for this week homework assignment.

For each Codewars user ID the program found in the CSV file, it makes a request to Codewars API endpoint and retrived the
list of completed challenges. It serach the list for the challenge slug given by the user. If said challenge is not found,
the program query for more pages (if any). If said challenge is not found when the last page is searched, program report
that the student did not complete the challenge.

If the challenge slug is found in one of the page, the program reports that the student had completed the challenge. When the
matching challenge slug is found or the last page is reached, the program report the status and move to the next student.
