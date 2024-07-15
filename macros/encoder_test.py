# SPDX-FileCopyrightText: 2023 Your Name
#
# SPDX-License-Identifier: MIT

from code import encoder_test_animation

app = {
    'name' : 'Encoder Test',
    'macros' : [
        # COLOR    LABEL    KEY SEQUENCE
        (0x000000, '', []),
        (0x000000, '', []),
        (0x000000, '', []),
        (0x000000, '', []),
        (0x000000, '', []),
        (0x000000, '', []),
        (0x000000, '', []),
        (0x000000, '', []),
        (0x000000, '', []),
        (0x000000, '', []),
        (0x000000, '', []),
        (0xFF0000, 'Test', [encoder_test_animation]),  # Red key to trigger the test
    ]
}