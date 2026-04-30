# Big-Log:
BIG-LOG
Hadoop-Based Industrial IoT Log Aggregator
Complete Demo and Command Guide

Purpose: This document gives the complete flow for opening WSL, switching to the Hadoop user, starting Hadoop, accessing HDFS/YARN from the browser, and showing the generated BIG-LOG project data during a professor demo.
Item	Value
Operating environment	WSL Ubuntu on Windows
Hadoop version used	Hadoop 3.4.3
Linux user used for Hadoop	hadoop
Project folder	~/big-log-project
HDFS project path	/biglog
Main dataset	/biglog/input/sensor_logs.csv

 
1. What This Project Does
BIG-LOG simulates Industrial IoT sensor logs from factory machines, stores those logs in HDFS, and processes them using Hadoop Streaming MapReduce. The dataset includes timestamp, sensor ID, sensor type, sensor value, factory, production line, and status.
The demo proves that data was generated locally, uploaded into HDFS, processed by Hadoop MapReduce, and viewed through both terminal commands and Hadoop web interfaces.
Feature	What it shows
Status count	Counts OK, WARN, and ERROR readings.
Factory error count	Counts ERROR readings per factory.
Average per factory and overall	Calculates average sensor values for each factory and also overall.
HDFS web browsing	Shows the project input and output files through the NameNode UI.
YARN job tracking	Shows completed MapReduce jobs through the ResourceManager UI.

2. Complete Demo Flow From Laptop Startup
Use this section when you open your laptop and want to prepare the project for a live demo.
Step 1: Open WSL Ubuntu
Open Ubuntu/WSL from the Windows Start Menu or Windows Terminal.
Step 2: Switch to the Hadoop user
sudo su - hadoop
What it does: switches from your normal Linux user, such as daniyal, into the hadoop user. Your Hadoop installation and environment variables are configured under this user, so the project should be run from here.
Check that you are now the Hadoop user:
whoami
Expected output:
hadoop
Step 3: Confirm Hadoop is available
hadoop version
What it does: confirms that Hadoop is installed and accessible from the terminal. In your setup it showed Hadoop 3.4.3.
Step 4: Go to the project folder
cd ~/big-log-project
What it does: opens your BIG-LOG project directory where your data, scripts, and results folders are stored.
Step 5: Start Hadoop services
start-dfs.sh
start-yarn.sh
What these commands do:
Command	Meaning
start-dfs.sh	Starts HDFS services such as NameNode, DataNode, and SecondaryNameNode. HDFS is used to store your project files.
start-yarn.sh	Starts YARN services such as ResourceManager and NodeManager. YARN is used to run Hadoop MapReduce jobs.

Step 6: Check running services
jps
Expected processes:
NameNode
DataNode
SecondaryNameNode
ResourceManager
NodeManager
Jps
What it does: lists Java processes running in WSL. If these Hadoop services appear, your Hadoop system is ready for the demo.
 
3. Access Hadoop in the Web Browser
Open these URLs in your Windows browser, such as Chrome or Edge. Make sure Hadoop services are running first.
Web interface	URL	Purpose
NameNode / HDFS UI	http://localhost:9870	Shows HDFS storage, files, directories, and DataNodes.
YARN ResourceManager UI	http://localhost:8088	Shows MapReduce/YARN jobs, job status, completed jobs, and logs.

If localhost does not open, run this in WSL:
hostname -I
Then open the same ports using the WSL IP address, for example:
http://172.xx.xx.xx:9870
http://172.xx.xx.xx:8088
How to browse your project files in HDFS Web UI
Step	Action
1	Open http://localhost:9870
2	Click Utilities.
3	Click Browse the file system.
4	Enter /biglog in the path box.
5	Open input or output folders, such as /biglog/input or /biglog/output_status.

Useful HDFS paths for demo
HDFS path	What to show
/biglog/input/sensor_logs.csv	Original generated sensor log dataset.
/biglog/output_status/part-00000	Output for OK/WARN/ERROR count.
/biglog/output_factory_errors/part-00000	Output for factory-wise ERROR count.
/biglog/output_avg_factory_overall/part-00000	Output for average values per factory and overall.

4. Check the Generated Data
These commands prove that your generated data exists locally and inside HDFS.
Check local generated CSV
head data/sensor_logs.csv
What it does: shows the first few rows of the local CSV file.
Check uploaded file in HDFS
hdfs dfs -ls /biglog/input
What it does: lists files inside the HDFS input folder.
hdfs dfs -cat /biglog/input/sensor_logs.csv | head
What it does: displays the first few rows of the CSV directly from HDFS, proving that the data is stored in Hadoop.
Dataset columns
Column	Meaning
timestamp	Time of sensor reading.
sensor_id	Unique sensor identifier.
sensor_type	Type of reading: temperature, humidity, pressure, or vibration.
value	Numeric reading from the sensor.
factory	Factory name such as Factory-A, Factory-B, Factory-C, or Factory-D.
line	Production line number such as Line-1, Line-2, Line-3, or Line-4.
status	Reading status: OK, WARN, or ERROR.

