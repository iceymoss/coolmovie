# -*- coding: utf-8 -*-
from application import manager
from flask_script import Server
# from controllers import index
from www import *
from jobs.launcher import runJob


# web server: python3 manager.py runserver
manager.add_command( "runserver",Server( host = "0.0.0.0",use_debugger=True,use_reloader= True, port=3000 ) )


# 启动job任务: python3 manager.py runjob -m movie
manager.add_command("runjob", runJob)


def main():
    manager.run()


if __name__ == "__main__":
    try:
        import sys
        sys.exit( main() )
    except Exception as e:
        import traceback
        traceback.print_exc()