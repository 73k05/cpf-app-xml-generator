# Write in Log file
def write_log(log_message):
    if isinstance(log_message, str):
        try:
            f = open("output.log", "a+")
            # Do something with the file
        except IOError:
            # print("File not accessible")
            f = open("output.log", "w+")

        f.write(log_message)
        f.write("\r\n")
        f.close()
    return


# Write in Log file
def write_server_log(log_message):
    # print(log_message)
    if isinstance(log_message, str):
        try:
            f = open("server.log", "a+")
            # Do something with the file
        except IOError:
            # print("File not accessible")
            f = open("server.log", "w+")

        f.write(log_message)
        f.write("\r\n")
        f.close()
    return
