HACKGAME_HELP = """

Hackgame CLI (Command Line Interface)

Hackgame is played via interacting with a central API, either manually via
typing in commands or by scripting. There are various different kinds of
in-game Objects. You play as one of these Objects, interacting with others.

"""


STATE_FILE_HELP = """

Path to a custom file location for storing client state (e.g. auth token). You
only need to set this if you want to run multiple hackgame command line
processes concurrently.

"""

OBJECT_TYPE_HELP = """

What is an "Object"?

An Object in hackgame is something that does things or has things done to it
via the API. Some conceptual hackgame things like Players (which represent
real-world people) and Tokens (which are for accessing the game) are not 
"Objects", as they are not intended to be scripted around and don't have
implementations for most of the available commands in hackgame (e.g. proxy,
post, etc.)

Every Object has:

- a "handle", a name it goes by, not necessarily unique
- a "public_uuid", a unique identifier for the Object
- a "private_uuid", anyone who knows this has admin rights over the Object
- ability to store "bytecoin", the currency in hackgame


Available Object Types:

ACCOUNT

an online presence, player or NPC-controlled

PROGRAM

ur phat l00t, ur equipment, the stuff that does cool things. Objects can have
installed programs that do unique things within the game. Usually found on
accounts, but not limited to this, any Object can have installed programs

NETWORK

virtual location where accounts are present. There is a tree structure of
networks in hackgame starting from a single top-level parent network.

CONNECTION

a link between two Objects, required for most in-game actions to take place.
Connections have a source and a destination, and allow the Objects on both
sides to initiate actions against each other.

ICE (Intrusion CountermeasurEs)

there are some horrible hackers out there, and ice is gonna protect you.
Ice is applied to either the source or destination of a Connection and before
actions can be taken (malicious or otherwise), ya need to break the ice. Ice
mostly comes into play as a result of having a Program that creates it
automatically when you initiate or receive a connection.

WORLD

planets/worlds in hackgame are distinct, each having their own internet
(known as a PAN, Planetary Area Network). Communication between worlds
is possible but limited. (Currently there is only one main world,
the same for all Players, however each player also has their own tutorial
world).

"""

ACTION_HELP = """

What is an "Action"?

hackgame provides a streamlined set of versatile commands, (known as Actions
to disambiguate from command-line commands such as hackgame login), to minimise
the amount of syntax you need to learn upfront to play. The goal is that every
Action can be used against every Object. Rather than spend time learning lots
of syntax, you can investigate the world by applying your set of commands in
new ways (e.g. Proxy-ing a Network rather than an Account).

The syntax of an Action (when run via the CLI) always includes the following:

hackgame [ACTION] [OBJECT_TYPE] <TARGET> <Action-Specific Options>

- ACTION (mandatory) being the name of an Action
- OBJECT_TYPE (mandatory) the type of Object you are taking the Action on
- TARGET (optional) being the public_uuid or a handle of an Object
- Action-Specific Options (optional) sometimes available to tweak the Action

GET

Get public info about any resource in the game. When called without a Target,
provides the public info about Objects you are currently aware of (e.g.
Networks you are on or adjacent to, Accounts you are, own or have a Connection
to)

CREATE

Create a new Object, such as an Account or Connection.

POST

Try to send data to an Object and get a synchronous response, in the same way 
you might POST data to a regular server. Object Types will respond to a Post 
Action differently, but generally responding to Post Actions is done to 
facilitate an in-game service, e.g. such as Networks, Ice, Connections, all 
provide.

PROXY

Change the Object identity that you are acting as. While you are logged into
hackgame with a Token, you are implicitly acting as an Object for every Action
that you take.

TRANSFER / MAIL / SEND (TODO decide on name)

Send data, an Object, or bytecoin, to another Object asynchronously, without
getting an immediate response.

"""
