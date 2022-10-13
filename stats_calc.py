"""
A simple statistics calculator
"""
#Your code here
values = []

print("Enter numbers. When finished type ‘stop’ to calculate statistics. ")

while 1:
    x = input()
    if x == 'stop':
        break
    values.append(int(x))

print("=== Results ===")
print("You entered " + str(len(values)) + " values")

print("Minimum number: " + str(min(values)))
print("Maximum number: " + str(max(values)))
mean = sum(values) / len(values)
print("Mean: " + str(mean))
