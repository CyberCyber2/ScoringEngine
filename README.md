# ScoringEngine

This project was designed for scoring users/teams based on their ability to patch a vulnerable Windows or Linux image,
although most of the code here was written for Linux and Windows integration is a WIP.

The code runs on a local client, and an (optional) server(if teams are being used).
Every vulnerability a user fixes, increases their point count.
If teams are being used, the point count will be sent to a server for further processing.
