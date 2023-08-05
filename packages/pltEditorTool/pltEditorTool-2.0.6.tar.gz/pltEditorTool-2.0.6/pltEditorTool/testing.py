# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 19:49:50 2020

@author: richardcouperthwaite
"""

from pltEditorTool import plotEditor

if __name__ == "__main__":
    """
    Test cases for the code sequentially test each situation that could arise
    For each test, the code generates the post processor window and the user
    should click --SHOW PLOT-- and --SAVE PLOT-- buttons and then close the window
    to continue on to the next test.

    The output in the console from this procedure should be:

    #################################################
    Test Case 1: Full data
    Test Case 1 Successful!
    #################################################
    Test Case 2: leave out error data
    Test Case 2 Successful!
    #################################################
    Test Case 3: leave out fill data
    Test Case 3 Successful!
    #################################################
    Test Case 4: leave out fill_alt data
    Test Case 4 Successful!
    #################################################
    Test Case 5: leave out labels
    No handles with labels found to put in legend.
    Test Case 5 Successful!
    #################################################
    Test Case 6: leave out y
    Test Case 6 Failed: List of Y data must be provided
    #################################################
    Test Case 7: leave out x
    Test Case 7 Failed: List of X data must be provided
    #################################################
    Test Case 8: x[0] has missing data
    Test Case 8 Failed: X and Y vectors must be same shape | Index 0
    #################################################
    Test Case 9: y[0] has missing data
    Test Case 9 Failed: X and Y vectors must be same shape | Index 0
    #################################################
    Test Case 10: x_err[1] has missing data
    Test Case 10 Failed: X-Error vector must be empty or same shape as X | Index 1
    #################################################
    Test Case 11: y_err[1] has missing data
    Test Case 11 Failed: Y-Error vector must be empty or same shape as X | Index 1
    #################################################
    Test Case 12: fill[0] has missing data
    Test Case 12 Failed: Fill-Top vector must be empty or same shape as X | Index 1
    #################################################
    Test Case 13: fill_alt[0] has missing data
    Test Case 13 Failed: Fill-Bottom vector must be empty or same shape as X | Index 1
    #################################################
    Test Case 14: labels has missing data
    Test Case 14 Successful!
    """
    # x_data = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
    # y_data = [[0.00, 0.84, 0.91, 0.14, -0.76, -0.96, -0.28, 0.66, 0.99, 0.41, -0.54],
    #           [1.00, 0.90, 0.82, 0.74, 0.67, 0.61, 0.55, 0.50, 0.45, 0.41, 0.37]]
    # x_err_data = [[], [0.1, 0.1, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.1, 0.1, 0.05]]
    # y_err_data = [[], [0.1, 0.1, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.1, 0.1, 0.05]]
    # fill_data = [[], [0.1, 0.1, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.1, 0.1, 0.05]]
    # fill_alt_data = [[], [0.3, 0.3, 0.6, 0.6, 0.9, 0.9, 0.6, 0.6, 0.3, 0.3, 0.15]]
    # labels_data = ['Experimental', 'Computation']
    
    # plotEditor(x=x_data, y=y_data, x_err=x_err_data,
    #            y_err=y_err_data, fill=fill_data,
    #            fill_alt=fill_alt_data, labels=labels_data)

    check_run_test = input("Do you wish to run the test cases (Y/N)?   ")

    x_data = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
    y_data = [[0.00, 0.84, 0.91, 0.14, -0.76, -0.96, -0.28, 0.66, 0.99, 0.41, -0.54],
              [1.00, 0.90, 0.82, 0.74, 0.67, 0.61, 0.55, 0.50, 0.45, 0.41, 0.37]]
    x_err_data = [[], [0.1, 0.1, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.1, 0.1, 0.05]]
    y_err_data = [[], [0.1, 0.1, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.1, 0.1, 0.05]]
    fill_data = [[], [0.1, 0.1, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.1, 0.1, 0.05]]
    fill_alt_data = [[], [0.3, 0.3, 0.6, 0.6, 0.9, 0.9, 0.6, 0.6, 0.3, 0.3, 0.15]]
    labels_data = ['Experimental', 'Computation']

    if check_run_test in ['Y', 'y']:
        for iii in range(14):
            test_case = iii+1

            if test_case == 1:
                print("#################################################")
                print("Test Case 1: Full data")
                try:
                    plotEditor(x=x_data, y=y_data, x_err=x_err_data,
                                y_err=y_err_data, fill=fill_data,
                                fill_alt=fill_alt_data, labels=labels_data)
                    print("Test Case 1 Successful!")
                except Exception as e:
                    print("Test Case 1 Failed: {}".format(e))
            elif test_case == 2:
                print("#################################################")
                print("Test Case 2: leave out error data")
                try:
                    plotEditor(x=x_data, y=y_data, x_err=x_err_data,
                                y_err=y_err_data, fill=fill_data,
                                fill_alt=fill_alt_data, labels=labels_data)
                    print("Test Case 2 Successful!")
                except Exception as e:
                    print("Test Case 2 Failed: {}".format(e))
            elif test_case == 3:
                print("#################################################")
                print("Test Case 3: leave out fill data")
                try:
                    plotEditor(x=x_data, y=y_data, x_err=x_err_data,
                                y_err=y_err_data, fill=fill_data,
                                fill_alt=fill_alt_data, labels=labels_data)
                    print("Test Case 3 Successful!")
                except Exception as e:
                    print("Test Case 3 Failed: {}".format(e))
            elif test_case == 4:
                print("#################################################")
                print("Test Case 4: leave out fill_alt data")
                try:
                    plotEditor(x=x_data, y=y_data, x_err=x_err_data,
                                y_err=y_err_data, fill=fill_data,
                                fill_alt=fill_alt_data, labels=labels_data)
                    print("Test Case 4 Successful!")
                except Exception as e:
                    print("Test Case 4 Failed: {}".format(e))
            elif test_case == 5:
                print("#################################################")
                print("Test Case 5: leave out labels")
                try:
                    plotEditor(x=x_data, y=y_data, x_err=x_err_data,
                                y_err=y_err_data, fill=fill_data,
                                fill_alt=fill_alt_data, labels=labels_data)
                    print("Test Case 5 Successful!")
                except Exception as e:
                    print("Test Case 5 Failed: {}".format(e))
            elif test_case == 6:
                print("#################################################")
                print("Test Case 6: leave out y")
                try:
                    plotEditor(x=x_data, y=y_data, x_err=x_err_data,
                                y_err=y_err_data, fill=fill_data,
                                fill_alt=fill_alt_data, labels=labels_data)
                    print("Test Case 6 Successful!")
                except Exception as e:
                    print("Test Case 6 Failed: {}".format(e))
            elif test_case == 7:
                print("#################################################")
                print("Test Case 7: leave out x")
                try:
                    plotEditor(x=x_data, y=y_data, x_err=x_err_data,
                                y_err=y_err_data, fill=fill_data,
                                fill_alt=fill_alt_data, labels=labels_data)
                    print("Test Case 7 Successful!")
                except Exception as e:
                    print("Test Case 7 Failed: {}".format(e))
            elif test_case == 8:
                print("#################################################")
                print("Test Case 8: x[0] has missing data")
                try:
                    x_data = [[0,1,2,3,4,5,6,7,8], [0,1,2,3,4,5,6,7,8,9,10]]
                    y_data = [[0.00,0.84,0.91,0.14,-0.76,-0.96,-0.28,0.66,0.99,0.41,-0.54],[1.00,0.90,0.82,0.74,0.67,0.61,0.55,0.50,0.45,0.41,0.37]]
                    x_err_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    y_err_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    fill_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    fill_alt_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    labels_data = ['Experimental','Computation']
                    plotEditor(x=x_data, y=y_data, x_err=x_err_data,
                                y_err=y_err_data, fill=fill_data,
                                fill_alt=fill_alt_data, labels=labels_data)
                    print("Test Case 8 Successful!")
                except Exception as e:
                    print("Test Case 8 Failed: {}".format(e))
            elif test_case == 9:
                print("#################################################")
                print("Test Case 9: y[0] has missing data")
                try:
                    x_data = [[0,1,2,3,4,5,6,7,8,9,10], [0,1,2,3,4,5,6,7,8,9,10]]
                    y_data = [[0.00,0.84,0.91,0.14,-0.76,-0.96,-0.28,0.66,0.99],[1.00,0.90,0.82,0.74,0.67,0.61,0.55,0.50,0.45,0.41,0.37]]
                    x_err_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    y_err_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    fill_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    fill_alt_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    labels_data = ['Experimental','Computation']
                    plotEditor(x=x_data, y=y_data, x_err=x_err_data,
                                y_err=y_err_data, fill=fill_data,
                                fill_alt=fill_alt_data, labels=labels_data)
                    print("Test Case 9 Successful!")
                except Exception as e:
                    print("Test Case 9 Failed: {}".format(e))
            elif test_case == 10:
                print("#################################################")
                print("Test Case 10: x_err[1] has missing data")
                try:
                    x_data = [[0,1,2,3,4,5,6,7,8,9,10], [0,1,2,3,4,5,6,7,8,9,10]]
                    y_data = [[0.00,0.84,0.91,0.14,-0.76,-0.96,-0.28,0.66,0.99,0.41,-0.54],[1.00,0.90,0.82,0.74,0.67,0.61,0.55,0.50,0.45,0.41,0.37]]
                    x_err_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1]]
                    y_err_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    fill_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    fill_alt_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    labels_data = ['Experimental','Computation']
                    plotEditor(x=x_data, y=y_data, x_err=x_err_data,
                                y_err=y_err_data, fill=fill_data,
                                fill_alt=fill_alt_data, labels=labels_data)
                    print("Test Case 10 Successful!")
                except Exception as e:
                    print("Test Case 10 Failed: {}".format(e))
            elif test_case == 11:
                print("#################################################")
                print("Test Case 11: y_err[1] has missing data")
                try:
                    x_data = [[0,1,2,3,4,5,6,7,8,9,10], [0,1,2,3,4,5,6,7,8,9,10]]
                    y_data = [[0.00,0.84,0.91,0.14,-0.76,-0.96,-0.28,0.66,0.99,0.41,-0.54],[1.00,0.90,0.82,0.74,0.67,0.61,0.55,0.50,0.45,0.41,0.37]]
                    x_err_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    y_err_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1]]
                    fill_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    fill_alt_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    labels_data = ['Experimental','Computation']
                    plotEditor(x=x_data, y=y_data, x_err=x_err_data,
                                y_err=y_err_data, fill=fill_data,
                                fill_alt=fill_alt_data, labels=labels_data)
                    print("Test Case 11 Successful!")
                except Exception as e:
                    print("Test Case 11 Failed: {}".format(e))
            elif test_case == 12:
                print("#################################################")
                print("Test Case 12: fill[0] has missing data")
                try:
                    x_data = [[0,1,2,3,4,5,6,7,8,9,10], [0,1,2,3,4,5,6,7,8,9,10]]
                    y_data = [[0.00,0.84,0.91,0.14,-0.76,-0.96,-0.28,0.66,0.99,0.41,-0.54],[1.00,0.90,0.82,0.74,0.67,0.61,0.55,0.50,0.45,0.41,0.37]]
                    x_err_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    y_err_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    fill_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1]]
                    fill_alt_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    labels_data = ['Experimental','Computation']
                    plotEditor(x=x_data, y=y_data, x_err=x_err_data,
                                y_err=y_err_data, fill=fill_data,
                                fill_alt=fill_alt_data, labels=labels_data)
                    print("Test Case 12 Successful!")
                except Exception as e:
                    print("Test Case 12 Failed: {}".format(e))
            elif test_case == 13:
                print("#################################################")
                print("Test Case 13: fill_alt[0] has missing data")
                try:
                    x_data = [[0,1,2,3,4,5,6,7,8,9,10], [0,1,2,3,4,5,6,7,8,9,10]]
                    y_data = [[0.00,0.84,0.91,0.14,-0.76,-0.96,-0.28,0.66,0.99,0.41,-0.54],[1.00,0.90,0.82,0.74,0.67,0.61,0.55,0.50,0.45,0.41,0.37]]
                    x_err_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    y_err_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    fill_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    fill_alt_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1]]
                    labels_data = ['Experimental','Computation']
                    plotEditor(x=x_data, y=y_data, x_err=x_err_data,
                                y_err=y_err_data, fill=fill_data,
                                fill_alt=fill_alt_data, labels=labels_data)
                    print("Test Case 13 Successful!")
                except Exception as e:
                    print("Test Case 13 Failed: {}".format(e))
            elif test_case == 14:
                print("#################################################")
                print("Test Case 14: labels has missing data")
                try:
                    x_data = [[0,1,2,3,4,5,6,7,8,9,10], [0,1,2,3,4,5,6,7,8,9,10]]
                    y_data = [[0.00,0.84,0.91,0.14,-0.76,-0.96,-0.28,0.66,0.99,0.41,-0.54],[1.00,0.90,0.82,0.74,0.67,0.61,0.55,0.50,0.45,0.41,0.37]]
                    x_err_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    y_err_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    fill_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    fill_alt_data = [[],[0.1,0.1,0.2,0.2,0.3,0.3,0.2,0.2,0.1,0.1,0.05]]
                    labels_data = ['Experimental']
                    plotEditor(x=x_data, y=y_data, x_err=x_err_data,
                                y_err=y_err_data, fill=fill_data,
                                fill_alt=fill_alt_data, labels=labels_data)
                    print("Test Case 14 Successful!")
                except Exception as e:
                    print("Test Case 14 Failed: {}".format(e))
    else:
        plotEditor(x=x_data, y=y_data, x_err=x_err_data,
                                y_err=y_err_data, fill=fill_data,
                                fill_alt=fill_alt_data, labels=labels_data)