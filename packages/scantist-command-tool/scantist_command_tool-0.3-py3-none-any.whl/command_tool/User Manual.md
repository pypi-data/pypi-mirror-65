# Manual

Make sure scantist-bom-detect.jar is is in the same folder as scantist-cmd.py.
Currently we have two authorization method for the script.

Set up config file

BASE_URL (e.g.): http://localhost:8000

EMAIL (e.g.): test@scantist.com (not necessary when you have api key)

PASSWORD (e.g.): abcd1234 (not necessary when you have api key)

OAUTH_TOKEN (e.g.): ab6d1234bzbwwd0f6cfef1234567eb6ce339ca2b (not necessary when you have api key)

SCANTIST_TOKEN(e.g.): af12345c-123b-89e4-a123-01abc123a1a1 (not necessary when you have api key)

API_KEY (e.g.): eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoic2xpZGluZyIsImV4cCI6MTU3ODE5MzU0NCwianRpIjoiNjljMDQxNDhjOWM4NDRlNzgxZGMzMWRmYjgzZGNjODAiLCJyZWZyZXNoX2V4cCI6MTU3NzkzNDM0NCwidXNlcl9pZCI6M30.xz2_Bj8qN4i4beyVAecMpiMS_MQV5V46jelhBj33IRM

## Obtain and Save $apikey and $scantist_token
- python3 authenticate.py -b $base_url -e $email -p $password


## Binary Scan
【set up baseurl, apikey in config file】
- python3 scantist_cmd.py -t binary -f $local_file_path 

- optional parameter: 
        
        -r [csv|pdf]: download scan report
        
        -v          : set the version of the project
        
        -p          : set the project name. if this parameter is null, will use file name as project name
        
        -j          : project id.
        
file + version -> create new project, name by file.【if duplicate name project exist, will update the project】

file + version + project_name -> create new project, name by the project_name.

local_binary_file + version + project_id -> create new version of existing project.

project_id -> scan existing project.

## Source code scan
【set up baseurl, apikey】
- python3 scantist_cmd.py -t source_code -f $local_file_path 

- optional parameter :

        -r [csv|pdf]: download scan report
        
## List user projects
【set up baseurl, apikey】
- python3 scantist_cmd.py -l


## Download scan result
Generate and download the most recent scan report if no $project_id given
【set up baseurl, apikey】

- python3 scantist_cmd.py -r ["csv"|"pdf"]

- optional parameter:

        -j  : project id.
