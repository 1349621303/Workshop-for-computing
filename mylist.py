"""
This program is some simple practice for using lists
"""
mylist = ["January","February","March","April","May","June","July","August","September","October","November","December"]
#Your code here
# 1. Print the third item in the list
print('the third item of mylist is: ', mylist[2])

# 2. Create a list containing the first three items of the list
new_list_1 = mylist[0:3]
print(new_list_1)

# 3. Create a list containing every other item in the list.
new_list_2 = mylist[3:len(mylist)]
print(new_list_2)

# 4. Test if the list contains January.
if "January" in mylist:
    print("existence")
else:
    print("in-existence")

