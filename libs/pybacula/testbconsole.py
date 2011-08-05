import bconsole

def main():
    bconsole.set_configfile("/etc/bacula/bconsole.conf")
    bconsole.connect()
    print bconsole.execute_command("status dir=linconet-dir")
    bconsole.close()


if __name__ == "__main__":
    main()
