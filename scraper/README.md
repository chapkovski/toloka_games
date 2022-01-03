## _Philipp Chapkovski_
# Interactive experiments in Toloka
## Getting real-time information about Toloka population composition

This module collects the data from Toloka regarding its online audience.

The main python code is located in `main.py`. 
The code is ran regurly (for the purpose of this paper every 15 minutes), using built-in crontab scheduler and a bash
script located in `task.sh`.

The second submodule collects the user profile info using assignment ids from oTree. It allows to associate user rating and
some other parameters publicly available in user profiles (such as gender, education, browser version etc. ) with the  responses 
collected in oTree during a study.
This module is in `user_scraper.py` file.

### Scraping the data about online presence.

The script file is `main.py`. The code works as follows:

- It loops through the `payload` folder and sends a content of each json file found there as a payload to the endpoint of Toloka that returns a number of currently active (online) users which satisfy the conditions described in a payload file. 
- Toloka requires that an id of the Project should be provided in a payload because it would filter out those participants who are blocked within a specific project. We used an empty project (id: 56044) where no pools were ran yet, so there were no blocked participants.
- Thus for replication, just use there any empty project id from your Toloka profile. 
- The obtained result is stored in `data/toloka_rt_data.csv` with *four* available columns:
  1. Column 1: Timestamp (in UTC)
  2. Column 2: Timestamp (as Unix epoch float number)
  3. Column 3: filename of the payload
  4. Column 4: Number of active users returned.

### Scraping information profiles of specific users.

This module (located in `user_scraper.py`) reads a csv file with assignments (usually obtained from oTree), gets a user id from the assignment id, and using this user id, obtains the full information available in this user Toloka profile.





