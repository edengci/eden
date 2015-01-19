# -*- coding: utf-8 -*-

""" S3 Framework Tables

    @copyright: 2009-2015 (c) Sahana Software Foundation
    @license: MIT

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following
    conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.
"""

__all__ = ("S3HierarchyModel",
           "S3ImportModel")

from gluon import *
from ..s3 import *

# =============================================================================
class S3ImportModel(S3Model):
    """Model for S3Import"""

    names = ("s3_import_upload")
    T = current.T

    import_upload_status = {
        1: T("Pending"),
        2: T("In error"),
        3: T("Completed"),
    }

    def model(self):

        define_table = self.define_table
        now = current.request.utcnow
        T = current.T

        tablename = "s3_import_upload"
        define_table(tablename,
                     Field("controller",
                           readable=False,
                           writable=False),
                     Field("function",
                           readable=False,
                           writable=False),
                     Field("file", "upload",
                           label=T("Import File"),
                           uploadfolder=os.path.join(current.request.folder,
                                                     "uploads", "imports"),
                           comment=DIV(_class="tooltip",
                                       _title="%s|%s" % ("Import File",
                                                         "Upload a file formatted according to the Template.")),
                           autodelete=True),
                     Field("filename",
                           readable=False,
                           writable=False),
                     Field("status", "integer",
                           default=1,
                           readable=False,
                           requires=IS_IN_SET(self.import_upload_status, zero=None),
                           represent=self.status_represent,
                           writable=False),
                     Field("extra_data",
                           readable=False,
                           writable=False),
                     Field("replace_option", "boolean",
                           label=T("Replace"),
                           default=False,
                           readable=False,
                           writable=False),
                     Field("job_id", length=128,
                           readable=False,
                           writable=False),
                     Field("user_id", "integer",
                           label=T("User Name"),
                           represent=self.user_name_represent,
                           readable=False,
                           writable=False),
                     Field("created_on", "datetime",
                           readable=False,
                           writable=False,
                           default=now,
                           represent=self.date_represent),
                     Field("modified_on", "datetime",
                           readable=False,
                           writable=False,
                           default=now,
                           update=now,
                           represent=self.date_represent),
                     Field("summary_added", "integer",
                           readable=False,
                           writable=False),
                     Field("summary_error", "integer",
                           readable=False,
                           writable=False),
                     Field("summary_ignored", "integer",
                           readable=False,
                           writable=False),
                     Field("completed_details", "text",
                           readable=False,
                           writable=False))
        # ---------------------------------------------------------------------
        # Return global names to s3.*
        #
        return {}

    # -------------------------------------------------------------------------
    @staticmethod
    def user_name_represent(id):
        # @todo: use s3_represent_user?

        if not id:
            return current.messages["NONE"]
        table = db.auth_user
        row = db(table.id == id).select(table.first_name,
                                        table.last_name,
                                        limitby=(0, 1)).first()
        try:
            return "%s %s" % (row.first_name, row.last_name)
        except:
            return current.messages.UNKNOWN_OPT

    # -------------------------------------------------------------------------
    @staticmethod
    def status_represent(index):
        if index is None:
            return current.messages.UNKNOWN_OPT
        else:
            return self.import_upload_status[index]

    # -------------------------------------------------------------------------
    @staticmethod
    def date_represent(date_obj):
        """
            Represent a datetime object as string

            @param date_obj: the datetime object

            @todo: replace by S3DateTime method?
        """

        return date_obj.strftime("%d %B %Y, %I:%M%p")

# =============================================================================
class S3HierarchyModel(S3Model):
    """ Model for stored object hierarchies, experimental """

    names = ("s3_hierarchy",)

    def model(self):

        define_table = self.define_table
        
        # -------------------------------------------------------------------------
        # Stored Object Hierarchy
        #
        tablename = "s3_hierarchy"
        define_table(tablename,
                     Field("tablename",
                           length=64),
                     Field("dirty", "boolean",
                           default=False),
                     Field("hierarchy", "json"),
                     *s3_timestamp())
        # ---------------------------------------------------------------------
        # Return global names to s3.*
        #
        return {}

    # -------------------------------------------------------------------------
    def defaults(self):
        """ Safe defaults if module is disabled """

        return {}


# END =========================================================================
