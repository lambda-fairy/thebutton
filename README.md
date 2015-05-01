# Button Presser MMXV

A script which presses [the button].

[the button]: https://www.reddit.com/r/thebutton/


## Dependencies

* Python 3.4

* [websockets](https://pypi.python.org/pypi/websockets)

* [PRAW](https://praw.readthedocs.org/)


## Setting up

Install websockets and PRAW:

    $ pip3 install websockets praw

Input your credentials:

    $ cat > praw.ini <<END
    [reddit]
    user: blahblahblah
    pswd: blahblahblah
    END

Run the script:

    $ python3 thebutton.py

By default, the script presses at 1 second. To change this limit, open up the script and edit the `TARGET` variable.


## Integrating with systemd

The script works well with [systemd]. An example unit file is provided (`thebutton.service`); the rest is left as an exercise.

[systemd]: http://www.freedesktop.org/wiki/Software/systemd/
