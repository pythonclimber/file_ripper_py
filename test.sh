source /users/asmitty/workspace/my_envs/file_ripper-env/bin/activate


echo '\n\nRunning fileconstants.py'
python /users/asmitty/workspace/file_ripper-py/file_ripper/fileconstants.py
echo 'Completed fileconstants.py\n\n'


echo 'Running filedefinition.py'
python /users/asmitty/workspace/file_ripper-py/file_ripper/filedefinition.py
echo 'Completed filedefinition.py\n\n'


echo 'Running fileservice'
python /users/asmitty/workspace/file_ripper-py/file_ripper/fileservice.py
echo 'Completed fileservice\n\n'


echo 'Running process'
python /users/asmitty/workspace/file_ripper-py/file_ripper/process.py
echo 'Completed process\n\n'


echo 'Running dataexport'
python /users/asmitty/workspace/file_ripper-py/file_ripper/dataexport.py
echo 'Completed dataexport\n\n'


echo 'Running databaseutils'
python /users/asmitty/workspace/file_ripper-py/file_ripper/databaseutils.py
echo 'Completed databaseutils\n\n'


echo 'Running __main__.py'
python /users/asmitty/workspace/file_ripper-py/file_ripper/__main__.py
echo 'Completed __main__.py\n\n'


deactivate