5. Run and Show Status Count Analysis
This analysis counts how many records are OK, WARN, and ERROR.
Run the MapReduce job
export STREAMING_JAR=/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.3.jar

hdfs dfs -rm -r -f /biglog/output_status

hadoop jar $STREAMING_JAR \
-file scripts/status_mapper.py \
-file scripts/status_reducer.py \
-input /biglog/input/sensor_logs.csv \
-output /biglog/output_status \
-mapper status_mapper.py \
-reducer status_reducer.py
What these commands do:
Command part	Meaning
export STREAMING_JAR=...	Stores the Hadoop Streaming JAR path in a variable so you can run Python mapper/reducer jobs.
hdfs dfs -rm -r -f /biglog/output_status	Deletes the old output folder. Hadoop requires the output folder to not already exist.
hadoop jar $STREAMING_JAR	Starts a Hadoop Streaming MapReduce job.
-file scripts/status_mapper.py	Sends the mapper Python file to Hadoop worker nodes.
-file scripts/status_reducer.py	Sends the reducer Python file to Hadoop worker nodes.
-input /biglog/input/sensor_logs.csv	Uses the HDFS CSV file as input.
-output /biglog/output_status	Writes the MapReduce output to this HDFS folder.
-mapper status_mapper.py	Runs the mapper that emits status values such as OK, WARN, ERROR.
-reducer status_reducer.py	Runs the reducer that adds counts for each status.

View output
hdfs dfs -cat /biglog/output_status/part-00000
Expected output from your project:
ERROR   11937
OK      25195
WARN    12868
Save output locally
hdfs dfs -cat /biglog/output_status/part-00000 > results/status_result.txt
cat results/status_result.txt
6. Run and Show Factory Error Count Analysis
This analysis counts how many ERROR readings occurred in each factory. It helps identify which factory has more machine/sensor problems.
hdfs dfs -rm -r -f /biglog/output_factory_errors

hadoop jar $STREAMING_JAR \
-file scripts/factory_error_mapper.py \
-file scripts/factory_error_reducer.py \
-input /biglog/input/sensor_logs.csv \
-output /biglog/output_factory_errors \
-mapper factory_error_mapper.py \
-reducer factory_error_reducer.py
View and save output
hdfs dfs -cat /biglog/output_factory_errors/part-00000
hdfs dfs -cat /biglog/output_factory_errors/part-00000 > results/factory_error_result.txt
Explanation: the mapper only selects rows where status is ERROR, then emits the factory name with value 1. The reducer adds all values for each factory.
7. Run and Show Average Per Factory and Overall
This analysis is useful for showing averages for all sensor attributes, both factory-wise and overall. It produces keys such as Factory-A_temperature and OVERALL_temperature.
hdfs dfs -rm -r -f /biglog/output_avg_factory_overall

hadoop jar $STREAMING_JAR \
-file scripts/avg_factory_overall_mapper.py \
-file scripts/avg_factory_overall_reducer.py \
-input /biglog/input/sensor_logs.csv \
-output /biglog/output_avg_factory_overall \
-mapper avg_factory_overall_mapper.py \
-reducer avg_factory_overall_reducer.py
View and save output
hdfs dfs -cat /biglog/output_avg_factory_overall/part-00000
hdfs dfs -cat /biglog/output_avg_factory_overall/part-00000 > results/avg_factory_overall_result.txt
Example output format:
Factory-A_humidity        57.40
Factory-A_pressure        114.82
Factory-A_temperature     75.22
Factory-A_vibration       40.10
OVERALL_humidity          57.62
OVERALL_pressure          114.97
OVERALL_temperature       75.08
OVERALL_vibration         39.96
Explanation: for every input row, the mapper emits two records: one for factory-level average and one for overall average. The reducer adds all values and divides by count to calculate the final average.
8. Commands to Access All Results Together
List all HDFS project folders
hdfs dfs -ls /biglog
Useful output folders:
Folder	Meaning
/biglog/input	Contains original sensor_logs.csv.
/biglog/output_status	Contains status count result.
/biglog/output_factory_errors	Contains factory-wise error count result.
/biglog/output_avg_factory_overall	Contains average per factory and overall result.

Display all HDFS results
echo "===== STATUS COUNT ====="
hdfs dfs -cat /biglog/output_status/part-00000

echo "===== FACTORY ERRORS ====="
hdfs dfs -cat /biglog/output_factory_errors/part-00000

echo "===== FACTORY + OVERALL AVERAGES ====="
hdfs dfs -cat /biglog/output_avg_factory_overall/part-00000
Display all locally saved result files
ls results
cat results/status_result.txt
cat results/factory_error_result.txt
cat results/avg_factory_overall_result.txt
9. Optional: Regenerate and Re-upload Data
Use this only if you want to create a fresh dataset. If you regenerate data, your output numbers will change.
cd ~/big-log-project/scripts
python3 generate_logs.py

