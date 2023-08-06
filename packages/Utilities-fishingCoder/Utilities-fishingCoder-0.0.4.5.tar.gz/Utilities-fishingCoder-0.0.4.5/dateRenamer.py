#! python3
"""Rename files with dates in their names to either European or American style"""
import os, shutil, re
os.chdir('/media/max/Asus C/Users/Max Fritzler/Documents/TestFiles')

# TODO: # Create a regex to match files with American date format, assuming numbers only not names
# Validate with regex101.com and SET THE FLAG to multiline and ignore whitespace
reAmericanDate = re.compile(r"""
    ^(\D*?)           # All non-digit text before first number
    (([01])?\d)       # The month
    ([\-./\\])        # separator
    ([0123]?\d)       # The day
    ([\-./\\])        # separator
    ([12]\d(\d{2})?)  # The year
    (.*)              # any remaining text
    """, re.VERBOSE)

test_str = "prefix 02/03/1922 suffix"

matches = re.search(reAmericanDate, test_str)

if matches:
    print('\nAmerican Date')
    print("Match was found at {start}-{end}: {match}".format(start=matches.start(), end=matches.end(),
                                                             match=matches.group()))

    for groupNum in range(0, len(matches.groups())):
        groupNum = groupNum + 1

        print(
            "Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum, start=matches.start(groupNum),
                                                                      end=matches.end(groupNum),
                                                                      group=matches.group(groupNum)))

# TODO: Create a regex to match files with European date format

reEuropeanDate = re.compile(r"""
    ^(.*?)            # All text before first number
    ([12]\d(\d{2})?)  # The year
    ([\-./\\])        # separator
    (([01])?\d)       # The month
    ([\-./\\])        # separator
    ([0123]?\d)       # The day
    (.*)              # any remaining text
    """, re.VERBOSE)

test_str = "prefix 1922.02/03 suffix"

matches = re.search(reEuropeanDate, test_str)

if matches:
    print('\nEuropean Date')
    print("Match was found at {start}-{end}: {match}".format(start=matches.start(), end=matches.end(),
                                                             match=matches.group()))

    for groupNum in range(0, len(matches.groups())):
        groupNum = groupNum + 1

        print(
            "Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum, start=matches.start(groupNum),
                                                                      end=matches.end(groupNum),
                                                                      group=matches.group(groupNum)))

# Loop over files in the current working directory
# Walking a directory tree with os.walk()
# Note that quickdoc (Ctrl-Q) on os.walk is VERY HELPFUL
for folderName, subfolders, filenames in os.walk(os.getcwd()):
    # Remember, for each loop, the foldername changes to the current position in the directory tree
    for filename in filenames:
        matchesAM = re.search(reAmericanDate, filename)
        matchesEU = re.search(reEuropeanDate, filename)
        if matchesAM is not None:
            # Parse the filename
            prefix = matchesAM.group(1)
            month = matchesAM.group(2)
            day = matchesAM.group(5)
            year = matchesAM.group(7)
            suffix = matchesAM.group(9)
        elif matchesEU is not None:
            # Parse the filename
            prefix = matchesEU.group(1)
            year = matchesEU.group(2)
            month = matchesEU.group(5)
            day = matchesEU.group(8)
            suffix = matchesEU.group(9)
        else:
            # Skip the files with no date of either format in the name
            print('File ' + filename + ' did not match either pattern, skipping.')
            continue

    # Form the new filename, switching the date format if necessary
        euroFilename = prefix + year + "-" + month + '-' + day + suffix
        amerFilename = prefix + month + '-' + day + "-" + year + suffix
    # Rename the files
        toFormat = 'American'           # Revise to pass as command line parameter
        toFormat = 'eUrOpEaN'
        if toFormat.lower() == 'american':
            newName = amerFilename
        elif toFormat.lower() == 'european':
            newName = euroFilename
        else:
            newName = filename      # This should not be executed, but if it is, rename file to current newName
        # Get the full, absolute file paths.  Change the name to an absolute path
        print('Renaming "%s" to "%s".' % (filename,newName))
        absWorkingDir = os.path.abspath(folderName)
        newName = os.path.join(absWorkingDir, newName)      # Convert newName to absolute path
        oldName = os.path.join(absWorkingDir,filename)
        shutil.move(oldName, newName)
