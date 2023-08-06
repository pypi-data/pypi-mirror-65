"""
    @copyright: 2020 Lari Huttunen
    @license: MIT <http://www.opensource.org/licenses/mit-license.php>
"""
import os
import sys
import shutil
from datetime import datetime


class Argunizer:

    def __init__(self, spath=None, dpath=None, semantics="symlink", dryrun=True, debug=False, verbose=False):
        self.spath = spath
        self.dpath = dpath
        self.semantics = semantics
        self.dryrun = dryrun
        self.debug = debug
        self.verbose = verbose
        self.directory = {}

    def __timestampIt(self, sdir, fname):
        full_path = os.path.join(sdir, fname)
        try:
            ts = os.path.getmtime(full_path)
        except FileNotFoundError as err:
            print("ERROR: {0}".format(err))
            return None
        else:
            if self.debug:
                print("DEBUG: {0} = {1}".format(repr(full_path), ts))
        return ts

    def __convertTime(self, ts):
        ds = datetime.utcfromtimestamp(ts)
        year = ds.strftime("%Y")
        month = ds.strftime("%m")
        day = ds.strftime("%d")
        cts = os.path.join(year, month, day)
        if self.debug:
            print("DEBUG: {0} = {1}".format(ts, cts))
        return cts

    def __makeDirs(self, ddir):
        try:
            os.makedirs(ddir, mode=0o770)
        except FileExistsError:
            return
        except PermissionError as err:
            sys.exit("ERROR: couldn't create a directory {0}".format(err))
        else:
            if self.verbose:
                print("INFO: Created {0}".format(ddir))

    def __symlinkFile(self, sdir, sfile, ddir):
        symlink = os.path.join(ddir, sfile)
        target_file = os.path.join(sdir, sfile)
        try:
            os.symlink(target_file, symlink)
        except FileExistsError:
            if self.verbose:
                print("INFO: symlink {0} -> {1} already exists.".format(repr(symlink), repr(target_file)))
            return
        else:
            if self.verbose:
                print("INFO: symlinked {0} -> {1}.".format(repr(symlink), repr(target_file)))

    def __copyFile(self, sdir, sfile, ddir):
        source_file = os.path.join(sdir, sfile)
        target_file = os.path.join(ddir, sfile)
        try:
            shutil.copy2(source_file, target_file)
        except shutil.SameFileError as err:
            sys.exit("ERROR: {0}".format(err))
        except PermissionError as err:
            print("ERROR: unable to set permissions {0}".format(err))
        else:
            if self.verbose:
                print("INFO: copied {0} -> {1}".format(repr(source_file), repr(target_file)))

    def __moveFile(self, sdir, sfile, ddir):
        source_file = os.path.join(sdir, sfile)
        target_file = os.path.join(ddir, sfile)
        try:
            shutil.move(source_file, target_file)
        except PermissionError as err:
            print("ERROR: {0}".format(err))
        else:
            if self.verbose:
                print("INFO: moved {0} -> {1}".format(repr(source_file), repr(target_file)))

    def walk(self):
        try:
            for dirpath, dirnames, fnames in os.walk(self.spath):
                self.directory[dirpath] = fnames
        except TypeError as e:
            raise e
        else:
            if len(self.directory) == 0:
                sys.exit("ERROR: Source directory {0} is inaccessible.".format(self.spath))

    def execute(self):
        for path, fnames in self.directory.items():
            if self.dpath is not None:
                if self.spath == self.dpath:
                    sys.exit("ERROR: source and destination paths cannot be the same!")
                for fname in fnames:
                    ts = self.__timestampIt(path, fname)
                    if ts is None:
                        continue
                    date_string = self.__convertTime(ts)
                    ddir = os.path.join(self.dpath, date_string)
                    if self.dryrun:
                        print("INFO: dry-run, {0}, {1}".format(ddir, repr(fname)))
                    else:
                        self.__makeDirs(ddir)
                        if self.semantics == "symlink":
                            self.__symlinkFile(path, fname, ddir)
                        elif self.semantics == "copy":
                            self.__copyFile(path, fname, ddir)
                        elif self.semantics == "move":
                            self.__moveFile(path, fname, ddir)
                        else:
                            sys.exit("ERROR: unknown semantics: {0}!".format(self.semantics))

    def clean(self):
        if shutil.rmtree.avoids_symlink_attacks:
            if self.dryrun:
                sys.exit("INFO: Would have cleaned up {0}".format(self.spath))
            try:
                shutil.rmtree(self.spath)
            except (PermissionError, FileNotFoundError) as err:
                sys.exit("ERROR: couldn't clean up the source directory {0}".format(err))
            else:
                if self.verbose:
                    print("INFO: cleaned up the source directory {0}".format(self.spath))