cd ~/big-log-project
hdfs dfs -put -f data/sensor_logs.csv /biglog/input/
Command	Meaning
python3 generate_logs.py	Creates a new local CSV dataset with simulated industrial sensor readings.
hdfs dfs -put -f ...	Uploads the new CSV to HDFS and overwrites the existing one.

10. Full One-Time Demo Command Sequence
Use this sequence during demo preparation. It assumes your scripts already exist.
sudo su - hadoop
cd ~/big-log-project
source ~/.bashrc

start-dfs.sh
start-yarn.sh
jps

export STREAMING_JAR=/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.4.3.jar

hdfs dfs -ls /biglog/input
hdfs dfs -cat /biglog/input/sensor_logs.csv | head

hdfs dfs -rm -r -f /biglog/output_status
hadoop jar $STREAMING_JAR -file scripts/status_mapper.py -file scripts/status_reducer.py -input /biglog/input/sensor_logs.csv -output /biglog/output_status -mapper status_mapper.py -reducer status_reducer.py
hdfs dfs -cat /biglog/output_status/part-00000

hdfs dfs -rm -r -f /biglog/output_factory_errors
hadoop jar $STREAMING_JAR -file scripts/factory_error_mapper.py -file scripts/factory_error_reducer.py -input /biglog/input/sensor_logs.csv -output /biglog/output_factory_errors -mapper factory_error_mapper.py -reducer factory_error_reducer.py
hdfs dfs -cat /biglog/output_factory_errors/part-00000

hdfs dfs -rm -r -f /biglog/output_avg_factory_overall
hadoop jar $STREAMING_JAR -file scripts/avg_factory_overall_mapper.py -file scripts/avg_factory_overall_reducer.py -input /biglog/input/sensor_logs.csv -output /biglog/output_avg_factory_overall -mapper avg_factory_overall_mapper.py -reducer avg_factory_overall_reducer.py
hdfs dfs -cat /biglog/output_avg_factory_overall/part-00000
11. What to Say During Demo
You can say the following in simple words:
My project is BIG-LOG, a Hadoop-based Industrial IoT log aggregation system. It simulates factory sensor logs such as temperature, humidity, pressure, and vibration. The generated logs are uploaded into HDFS for distributed storage. Then I run Hadoop Streaming MapReduce jobs to analyze the data. The project calculates OK/WARN/ERROR counts, error count per factory, and average sensor readings per factory and overall. I can also show the stored input and output files through the Hadoop NameNode web interface and the completed jobs through the YARN ResourceManager interface.
12. Screenshot Checklist for Submission
No.	Screenshot to take
1	Terminal showing sudo su - hadoop and hadoop version.
2	jps showing NameNode, DataNode, ResourceManager, NodeManager, SecondaryNameNode.
3	hdfs dfs -ls /biglog/input showing sensor_logs.csv.
4	hdfs dfs -cat /biglog/input/sensor_logs.csv | head showing sample data.
5	Hadoop MapReduce job completion in terminal.
6	hdfs dfs -cat /biglog/output_status/part-00000 showing OK/WARN/ERROR counts.
7	http://localhost:9870 showing NameNode UI.
8	http://localhost:9870 file browser showing /biglog folder.
9	http://localhost:8088 showing YARN jobs.

13. Common Problems and Fixes
Problem	Solution
hadoop: command not found	You are probably in the wrong Linux user. Run sudo su - hadoop, then try hadoop version again.
NativeCodeLoader warning	This is only a warning. Hadoop will use built-in Java classes. You can ignore it for this project.
Output path already exists	Run hdfs dfs -rm -r -f /biglog/output_folder_name before rerunning the job.
No such file or directory for part-00000	The MapReduce job did not complete successfully or the output folder name is wrong. Check the terminal output and YARN UI.
localhost:9870 does not open	Make sure start-dfs.sh was run and jps shows NameNode. If needed, use hostname -I and open http://WSL_IP:9870.
localhost:8088 does not open	Make sure start-yarn.sh was run and jps shows ResourceManager.
Could not find MRAppMaster	Fix mapred-site.xml by adding HADOOP_MAPRED_HOME settings, then restart DFS and YARN.

14. Important Notes
Do not run the project from the daniyal user if Hadoop commands are not configured there. Use sudo su - hadoop first.
The local test using cat data/sensor_logs.csv | mapper | sort | reducer proves your Python logic is correct. The Hadoop run proves the same logic works through HDFS and MapReduce.
If you regenerate the dataset, the counts and averages will change. This is normal because the data is randomly generated.
For grading, focus on showing the complete big data pipeline: data generation, HDFS storage, MapReduce processing, HDFS output, and web UI proof.
Appendix A: Key Script Purposes
Script	Purpose
generate_logs.py	Generates 50,000 fake Industrial IoT sensor log rows.
status_mapper.py	Reads each row and emits status with count 1.
status_reducer.py	Adds counts for each status.
factory_error_mapper.py	Emits factory name only for ERROR rows.
factory_error_reducer.py	Adds ERROR counts for each factory.
avg_factory_overall_mapper.py	Emits factory-level and overall keys with value,count pairs.
avg_factory_overall_reducer.py	Calculates averages by dividing total value by total count.

