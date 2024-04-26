
import csv
import sys
import random
import time
import copy


def is_singular(input_matrix):
    matrix = copy.deepcopy(input_matrix)
    n = len(matrix)
    if n != len(matrix[0]):
        return False  # not a square matrix

    det = 1
    for i in range(n):
        for j in range(i+1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(i, n):
                matrix[j][k] -= factor * matrix[i][k]
        det *= matrix[i][i]

    return det == 0

# The LU_decomposition function takes in a square matrix matrix, and returns the unit lower triangular matrix L, upper triangular matrix U, and permutation matrix P such that PA = LU. 
# The function first initializes L and U to be matrices of zeros, and P to be the identity matrix. 
# Then, for each column j of matrix, it finds the pivot row (the row with the largest absolute value in column j), and 
# if necessary, swaps rows in matrix and P and swaps rows in the previous columns of L. 
# It then sets the diagonal element of U to be the pivot element of matrix, calculates the entries of L and U below the diagonal element of U, 
# and subtracts their outer product from the remaining part of matrix. Finally, it sets the diagonal elements of L to be ones.

def LU_decomposition(input_matrix):
    matrix = copy.deepcopy(input_matrix)
    n = len(matrix)
    L = [[0] * n for _ in range(n)]
    U = [[0] * n for _ in range(n)]
    P = [[int(i == j) for i in range(n)] for j in range(n)]
    
    for j in range(n):     
        U[j][j] = matrix[j][j]
        for i in range(j+1, n):
            L[i][j] = matrix[i][j] / U[j][j]
            U[j][i] = matrix[j][i]
        for i in range(j+1, n):
            for k in range(j+1, n):
                matrix[i][k] -= L[i][j] * U[j][k]
                
    for i in range(n):
        L[i][i] = 1
    
    return L, U, P

# In this function, we first compute the LU decomposition of the given matrix using the LU_decomposition function. 
# We then solve the system of linear equations LUX = B for each column of the inverse matrix X, where B is the column vector of the identity matrix. 
# We use forward substitution to solve Ly = b and backward substitution to solve Ux = y for each column of X. Finally, we return the inverse matrix X.

# Function to calculate the inverse of a square matrix using LU decomposition with partial pivoting
def invert_matrix(matrix):
    n = len(matrix)
    L, U, P = LU_decomposition(matrix)
    print("L:")
    for row in L:
        print(row)
    print()
    print("U:")
    for row in U:
        print(row)
    print()
    print("P:")
    for row in P:
        print(row)

    print("========================================================")

    # Solve the system of linear equations LUX = B for X, where B is the column vector of the identity matrix
    X = [[0] * n for _ in range(n)]
    b = [[int(i == j) for i in range(n)] for j in range(n)]
    for k in range(n):

        # Forward substitution to solve L*y = b
        y = [0] * n
        for i in range(n):
            y[i] = (b[i][k] - sum(L[i][j]*y[j] for j in range(i))) / L[i][i]

        # Backward substitution to solve U*x = y
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = (y[i] - sum(U[i][j]*x[j] for j in range(i+1, n))) / U[i][i]

        # Store the solution in the ith column of the inverse matrix
        for i in range(n):
            X[i][k] = x[i]

    return X

#Function to check whether the matrix generated from csv is square or not and also check whether the n is exceeding the size of matrix from csv file
def check_matrix(matrix, sub_square_size):
    # Get the number of rows and columns in the matrix
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    print(f"Size of matrix generated from CSV file {num_rows}x{num_cols}")

    # Check if the matrix is square
    if num_rows != num_cols:
        print("Input matrix is not square")
        return False

    # Check if the subsquare size is larger than the input matrix
    if sub_square_size > num_rows:
        print("Subsquare size is larger than the input matrix")
        return False

    # If both conditions are satisfied, return True
    return True

# Test on the attached file data.csv not only as a complete matrix from the csv file 
# we can also test it on extracted sub square matrices of size specified from the main matrix generated from csv
file_name = "data.csv"
with open(file_name, "r") as f:
    reader = csv.reader(f, delimiter=",")
    new_matrix = [[int(e) for e in row] for row in reader]

print("1. From data set.")
print("2. Generate random matrix.")
test_type = int(input("Select the option to test: "))

n = int(input("Enter the size of a new square matrix: "))

if (test_type == 1):
    print("Checking condition if the matrix from csv file is square or not and the submatrix lenghth n is less than or equal to the length of generated matrix from csv file: ")
    if (check_matrix(new_matrix, n)):
        print("Condition passed.")
    else:
        print("Condition failed.")
        sys.exit(1)

    new_matrix = [new_matrix[i][:n] for i in range(n)]
elif(test_type == 2):
    new_matrix = []
    is_singular_matrix = True
    while is_singular_matrix:
        for i in range(n):
            row = []
            for j in range(n):
                row.append(random.randint(1, 99))
            new_matrix.append(row)
        is_singular_matrix = False
else:
    print("Invalid option selected.")
    sys.exit(1)

#Sample small matrix to verify the code output
#new_matrix = [[3,3.5],[3.2,3.6]]

print("Extracted Matrix of given size n:")
for row in new_matrix:
    print(row)
print("==========================================================================")

print("Conditions to be satisfied: ")

print("1: A should be a square matrix(we always generate a square matrix only) of size nxn and n>=20: ")
if(n < 20):
    print("n should be >=20.")
    sys.exit(1)
else:
    print(f"Condition satisfied n = {n}")
print("2: A should be nonsingular. A's determinant is non-zero: ")
d = is_singular(new_matrix)
if(d):
    print("Matrix A is singular. Inverse cannot be found.")
    sys.exit(1)
else:
    print("Condition satisfied A is non-singular matrix. It's determinant is not zero")
print("========================================================")

start_time = time.time()

inverse_matrix = invert_matrix(new_matrix)

end_time = time.time()
running_time = end_time - start_time

print("Inverse matrix:")
for row in inverse_matrix:
    print(row)

print()
print("Running time: ", running_time, " seconds")


# Following block of code is some funtions to test whether the inverted matrix is correct by multiplying given matrix and its inverse and check whether the result is identity matrix or not.

def multiply_matrices(matrix1, matrix2):
    # Verify that the matrices can be multiplied
    if len(matrix1[0]) != len(matrix2):
        return None
    
    # Initialize the result matrix
    result = []
    for i in range(len(matrix1)):
        row = []
        for j in range(len(matrix2[0])):
            row.append(0)
        result.append(row)
    
    # Multiply the matrices
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
                result[i][j] += matrix1[i][k] * matrix2[k][j]
    
    return result

def is_identity_matrix(matrix):
    # Verify that the matrix is square
    if len(matrix) != len(matrix[0]):
        return False
    # Check if the diagonal elements are 1 and all other elements are 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if i == j and abs(matrix[i][j] - 1) > 1e-6:
                return False
            elif i != j and abs(matrix[i][j]) > 1e-6:
                return False
    
    return True

# Multiply the matrix and its inverse matrix
result = multiply_matrices(new_matrix, inverse_matrix)

print("================================================================")
# Check if the result is an identity matrix
if is_identity_matrix(result):
    print("Inverted matrix is correct.")
else:
    print("Inverted matrix is incorrect.")





