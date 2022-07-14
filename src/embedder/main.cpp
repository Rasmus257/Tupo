#include <stdio.h>
#include <conio.h>
#include <Python.h>

int main()
{
	PyObject* pInt;

	Py_Initialize();

	PyRun_SimpleString("from time import time,ctime\n"
						"print('Today is',ctime(time()))\n");
	
	Py_Finalize();

	printf("\nPress any key to exit...\n");
	if(!_getch()) _getch();
	return 0;
}