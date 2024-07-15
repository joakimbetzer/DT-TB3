To create the rust project the using the tessla specification file and telegraf configuration file use the following command:
./TesslaTelegrafConnector -i ./monitoring.tessla -c ./telegraf.conf

To launch the program 'cd' into the "/outputRustProject" and run:

cargo run

For this project some things needs to be changed in the "main.rs" file:

Change

let workStringSome = workStringA.strip_prefix(" ");

to

let workStringSome = workStringA.strip_prefix(",");


Change

.strip_prefix(" ");

to

.strip_prefix(",");


After having run the rust project, the telegraf should be (re)started using the following command:

telegraf --config telegraf.conf
