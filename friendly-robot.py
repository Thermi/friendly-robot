#! /bin/env python2
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import defusedxml.ElementTree as ET
import hashlib

HASH="HASH GOES HERE"
FILE="PATH TO XML FILE OF KEEPASSX"

def testHash(inputString):
    if inputString == None:
        return False
    try:
        # change the occurences of sha1 in this method to whatever hash method you got the original hash from
        sha1=hashlib.sha1(inputString.encode('utf-8'))
    except:
        raise
    thisHash = sha1.hexdigest()
    if sha1.hexdigest() == HASH.encode('utf-8'):
        return True
    else:
        False
def testElement(element):
    if element.tag == "entry":
        elements=element.getchildren()
        # look for the password object
        for i in element.getchildren():
            # check tag to find the right object
            if i.tag == "password":
                try:
                    # test the password against the hash we have
                    if testHash(i.text):
                        print "SUCCESS!"
                        for j in elements:
                            if not j.tag == "password":
                                print str(j.text)
                                exit()
                except:
                    # iterate over element and its subelements to find title name
                    for k in element.getchildren():
                        if k.tag == "title":
                            text=k.text
                    print "exception occured while hashing password of element {}".format(text)
                    print "Could not hash over element with title {}".format(text)

def recurse(group):
    for i in group:
        if i.tag == "group":
            # the title of the group or entry is always the first object in the branch below the parent object
            print "recursing into {}".format(i[0].text)
            recurse(i)
        elif i.tag == "entry":
            # the title of the group or entry is always the first object in the branch below the parent object
            print "testing entry with name {}".format(i[0].text.encode('utf-8'))
            # iterate over objects in entry (title, password, url, ...)
            # i is an entry
            testElement(i)

# read xml from file

tree=ET.parse(FILE)
root=tree.getroot()

for group in root:
    if group.tag == "group":
        print "recursing into {}".format(group[0].text)
        recurse(group)
    else:
        print "not recursing into {}".format(group)
#        print element
