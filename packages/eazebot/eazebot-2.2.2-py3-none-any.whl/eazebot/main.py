import argparse


# execute main if running as script
def main(sysargv = None):
    parser = argparse.ArgumentParser(description='Processes input to eazebot main function.')
    parser.add_argument('--init', dest='init', action='store_true', required=False,
                        help='copies the necessary user config files to the current directory')
    parser.add_argument('--config', dest='config', action='store_true', required=False,
                        help='calls a dialog to fill out the configs interactively')
    parser.add_argument('--no-warning', dest='warning', action='store_false', required=False,
                        help='does not warn for preexisting config files when running the --init flag')
    args = parser.parse_args(sysargv)

    if args.init:
        from eazebot.auxiliaries import copy_init_files
        copy_init_files(warning=args.warning)
    elif args.config:
        from eazebot.auxiliaries import start_config_dialog
        start_config_dialog()
    else:
        from eazebot.bot import EazeBot
        EazeBot().start_bot()


if __name__ == '__main__':
    main()
