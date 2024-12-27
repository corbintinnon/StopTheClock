#!/usr/bin/env python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import numpy as np
import os.path
import vtk
from vtk.util.numpy_support import vtk_to_numpy
from vtk.util.numpy_support import numpy_to_vtk


def convert(poly, image):
	"""Convert a VTK poly data object to an image mask.

	If an image is specified, then the surface mask is created in that image's 
	domain. Otherwise, an image is created using the surface's bounding box
	domain.

	Input:
		poly (vtkPolyData): the VTK surface object.
		image (vtkImageData): an optional VTK image data object.
	Output:
		mask image (vtkImageData)

	"""

	vol = vtk.vtkImageData()
	vol.CopyStructure(image)
	vol.AllocateScalars(vtk.VTK_INT, 1)
	# Fill the volume with ones
	vol.GetPointData().GetScalars().FillComponent(0,1.0)

	# Create the image stencil
	stencil = vtk.vtkPolyDataToImageStencil()
	stencil.SetInputData(poly)
	#stencil.SetInformationInput(vol)
	stencil.Update()

	img_stencil = vtk.vtkImageStencil()
	img_stencil.SetStencilData(stencil.GetOutput())
	img_stencil.SetInputData(vol)
	img_stencil.SetBackgroundValue(0)
	img_stencil.Update()

	return img_stencil.GetOutput()



if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Convert OFF to VTK')
	parser.add_argument('surface', help='Input VTK surface file.')
	parser.add_argument('image', default=None, help='Input NIfTI image file.')
	parser.add_argument('--prefix', default=None, help='Prefix to add to file names, default=None')
	parser.add_argument('--output', default='.', help='Output path for the mask image, default=the current dir')
	args = parser.parse_args()


	prefix = ''
	if args.prefix is not None:
		prefix = args.prefix+'_'

	surface_path = os.path.abspath(args.surface)
	print('Loading VTK file: %s' % surface_path)

	# Read the VTK surface file in
	poly_reader = vtk.vtkPolyDataReader()
	poly_reader.SetFileName(surface_path)
	poly_reader.Update()
	vtk_poly = vtk.vtkPolyData()
	vtk_poly.ShallowCopy(poly_reader.GetOutput())
	print('VTK surface has %d points' % vtk_poly.GetNumberOfPoints())

	# Read the NIfTI image in
	vtk_image = None
	nifti_header = None

	image_path = os.path.abspath(args.image)
	print('Loading NIfTI file: %s' % image_path)
	nifti_reader = vtk.vtkNIFTIImageReader()
	nifti_reader.SetFileName(image_path)
	nifti_reader.Update()

	nifti_header = vtk.vtkNIFTIImageHeader()
	nifti_header.DeepCopy(nifti_reader.GetNIFTIHeader())

	vtk_image = vtk.vtkImageData()
	vtk_image.ShallowCopy(nifti_reader.GetOutput())
	print('NIfTI file has dims = %s' % str(vtk_image.GetDimensions()))

	mask_image = convert(vtk_poly, vtk_image)

	# Output the result
	input_file_name = os.path.split(surface_path)[1]
	input_root = os.path.splitext(input_file_name)[0]
	output_file_name = prefix + input_root + '.nii.gz'
	output_path = os.path.join(os.path.abspath(args.output),output_file_name)
	print('Saving mask image to: %s' % output_path)

	writer = vtk.vtkNIFTIImageWriter()
	writer.SetInputData(mask_image)
	# if nifti_header is not None:
	# 	writer.SetNIFTIHeader(nifti_header)
	writer.SetFileName(output_path)
	writer.Update()



