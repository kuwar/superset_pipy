# Introduction

Superset is a modern data exploration and visualization platform designed to be fast, intuitive, and powerful. 
It allows users to create interactive dashboards, explore datasets, and share insights seamlessly. This project 
provides a setup guide and essential commands to get started with Superset in a Python-based environment.
---

# System Requirements

- Python 3.11.12
---

# Setting up environment

- copy example.env to .env
- set up your environment variables in .env i.e. `cp example.env .env`
- in the terminal, from root directory, `source .env`
- create a virtual environment with python 3.11.12
---

# Commands to run Superset

```bash
<!-- initialize the database -->
superset db upgrade

<!-- Create an admin user in your metadata database (use `admin` as username to be able to load the examples) -->
superset fab create-admin

<!-- Load some data to play with -->
superset load_examples

<!-- Create default roles and permissions -->
superset init

<!-- start a development web server on port 8088, use -p to bind to another port -->
superset run --debug -p 8088 --with-threads --debugger
```
---

# Troubleshooting

- Consider [Error encounter and resolved](./note.md)
---

# References

- [Apache Superset](https://superset.apache.org/docs/intro)
---

# About Me
