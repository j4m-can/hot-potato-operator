# Hot Potato Operator

## Description

This operator fulfills the requirements of the HPC Team Hot Potato
exercise.

This operator works along the lines of the hot potato game:

* multiple players
* a hot-potato (object) is passed from one player to any other
* this happens until the maximum number of passes allowed

### How It Works

This operator uses the leader as a mediator of the "latest" information
and uses the application bucket to store it and units determine their
next step based on it.

All units are part of the pool that can receive and pass the potato.
Each unit has its own unit information:

* `next_owner` - next unit elected to get the potato
* `next_total_passes` - updated total passes for next unit
* `npasses` - number of passes handled by unit

The leader manages application information:

* `owner` - elected owner
* `running` - flag to indicate/allow running or not
* `total_passes` - total number of passes handled by all units

When an application event occurs, each unit peeks at the application
"owner" setting. If it matches the unit, the unit then elects the next
owner and updates the `next_owner` value, increments its own `npasses`
by 1, and updates the the `next_total_passes` by 1.

When a unit event occurs, *only* the leader takes action and updates
the application information based on the updated unit information. At
which point, the units are notified of another application event.

The leader is used to manage the transactions rather than having each
of the units peek into each other's buckets (which can also work).

The status message contains application information (leader only) and
unit information (non-leaders).

### Kinds of Operators

There are 2 versions:

* uses `hpctlib` Interface/SuperInterface (`charmiface.py`)
* standard, non-interface/superinterface (`charmnoiface.py`)

These provide a way to compare the interface and non-interface
approaches.

## Usage

### To Deploy and Set Up

For 3 "players":

1. `juju deploy <charmfile> -n 3`
2. `juju run-action hot-potato/leader configure owner=<unit> --wait`
3. `juju run-action hot-potato/leader run run=true --wait`
4. `juju status`

At this point, everything is ready. See Control to run.

### Configuration

The configuration settings can be done at any time, but likely makes
more sense before the `run` action is invoked.

To set a "starting" owner:

```
juju run-action hot-potato/leader configure owner=<unit> --wait
```

To set delay (in seconds):

```
juju run-action hot-potato/leader configure delay=<float> --wait
```

To set max passes:

```
juju run-action hot-potato/leader configure max_passes=<max> --wait
```

### Control

Control is done via the leader only.

To start:

```juju run-action hot-potato/leader run run=true --wait```

To stop:

```juju run-action hot-potato/leader run run=false --wait```
