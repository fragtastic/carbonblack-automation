# carbonblack-automation
Automatically assign the `sensor policy` of `REGISTERED` sensors. Sensors that are not `REGISTERED` will not be modified.
This readme assumes that the environment is either Linux or MacOS.
By default this program will attempt to place sensors in both the `Standard` and `Unknown` policies into appropriate policies.

## Requirements
Python3 must be installed and binary/alias `python3` available in `$PATH`.

## Install
Each of the following sections is required before running the program.

Mark `setup.sh` and `run.sh` as executable with `chmod +x setup.sh run.sh`

### Environment
Run `setup.sh` or manually set up environment.
Running `setup.sh` multiple times is safe. This will upgrade the virtual environment and dependencies in place.

### Credentials
Program uses the `[psc]` section of `.carbonblack/credentials.psc`.
Copy `credentials.psc.example` to `.carbonblack/credentials.psc` then modify where needed.


### Sensor Policies
Examine `mappings.py` for the policy types that are used.

Create sensor policies where needed. Note the policy ID of each, including `Standard`.

In Firefox, the policy ID can be easily found opening the `Network` tab of the `Web Developer` tools. Clicking on each of the policies in the policy tab of the CarbonBlack console should show an `XHR` method and then a number next to it corresponding to the policy ID. This can be done in Chrome too using the equivalent tool menu.

### Mapping
Rename `mappings.py.example` to `mappings.py`.

Modify sensor policy IDs inside `mapping.py` to match whatever is being used.

Modify `OrganizationalUnits.DOMAIN_CONTROLLER` to match what is currently being used.

### Execution
The following are good ideas to ensure success.
- Create a dedicated user for this program
- Modify `crontab` for that user to execute `run.sh` at a given interval. (Assuming this is being run on a Linux or MacOS environment)

## Run
Loading of the virtual environment and execution of the program is handled by `run.sh`.

Execute `run.sh`.

Output should look something like this.
```
Activated virtual environment
INFO:root:Number of devices found 5
Changing policy for device deviceID:123456781 from "12341" to "12342"
Changing policy for device deviceID:123456782 from "12341" to "12343"
Changing policy for device deviceID:123456783 from "12341" to "12342"
INFO:root:Number of devices assigned 3
```
