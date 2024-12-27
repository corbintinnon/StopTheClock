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


def convert(file_name):

	# Open the file for reading only
	fid = open(file_name, 'r')
	first = fid.readline()
	# print('Input file, first line: %s' % first)
	second = fid.readline()
	# print(second)
	n_verts, n_faces, n_edges = second.split() 
	n_verts = int(n_verts)
	n_faces = int(n_faces)


	print('Surface has %d points and %d faces' % (n_verts, n_faces))
	points = vtk.vtkPoints()
	vertices = vtk.vtkCellArray()
	for i in range(0,n_verts):
		p = np.array(fid.readline().split(), dtype=np.float16)
		id = points.InsertNextPoint(p)
		vertices.InsertNextCell(1)
		vertices.InsertCellPoint(id)

	triangles = vtk.vtkCellArray()
	for i in range(0,n_faces):
		values = fid.readline().split()
		triangles.InsertNextCell(int(values[0]))
		ids = np.array(values[1:], dtype=np.int)
		for j in ids:
			triangles.InsertCellPoint(j)
		# triangles.InsertCellPoint(F[i,0])
		# triangles.InsertCellPoint(F[i,1])
		# triangles.InsertCellPoint(F[i,2])

	# Close the file
	fid.close()


	poly = vtk.vtkPolyData()
	poly.SetPoints(points)
	poly.SetVerts(vertices)
	poly.SetPolys(triangles)

	return poly



if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Convert OFF to VTK')
	parser.add_argument('input', nargs='+', help='Input .off file(s).')
	parser.add_argument('--prefix', default=None, help='Prefix to add to file names, default=None')
	args = parser.parse_args()


	prefix = ''
	if args.prefix is not None:
		prefix = args.prefix+'_'

	for input_file in args.input:
		full_path = os.path.abspath(input_file)
		print('Loading OFF file: %s' % full_path)
		vtk_poly = convert(full_path)

		output_path,base_name = os.path.split(full_path)
		base_name = os.path.splitext(base_name)[0]
		output_path = os.path.join(output_path,prefix+base_name+'.vtk')

		print('Saving VTK file: %s' % output_path)
		writer = vtk.vtkPolyDataWriter()
		writer.SetFileName(output_path)
		writer.SetInputData(vtk_poly)
		writer.Update()



