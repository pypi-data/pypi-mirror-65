#!/bin/bash

# Copyright (C) 2019  David Arroyo Menéndez

# Author: David Arroyo Menéndez <davidam@gnu.org>
# Maintainer: David Arroyo Menéndez <davidam@gnu.org>

# This file is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with damewebutils; see the file LICENSE.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301 USA,

python3 dameurls.py http://www.davidam.com > damewebutils/files/tests/davidam-index-$(date "+%Y-%m-%d-%H").txt

if ! cmp damewebutils/files/tests/davidam-index.txt damewebutils/files/tests/davidam-index-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
    echo "dameurls.py with davidam.com test is failing"
else
    echo "dameurls.py with davidam.com test is ok"
fi

python3 dameimgs.py http://www.damegender.net > damewebutils/files/tests/damegender-imgs-$(date "+%Y-%m-%d-%H").txt

if ! cmp damewebutils/files/tests/damegender-imgs.txt damewebutils/files/tests/damegender-imgs-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
    echo "dameimgs.py with damegender.net test is failing"
else
    echo "dameimgs.py with damegender.net test is ok"
fi

python3 template.py > damewebutils/files/tests/template-$(date "+%Y-%m-%d-%H").txt

if ! cmp damewebutils/files/tests/template.txt damewebutils/files/tests/template-$(date "+%Y-%m-%d-%H").txt >/dev/null 2>&1
then
    echo "template.py is failing"
else
    echo "template.py is ok"
fi

rm damewebutils/files/tests/*-$(date "+%Y-%m-%d-%H").txt
