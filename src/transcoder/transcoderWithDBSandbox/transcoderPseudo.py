
interval = 0
increaseInterval = 0.1
maxInterval = 2
maxProcessingTime = 88888888888888888888888888
stderror 
stdout

while(! popen.poll())
    sleep(interval)

    Popen.communicate(input=None)
    append the output to stderror and stdout
    
    if interval < maxInterval:
        interval += increaseInterval

    if "processing time" > maxProcessingTime:
        kill
        exit code = 1000
        append text to standard error.
        break

        

======================================


#main
Identify file type(s)

if no file types, run default command - copy/northing/parameter

for each file type, get commands/grouping.
    Class commands, id
    dic, gouping pointer to command class object.
    dic, based on id (no duplicates) of command class objects

for every Command in the dictionary
    run the command.
    store the exit code in the command object
    
dic, exit code grouping.
for each item in the grouping dictionary
    if grouping in exit code grouping.
        UPDATE it.
    else
        create it.
        
compute exit code base on exit code grouping
exit

