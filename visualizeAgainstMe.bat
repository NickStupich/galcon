del debugLog.txt

::java -jar tools/PlayGame.jar maps/map53.txt 200 200 log.txt "python MyBot.py" "java -jar example_bots/RageBot.jar" | java -jar tools/ShowGame.jar
::java -jar tools/PlayGame.jar maps/map53.txt 200 200 log.txt "python MyBot.py" "java -jar example_bots/BullyBot.jar" | java -jar tools/ShowGame.jar
java -jar tools/PlayGame.jar maps/map53.txt 200 200 log.txt "python MyBot.py" "python MyBot1.py" | java -jar tools/ShowGame.jar


