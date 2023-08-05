import hashlib
import os
import shutil
import uuid
import logging

from plom import specdir

log = logging.getLogger("servID")


def IDprogressCount(self):
    """Send back current ID progress counts to the client"""
    return [self.DB.IDcountIdentified(), self.DB.IDcountAll()]


def IDgetNextTask(self):
    # Get number of next unidentified test from the database
    give = self.DB.IDgetNextTask()
    if give is None:
        return [False]
    else:
        return [True, give]


def IDgetDoneTasks(self, user):
    """When a id-client logs on they request a list of papers they have already IDd.
    Send back the list.
    """
    return self.DB.IDgetDoneTasks(user)


def IDgetImage(self, username, testNumber):
    """When a id-client logs on they request a list of papers they have already IDd.
    Send back the list.
    """
    return self.DB.IDgetImage(username, testNumber)


def IDclaimThisTask(self, user, testNumber):
    return self.DB.IDgiveTaskToClient(user, testNumber)
    # return [true, image-filename1, name2,...]
    # or return [false]


def IDreturnIDdTask(self, user, ret, sid, sname):
    """Client has ID'd the pageimage with code=ret, student-number=sid,
    and student-name=sname. Send the information to the database (which
    checks if that number has been used previously). If okay then send
    and ACK, else send an error that the number has been used.
    """
    # TODO - improve this
    # returns [True] if all good
    # [False, True] - if student number already in use
    # [False, False] - if bigger error
    return self.DB.IDtakeTaskFromClient(ret, user, sid, sname)


def IDdidNotFinish(self, user, testNumber):
    """User didn't finish IDing the image with given code. Tell the
    database to put this back on the todo-pile.
    """
    self.DB.IDdidNotFinish(user, testNumber)
    return


def IDgetRandomImage(self):
    return self.DB.IDgetRandomImage()


def IDdeletePredictions(self):
    # move old file out of way
    if not os.path.isfile(Path(specdir) / "predictionlist.csv"):
        return False
    shutil.move(
        Path(specdir) / "predictionlist.csv", Path(specdir) / "predictionlist.bak"
    )
    with open(Path(specdir) / "predictionlist.csv", "w") as fh:
        fh.write("test, id\n")
    log.info("ID prediction list deleted")

    return True


def IDreviewID(self, testNumber):
    return self.DB.IDreviewID(testNumber)
