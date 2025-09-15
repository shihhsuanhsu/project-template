"""
Shih-Hsuan Hsu
July 22, 2024
All the monkey patches for SCons go here.
"""

import SCons.Warnings

WARNINGS = []
"""List of warnings that have been issued."""


def override_warn():
    """
    Override the SCons warning function to collect warnings.
    """
    # Store the original warning function locally
    orig_warn = SCons.Warnings.warn

    def collecting_warn(clazz, *args):
        """
        Collect warnings issued by SCons.
        """
        warning = clazz(args)
        WARNINGS.append(warning)
        return orig_warn(clazz, *args)  # Use the local variable

    # Override the SCons warning function
    SCons.Warnings.warn = collecting_warn
