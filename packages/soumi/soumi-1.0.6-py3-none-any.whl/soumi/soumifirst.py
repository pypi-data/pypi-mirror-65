# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 12:08:38 2019

@author: Soumitra
"""
def sayhello():
    print("Hi There Beautiful Person!")

def add(x,y):
    print(x+y)
def minus(x,y):
    print(x-y)
def prod(x,y):
    print(x*y)
def div(x,y):
    print(x/y)
def fldiv(x,y):
    print(x//y)
def power(x,y):
    print(x**y)


def fact(x):
    """
    factorial of a number.
    """
    if type(x)==int:
        flg="invalid for negative integers"
        if x>0:
            return fact(x-1)*x
        elif x<0:
            raise Exception(flg)
        else:
            return 1
    else:
        raise Exception("invalid for non-integers")


def strrev(s):
    if type(s)==str:
        return s[::-1]
    else:
        raise Exception("Not a string")

def numrev(n):
    if type(n)==int:
        a=n
        rev=0
        while(a>0):
            rev=rev*10
            rev=rev+a%10
            a=a//10
        return rev
    else:
        raise Exception("Only positive integers allowed")

        
def palindrome(x):
    if type(x)==int:
        if numrev(x)==x:
            return True
        else:
            return False
    elif type(x)==str:
        if strrev(x)==x:
            return True
        else:
            return False
    else:
        raise Exception("Only positive integers and strings allowed")

def ncr(n,r):
    """
       combinattion formula:
        npr: r out of n combinations
    """
    if(n>r):
        p=fact(r)*fact(n-r)
        return int((fact(n)/p))
    else:
        raise Exception("First Argument Must be Greater than Second Argument")

def npr(n,r):
    """
    Permutation formula:
        npr: r out of n permutations
    """
    if(n>r):
        return int((fact(n)/fact(n-r)))
    else:
        raise Exception("First Argument Must be Greater than Second Argument")

def bubble(l):
    """
    Takes a list as the argument and returns a sorted array.

    """
    n=len(l)
    for i in range(n-1):
        for j in range(n-i-1):
            if(l[j]>l[j+1]):
                l[j]=l[j]+l[j+1]
                l[j+1]=l[j]-l[j+1]
                l[j]=l[j]-l[j+1]
    return l

    
def check_sorted(l):
    """
    check if the array is sorted.
    """
    
    for i in range(len(l)-1):
        if l[i]<l[i+1]:
            continue
        else:
            return False
def linsearch(l,x):
    """
    linear search for an elememnt in an array.
    linsearch(l,x)-->l is the list and x is the item to be serached.
    """
    for i in range(len(l)):
        if x==l[i]:
            return i
        else: 
            return False

def binsearch(arr, x): 
    """
    Binary search:
        Takes an array and the item to be found.
    """
    l=0
    r=len(arr)
    # Check base case 
    if r >= l: 
  
        mid = int(l + (r - l)/2)
  
        # If element is present at the middle itself 
        if arr[mid] == x: 
            return mid 
          
        # If element is smaller than mid, then it  
        # can only be present in left subarray 
        elif arr[mid] > x: 
            return binsearch(arr, l, mid-1, x) 
  
        # Else the element can only be present  
        # in right subarray 
        else: 
            return binsearch(arr, mid + 1, r, x) 
  
    else: 
        # Element is not present in the array 
        return -1

def ciphertext(path,k):
    """Ciphertext(path,k) takes two aruguments. The first argument is the path for the text file. The second argument is the key for caesar cipher."""
    obj=open(path,'r')
    m=obj.read()
    coded=""
    for c in m:
        coded=coded+chr(ord(c)+(k))
    obj.close()
    obj=open(path,'w+')
    obj.write(coded)
    obj.close()
 
def deciphertext(path,k):
    """Deciphertext(path,k) takes two aruguments. The first argument is the path for the text file. The second argument is the key for caesar cipher."""
    obj=open(path,'r')
    coded=obj.read()
    decoded=""
    for d in coded:
        decoded=decoded+chr(ord(d)-(k))
    obj.close()
    obj=open(path,'w+')
    obj.write(decoded)
    obj.close()