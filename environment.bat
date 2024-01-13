@ECHO Off
REM Virtual Environment

SET prefix=J:\programs\anaconda3\envs\pollutants
start "BUILD" /B /wait conda env create -f environment.yml -p %prefix%
exit