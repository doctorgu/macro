cd c:\source\macro
CALL .venv\Scripts\activate.bat
IF %ERRORLEVEL% NEQ 0 (
    ECHO Error in batch
    EXIT /B %ERRORLEVEL%
)
python -m coupang.ad_cancel
