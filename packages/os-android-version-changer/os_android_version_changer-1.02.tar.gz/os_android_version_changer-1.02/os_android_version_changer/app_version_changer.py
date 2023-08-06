import fileinput
import sys
import re
import os_tools.logger_handler as lh


###########################################################################
#
# this module meant to change the version code and version name of an app
#
###########################################################################

def run(project_path, version_code, version_name):
    logger = lh.Logger(__file__)
    build_gradle_file = project_path + "/app/build.gradle"
    versions_dict = {'versionCode': version_code, 'versionName': version_name}
    for line in fileinput.input(build_gradle_file, inplace=1):
        for key in versions_dict:
            if key in line:
                first_position = re.search("[a-z]", line).start()
                val = versions_dict.get(key, "")
                if key == "versionName":
                    val = "\"" + versions_dict.get(key, "") + "\""
                    logger.info('app\'s version name changed to: ' + version_name)
                elif key == 'versionCode':
                    logger.info('app\'s code changed to: ' + version_code)
                line = line[:first_position] + key + " " + val + "\n"
        sys.stdout.write(line)
