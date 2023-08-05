"""
Custom JSON Encoder to support PyMassSpec classes
"""

################################################################################
#                                                                              #
#    PyMassSpec software for processing of mass-spectrometry data              #
#    Copyright (C) 2020 Dominic Davis-Foster                                   #
#                                                                              #
#    This program is free software; you can redistribute it and/or modify      #
#    it under the terms of the GNU General Public License version 2 as         #
#    published by the Free Software Foundation.                                #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    You should have received a copy of the GNU General Public License         #
#    along with this program; if not, write to the Free Software               #
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.                 #
#                                                                              #
################################################################################

# 3rd party
from json import JSONEncoder

# this package
from pyms.Spectrum import MassSpectrum, Scan


class PyMassSpecEncoder(JSONEncoder):
	"""
	Custom JSON Encoder to support PyMassSpec classes
	
	.. note: Currently only supports Scan and MassSpectrum objects
	"""
	
	def default(self, o):
		if isinstance(o, (Scan, MassSpectrum)):
			return dict(o)
		else:
			return JSONEncoder.default(self, o)

