"""
Shih-Hsuan Hsu
Aug. 11, 2024
This file provides a warning classes for SCons to warn users.
"""

import SCons.Warnings


class CustomWarning(SCons.Warnings.SConsWarning):
    """
    A custom warning class for SCons.
    This class is used to create specific warning types that can be
    compared and hashed.
    """

    def __init__(self, message):
        self.message = message

    def __hash__(self):
        return hash(self.message)

    def __eq__(self, other):
        if isinstance(other, CustomWarning):
            return self.message == other.message
        return False


class SymLinkWarning(CustomWarning):
    """
    A warning class for SCons to warn users when symbolic link is not supported.
    """


class NoPDFCompilerWarning(CustomWarning):
    """
    A warning class for SCons to warn users when PDF compiler is not available.
    """


class FileNotFoundWarning(CustomWarning):
    """
    A warning class for SCons to warn users when a file is not found.
    This is used in the `check_target_exists` function.
    """


class CannotInitProjectLockWarning(CustomWarning):
    """
    A warning class for SCons to warn users when the project lock cannot be initialized.
    This is used in the `ProjectLock` class.
    """


def warn(warning_obj, message):
    """
    Issue the warning message.
    """
    SCons.Warnings.warn(warning_obj, message)


def no_symlink_permission(msg="You do not have permission to create symlinks."):
    """
    Issue a warning message when symbolic link is not supported.
    """
    warn(SymLinkWarning, msg)


def no_pdf_compiler():
    """
    Issue a warning message when PDF compiler is not available.
    """
    warn(NoPDFCompilerWarning, "No PDF compiler is available.")


def file_not_found_warning(file_path):
    """
    Issue a warning message when a file is not found.
    """
    warn(FileNotFoundWarning, f"File was not created: {file_path}")


def cannot_init_project_lock_warning():
    """
    Issue a warning message when the project lock cannot be initialized.
    """
    warn(CannotInitProjectLockWarning, "Cannot initialize project lock.")


# enable the warning class
SCons.Warnings.enableWarningClass(SymLinkWarning)
SCons.Warnings.enableWarningClass(NoPDFCompilerWarning)
SCons.Warnings.enableWarningClass(FileNotFoundWarning)
SCons.Warnings.enableWarningClass(CannotInitProjectLockWarning)
